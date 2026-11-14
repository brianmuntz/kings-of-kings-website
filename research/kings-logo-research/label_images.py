import json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
root=Path('outputs/kings-site/assets/identity/records');r=json.load(open('work/kings-logo-research/label.json'));can=Image.new('RGB',(1200,900),'white');d=ImageDraw.Draw(can)
for n,x in enumerate(r['images']):
 p=Path(f'work/kings-logo-research/brand-{n}.source');subprocess.run(['curl','-L','-s',x['uri'],'-o',str(p)]);im=Image.open(p).convert('RGB');im.save(root/f'brand-{n}.webp',lossless=True);im.thumbnail((580,400));can.paste(im,(n%2*600,n//2*450));d.text((n%2*600,n//2*450+410),str(n),fill='black')
can.save('work/kings-logo-research/brands.jpg')
