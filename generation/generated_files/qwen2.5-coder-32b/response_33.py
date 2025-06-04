import paramiko
from datetime import datetime
import schedule
import time

def upload_logs():
    sftp_host = 'your_sftp_server'
    sftp_port = 22
    sftp_username = 'your_username'
    sftp_password = 'your_password'
    local_log_path = '/path/to/local/logs/'
    remote_log_path = '/path/on/sftp/server/'

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(sftp_host, port=sftp_port, username=sftp_username, password=sftp_password)
    sftp_client = ssh_client.open_sftp()

    try:
        for file in ['log1.txt', 'log2.txt']:  # Specify your log files
            local_path = local_log_path + file
            remote_path = remote_log_path + file
            sftp_client.put(local_path, remote_path)
    finally:
        sftp_client.close()
        ssh_client.close()

schedule.every().day.at("10:30").do(upload_logs)

while True:
    schedule.run_pending()
    time.sleep(60)