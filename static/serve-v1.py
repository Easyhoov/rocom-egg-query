#!/usr/bin/env python3
"""新项目原型服务器 — 端口 20204，干净URL映射到 -v1.html，/api/ 代理到 2026"""
import http.server
import socketserver
import urllib.request
import urllib.error
import os

PORT = 20204
STATIC_DIR = "/root/.hermes/projects/rocom-egg-query/static"
API_BACKEND = "http://127.0.0.1:2026"

# 干净URL → 文件映射
ROUTES = {
    "/": "home-v1.html",
    "/egg-query": "egg-query-v1.html",
    "/compendium": "compendium-v1.html",
    "/compendium-detail": "compendium-detail-v1.html",
    "/egg-group": "egg-group-v1.html",
    "/garden": "garden-v1.html",
    "/merchant": "merchant-v1.html",
}

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_GET(self):
        # API 代理：转发到 2026 端口
        if self.path.startswith("/api/"):
            return self._proxy_to_backend()

        # 精确匹配路由
        if self.path in ROUTES:
            self.path = "/" + ROUTES[self.path]
        # 带子路径的 compendium (如 /compendium/5)
        elif self.path.startswith("/compendium/") and self.path != "/compendium-detail":
            self.path = "/" + ROUTES["/compendium-detail"]
        return super().do_GET()

    def _proxy_to_backend(self):
        """代理 /api/ 请求到 2026 端口"""
        target_url = API_BACKEND + self.path
        try:
            req = urllib.request.Request(target_url)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                self.send_response(resp.status)
                # 转发 Content-Type
                content_type = resp.headers.get("Content-Type", "application/json")
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(data)))
                # CORS 头
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(f'{{"error": "Backend unavailable: {str(e)}"}}'.encode())

    def log_message(self, format, *args):
        pass  # 静默日志

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

if __name__ == "__main__":
    with ThreadedHTTPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"新项目原型服务器: http://0.0.0.0:{PORT}")
        print(f"API 代理: /api/* → {API_BACKEND}/api/*")
        httpd.serve_forever()
