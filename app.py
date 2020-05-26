from googleapiclient.discovery import build
from apiclient import errors
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from credentials import get_credentials

credentials = get_credentials()
service = build('gmail','v1',credentials=credentials)
#see labels
results = service.users().labels().list(userId = 'me').execute()
labels = results.get('labels',[])

for label in labels:
    print(label['name'])

#create message
def create_message(sender,to,subject,msgPlain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msgPlain,'plain'))
    b64_bytes = base64.urlsafe_b64encode(msg.as_bytes())
    b64_string = b64_bytes.decode()
    return {'raw':b64_string}

#send message
def send_message(sender,to,subject,msgPlain):
    credentials = get_credentials()
    service = build('gmail', 'v1', credentials=credentials)
    msg = create_message(sender,to,subject,msgPlain)
    return send_messsage_Internal(service,'me',msg)

def send_messsage_Internal(service,user_id,message):
    try:
        message = service.users().messages().send(userId=user_id,body = message).execute()
        print('message Id: %s'%message['id'])
        return message
    except errors.HttpError as error:
        print('error')
        return error
def main():
    to = input('Enter recipient email id: ')
    sender = input('Enter your email id: ')
    subject = input('Enter subject: ')
    msgPlain = input('msg plainText')
    send_message(sender,to,subject,msgPlain)
if __name__ == '__main__':
    main()
