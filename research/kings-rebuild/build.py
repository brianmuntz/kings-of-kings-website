from pathlib import Path
import json,html,re,shutil,hashlib
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
from PIL import Image
ROOT=Path('/Users/brianmuntz/Documents/Codex/2026-10-14/w')
OUT=ROOT/'outputs/kings-site'; UP=ROOT/'work/kings-local/site/wp-content/uploads'; AS=OUT/'assets'; AS.mkdir(exist_ok=True)
def esc(s):return html.escape(str(s),quote=True)
def asset(rel,name=None):
 p=UP/rel
 if not p.is_file():return ''
 dest=AS/(name or p.name)
 shutil.copy2(p,dest)
 return '/assets/'+dest.name
def pic(rel,name):
 p=UP/rel;im=Image.open(p);im.thumbnail((1600,1600));dest=AS/(name+'.webp');im.convert('RGB').save(dest,'WEBP',quality=88)
 return '/assets/'+dest.name,im.width,im.height
logo=asset('2023/12/kok-header-logo.png','kings-logo.png')
hero,hw,hh=pic('2024/01/reggae-concert.jpg','concert')
brand,bw,bh=pic('2023/08/koki-splash.jpg','kings-culture')
art,aw,ah=pic('2023/08/Wonderfulvibrations-ai.jpg','wonderful-vibrations')
for filename in ['DMSans-Regular.woff2','DMSans-Bold.woff2']:
 shutil.copy2(ROOT/'work/kings-local/site/wp-content/themes/twentytwentythree/assets/fonts/dm-sans'/filename,AS/filename)
events=[
 {'slug':'reggae-ambassadors-pickering-2026','title':'Reggae Ambassadors Day Rave','date':'2026-10-11','display':'11 OCT 2026','city':'Pickering, Ontario','venue':'Aquário Beach Club','address':'949 Dillingham Road, Pickering, Ontario','image':pic('2026/09/Aquarios_oct_11-A-WEB.png','pickering-poster')[0], 'performers':['Marcia Griffiths','Turbulence','Jah Mason','Iley Dread','Angie Angel'],'description':'An afternoon and evening of live reggae at Aquário Beach Club, presented by Kings of Kings International and Farex Entertainment. The lineup featured Marcia Griffiths, Turbulence, Jah Mason, Iley Dread and Angie Angel.'},
 {'slug':'reggae-ambassadors-niagara-2026','title':'Reggae Ambassadors in Concert','date':'2026-10-10','display':'10 OCT 2026','city':'Niagara Falls, Ontario','venue':'The Columbus Room','address':'6990 Stanley Avenue, Niagara Falls, Ontario','image':pic('2026/08/NIAGRARA-October-10-SIDE-A-web.png','niagara-poster')[0], 'performers':['Marcia Griffiths','Turbulence','Jah Mason','Iley Dread','Angie Angel'],'description':'The Reggae Ambassadors concert brought Marcia Griffiths and a lineup of reggae performers to The Columbus Room in Niagara Falls.'},
 {'slug':'reggae-ambassadors-toronto-2026','title':'Reggae Ambassadors in Concert','date':'2026-10-09','display':'09 OCT 2026','city':'Toronto, Ontario','venue':'Phoenix Concert Theatre','address':'41 Sherbourne Street, Toronto, Ontario','image':pic('2026/06/October-A-side-with-web-1.png','toronto-poster')[0], 'performers':['Sister Nancy','Turbulence','Jah Mason','Iley Dread','Angie Angel'],'description':'Sister Nancy joined Turbulence, Jah Mason, Iley Dread and Angie Angel for the Toronto Reggae Ambassadors concert at Phoenix Concert Theatre.'}
]
(OUT/'content/events.json').write_text(json.dumps(events,indent=2))
SITE='https://kingsofkingsinternational.com'
nav=[('/studio/','Events'),('/about/','Our story'),('/gallery/','Gallery'),('/blog/','News'),('/contact/','Contact')]
pages={}
def image(src,alt,cls='',eager=False):
 path=OUT/src.lstrip('/');im=Image.open(path)
 return f'<img src="{esc(src)}" alt="{esc(alt)}" width="{im.width}" height="{im.height}" class="{cls}" loading="{"eager" if eager else "lazy"}" decoding="async"'+(' fetchpriority="high"' if eager else '')+'>'
