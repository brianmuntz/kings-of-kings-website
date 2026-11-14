from pathlib import Path
import json,re
root=Path('outputs/kings-site');events=json.load(open(root/'content/events.json'));by={r['slug']:r for r in events};mapping={}
def link(nums,slug):
 for n in nums:mapping[n]=by[slug]
link([0,56,70],'30th-anniversary-2025');link([1,7,18,61,86],'tribute-to-the-legends-2024');link([2,8,19,62,81],'unite-the-people-2024');link([3,9,20,63,80],'wonderful-vibrations-2024');link([5],'reggae-extravaganza-brantford-2024');link([14],'rub-a-dub-live-2025');link([15],'icho-candy-toronto-2025');link([16,17,57,58],'lt-stitchie-benefit-2024');link([45,67],'reggae-ambassadors-pickering-2026');link([46,48,49,66],'reggae-ambassadors-toronto-2026');link([47],'sizzla-rise-to-the-occasion-2026');link([50,68],'reggae-ambassadors-niagara-2026');link([51],'31st-anniversary-montreal-2026');link([53],'31st-anniversary-toronto-2026');link([54,69],'oasis-music-festival-2025');link([55],'reggae-r-us-2025');link([59],'classic-super-d-2024');link([73],'reggae-extravaganza-oshawa-2025');link([74],'nostalgia-eban-brown-2025');link([77],'unleashed-toronto-2016');link([82],'magnum-christmas-extravaganza-2008')
posters=json.load(open(root/'content/live-event-posters.json'));posters={r['image']:r for r in posters}
rows=[]
for r in json.load(open(root/'content/live-flyer-collection.json')):
 n=re.search(r'live-(\d+)',r['image']);n=int(n[1]) if n else -1
 if n in [87,88]:continue # festival/community logos are not event flyers
 e=mapping.get(n);other=posters.get(r['image'])
 row={**r,'id':f'flyer-{n}' if n>=0 else 'lt-stitchie-benefit-inline','title':e['title'] if e else other['title'] if other else r['title'],'date':e['display'] if e else 'Date not fully confirmed','venue':e['venue'] if e else 'See original announcement','location':e['address'] if e else 'Not fully confirmed','stars':e['performers'] if e else [],'description':e['description'] if e else other['description'] if other else 'Original event campaign artwork preserved from the Kings of Kings website.','event_url':'/events/'+e['slug']+'/' if e else None}
 if n in [16,17,57,58,-1]:row['stars']=['Lt. Stitchie — benefit honouree'];row['description']+=' Guest lineups vary between poster versions; see the full original artwork.'
 details={4:('August 25, 2024','Venue not specified','Toronto, Ontario',['Iley Dread','Anthony B']),60:('October 13 — year disputed','Jamaican Canadian Association','995 Arrow Road, North York, Ontario',['I-Octane']),64:('August 23 — year unconfirmed','MTELUS','59 St Catherine Street East, Montréal',['Tony Rebel','Everton Blender','Jah Cuttah','Len Hammond','Etana','Natural Black','Moses I','Jah Mason','Warrior King','Anthony B','Richie Flo','Turbulence','Miss Diva','Aaron Silk']),65:('November 5, 2026','Scotiabank Arena','Toronto, Ontario',['Mavado','Armani','Masicka']),76:('December 19 — year not printed','Annex WreckRoom','794 Bathurst Street, Toronto',['Colin Levy','Lenn Hammond','Geoffrey Star','Chrisinti','Nana McLean']),83:('2006 — full date not supplied','Not specified on this cover','Not confirmed',['Beres Hammond','Capleton','Beenie Man','Buju Banton','Baby Cham','Gregory Isaacs','Assassin','Cocoa Tea']),84:('August 13 — year not legible','EB Club Lounge','5345 de Maisonneuve West, Montréal',['I-Octane','Stone Love','King Mee','Nikkit']),85:('March 1, 2008','South Birmingham College Auditorium','Birmingham, United Kingdom',['Ini Kamoze','Mutabaruka'])}
 if n in details:row['date'],row['venue'],row['location'],row['stars']=details[n]
 if n in [6,11,12]:row['date']='2024 campaign — no show date';row['location']={6:'Canada',11:'Germany',12:'Jamaica'}[n];row['stars']=[]
 rows.append(row)
(root/'content/flyers.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n');print('Individual flyers:',len(rows))
