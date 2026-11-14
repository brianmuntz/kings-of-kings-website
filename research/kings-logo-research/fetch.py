from pathlib import Path
import subprocess,json,concurrent.futures
ids=[20579713,2049478,7083051,4592070,4649171,4021445,2051414,2834348,3379025,7630819,6553253,1787965,2901628,3622065,4257524]
def fetch(i):
 p=Path(f'work/kings-logo-research/{i}.json');subprocess.run(['curl','-L','-s','--max-time','20','-A','KingsArchiveResearch/1.0',f'https://api.discogs.com/releases/{i}','-o',str(p)])
 try:
  r=json.loads(p.read_text());return (i,r.get('year'),r.get('title'),[(x['id'],x['name']) for x in r.get('labels',[])],len(r.get('images',[])))
 except Exception:return(i,'failed')
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for r in ex.map(fetch,ids):print(r)
