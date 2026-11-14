const menu = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
menu?.addEventListener('click', () => {
  const expanded = menu.getAttribute('aria-expanded') === 'true';
  menu.setAttribute('aria-expanded', String(!expanded));
  navigation.classList.toggle('open', !expanded);
});
document.addEventListener('keydown', e => {
  if(e.key === 'Escape' && navigation?.classList.contains('open')) {
    navigation.classList.remove('open'); menu.setAttribute('aria-expanded','false'); menu.focus();
  }
});
document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('[data-filter]').forEach(b => { b.classList.toggle('active',b===button); b.setAttribute('aria-pressed',String(b===button)); });
  document.querySelectorAll('[data-city]').forEach(card => {card.hidden = button.dataset.filter !== 'all' && card.dataset.city !== button.dataset.filter;});
}));
const dialog = document.querySelector('#image-dialog');
document.querySelectorAll('[data-image]').forEach(button => button.addEventListener('click', () => {
  const img = dialog.querySelector('img');img.src = button.dataset.image;img.alt = button.dataset.alt;dialog.showModal();
}));
dialog?.querySelector('button').addEventListener('click', () => dialog.close());
dialog?.addEventListener('click', e => {if(e.target === dialog) dialog.close();});
if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observer = new IntersectionObserver(entries => entries.forEach(e => {if(e.isIntersecting){e.target.classList.add('reveal');observer.unobserve(e.target);}}), {threshold:.08});
  document.querySelectorAll('.culture-copy,.event-card,.pathways>a').forEach(el=>observer.observe(el));
}
// Local development only: refresh after a project file changes.
if (['localhost','127.0.0.1'].includes(location.hostname)) {
  let version;setInterval(async()=>{try{const r=await fetch('/__version',{cache:'no-store'});if(!r.ok)return;const v=await r.text();if(version && version!==v)location.reload();version=v;}catch{}},2000);
}
document.querySelectorAll('[data-show]').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('[data-show]').forEach(b=>{const active=b===button;b.classList.toggle('selected',active);b.setAttribute('aria-pressed',String(active));});
  document.querySelectorAll('[data-show-panel]').forEach(panel=>{panel.hidden=panel.dataset.showPanel!==button.dataset.show;});
}));
const catalogueSearch=document.querySelector('#catalogue-search');
const catalogueArtist=document.querySelector('#catalogue-artist');
function filterCatalogue(){
 if(!catalogueSearch)return;
 const query=catalogueSearch.value.toLowerCase().trim(),artist=catalogueArtist.value;let count=0;
 document.querySelectorAll('[data-catalogue-item]').forEach(item=>{const show=item.dataset.search.includes(query)&&(!artist||item.dataset.artist===artist);item.hidden=!show;if(show)count++;});
 document.querySelector('#catalogue-count').textContent=`${count} release${count===1?'':'s'}`;
 document.querySelector('#catalogue-empty').hidden=count>0;
}
catalogueSearch?.addEventListener('input',filterCatalogue);
catalogueArtist?.addEventListener('change',filterCatalogue);
if(catalogueSearch){catalogueSearch.value=new URLSearchParams(location.search).get('artist')||'';filterCatalogue();}
document.querySelectorAll('.current-releases').forEach(section=>{
 const flow=section.querySelector('.release-flow'),pause=section.querySelector('.release-pause');
 let paused=matchMedia('(prefers-reduced-motion: reduce)').matches,hover=false,focused=false,last=0,idleUntil=0;
 const update=()=>{pause.textContent=paused?'Resume motion':'Pause motion';pause.setAttribute('aria-pressed',String(paused));};update();
 pause.addEventListener('click',()=>{paused=!paused;update();});
 section.querySelector('.release-prev').addEventListener('click',()=>{idleUntil=performance.now()+7000;flow.scrollBy({left:-flow.clientWidth*.7,behavior:'smooth'});});
 section.querySelector('.release-next').addEventListener('click',()=>{idleUntil=performance.now()+7000;flow.scrollBy({left:flow.clientWidth*.7,behavior:'smooth'});});
 flow.addEventListener('mouseenter',()=>hover=true);flow.addEventListener('mouseleave',()=>hover=false);
 flow.addEventListener('focusin',()=>focused=true);flow.addEventListener('focusout',()=>focused=false);
 flow.addEventListener('pointerdown',()=>idleUntil=performance.now()+10000);flow.addEventListener('wheel',()=>idleUntil=performance.now()+10000,{passive:true});
 let direction=1;
 function move(now){const dt=Math.min(now-last,40);last=now;const rect=flow.getBoundingClientRect();if(!paused&&!hover&&!focused&&!document.hidden&&now>idleUntil&&rect.top<innerHeight&&rect.bottom>0){const max=flow.scrollWidth-flow.clientWidth;if(max>0){if(flow.scrollLeft>=max-1)direction=-1;if(flow.scrollLeft<=0)direction=1;flow.scrollLeft+=direction*dt*.018;}}requestAnimationFrame(move);}requestAnimationFrame(move);
});
document.querySelectorAll('.recent-shows').forEach(section=>{
 const slides=[...section.querySelectorAll('.show-slide')],pause=section.querySelector('[data-show-pause]');let index=0,paused=matchMedia('(prefers-reduced-motion: reduce)').matches,hover=false,focused=false;
 function show(next){index=(next+slides.length)%slides.length;slides.forEach((slide,i)=>slide.hidden=i!==index);const prev=section.querySelector('.show-preview-prev img'),after=section.querySelector('.show-preview-next img');if(prev)prev.src=slides[(index-1+slides.length)%slides.length].querySelector('img').src;if(after)after.src=slides[(index+1)%slides.length].querySelector('img').src;}
 section.querySelector('.show-preview-prev')?.addEventListener('click',()=>show(index-1));section.querySelector('.show-preview-next')?.addEventListener('click',()=>show(index+1));
 function label(){pause.textContent=paused?'Resume slideshow':'Pause slideshow';pause.setAttribute('aria-pressed',String(paused));}label();
 section.querySelector('[data-show-prev]').addEventListener('click',()=>show(index-1));section.querySelector('[data-show-next]').addEventListener('click',()=>show(index+1));pause.addEventListener('click',()=>{paused=!paused;label();});
 section.addEventListener('mouseenter',()=>hover=true);section.addEventListener('mouseleave',()=>hover=false);section.addEventListener('focusin',()=>focused=true);section.addEventListener('focusout',()=>focused=false);
 setInterval(()=>{const r=section.getBoundingClientRect();if(!paused&&!hover&&!focused&&!document.hidden&&r.top<innerHeight&&r.bottom>0)show(index+1);},6000);
});
const privacyNotice=document.querySelector('.privacy-notice');
try{if(privacyNotice&&!localStorage.getItem('kok_privacy_notice'))privacyNotice.hidden=false;}catch{if(privacyNotice)privacyNotice.hidden=false;}
document.querySelector('[data-privacy-accept]')?.addEventListener('click',()=>{try{localStorage.setItem('kok_privacy_notice','accepted');}catch{}privacyNotice.hidden=true;});
const enquiryDialog=document.querySelector('#enquiry-dialog'),enquiryForm=document.querySelector('#enquiry-form');
const enquiryTitles={giveaway:['Upliftment newsletter & giveaway','Sign up for Kings news and the album-release giveaway. Entrants must be 18 or older.'],bookings:['Event bookings','Tell us about your show, your act or the event you have in mind.'],artists:['Artist enquiries','Choose a record-release enquiry, an artist booking or booking Iley Dread.'],partners:['Sponsorship & charities','Introduce your charity or sponsorship proposal.'],'mailing-list':['Join the mailing list','Receive upcoming show announcements and Kings news.'],'top-15':['Kings of Kings Top 15','Be the first to hear when the chart launches.'],'contest-news':['Upliftment giveaway notifications','Get notified when rules and registration are available. This is not a contest entry.'],general:['General enquiries','Send the Kings of Kings team your question.']};
document.querySelectorAll('.enquiry-open').forEach(button=>button.addEventListener('click',()=>{
 const category=button.dataset.enquiry,[title,context]=enquiryTitles[category]||enquiryTitles.general;enquiryForm.reset();enquiryForm.elements.category.value=category;document.querySelector('#enquiry-title').textContent=title;document.querySelector('#enquiry-context').textContent=context;
 const subscription=['mailing-list','top-15','contest-news','giveaway'].includes(category);
 [['[data-event-fields]',category==='bookings'],['[data-artist-fields]',category==='artists']].forEach(([selector,on])=>{const area=enquiryDialog.querySelector(selector);area.hidden=!on;area.querySelectorAll('input,select').forEach(el=>el.disabled=!on);});
 const giveaway=['mailing-list','giveaway'].includes(category);
 ['[data-phone-field]','[data-location-field]'].forEach(selector=>{const area=enquiryDialog.querySelector(selector);area.hidden=giveaway;area.querySelector('input').disabled=giveaway;});
 const giveawayFields=enquiryDialog.querySelector('[data-giveaway-fields]');giveawayFields.hidden=!giveaway;giveawayFields.querySelectorAll('input').forEach(el=>{el.disabled=!giveaway;el.required=giveaway;});
 enquiryDialog.querySelector('[data-message-field]').hidden=giveaway;enquiryForm.elements.message.disabled=giveaway;
 enquiryForm.elements.message.required=!subscription;enquiryDialog.querySelector('[data-message-field]').firstChild.textContent=subscription?'Anything you would like us to know? (optional)':'Tell us the details';
 const consent=enquiryDialog.querySelector('[data-updates-consent]');consent.hidden=!subscription;enquiryForm.elements.updates_consent.required=subscription;enquiryForm.elements.updates_consent.disabled=!subscription;
 enquiryDialog.querySelector('.form-status').textContent='';enquiryDialog.showModal();
}));
enquiryDialog?.querySelector('.enquiry-close').addEventListener('click',()=>enquiryDialog.close());
enquiryForm?.addEventListener('submit',async event=>{
 event.preventDefault();if(!enquiryForm.reportValidity())return;const status=enquiryForm.querySelector('.form-status');
 if(['localhost','127.0.0.1'].includes(location.hostname)){status.textContent='Form reviewed. Email delivery is not configured, so nothing has been sent and you have not been registered.';return;}
 const submit=enquiryForm.querySelector('[type=submit]');submit.disabled=true;status.textContent='Sending…';
 try{const payload=Object.fromEntries(new FormData(enquiryForm));const response=await fetch('/api/enquiries',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});if(!response.ok)throw new Error('delivery');const result=await response.json();if(!result.sent)throw new Error('delivery');status.textContent='Thank you. Your message has been sent. Please check your inbox for confirmation.';enquiryForm.reset();}catch{status.textContent='Your message could not be sent. Please try again later. No registration has been confirmed.';}finally{submit.disabled=false;}
});
