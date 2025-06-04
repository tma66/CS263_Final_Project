import os
from datetime import datetime
import paramiko
import schedule
import time

# Function to upload log files via SFTP
def upload_logs():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('sftp_server_ip', username='username', password='password')

        sftp = ssh.open_sftp()

        for filename in os.listdir('/path/to/local/logs'):
            if filename.endswith('.log'):
                log_path = '/path/to/local/logs/' + filename
                remote_path = '/remote/path/for/logs/' + filename
                sftp.put(log_path, remote_path)
                print(f'Uploaded {filename} to SFTP server')
        ssh.close()

    except Exception as e:
        print(f"Error uploading logs: {e}")

# Schedule upload every 5 minutes
schedule.every(5).minutes.do(upload_logs)

while True:
    schedule.run_pending()
    time.sleep(1)