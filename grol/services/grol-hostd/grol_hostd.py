#!/usr/bin/env python3
"""GROL host information plane. HOST_API_V0. Read-only."""
from __future__ import annotations

import argparse
import json
import os
import socket
import struct
import sys
import threading
import time
from pathlib import Path
from typing import Any

SO_PEERCRED = 17
PEERCRED_FMT = "3i"
MAX_REQUEST_BYTES = 4096
MAX_RESPONSE_BYTES = 16 * 1024
MAX_INFLIGHT = 2
ALLOWED_METHODS = {
    "grol.system.status",
    "grol.update.status",
    "grol.network.status",
    "grol.hardware.status",
    "grol.service.status",
}
KNOWN_SERVICES = (
    "grol-hostd",
    "grol-healthd",
    "grol-identity",
    "grol-provision",
    "grol-ai-gateway",
    "grol-bot",
    "grol-action-broker",
    "docker",
    "networkmanager",
    "rauc",
    "supervisor",
    "os-agent",
)
SERVICE_UNITS = {
    "grol-hostd": "grol-hostd.service",
    "grol-healthd": "grol-healthd.service",
    "grol-identity": "grol-identity.service",
    "grol-provision": "grol-provision.service",
    "grol-ai-gateway": "grol-ai-gateway.service",
    "grol-bot": "grol-bot.service",
    "grol-action-broker": "grol-action-broker.service",
    "docker": "docker.service",
    "networkmanager": "NetworkManager.service",
    "rauc": "rauc.service",
    "supervisor": "hassio-supervisor.service",
    "os-agent": "haos-agent.service",
}

_BOOT = time.time()
_INFLIGHT: dict[int, int] = {}
_INFLIGHT_LOCK = threading.Lock()