def card(e):
 return f'''<article class="event-card"><a class="poster" href="/events/{e['slug']}/">{image(e['image'],e['title']+' — '+e['display']+' at '+e['venue'])}<span class="past-tag">PAST EVENT</span><span class="poster-arrow" aria-hidden="true">↗</span></a><div class="event-meta"><span>{e['display']}</span><span>{esc(e['city'].split(',')[0])}</span></div><h3><a href="/events/{e['slug']}/">{esc(e['title'])}</a></h3><p>{esc(e['venue'])}</p></article>'''
def shell(path,title,desc,body,extra=None):
 canonical=SITE+path
 schema=[{'@context':'https://schema.org','@type':'Organization','@id':SITE+'/#organization','name':'Kings of Kings International','url':SITE+'/','logo':SITE+logo,'email':'info@kingsofkingsinternational.com','sameAs':['https://www.facebook.com/KingsofKingsIntl/','https://www.instagram.com/kingsofkingsinternational/','https://www.youtube.com/@KingsofKingsInternational']}]
 if path!='/':schema.append({'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':SITE+'/'},{'@type':'ListItem','position':2,'name':title,'item':canonical}]})
 if extra:schema.append(extra)
 headtitle=title if path=='/' else title+' | Kings of Kings International'
 active=lambda url:' aria-current="page"' if url==path else ''
 links=''.join(f'<a href="{url}"{active(url)}>{name}</a>' for url,name in nav)
 document=f'''<!doctype html>
<html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(headtitle)}</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="noindex,nofollow"><link rel="canonical" href="{canonical}"><meta name="theme-color" content="#101510"><meta property="og:type" content="website"><meta property="og:title" content="{esc(headtitle)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE}{brand}"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/assets/favicon.png"><link rel="preload" href="/assets/DMSans-Regular.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/assets/site.css"><script type="application/ld+json">{json.dumps(schema).replace('</','<\\/')}</script><script src="/assets/site.js" defer></script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="header"><a class="logo" href="/" aria-label="Kings of Kings International home"><img src="{logo}" alt="Kings of Kings" width="600" height="146"></a><button class="menu-toggle" aria-expanded="false" aria-controls="navigation">Menu <span aria-hidden="true">☰</span></button><nav id="navigation" aria-label="Main navigation">{links}<a class="nav-cta" href="/contact/#bookings">Work with us <span aria-hidden="true">↗</span></a></nav></header><main id="main">{body}</main><footer><div class="footer-top"><p class="eyebrow">THE MUSIC CONNECTS US.</p><a href="/contact/">Let’s make<br>something <em>move.</em> <span aria-hidden="true">↗</span></a></div><div class="footer-bottom"><div><strong>KINGS OF KINGS<br>INTERNATIONAL</strong><p>Roots. Culture. Truth. Love.</p></div><nav aria-label="Footer navigation"><a href="/studio/">Events</a><a href="/programs/">Merchandise</a><a href="/tickets/">Tickets</a><a href="/contact/">Contact</a><a href="/site-map/">Site map</a></nav><div class="socials"><a href="https://www.instagram.com/kingsofkingsinternational/">Instagram ↗</a><a href="https://www.facebook.com/KingsofKingsIntl/">Facebook ↗</a><a href="https://www.youtube.com/@KingsofKingsInternational">YouTube ↗</a></div></div><div class="copyright"><span>© 2026 Kings of Kings International</span><span>REGGAE. LIVE. WORLDWIDE.</span></div></footer><dialog id="image-dialog"><button class="dialog-close" aria-label="Close image">Close ×</button><img src="{brand}" alt=""></dialog></body></html>'''
 target=OUT/('index.html' if path=='/' else path.strip('/')+'/index.html');target.parent.mkdir(parents=True,exist_ok=True);target.write_text(document)
 pages[path]={'title':headtitle,'description':desc}
