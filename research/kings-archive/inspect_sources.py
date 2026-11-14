from numbers_parser import Document
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
from psd_tools import PSDImage
from pypdf import PdfReader
import json,zipfile
base=Path('/Volumes/MultiMedia-12TB/Colin Levy');out=Path('work/kings-archive');out.mkdir(exist_ok=True)
with zipfile.ZipFile(base/'KOK discography/KOK label discography.numbers') as z:
 names=[n for n in z.namelist() if n.startswith('Data/')];print('EMBEDDED',names[:12],len(names))
 for n in names:
  if n.lower().endswith(('.jpg','.jpeg','.png')):(out/Path(n).name).write_bytes(z.read(n))
for rel,name in [('2009/Capleton Show BB KIng Blues Clug flyer.psd','capleton-2009'),('2010/Ad reggae exclusive cover rear.psd','reggaexclusive-2010')]:
 p=base/rel
 try:
  psd=PSDImage.open(p);im=psd.topil();im.thumbnail((1800,2200));im.save(out/(name+'.png'));print('PSD',name,psd.size)
 except Exception as e:print('PSD error',name,type(e).__name__)
p=base/'2017/Flyers for Colin/Montreal Flyer 5x8.pdf';print('PDF TEXT', ''.join(x.extract_text() or '' for x in PdfReader(p).pages)[:4500])