def _read_kv(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return out
    for raw in text.splitlines():
        if not raw or raw.startswith("#") or "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        out[key.strip()] = value.strip().strip('"')
    return out


def _cmd_text(argv: list[str]) -> str | None:
    import subprocess

    try:
        proc = subprocess.run(
            argv, check=False, capture_output=True, text=True, timeout=2
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def peercred(conn: socket.socket) -> tuple[int, int, int] | None:
    try:
        raw = conn.getsockopt(
            socket.SOL_SOCKET, SO_PEERCRED, struct.calcsize(PEERCRED_FMT)
        )
    except OSError:
        return None
    pid, uid, gid = struct.unpack(PEERCRED_FMT, raw)
    return pid, uid, gid


def load_allowlist(path: Path | None) -> set[int] | None:
    if path is None or not path.is_file():
        return None
    allowed: set[int] = set()
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        allowed.add(int(line))
    return allowed


def acquire_slot(uid: int) -> bool:
    with _INFLIGHT_LOCK:
        used = _INFLIGHT.get(uid, 0)
        if used >= MAX_INFLIGHT:
            return False
        _INFLIGHT[uid] = used + 1
        return True


def release_slot(uid: int) -> None:
    with _INFLIGHT_LOCK:
        used = _INFLIGHT.get(uid, 0)
        if used <= 1:
            _INFLIGHT.pop(uid, None)
        else:
            _INFLIGHT[uid] = used - 1


def system_status() -> dict[str, Any]:
    osrel = _read_kv(Path("/etc/os-release"))
    if not osrel:
        osrel = _read_kv(Path("/usr/lib/os-release"))
    machine = _read_kv(Path("/etc/machine-info"))
    return {
        "status": "ok",
        "grol_version": osrel.get("VERSION_ID", "unknown"),
        "os_name": osrel.get("NAME", "GROL5000 OS"),
        "pretty_name": osrel.get("PRETTY_NAME", osrel.get("NAME", "GROL5000 OS")),
        "board": osrel.get("VARIANT_ID", machine.get("CHASSIS", "unknown")),
        "channel": machine.get("DEPLOYMENT", "unknown"),
        "uptime_seconds": int(time.time() - _BOOT),
    }


def update_status() -> dict[str, Any]:
    osrel = _read_kv(Path("/etc/os-release"))
    if not osrel:
        osrel = _read_kv(Path("/usr/lib/os-release"))
    rauc = _cmd_text(["rauc", "status"])
    slot = "unknown"
    rauc_state = "unavailable"
    if rauc:
        rauc_state = "ok"
        for line in rauc.splitlines():
            if "booted" in line.lower() and "[" in line:
                slot = line.split("[", 1)[0].strip()[-1:].upper() or "unknown"
                break
    return {
        "status": "degraded" if rauc_state == "unavailable" else "ok",
        "os_version": osrel.get("VERSION_ID", "unknown"),
        "active_slot": slot,
        "update_available": False,
        "rauc": rauc_state,
        "rollback_available": False,
        "components": {"rauc": rauc_state},
    }


def network_status() -> dict[str, Any]:
    primary = None
    has_default = False
    route = _cmd_text(["ip", "-4", "route", "show", "default"])
    if route:
        has_default = True
        parts = route.split()
        if "dev" in parts:
            primary = parts[parts.index("dev") + 1]
    dns_ok = Path("/etc/resolv.conf").is_file()
    connectivity = "online" if has_default else "offline"
    return {
        "status": "ok" if has_default else "degraded",
        "primary_interface": primary,
        "connectivity": connectivity,
        "ipv4": has_default,
        "default_route": has_default,
        "dns": "ok" if dns_ok else "unavailable",
    }


def hardware_status() -> dict[str, Any]:
    mem_total = None
    mem_avail = None
    try:
        for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
            if line.startswith("MemTotal:"):
                mem_total = int(line.split()[1]) * 1024
            elif line.startswith("MemAvailable:"):
                mem_avail = int(line.split()[1]) * 1024
    except OSError:
        pass
    pressure = "unavailable"
    if mem_total and mem_avail is not None:
        used = 1 - (mem_avail / mem_total)
        if used > 0.9:
            pressure = "critical"
        elif used > 0.75:
            pressure = "warn"
        else:
            pressure = "ok"
    return {
        "status": "ok" if mem_total else "degraded",
        "cpu_arch": os.uname().machine,
        "memory_total_bytes": mem_total,
        "memory_available_bytes": mem_avail,
        "memory_pressure": pressure,
        "storage_pressure": "unavailable",
    }


def _unit_state(unit: str) -> str:
    text = _cmd_text(["systemctl", "is-active", unit])
    if text == "active":
        return "running"
    if text == "inactive":
        return "stopped"
    if text in {"activating", "deactivating", "reloading"}:
        return "degraded"
    return "unavailable"


def service_status(name: str | None) -> dict[str, Any]:
    if name:
        if name not in KNOWN_SERVICES:
            return {"status": "error", "error": "unknown_service", "service": name}
        return {"status": "ok", "service": name, "state": _unit_state(SERVICE_UNITS[name])}
    components = {
        item: _unit_state(SERVICE_UNITS[item]) for item in KNOWN_SERVICES
    }
    return {"status": "ok", "components": components}


def dispatch(method: str, params: dict[str, Any]) -> dict[str, Any]:
    if method == "grol.system.status":
        return system_status()
    if method == "grol.update.status":
        return update_status()
    if method == "grol.network.status":
        return network_status()
    if method == "grol.hardware.status":
        return hardware_status()
    if method == "grol.service.status":
        return service_status(params.get("name"))
    return {"status": "error", "error": "unknown_method"}


def handle_request(raw: str) -> dict[str, Any]:
    try:
        msg = json.loads(raw)
    except json.JSONDecodeError:
        return {"ok": False, "error": "invalid_json"}
    if not isinstance(msg, dict):
        return {"ok": False, "error": "invalid_json"}
    req_id = msg.get("id")
    method = msg.get("method")
    params = msg.get("params") or {}
    if not isinstance(params, dict):
        return {"id": req_id, "ok": False, "error": "invalid_params"}
    if method not in ALLOWED_METHODS:
        return {"id": req_id, "ok": False, "error": "method_not_allowed", "method": method}
    result = dispatch(method, params)
    return {"id": req_id, "ok": True, "result": result}


def send_json(conn: socket.socket, payload: dict[str, Any]) -> None:
    data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    if len(data) > MAX_RESPONSE_BYTES:
        data = json.dumps(
            {"id": payload.get("id"), "ok": False, "error": "response_too_large"},
            separators=(",", ":"),
        ).encode("utf-8")
    conn.sendall(data + b"\n")


def serve_conn(conn: socket.socket, allow: set[int] | None) -> None:
    creds = peercred(conn)
    if creds is None:
        send_json(conn, {"ok": False, "error": "peercred_required"})
        return
    pid, uid, gid = creds
    if allow is not None and uid not in allow:
        send_json(conn, {"ok": False, "error": "forbidden", "uid": uid})
        return
    if not acquire_slot(uid):
        send_json(conn, {"ok": False, "error": "too_many_inflight"})
        return
    try:
        buf = b""
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                return
            buf += chunk
            if len(buf) > MAX_REQUEST_BYTES:
                send_json(conn, {"ok": False, "error": "request_too_large"})
                return
            if b"\n" in buf:
                raw, _rest = buf.split(b"\n", 1)
                send_json(conn, handle_request(raw.decode("utf-8", errors="replace")))
                return
    finally:
        release_slot(uid)
        _ = (pid, gid)


def run_server(sock_path: str, allowlist_path: str | None) -> None:
    path = Path(sock_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    allow = load_allowlist(Path(allowlist_path) if allowlist_path else None)
    if allow is None:
        allow = {os.getuid()}
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(sock_path)
    os.chmod(sock_path, 0o660)
    server.listen(8)
    while True:
        conn, _ = server.accept()
        threading.Thread(target=_safe_serve, args=(conn, allow), daemon=True).start()


def _safe_serve(conn: socket.socket, allow: set[int] | None) -> None:
    try:
        with conn:
            serve_conn(conn, allow)
    except OSError:
        return


def main() -> int:
    parser = argparse.ArgumentParser(description="GROL host API daemon")
    parser.add_argument("--socket", default="/run/grol/hostapi.sock")
    parser.add_argument("--allowlist", default="/etc/grol/hostapi-allowlist")
    args = parser.parse_args()
    run_server(args.socket, args.allowlist)
    return 0


if __name__ == "__main__":
    sys.exit(main())
