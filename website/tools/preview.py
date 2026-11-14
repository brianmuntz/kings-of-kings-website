from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import os,json
root=Path(__file__).resolve().parents[1];os.chdir(root)
class Handler(SimpleHTTPRequestHandler):
 def do_GET(self):
  if self.path=='/__version':
   s=str(max(p.stat().st_mtime_ns for p in root.rglob('*') if p.is_file()));self.send_response(200);self.send_header('Content-Type','text/plain');self.end_headers();self.wfile.write(s.encode());return
  return super().do_GET()
 def end_headers(self):
  self.send_header('X-Robots-Tag','noindex, nofollow');self.send_header('Cache-Control','no-cache');self.send_header('X-Content-Type-Options','nosniff');super().end_headers()
 def log_message(self,*args):pass
print('Kings rebuild preview: http://localhost:8090',flush=True)
ThreadingHTTPServer(('127.0.0.1',8090),Handler).serve_forever()
