package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"sync"
	"syscall"
)

const (
	maxRequestBytes  = 4096
	maxResponseBytes = 16 * 1024
	maxInflight      = 2
)

func main() {
	sock := flag.String("socket", "/run/grol/hostapi.sock", "unix socket path")
	allow := flag.String("allowlist", "/etc/grol/hostapi-allowlist", "uid allowlist file")
	flag.Parse()
	if err := serve(*sock, *allow); err != nil {
		log.Fatal(err)
	}
}

func serve(sockPath, allowPath string) error {
	allow, err := loadAllowlist(allowPath)
	if err != nil || len(allow) == 0 {
		allow = map[int]struct{}{os.Getuid(): {}}
	}
	_ = os.Remove(sockPath)
	if err := os.MkdirAll(parentDir(sockPath), 0o750); err != nil {
		return err
	}
	ln, err := net.Listen("unix", sockPath)
	if err != nil {
		return err
	}
	if err := os.Chmod(sockPath, 0o660); err != nil {
		return err
	}
	slots := newLimiter()
	for {
		conn, err := ln.Accept()
		if err != nil {
			return err
		}
		go handleConn(conn, allow, slots)
	}
}

func parentDir(p string) string {
	for i := len(p) - 1; i >= 0; i-- {
		if p[i] == '/' {
			if i == 0 {
				return "/"
			}
			return p[:i]
		}
	}
	return "."
}

func handleConn(conn net.Conn, allow map[int]struct{}, slots *limiter) {
	defer conn.Close()
	ucred, err := peercred(conn)
	if err != nil {
		writeJSON(conn, Response{OK: false, Error: "peercred_required"})
		return
	}
	if _, ok := allow[int(ucred.Uid)]; !ok {
		writeJSON(conn, Response{OK: false, Error: "forbidden", UID: int(ucred.Uid)})
		return
	}
	uid := int(ucred.Uid)
	if !slots.acquire(uid) {
		writeJSON(conn, Response{OK: false, Error: "too_many_inflight"})
		return
	}
	defer slots.release(uid)

	r := bufio.NewReader(conn)
	var buf []byte
	for {
		b, err := r.ReadByte()
		if err != nil {
			return
		}
		buf = append(buf, b)
		if len(buf) > maxRequestBytes {
			writeJSON(conn, Response{OK: false, Error: "request_too_large"})
			return
		}
		if b == '\n' {
			writeJSON(conn, handleRequest(string(buf)))
			return
		}
	}
}

func peercred(conn net.Conn) (*syscall.Ucred, error) {
	uc, ok := conn.(*net.UnixConn)
	if !ok {
		return nil, fmt.Errorf("not unix")
	}
	rc, err := uc.SyscallConn()
	if err != nil {
		return nil, err
	}
	var cred *syscall.Ucred
	var inner error
	err = rc.Control(func(fd uintptr) {
		cred, inner = syscall.GetsockoptUcred(int(fd), syscall.SOL_SOCKET, syscall.SO_PEERCRED)
	})
	if err != nil {
		return nil, err
	}
	return cred, inner
}

type limiter struct {
	mu   sync.Mutex
	used map[int]int
}

func newLimiter() *limiter { return &limiter{used: map[int]int{}} }

func (l *limiter) acquire(uid int) bool {
	l.mu.Lock()
	defer l.mu.Unlock()
	if l.used[uid] >= maxInflight {
		return false
	}
	l.used[uid]++
	return true
}

func (l *limiter) release(uid int) {
	l.mu.Lock()
	defer l.mu.Unlock()
	if l.used[uid] <= 1 {
		delete(l.used, uid)
		return
	}
	l.used[uid]--
}

func writeJSON(conn net.Conn, payload Response) {
	data, err := json.Marshal(payload)
	if err != nil || len(data) > maxResponseBytes {
		data, _ = json.Marshal(Response{ID: payload.ID, OK: false, Error: "response_too_large"})
	}
	data = append(data, '\n')
	_, _ = conn.Write(data)
}
