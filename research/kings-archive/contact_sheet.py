from PIL import Image,ImageDraw
from pathlib import Path
paths=[Path('work/kings-archive/capleton-2009.png'),Path('work/kings-archive/reggaexclusive-2010.png'),Path('work/kings-archive/montreal.png')]
can=Image.new('RGB',(1200,760),'#ddd');d=ImageDraw.Draw(can)
for i,p in enumerate(paths):
 im=Image.open(p).convert('RGB');im.thumbnail((380,690));can.paste(im,(400*i,0));d.text((400*i,710),p.name,fill='black')
can.save('work/kings-archive/source-review.jpg')
import csv,re,collections
rows=list(csv.DictReader(open('/Volumes/Kings of Kings/Catalog Legal Research/Kings_catalog.csv',encoding='utf-8-sig')))
matches=[]
for r in rows:
 if r['Verification status']=='Discogs public API retrieved' and 'kings' in r['Label'].lower():
  files=list(Path('work/kings-archive').glob('R-'+r['Release ID']+'-*'))
  if files:matches.append((r['Artist'],r['Title'],r['Year'],files[0].name,Image.open(files[0]).size))
print('MATCHED',len(matches),matches[:18])
