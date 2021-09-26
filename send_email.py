import smtplib
from email.message import EmailMessage
import json

with open('profile.json') as f:
    data = json.load(f)

EMAIL_ADDRESS = 'farpostbot@gmail.com'
EMAIL_PASSWORD = 'farpostbot2809'


def send(subject):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        msg = EmailMessage()
        msg['From'] = 'ОШИБКА ПРОГРАММЫ'
        msg['To'] = data['mail']
        msg['Subject'] = subject
        msg.set_content('Исправте ошибку, либо свяжитесь с тех. поддержкой')
        with open('logging.log') as f:
            log = f.read()
        msg.add_attachment(log, filename='logging.log')
        smtp.send_message(msg)