def intro(kicker,title,text):return f'<section class="page-intro"><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="intro-text">{text}</p></section>'
home=f'''<section class="hero"><div class="hero-photo">{image(hero,'Concert crowd beneath green and gold stage lights',eager=True)}</div><div class="hero-content"><p class="eyebrow"><span class="live-dot"></span> KINGS OF KINGS INTERNATIONAL</p><h1>ROOTS.<br>CULTURE.<br><em>LIVE.</em></h1><p>Reggae that brings us together.<br>Concerts, culture and unforgettable live performances.</p><div class="hero-actions"><a class="button gold" href="/studio/">Explore the events <span aria-hidden="true">↗</span></a><a class="text-link" href="/about/">Discover our story <span aria-hidden="true">→</span></a></div></div><div class="hero-caption"><span>FROM THE ROOTS. FOR THE PEOPLE.</span><a href="#latest" aria-label="Scroll to the latest events">SCROLL TO EXPLORE ↓</a></div></section>
<div class="ticker" aria-hidden="true"><div>ROOTS REGGAE <b>✳</b> LIVE CULTURE <b>✳</b> POSITIVE VIBRATIONS <b>✳</b> KINGS OF KINGS <b>✳</b> ROOTS REGGAE <b>✳</b> LIVE CULTURE <b>✳</b> POSITIVE VIBRATIONS <b>✳</b></div></div>
<section class="section events-section" id="latest"><div class="section-heading"><div><p class="eyebrow">THE LIVE EXPERIENCE / EVENT ARCHIVE</p><h2>Good music.<br><em>Great memories.</em></h2></div><a class="text-link" href="/studio/">Explore all events ↗</a></div><div class="event-grid">{''.join(card(e) for e in events)}</div><div class="announcement"><span class="status-dot"></span><div><strong>Be part of what’s next.</strong><p>For upcoming show announcements, follow Kings of Kings or contact our events team.</p></div><a class="text-link" href="/contact/#bookings">Get in touch ↗</a></div></section>
<section class="culture section"><div class="culture-image">{image(brand,'Kings of Kings International crown artwork with reggae colours and a concert audience')}</div><div class="culture-copy"><p class="eyebrow">MORE THAN A SHOW</p><h2>The roots run deep.<br><em>The music lives on.</em></h2><p>Kings of Kings International brings people together through roots reggae, lover’s rock and uplifting live performances.</p><p>From international concert lineups to Wonderful Vibrations showcases, the connection between artists and audiences is at the heart of every gathering.</p><a class="button outline" href="/about/">Meet Kings of Kings ↗</a></div></section>
<section class="section pathways"><p class="eyebrow">FIND YOUR CONNECTION</p><a href="/contact/#bookings"><span>01 / LIVE EVENTS</span><h2>Bring the experience.</h2><span aria-hidden="true">↗</span></a><a href="/contact/#artists"><span>02 / ARTISTS</span><h2>Share your sound.</h2><span aria-hidden="true">↗</span></a><a href="/contact/#partners"><span>03 / PARTNERSHIPS</span><h2>Build something together.</h2><span aria-hidden="true">↗</span></a></section>'''
shell('/','Kings of Kings International | Reggae Concerts & Culture','Discover Kings of Kings International: reggae concerts, Wonderful Vibrations showcases, event archives, artist enquiries and partnerships.',home)
shell('/studio/','Reggae Events & Concert Archive','Explore Kings of Kings International reggae concerts in Toronto, Niagara Falls and Pickering, with past-event details and upcoming-show enquiries.',intro('LIVE MUSIC / SHARED EXPERIENCES','The music.<br><em>The moments.</em>','Explore the Kings of Kings event archive. For new show announcements and booking enquiries, connect with our team.')+f'<section class="section"><div class="filter-row" role="group" aria-label="Filter events by city"><button class="filter active" data-filter="all" aria-pressed="true">All cities</button>'+''.join(f'<button class="filter" data-filter="{c}" aria-pressed="false">{c}</button>' for c in ['Toronto','Niagara Falls','Pickering'])+f'</div><div class="event-grid filter-grid">'+''.join('<div data-city="'+e['city'].split(',')[0]+'">'+card(e)+'</div>' for e in events)+'</div><p class="small-note">These events have taken place. Archived posters may contain expired ticket offers.</p><a class="button outline" href="/reggae-events/">Explore earlier concerts ↗</a></section>')
for e in events:
 path='/events/'+e['slug']+'/'
 extra={'@context':'https://schema.org','@type':'Event','name':e['title'],'startDate':e['date'],'eventStatus':'https://schema.org/EventScheduled','eventAttendanceMode':'https://schema.org/OfflineEventAttendanceMode','location':{'@type':'Place','name':e['venue'],'address':e['address']},'image':[SITE+e['image']],'description':e['description'],'organizer':{'@id':SITE+'/#organization'},'url':SITE+path}
 shell(path,e['title']+' — '+e['city'].split(',')[0]+' '+e['display'],e['description'],intro('EVENT ARCHIVE / '+e['display'],esc(e['title']),esc(e['city']))+f'<section class="section event-detail"><div class="detail-poster">{image(e["image"],e["title"]+" original event poster")}</div><div class="detail-copy"><span class="label">PAST EVENT</span><h2>{esc(e["venue"])}</h2><p>{esc(e["description"])}</p><dl><dt>Date</dt><dd><time datetime="{e["date"]}">{e["display"]}</time></dd><dt>Venue</dt><dd>{esc(e["venue"])}</dd><dt>Location</dt><dd>{esc(e["address"])}</dd></dl><h3>Featured performers</h3><p>{esc(" · ".join(e["performers"]))}</p><p class="small-note">This event has taken place. The original poster is preserved as an archive; ticket prices and offers are no longer current.</p><a class="button gold" href="/contact/#bookings">Ask about upcoming events ↗</a><a class="back-link" href="/studio/">← Back to events</a></div></section>',extra)
