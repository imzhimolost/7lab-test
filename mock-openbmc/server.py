#!/usr/bin/env python3

import http.server
import socketserver
import json
import os
import sys

MOCK_DIR = os.path.dirname(os.path.abspath(__file__))

class OpenBMCRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=MOCK_DIR, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        # Redfish API
        if self.path == '/redfish/v1':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "@odata.id": "/redfish/v1",
                "RedfishVersion": "1.0.0",
                "Systems": {"@odata.id": "/redfish/v1/Systems"},
                "Managers": {"@odata.id": "/redfish/v1/Managers"}
            }
            self.wfile.write(json.dumps(response).encode())
            return

        elif self.path == '/redfish/v1/Managers/bmc':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "@odata.id": "/redfish/v1/Managers/bmc",
                "FirmwareVersion": "OpenBMC v2.10-mock",
                "ManagerType": "BMC"
            }
            self.wfile.write(json.dumps(response).encode())
            return

        elif self.path == '/redfish/v1/Systems/system':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "@odata.id": "/redfish/v1/Systems/system",
                "PowerState": "On"
            }
            self.wfile.write(json.dumps(response).encode())
            return

        # WebUI
        elif self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(os.path.join(MOCK_DIR, 'index.html'), 'rb') as f:
                self.wfile.write(f.read())
            return

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/login':
            # Простая аутентификация: принимаем любой POST
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "success"}')
            return
        self.send_response(404)
        self.end_headers()

if __name__ == '__main__':
    PORT = 4430
    httpd = socketserver.TCPServer(('localhost', PORT), OpenBMCRequestHandler)
    print(f"OpenBMC Mock запущен на http://localhost:{PORT}")
    print("   Redfish API: /redfish/v1")
    print("   WebUI: /")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹  Остановка сервера...")
        httpd.shutdown()