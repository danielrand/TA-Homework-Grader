import imaplib
import base64
import os
import email
from email.parser import HeaderParser

def get_mostnew_email(messages):
    # Getting in most recent emails
    ids = messages[0]  # data is a list.
    id_list = ids.split()  # ids is a space separated string
    #latest_ten_email_id = id_list  # get all
    latest_ten_email_id = id_list[-75:]  # get the latest 10
    keys = map(int, latest_ten_email_id)
    news_keys = sorted(keys, reverse=True)
    str_keys = [str(e) for e in news_keys]
    return  str_keys

username = raw_input ('Username: ')
password = raw_input ('Password: ')
folder = raw_input ('Path of Dirctory to save the projects in: ')
projectInput = raw_input ('Search string for project: ')

mail = imaplib.IMAP4_SSL("imap.gmail.com",993)
mail.login(username,password)
mail.select()
mail.select()
(retcode, messages) =mail.search(None, 'ALL')
news_mail = get_mostnew_email(messages)

for i in news_mail :
    typ, data = mail.fetch(i, '(RFC822)')
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    try:
        email_message = email.message_from_string(raw_email_string)
    except Exception as e:
        continue
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        subjectString = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
        subject = subjectString.lower().replace(" ", "")
        project = projectInput.lower().replace(" ", "")
        if project not in subject:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join(folder, fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            print('Downloaded "{file}"'.format(file=fileName))