import os
import subprocess
from datetime import datetime

def backup_database():
    host = 'your_host'
    port = 'your_port'
    user = 'your_user'
    password = 'your_password'
    dbname = 'your_dbname'
    backup_dir = '/path/to/backup/directory'

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'{dbname}_{timestamp}.sql')

    with open(os.devnull, 'w') as devnull:
        subprocess.call(
            ['pg_dump', '-h', host, '-p', port, '-U', user, '-F', 'c', '-b', '-v', '-f', backup_file, dbname],
            stdout=devnull,
            stderr=subprocess.STDOUT,
            env={'PGPASSWORD': password}
        )

if __name__ == '__main__':
    backup_database()