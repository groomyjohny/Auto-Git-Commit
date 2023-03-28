from datetime import datetime
import os, sys, csv
import time, threading

version = '1.0 alpha 1'

class Logger:
    prev_str = '\n'
    lock = threading.Lock()
 
    def __init__(self, filename):
        self.console = sys.stdout
        self.file = open(filename, 'a')
 
    def write(self, message):        
        datetime_str = f'[{datetime.now()}] '
        if not (len(self.prev_str) > 0 and self.prev_str[-1] == '\n'):
            datetime_str = ''
        new_message = f'{datetime_str}{message}'
        self.lock.acquire()
        try:
            self.console.write(new_message)
            self.file.write(new_message)
        finally:
            self.lock.release()
        self.prev_str = message
 
    def flush(self):
        self.console.flush()
        self.file.flush()
		
def repo_updater_routine(path, wait_time):
    wait_time = 86400 if not wait_time else float(wait_time) # if not set, then default to 1 day
    wait_time = 86400 if not wait_time else wait_time
    print(f'Started a worker for repo {path}', f'Wait period is set to {wait_time} sec.')
    while True:
        print(f'Attempting to commit path: {path}')
        try:
            os.chdir(path)
            now = datetime.now()
            msg = f'AutoGitCommit {now}'
            cmd = f'git commit -m "{msg}"'
            print(cmd)
            os.system('git add -A')
            os.system(cmd)
            print('Success!')
        except Exception as e:
            print(f'Path {path} failed: {e}')
        print()
        time.sleep(wait_time)
        
sys.stdout = Logger('log.txt')		
repoPaths = None
print(f'\nLaunched AutoGitCommit instance, version: {version}')

threads = []
with open('repos.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:
        _path = row[0]
        wait_time = row[1] if len(row) > 1 else None
        path = _path[:-1] if _path[-1] == '\n' else _path # strip newline
        thread = threading.Thread(target=repo_updater_routine, args=(path, wait_time))
        threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()