package main

import (
	"encoding/json"
	"os"
	"strconv"
	"strings"
)

var allowedMethods = map[string]struct{}{
	"grol.system.status":   {},
	"grol.update.status":   {},
	"grol.network.status":  {},
	"grol.hardware.status": {},
	"grol.service.status":  {},
}

type Request struct {
	ID     any            `json:"id"`
	Method string         `json:"method"`
	Params map[string]any `json:"params"`
}

type Response struct {
	ID     any    `json:"id,omitempty"`
	OK     bool   `json:"ok"`
	Error  string `json:"error,omitempty"`
	Method string `json:"method,omitempty"`
	UID    int    `json:"uid,omitempty"`
	Result any    `json:"result,omitempty"`
}

func handleRequest(raw string) Response {
	raw = strings.TrimSpace(raw)
	var req Request
	if err := json.Unmarshal([]byte(raw), &req); err != nil {
		return Response{OK: false, Error: "invalid_json"}
	}
	if _, ok := allowedMethods[req.Method]; !ok {
		return Response{ID: req.ID, OK: false, Error: "method_not_allowed", Method: req.Method}
	}
	if req.Params == nil {
		req.Params = map[string]any{}
	}
	return Response{ID: req.ID, OK: true, Result: dispatch(req.Method, req.Params)}
}

func dispatch(method string, params map[string]any) map[string]any {
	switch method {
	case "grol.system.status":
		return systemStatus()
	case "grol.update.status":
		return updateStatus()
	case "grol.network.status":
		return networkStatus()
	case "grol.hardware.status":
		return hardwareStatus()
	case "grol.service.status":
		name, _ := params["name"].(string)
		return serviceStatus(name)
	default:
		return map[string]any{"status": "error", "error": "unknown_method"}
	}
}

func loadAllowlist(path string) (map[int]struct{}, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	out := map[int]struct{}{}
	for _, line := range strings.Split(string(data), "\n") {
		line = strings.TrimSpace(strings.Split(line, "#")[0])
		if line == "" {
			continue
		}
		n, err := strconv.Atoi(line)
		if err != nil {
			continue
		}
		out[n] = struct{}{}
	}
	return out, nil
}
