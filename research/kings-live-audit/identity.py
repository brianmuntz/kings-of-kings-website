import json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
root=Path('outputs/kings-site');dest=root/'assets/identity';dest.mkdir(exist_ok=True)
rows=[]
for r in json.load(open('work/kings-live-audit/logo-media.json')):
 if r['id'] not in [1360,1357,1343,1135,1126]:continue
 path=Path('work/kings-live-audit')/f'logo-{r["id"]}.source';subprocess.run(['curl','-L','-s',r['source_url'],'-o',str(path)])
 im=Image.open(path);im.thumbnail((1600,1600));im.convert('RGBA').save(dest/f'logo-{r["id"]}.webp',quality=95)
 rows.append(dict(id=r['id'],image=f'/assets/identity/logo-{r["id"]}.webp',source=r['source_url']))
(root/'content/identity-sources.json').write_text(json.dumps(rows,indent=2)+'\n')
can=Image.new('RGB',(1000,900),'#ddd');d=ImageDraw.Draw(can)
for j,r in enumerate(rows):
 im=Image.open(root/r['image'].lstrip('/'));im.thumbnail((450,250));x=j%2*500;y=j//2*300;can.paste(im,(x,y),im if im.mode=='RGBA' else None);d.text((x,y+260),str(r['id']),fill='black')
can.save('work/kings-live-audit/identity-sheet.jpg')
