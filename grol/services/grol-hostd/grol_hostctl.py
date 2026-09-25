#!/usr/bin/env python3
"""Tiny Host API client for console / tests."""
from __future__ import annotations

import argparse
import json
import socket
import sys


def call(sock_path: str, method: str, params: dict | None = None) -> dict:
    req = {"id": "hostctl", "method": method, "params": params or {}}
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(5)
    client.connect(sock_path)
    client.sendall(json.dumps(req).encode("utf-8") + b"\n")
    buf = b""
    while b"\n" not in buf:
        chunk = client.recv(4096)
        if not chunk:
            break
        buf += chunk
    client.close()
    if not buf:
        raise SystemExit("empty response")
    return json.loads(buf.decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("method", nargs="?", default="grol.system.status")
    parser.add_argument("--socket", default="/run/grol/hostapi.sock")
    parser.add_argument("--name", help="optional service name for grol.service.status")
    args = parser.parse_args()
    params = {"name": args.name} if args.name else {}
    print(json.dumps(call(args.socket, args.method, params), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
