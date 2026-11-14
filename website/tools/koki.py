#!/usr/bin/env python3
"""Local KOKI content editor. No credentials, network access or publishing."""
import argparse,datetime,json,re,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
COLLECTIONS={'events':'slug','releases':'id','featured-releases':'id','archive-stories':'id','current-releases':'id'}
def validate(kind,items):
    key=COLLECTIONS[kind];seen=set()
    required={'events':['title','date','display','city','venue','address','image','performers','description','status'],'releases':['artist','title','year','label','format','source_url'],'current-releases':['title','artist','edition','image','description'],'featured-releases':['title','artist','edition','image','description'],'archive-stories':['title','kicker','image','text','caption']}[kind]
    for item in items:
        ident=str(item.get(key,''))
        if not re.fullmatch(r'[a-zA-Z0-9_-]+',ident) or ident in seen:raise ValueError(f'{kind}: invalid or duplicate {key}: {ident}')
        seen.add(ident)
        for field in required:
            if field not in item:raise ValueError(f'{ident}: missing {field}')
        if kind=='events':
            datetime.date.fromisoformat(item['date'])
            if item['status'] not in ['past','upcoming','cancelled']:raise ValueError('Invalid event status')
            if not isinstance(item['performers'],list):raise ValueError('performers must be a list')
            if item['status']=='cancelled':raise ValueError('Cancelled events need a reviewed page template before applying')
        if item.get('ticket_url') and not item['ticket_url'].startswith('https://'):raise ValueError('Ticket URL must use HTTPS')
        if item.get('source_url') and not item['source_url'].startswith('https://'):raise ValueError('Source URL must use HTTPS')
        if item.get('image'):
            image=item['image'];target=(ROOT/image.lstrip('/')).resolve()
            if not image.startswith('/assets/') or not target.is_relative_to(ROOT/'assets') or not target.is_file():raise ValueError(f'{ident}: image missing or outside assets')
    return len(items)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['validate','update']);p.add_argument('--collection',choices=COLLECTIONS);p.add_argument('--file',type=Path);p.add_argument('--apply',action='store_true');a=p.parse_args()
    if a.command=='validate':
        for kind in COLLECTIONS:print(kind,validate(kind,json.loads((ROOT/'content'/f'{kind}.json').read_text())))
        return
    if not a.collection or not a.file:p.error('update requires --collection and --file containing one complete record')
    path=ROOT/'content'/f'{a.collection}.json';items=json.loads(path.read_text());record=json.loads(a.file.read_text());key=COLLECTIONS[a.collection]
    ident=record.get(key);existing=next((i for i,r in enumerate(items) if r[key]==ident),None)
    if existing is None:items.append(record)
    else:items[existing]=record
    validate(a.collection,items)
    print(('Update' if existing is not None else 'Add')+f' {ident}; collection validates ({len(items)} records).')
    if not a.apply:print('Preview only. No files changed. Add --apply to save.');return
    backup=ROOT/'.koki/backups'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f');backup.mkdir(parents=True);shutil.copy2(path,backup/path.name)
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(items,indent=2,ensure_ascii=False)+'\n');temp.replace(path)
    print('Saved with a recoverable backup. Run tools/build.py and tools/check.py, then inspect the preview.')
if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError) as e:sys.exit(str(e))
