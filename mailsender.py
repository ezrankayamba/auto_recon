from smtplib import SMTP, SMTP_SSL
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import configparser


context = ssl.create_default_context()
config = configparser.ConfigParser()
config.read('mailsender.ini')


def send_mail():
    mail_content = 'Test Office 365'
    sender = config['DEFAULT']['SOURCE_ADDR']
    pwd = config['DEFAULT']['SOURCE_PWD']
    to = 'ezrankayamba@gmail.com'
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = to
    message['Subject'] = 'Test Mail'
    message.attach(MIMEText(mail_content, 'plain'))
    with SMTP(config['DEFAULT']['SMTP_SERVER'], config['DEFAULT']['PORT']) as smtp:
        smtp.noop()
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender, pwd)
        text = message.as_string()
        smtp.send_message(message)
        smtp.quit()
    print('Mail sent...')


if __name__ == '__main__':
    send_mail()
