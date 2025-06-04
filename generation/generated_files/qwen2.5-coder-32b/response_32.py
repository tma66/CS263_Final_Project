import requests
from jenkinsapi.jenkins import Jenkins
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def trigger_job(jenkins_url, job_name, username, password):
    server = Jenkins(jenkins_url, username=username, password=password)
    job = server.get_job(job_name)
    queue_id = job.invoke()
    return queue_id

def get_build_number(jenkins_url, job_name, username, password, queue_id):
    server = Jenkins(jenkins_url, username=username, password=password)
    job = server.get_job(job_name)
    while not job.is_queued_or_running(queue_id):
        pass
    build_number = job.get_last_buildnumber()
    return build_number

def get_build_logs(jenkins_url, job_name, build_number, username, password):
    server = Jenkins(jenkins_url, username=username, password=password)
    job = server.get_job(job_name)
    build = job.get_build(build_number)
    logs = build.get_console()
    return logs

def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, login, password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(login, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

jenkins_url = 'http://your-jenkins-url'
job_name = 'your-job-name'
username = 'your-username'
password = 'your-password'
smtp_server = 'smtp.yourserver.com'
smtp_port = 587
from_email = 'from@example.com'
to_email = 'to@example.com'

queue_id = trigger_job(jenkins_url, job_name, username, password)
build_number = get_build_number(jenkins_url, job_name, username, password, queue_id)
logs = get_build_logs(jenkins_url, job_name, build_number, username, password)

subject = f'Build {build_number} Logs'
send_email(subject, logs, to_email, from_email, smtp_server, smtp_port, username, password)