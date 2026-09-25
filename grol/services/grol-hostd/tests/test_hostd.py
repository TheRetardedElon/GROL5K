#!/usr/bin/env python3
import json
import os
import socket
import tempfile
import threading
import time
import unittest
from pathlib import Path

from grol_hostd import handle_request, run_server


class DispatchTests(unittest.TestCase):
    def test_rejects_mutation_shaped_methods(self):
        raw = json.dumps({"id": "1", "method": "grol.host.reboot", "params": {}})
        out = handle_request(raw)
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"], "method_not_allowed")

    def test_system_status_shape(self):
        raw = json.dumps({"id": "2", "method": "grol.system.status"})
        out = handle_request(raw)
        self.assertTrue(out["ok"])
        self.assertIn("grol_version", out["result"])
        self.assertIn("uptime_seconds", out["result"])

    def test_unknown_service_name(self):
        raw = json.dumps(
            {
                "id": "3",
                "method": "grol.service.status",
                "params": {"name": "sshd"},
            }
        )
        out = handle_request(raw)
        self.assertTrue(out["ok"])
        self.assertEqual(out["result"]["error"], "unknown_service")


class SocketTests(unittest.TestCase):
    def test_roundtrip_on_unix_socket(self):
        tmp = tempfile.mkdtemp(prefix="grol-hostd-")
        sock_path = str(Path(tmp) / "hostapi.sock")
        allow = Path(tmp) / "allow"
        allow.write_text(f"{os.getuid()}\n", encoding="utf-8")
        thread = threading.Thread(
            target=run_server, args=(sock_path, str(allow)), daemon=True
        )
        thread.start()
        deadline = time.time() + 3
        while not Path(sock_path).exists() and time.time() < deadline:
            time.sleep(0.05)
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.settimeout(3)
        client.connect(sock_path)
        client.sendall(
            json.dumps({"id": "rt", "method": "grol.system.status"}).encode()
            + b"\n"
        )
        buf = b""
        while b"\n" not in buf:
            buf += client.recv(4096)
        client.close()
        payload = json.loads(buf.decode())
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["id"], "rt")


if __name__ == "__main__":
    unittest.main()
