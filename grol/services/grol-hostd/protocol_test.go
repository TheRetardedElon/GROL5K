package main

import (
	"encoding/json"
	"fmt"
	"net"
	"os"
	"path/filepath"
	"testing"
	"time"
)

func TestRejectsMutation(t *testing.T) {
	out := handleRequest(`{"id":"1","method":"grol.host.reboot","params":{}}`)
	if out.OK {
		t.Fatal("expected reject")
	}
	if out.Error != "method_not_allowed" {
		t.Fatalf("got %q", out.Error)
	}
}

func TestSystemStatusShape(t *testing.T) {
	out := handleRequest(`{"id":"2","method":"grol.system.status"}`)
	if !out.OK {
		t.Fatalf("unexpected %#v", out)
	}
	res := out.Result.(map[string]any)
	if _, ok := res["grol_version"]; !ok {
		t.Fatal("missing grol_version")
	}
}

func TestUnknownService(t *testing.T) {
	out := handleRequest(`{"id":"3","method":"grol.service.status","params":{"name":"sshd"}}`)
	if !out.OK {
		t.Fatal(out)
	}
	res := out.Result.(map[string]any)
	if res["error"] != "unknown_service" {
		t.Fatalf("got %#v", res)
	}
}

func TestUnixRoundtrip(t *testing.T) {
	dir := t.TempDir()
	sock := filepath.Join(dir, "hostapi.sock")
	allow := filepath.Join(dir, "allow")
	if err := os.WriteFile(allow, []byte(fmt.Sprintf("%d\n", os.Getuid())), 0o644); err != nil {
		t.Fatal(err)
	}
	errCh := make(chan error, 1)
	go func() { errCh <- serve(sock, allow) }()

	deadline := time.Now().Add(2 * time.Second)
	var conn net.Conn
	var err error
	for time.Now().Before(deadline) {
		conn, err = net.Dial("unix", sock)
		if err == nil {
			break
		}
		time.Sleep(20 * time.Millisecond)
	}
	if err != nil {
		t.Fatal(err)
	}
	defer conn.Close()
	if _, err := conn.Write([]byte(`{"id":"rt","method":"grol.system.status"}` + "\n")); err != nil {
		t.Fatal(err)
	}
	buf := make([]byte, 4096)
	n, err := conn.Read(buf)
	if err != nil {
		t.Fatal(err)
	}
	var payload Response
	if err := json.Unmarshal(buf[:n], &payload); err != nil {
		t.Fatal(err, string(buf[:n]))
	}
	if !payload.OK || payload.ID != "rt" {
		t.Fatalf("%#v", payload)
	}
}