shell('/about/','Our Story: Reggae, Culture & Live Music','Learn about Kings of Kings International and its roots reggae, lover’s rock, Wonderful Vibrations showcases and international live performances.',intro('OUR STORY','Rooted in reggae.<br><em>Connected by culture.</em>','Kings of Kings International brings artists and audiences together through live music, positive vibrations and a shared love of reggae.')+f'<section class="section culture"><div class="culture-image">{image(art,"Kings of Kings Wonderful Vibrations illustrated lion and musician artwork")}</div><div class="culture-copy"><p class="eyebrow">WONDERFUL VIBRATIONS</p><h2>Music with<br><em>meaning.</em></h2><p>The Wonderful Vibrations showcase brings together reggae performers and audiences in a celebration of the music and the culture behind it.</p><p>Our programme spans roots reggae, lover’s rock and Christian reggae, alongside concerts, stage performances and opportunities for artists to connect.</p><a class="button gold" href="/contact/">Connect with the team ↗</a></div></section><section class="section statement"><p class="eyebrow">WHAT BRINGS US TOGETHER</p><h2>ROOTS. CULTURE.<br>TRUTH. <em>LOVE.</em></h2></section>')
contacts=[('bookings','Event bookings','Bring Kings of Kings to your venue, or ask about upcoming shows.','events@kingsofkingsinternational.com'),('artists','Artist enquiries','Connect about performances and artist registration.','artists@kingsofkingsinternational.com'),('partners','Sponsorship','Talk with us about event sponsorship and partnerships.','sponsorship@kingsofkingsinternational.com'),('merchandise','Merchandise','Ask about merchandise and affiliation opportunities.','merchandise@kingsofkingsinternational.com'),('contests','Contest registration','Ask our team about current competitions and eligibility.','contest@kingsofkingsinternational.com'),('general','General enquiries','For everything else, start here.','info@kingsofkingsinternational.com')]
shell('/contact/','Contact & Event Booking Enquiries','Contact Kings of Kings International for event bookings, artist enquiries, sponsorship, merchandise and general information.',intro('LET’S CONNECT','Good things start<br><em>with a conversation.</em>','Find the right team for your enquiry. Email us directly using the contact details below.')+'<section class="section contact-grid">'+''.join(f'<article id="{i}"><span class="eyebrow">0{n+1}</span><h2>{t}</h2><p>{d}</p><a href="mailto:{email}">{email} <span aria-hidden="true">↗</span></a></article>' for n,(i,t,d,email) in enumerate(contacts))+'</section>')
# Preserve substantive legacy content in clean HTML instead of carrying builder markup and scripts.
class Extract(HTMLParser):
 def __init__(self):super().__init__();self.blocks=[];self.tag=None;self.buf=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ['script','style']:self.skip+=1
  if not self.skip and tag in ['p','h1','h2','h3','h4','li']:
   if self.tag:self.endblock()
   self.tag=tag;self.buf=[]
 def handle_endtag(self,tag):
  if tag in ['script','style']:self.skip=max(0,self.skip-1)
  if tag==self.tag:self.endblock()
 def handle_data(self,data):
  if self.tag and not self.skip:self.buf.append(data)
 def endblock(self):
  text=' '.join(' '.join(self.buf).split())
  if text:self.blocks.append((self.tag,text))
  self.tag=None;self.buf=[]
