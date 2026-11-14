from pathlib import Path
from PIL import Image
import csv,json,re,shutil,concurrent.futures,urllib.request,hashlib
out=Path('outputs/kings-site');dest=out/'assets/archive';dest.mkdir(exist_ok=True)
base=Path('/Volumes/MultiMedia-12TB/Colin Levy')
files={
'kings-international-logo':base/'KOK-Logo-profile.png','kings-records-logo':base/'2016/KOK WHITE.jpg','shows-display':base/"flyer's display.png",'miracle':base/'Miracle.jpg','unite-the-people':base/'Unite the people remastered art.jpg','cocoa-tea-2018':base/'1000-Degrees.jpg','lovers-holiday-ad':base/'2010/8x10 ad reggaeXclusive.jpg','release-showcase-2010':base/'2010/Single Release Party 2.jpg','lovers-holiday':base/'2011/cover for download site.jpg','unleashed-press':base/'2011/mag cover.jpg','western-consciousness-2011':base/'2011/western2.jpg','unleashed-2016':base/'2016/Iley-UNLEASHED-Cover-4x5.jpg','toronto-2016':base/'2016/May 1 flyer/Toronto Flyer 5x8.jpg','montreal-2016':Path('work/kings-archive/montreal.png'),'capleton-archive':Path('work/kings-archive/capleton-2009.png'),'unleashed-portrait':Path('work/kings-archive/reggaexclusive-2010.png'),'miracle-jamaica-day':base/'miracle jamacia day flyer.jpg'}
manifest=[]
for name,path in files.items():
 im=Image.open(path); w,h=im.size;profile=bool(im.info.get('icc_profile'));alpha='A' in im.getbands()
 # Web derivative only; preserve whole artwork, aspect ratio, and source files.
 im.thumbnail((1800,2200));im.save(dest/(name+'.webp'),'WEBP',quality=92)
 manifest.append({'name':name,'source':str(path),'source_dimensions':[w,h],'web_dimensions':list(im.size),'source_color_mode':Image.open(path).mode,'embedded_profile':profile,'alpha':alpha})
Path('work/kings-archive/asset-manifest.json').write_text(json.dumps(manifest,indent=2))
rows=list(csv.DictReader(open('/Volumes/Kings of Kings/Catalog Legal Research/Kings_catalog.csv',encoding='utf-8-sig')))
releases=[];seen=set()
for r in rows:
 if r['Verification status']!='Discogs public API retrieved' or 'kings' not in r['Label'].lower() or 'not established' in r['Catalog relationship']:continue
 key=(r['Artist'].lower(),r['Title'].lower())
 if key in seen:continue
 seen.add(key)
 releases.append({'id':r['Release ID'],'artist':re.sub(r' \(\d+\)|\*','',r['Artist']),'title':r['Title'],'year':r['Year'],'label':re.sub(r' \(\d+\)','',r['Label']),'catalogue':r['Catalog no.'],'format':r['Format / pressing'].split('|')[0].strip(),'source_url':r['Discogs URL'],'image_url':r['Image URLs'].split(' | ')[0], 'relationship':'release credit','source_status':'Discogs metadata in supplied catalogue','image':''})
def fetch(r):
 try:
  u=r['image_url']
  if not u.startswith('https://i.discogs.com/'):return
  data=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'KingsArchiveSite/1.0'}),timeout=20).read()
  import io
  im=Image.open(io.BytesIO(data))
  if min(im.size)<300:return
  im.thumbnail((800,800));im.convert('RGB').save(dest/('record-'+r['id']+'.webp'),'WEBP',quality=90);r['image']='/assets/archive/record-'+r['id']+'.webp'
 except Exception:pass
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(fetch,releases))
for r in releases:r.pop('image_url')
(out/'content/releases.json').write_text(json.dumps(releases,indent=2))
print('Prepared source artwork:',len(manifest),'Supported catalogue entries:',len(releases),'Record images:',sum(bool(r['image']) for r in releases))
