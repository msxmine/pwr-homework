import subprocess
import threading
import time
import json
import http.server

known_cookies = {}

def run_tcpdump():
    p1 = subprocess.Popen(("sudo", "tcpdump", "-A", "-l", "-i", "lo", "dst", "port", "5000"), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(("egrep", "--line-buffered" ,"^Cookie: |^Host: "), stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    return iter(p2.stdout.readline, b'')

def process_network():
    cur_host = ""
    for line in run_tcpdump():
        strval = line.decode("utf-8").rstrip("\n")
        if strval.startswith("Host: "):
            cur_host = strval[6:]
            continue
        if strval.startswith("Cookie: "):
            cookieline = strval[8:]
            cookies = cookieline.split("; ")
            cobj = {}
            for ck in cookies:
                carr = ck.split("=", 1)
                cobj[carr[0]] = carr[1]
            known_cookies[cur_host] = cobj


netthread = threading.Thread(target=process_network, daemon=True)
netthread.start()

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=UTF-8")
        self.end_headers()
        self.wfile.write(json.dumps(known_cookies).encode("utf-8"))

server = http.server.HTTPServer(("localhost", 5555), MyHandler)
server.serve_forever()

