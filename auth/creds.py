import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64

SCOPES = ['https://mail.google.com/']

def create_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message(to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['subject'] = subject
  b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
  b64_string = b64_bytes.decode()
  return {'raw': b64_string}

def send_message(to,subject,msgplain):
    service = create_service()
    msg = create_message(to,subject,msgplain)
    send_message_internal(service,'me',msg)
    return None

def send_message_internal(service, user_id, message):
    message = (service.users().messages().send(userId=user_id, body=message).execute())
    print('Message Id: %s' % message['id'])
    return message

to = input('Enter recipient email id: ')
subject = input('Enter subject: ')
msgPlain = input('msg plainText: ')
send_message(to,subject,msgPlain)