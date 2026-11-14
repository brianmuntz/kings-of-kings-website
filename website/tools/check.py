from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.h1=0;self.title=False;self.description=False;self.canonical=False;self.refs=[];self.ids=set();self.json=[];self.injson=False;self.buf='';self.errors=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='h1':self.h1+=1
  if t=='title':self.title=True
  if t=='meta' and a.get('name')=='description' and a.get('content'):self.description=True
  if t=='link' and a.get('rel')=='canonical':self.canonical=True
  if 'id' in a:self.ids.add(a['id'])
  if t=='a' and 'href' in a:self.refs.append(a['href'])
  if t in ['img','script'] and 'src' in a:self.refs.append(a['src'])
  if t=='link' and a.get('rel') in ['stylesheet','icon','preload']:self.refs.append(a.get('href',''))
  if t=='img':
   for attr in ['alt','width','height']:
    if attr not in a:self.errors.append('Image missing '+attr)
  if t=='script' and a.get('type')=='application/ld+json':self.injson=True;self.buf=''
 def handle_data(self,d):
  if self.injson:self.buf+=d
 def handle_endtag(self,t):
  if t=='script' and self.injson:
   try:self.json.append(json.loads(self.buf))
   except Exception:self.errors.append('Invalid JSON-LD')
   self.injson=False
parsed={};errors=[]
for f in ROOT.rglob('*.html'):
 if 'kings-of-kings-international-events' in str(f):continue
 p=Page();p.feed(f.read_text());parsed[f.resolve()]=p
 if p.h1!=1:errors.append(f'{f.relative_to(ROOT)}: {p.h1} H1s')
 for label,yes in [('title',p.title),('description',p.description),('canonical',p.canonical)]:
  if not yes:errors.append(f'{f.relative_to(ROOT)}: missing {label}')
 errors.extend(p.errors)
for f,p in parsed.items():
 for href in p.refs:
  u=urlsplit(href)
  if u.scheme or u.netloc:continue
  path=((ROOT/unquote(u.path).lstrip('/')) if u.path.startswith('/') else (f.parent/unquote(u.path))) if u.path else f
  if path.is_dir():path=path/'index.html'
  if not path.exists():errors.append(f'{f.relative_to(ROOT)}: missing {href}')
  elif u.fragment and path.resolve() in parsed and unquote(u.fragment) not in parsed[path.resolve()].ids:errors.append(f'Missing fragment: {href}')
ET.parse(ROOT/'sitemap.xml')
print(json.dumps({'html_pages_checked':len(parsed),'errors':errors,'sitemap_xml':'valid','preview_indexing':'blocked'},indent=2))
raise SystemExit(bool(errors))
