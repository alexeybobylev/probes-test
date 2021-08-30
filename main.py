import http.server
import os
import socketserver
import logging
import sys
from time import sleep

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logs_handler = logging.StreamHandler(sys.stdout)
logs_handler.setLevel(logging.DEBUG)
logs_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logs_handler.setFormatter(logs_formatter)
logger.addHandler(logs_handler)

PORT = 8000


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        logger.debug(self.path)
        if self.path == '/die':
            self.response()
            exit(0)
        if self.path == '/startup':
            self.response(os.getenv('STARTUP', default=0))
        if self.path == '/liveness':
            self.response(os.getenv('LIVENESS', default=0))
        if self.path == '/readiness':
            self.response(os.getenv('READINESS', default=0))
        self.response()


    def response(self, wait=0):
        logger.debug("Sending response")
        self.send_response(200)
        logger.debug("Sending headers")
        self.send_header("Content-type", "text")
        logger.debug("Waiting")
        sleep(int(wait))
        logger.debug("Finishing request")
        self.end_headers()



Handler = MyHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
