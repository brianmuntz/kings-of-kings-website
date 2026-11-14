import json,subprocess,concurrent.futures
from pathlib import Path
from PIL import Image,ImageDraw
root=Path('work/kings-logo-research');dest=Path('outputs/kings-site/assets/identity/records');dest.mkdir(exist_ok=True)
def get(p):
 r=json.loads(p.read_text())
 if not r.get('images'):return
 url=r['images'][0]['uri'];out=root/(p.stem+'.source');subprocess.run(['curl','-L','-s','--max-time','20',url,'-o',str(out)])
 try:
  im=Image.open(out).convert('RGB');im.save(dest/(p.stem+'.webp'),lossless=True);return r
 except Exception:return
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=[r for r in ex.map(get,root.glob('*.json')) if r]
json.dump([r['id'] for r in rows],open(root/'downloaded.json','w'))
can=Image.new('RGB',(1200,((len(rows)+3)//4)*340),'white');d=ImageDraw.Draw(can)
for i,r in enumerate(sorted(rows,key=lambda r:r['year'])):
 im=Image.open(dest/(str(r['id'])+'.webp'));im.thumbnail((290,300));x=i%4*300;y=i//4*340;can.paste(im,(x,y));d.text((x,y+305),f"{r['id']} / {r['year']}",fill='black')
can.save(root/'sheet.jpg');print(len(rows))
