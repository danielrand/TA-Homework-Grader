import imaplib
import base64
import os
import email

username = raw_input ('Username: ')
password = raw_input ('Password: ')

mail = imaplib.IMAP4_SSL("imap.gmail.com",993)
mail.login(username,password)
mail.select()

type, data = mail.search(None, 'ALL')
mail_ids = data[0]
id_list = mail_ids.split()

for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)' )
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    try:
    	email_message = email.message_from_string(raw_email_string)
    except Exception as e:
    	continue
# downloading attachments
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join('/Users/danielrand/Desktop/Queens_College_Classes/CS323_35(TA)', fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
            print('Downloaded "{file}" from email titled "{subject}".'.format(file=fileName, subject=subject))