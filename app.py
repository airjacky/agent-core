"""agent-core: Agent 对话编排引擎（最小示例）"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

SERVICE_NAME = "agent-core"
PORT = 8000
TOOLS_AVAILABLE = 3


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/healthz"):
            self._send(200, {
                "service": SERVICE_NAME,
                "role": "Agent 对话编排引擎",
                "status": "ok",
            })
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/chat":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length else b"{}"
            try:
                message = json.loads(raw or b"{}").get("message", "")
            except json.JSONDecodeError:
                message = ""
            reply = f"我是 agent-flow 智能体，已收到：{message}" if message else "请输入 message 字段"
            self._send(200, {
                "service": SERVICE_NAME,
                "reply": reply,
                "tools_available": TOOLS_AVAILABLE,
            })
        else:
            self.send_response(404)
            self.end_headers()

    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"[{SERVICE_NAME}] listening on :{PORT}")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
