'"""
A simple HTTP server for the BitOS Cloud Dashboard v3.

This script runs a basic HTTP server and serves the dashboard.
"""

import http.server
import socketserver

PORT = 8080

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    pass

with socketserver.TCPServer(('', PORT), MyRequestHandler) as httpd:8080
    print(f"Serving at port {PORT}")
    httpd.serve_forever()