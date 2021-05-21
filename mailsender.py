from smtplib import SMTP, SMTP_SSL
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import configparser
from email.mime.application import MIMEApplication
from os.path import basename
import bg
from zipfile import ZipFile
import os

context = ssl.create_default_context()
config = configparser.ConfigParser()
config.read('mailsender.ini')


def attach_file(message, file_to_attach):
    with open(file_to_attach, 'rb') as attach_file:
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Decomposition', 'attachment', filename=file_to_attach)
        message.attach(payload)


def send_mail(to, subject='DAILY RECON', text='Hello,\nKindly see reconciliation result as attached.\n\nRegards,\nRecon Tool', files=None, zip_name=None):
    def run():
        sender = config['DEFAULT']['SOURCE_ADDR']
        pwd = config['DEFAULT']['SOURCE_PWD']
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = ", ".join(to)
        message['Subject'] = subject
        message.attach(MIMEText(text, 'plain'))

        def f_info(f):
            st = os.stat(f)
            print(f'{basename(f)} => {(st.st_size/1024):.0f}MB')

        if not zip_name:
            for f in files or []:
                f_info(f)
                with open(f, "rb") as fil:
                    part = MIMEApplication(
                        fil.read(),
                        Name=basename(f)
                    )
                # After the file is closed
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                message.attach(part)
        else:
            z_file = f'outputs/{zip_name}.zip'
            with ZipFile(z_file, 'w') as fil:
                for f in files or []:
                    f_info(f)
                    fil.write(f)
            if files and len(files):
                f_info(z_file)
                with open(z_file, "rb") as fil:
                    part = MIMEApplication(
                        fil.read(),
                        Name=basename(z_file)
                    )
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(z_file)
                message.attach(part)

        with SMTP(config['DEFAULT']['SMTP_SERVER'], config['DEFAULT']['PORT']) as smtp:
            smtp.noop()
            smtp.ehlo()
            smtp.starttls()
            smtp.login(sender, pwd)
            # smtp.send_message(message)
            smtp.sendmail(sender, to, message.as_string())
            smtp.quit()
        print('Mail sent...')
    bg.run_in_background(run)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Send mail')
    parser.add_argument('receivers', type=str, nargs='+', help='Receiver(s) separated by space')
    args = parser.parse_args()
    print(args.receivers)
    files = ['README.md']
    send_mail(args.receivers, files=files)
