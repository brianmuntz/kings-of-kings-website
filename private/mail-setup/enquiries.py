"""Prepared mail transport. Wire behind POST /api/enquiries after hosting is chosen.
Never serve this file as a public asset. All configuration comes from environment.
"""
import os,re,ssl,smtplib,uuid
from email.message import EmailMessage
RECIPIENT='kingsofkingsinternational@gmail.com'
SENDER='no-reply@kingsofkingsinternational.com'
CATEGORIES={'bookings','artists','partners','general','mailing-list','top-15','contest-news','giveaway'}
FIELDS={'age_18':10,'winner_publicity':10,'name':120,'email':254,'phone':60,'location':160,'message':6000,'event_intent':80,'event_name':160,'event_date':20,'venue':250,'artist_intent':80,'artist_name':160,'music_url':1000,'category':40,'privacy_consent':10,'updates_consent':10,'website':250}
def validate(payload):
 if not isinstance(payload,dict):raise ValueError('Invalid enquiry')
 data={key:str(payload.get(key,''))[:limit].strip() for key,limit in FIELDS.items()}
 if data['website']:raise ValueError('Invalid enquiry')
 if data['category'] not in CATEGORIES or not data['name'] or data['privacy_consent']!='yes':raise ValueError('Complete the required fields')
 if '\r' in data['email'] or '\n' in data['email'] or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',data['email']):raise ValueError('Invalid email')
 if data['category'] in {'mailing-list','top-15','contest-news','giveaway'}:
  if data['updates_consent']!='yes':raise ValueError('Update consent is required')
 elif not data['message']:raise ValueError('Message is required')
 if data['category'] in {'mailing-list','giveaway'} and (data['age_18']!='yes' or data['winner_publicity']!='yes'):raise ValueError('Giveaway age and publication agreements are required')
 return data
def messages(data):
 reference=uuid.uuid4().hex[:12].upper()
 admin=EmailMessage();admin['From']=SENDER;admin['To']=RECIPIENT;admin['Reply-To']=data['email'];admin['Subject']=f"Kings enquiry: {data['category']} [{reference}]"
 admin.set_content('\n'.join(f'{key}: {value}' for key,value in data.items() if value and key!='website')+'\nReference: '+reference)
 acknowledgement=EmailMessage();acknowledgement['From']=SENDER;acknowledgement['To']=data['email'];acknowledgement['Subject']='Kings of Kings — we received your message'
 text='Thank you for contacting Kings of Kings International. We have received your '+data['category'].replace('-',' ')+' request. Our team will follow up as appropriate.\n\nReference: '+reference
 if data['category']=='contest-news':text+='\nThis is a notification request, not a contest entry.'
 if data['updates_consent']=='yes':text+='\nTo stop requested updates, reply to an update with “unsubscribe”.'
 acknowledgement.set_content(text+'\n\nPlease do not reply to this automated confirmation.\nKings of Kings International')
 return admin,acknowledgement
def deliver(payload):
 data=validate(payload)
 if os.getenv('KOK_MAIL_ENABLED')!='yes':raise RuntimeError('Email delivery is not configured')
 host=os.environ['KOK_SMTP_HOST'];port=int(os.getenv('KOK_SMTP_PORT','587'));user=os.environ['KOK_SMTP_USER'];password=os.environ['KOK_SMTP_PASSWORD']
 admin,ack=messages(data)
 with smtplib.SMTP(host,port,timeout=20) as smtp:
  smtp.ehlo();smtp.starttls(context=ssl.create_default_context());smtp.ehlo();smtp.login(user,password);smtp.send_message(admin)
  try:smtp.send_message(ack)
  except smtplib.SMTPException:return {'sent':True,'confirmation_sent':False}
 return {'sent':True,'confirmation_sent':True}