def legacy_blocks(page):
 parser=Extract();parser.feed(page['content']['rendered']);seen=set();out=[]
 for tag,txt in parser.blocks:
  if txt in seen or len(txt)<12:continue
  if any(s in txt.lower() for s in ['buy tickets','tickets are expected','first 100','register your advanced']):continue
  seen.add(txt);out.append(f'<{"h2" if tag.startswith("h") else "p"}>{esc(txt)}</{"h2" if tag.startswith("h") else "p"}>')
 return ''.join(out)
source=json.loads((ROOT/'work/kings-rebuild/source/pages.json').read_text())
for slug,title,desc in [('reggae-events','Earlier Reggae Events','Explore the Kings of Kings International archive of earlier reggae concerts, performers and cultural events.'),('canada','Canada Concert Archive','Explore archived Canadian reggae concert information from Kings of Kings International and Wonderful Vibrations.'),('blog','News & Statements Archive','Read archived news and statements from Kings of Kings International.')]:
 page=next(x for x in source if x['slug']==slug)
 body=intro('FROM THE ARCHIVE',title,'Historical content from the original Kings of Kings website. Dates, venue information and offers below refer to earlier events.')+'<section class="section reading"><aside class="archive-note">Archive: these announcements are retained for reference. For current events and enquiries, <a href="/contact/">contact our team</a>.</aside>'+legacy_blocks(page)+'</section>'
 shell('/'+slug+'/',title,desc,body)
# Gallery: keep source images with honest descriptions, not invented concert photography.
gallerypage=next(x for x in source if x['slug']=='gallery')
urls=list(dict.fromkeys(re.findall(r'<img[^>]+src=[\"\']([^\"\']+)',gallerypage['content']['rendered'])))[:12]
gallery=[]
for i,url in enumerate(urls):
 if '/uploads/' not in url:continue
 rel=unquote(url.split('/uploads/',1)[1]);p=UP/rel
 if not p.exists():continue
 try:
  src,w,h=pic(rel,'gallery-'+str(i));gallery.append(f'<button class="gallery-item" data-image="{src}" data-alt="Kings of Kings original visual archive, image {i+1}" aria-label="Enlarge archive image {i+1}">{image(src,"Kings of Kings visual archive — branded illustration or merchandise artwork")}<span aria-hidden="true">↗</span></button>')
 except Exception:pass
