import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from flask import current_app


def send_email(subject, message):
    """ Отправка email через SMTP Яндекса. """
    try:
        msg = MIMEMultipart()
        msg['From'] = current_app.config['MAIL_USERNAME']
        msg['To'] = current_app.config['MAIL_USERNAME']
        msg['Subject'] = Header(subject, 'utf-8')

        msg.attach(MIMEText(message, 'plain', 'utf-8'))

        server = smtplib.SMTP_SSL(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])

        server.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))
        server.quit()
        return True

    except Exception as e:
        print(f"🚨 Ошибка при отправке email: {e}")
        return False

