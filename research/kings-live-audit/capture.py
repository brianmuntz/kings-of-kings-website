import json,re,html,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
root=Path('work/kings-live-audit');dest=Path('outputs/kings-site/assets/live-archive');dest.mkdir(exist_ok=True)
items={}
for page in json.load(open(root/'pages.json'))+json.load(open(root/'posts.json')):
 for tag in re.findall(r'<img[^>]+>',page['content']['rendered']):
  src=re.search(r'src=[\"\']([^\"\']+)',tag)
  if not src or not src[1].startswith('https://kingsofkingsinternational.com/wp-content/uploads/'):continue
  url=html.unescape(src[1]);full=re.sub(r'-\d+x\d+(?=\.[^.]+$)','',url)
  if full in items:continue
  n=len(items);path=root/f'image-{n}.source';subprocess.run(['curl','-L','-s',full,'-o',str(path)])
  try:im=Image.open(path);im.load()
  except Exception:
   subprocess.run(['curl','-L','-s',url,'-o',str(path)])
   try:im=Image.open(path);im.load();full=url
   except Exception:continue
  im=ImageOps.exif_transpose(im).convert('RGB');size=im.size;im.thumbnail((1800,2200));im.save(dest/f'live-{n}.webp',quality=90)
  items[full]={'n':n,'url':full,'image':f'/assets/live-archive/live-{n}.webp','size':size,'page':page['link'],'alt':(re.search(r'alt=[\"\']([^\"\']*)',tag) or ['', ''])[1]}
json.dump(list(items.values()),open(root/'images.json','w'),indent=2)
can=Image.new('RGB',(1200,((len(items)+5)//6)*270),'#eee');d=ImageDraw.Draw(can)
for i,r in enumerate(items.values()):
 im=Image.open('outputs/kings-site'+r['image']);im.thumbnail((190,235));x=i%6*200;y=i//6*270;can.paste(im,(x,y));d.text((x,y+237),f"{r['n']} "+r['alt'][:22],fill='black')
can.save(root/'contact.jpg');print('Captured',len(items),'images')