shell('/gallery/','Kings of Kings Visual Archive','Explore the Kings of Kings International visual archive, including branded artwork, Wonderful Vibrations imagery and merchandise designs.',intro('THE VISUAL ARCHIVE','A culture.<br><em>A world of colour.</em>','Explore original Kings of Kings artwork and merchandise imagery. These images include illustrations and product mockups from the existing site.')+'<section class="section gallery-grid">'+''.join(gallery)+'</section>')
shell('/programs/','Merchandise & Affiliation Enquiries','Ask Kings of Kings International about reggae-inspired merchandise, product availability and merchandise affiliation opportunities.',intro('KINGS OF KINGS / MERCHANDISE','Wear the culture.<br><em>Carry the vibration.</em>','Reggae-inspired artwork and merchandise from the Kings of Kings collection.')+f'<section class="section culture"><div class="culture-image">{image("/assets/gallery-1.webp" if (AS/"gallery-1.webp").exists() else brand,"Kings of Kings merchandise artwork")}</div><div class="culture-copy"><span class="label">AVAILABILITY BY ENQUIRY</span><h2>Made for<br><em>reggae lovers.</em></h2><p>The original collection features apparel, bags and mugs inspired by reggae culture. Contact the merchandise team for current product availability and affiliation enquiries.</p><a class="button gold" href="mailto:merchandise@kingsofkingsinternational.com">Enquire about merchandise ↗</a></div></section>')
shell('/tickets/','Tickets & Show Information','Contact Kings of Kings International for current reggae concert announcements, ticket availability and official purchasing information.',intro('TICKETS / OFFICIAL INFORMATION','Your next<br><em>live experience.</em>','The October 2026 Reggae Ambassadors shows have taken place. Contact the events team for confirmed upcoming dates and official ticket information.')+'<section class="section ticket-panel"><p class="eyebrow">CHECK BEFORE YOU BOOK</p><h2>Find your next show.</h2><p>We’ll share confirmed dates and official ticket links when new events are announced. Archived posters and old retail listings may contain expired prices or offers.</p><a class="button gold" href="mailto:events@kingsofkingsinternational.com">Ask about tickets ↗</a><a class="text-link" href="/studio/">Browse the event archive →</a></section>')
shell('/site-map/','Site Map','Find Kings of Kings International events, archives, contact information, merchandise enquiries and company information. ',intro('EXPLORE','Find your way.','Every section of Kings of Kings International, in one place.')+'<section class="section reading"><ul class="sitemap-links">'+''.join(f'<li><a href="{p}">{esc(v["title"].split(" | ")[0])}</a></li>' for p,v in list(pages.items()))+'</ul></section>')
shell('/404/','Page Not Found','Find your way back to Kings of Kings International events, artist enquiries and reggae culture.',intro('404 / PAGE NOT FOUND','Lost in the rhythm?','This page couldn’t be found. Explore our events or return to the homepage.')+'<section class="section"><a class="button gold" href="/">Back to home ↗</a></section>')
shutil.copy2(OUT/'404/index.html',OUT/'404.html')
# Keep legacy home route reachable without duplicate content when deployed.
p=OUT/'kings-of-kings-international-events';p.mkdir(exist_ok=True);(p/'index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Kings of Kings International</title><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=/"><link rel="canonical" href="'+SITE+'/"></head><body><a href="/">Kings of Kings International home</a></body></html>')
(OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+SITE+p+'</loc></url>' for p in pages if p!='/404/')+'</urlset>')
(OUT/'.htaccess').write_text('Options -Indexes\nErrorDocument 404 /404.html\n<IfModule mod_rewrite.c>\nRewriteEngine On\nRewriteRule ^kings-of-kings-international-events/?$ / [R=301,L]\n</IfModule>\n<IfModule mod_headers.c>\nHeader always set X-Content-Type-Options "nosniff"\nHeader always set Referrer-Policy "strict-origin-when-cross-origin"\n</IfModule>\n')
# Existing icon, preserved without redrawing the identity.
asset('2023/08/kok-logo-ico-4.png','favicon.png')
(OUT/'content/page-index.json').write_text(json.dumps(pages,indent=2))
print('Built',len(pages),'pages. Preview remains noindex. Existing branding/assets preserved; live site unchanged.')
