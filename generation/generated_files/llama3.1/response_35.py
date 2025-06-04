import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import schedule
import time

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
FROM_EMAIL = "your-email@gmail.com"
PASSWORD = "your-password"

# To email configuration
TO_EMAIL = "recipient-email@example.com"

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, 587)
    server.starttls()
    server.login(FROM_EMAIL, PASSWORD)
    text = msg.as_string()
    server.sendmail(FROM_EMAIL, TO_EMAIL, text)
    server.quit()

def scheduled_report():
    subject = "Daily Report"
    body = "This is a daily report."
    send_email(subject, body)

schedule.every(1).days.do(scheduled_report) # Run every 24 hours

while True:
    schedule.run_pending()
    time.sleep(60)