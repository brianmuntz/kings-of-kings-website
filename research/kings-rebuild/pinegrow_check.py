import tomllib,pathlib,urllib.request,json
c=tomllib.loads((pathlib.Path.home()/'.codex/config.toml').read_text())['mcp_servers']['pinegrow_desktop'];h=dict(c.get('http_headers',{}));h.update({'Content-Type':'application/json','Accept':'application/json, text/event-stream'})
def call(p):
 r=urllib.request.urlopen(urllib.request.Request(c['url'],data=json.dumps(p).encode(),headers=h),timeout=15)
 if r.headers.get('Mcp-Session-Id'):h['Mcp-Session-Id']=r.headers['Mcp-Session-Id']
 s=r.read().decode()
 for line in s.splitlines():
  if line.startswith('data: '):return json.loads(line[6:])
 return json.loads(s) if s else {}
try:
 call({'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'kings-project','version':'1.0'}}});call({'jsonrpc':'2.0','method':'notifications/initialized'})
 result=call({'jsonrpc':'2.0','id':2,'method':'tools/list','params':{}})
 print(json.dumps(result))
except Exception as e:print(type(e).__name__,str(e))
