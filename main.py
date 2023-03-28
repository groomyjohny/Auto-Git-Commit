from datetime import datetime
import os, sys, csv
import time, threading

version = '1.0 beta 1'

class Logger:
    prev_str = '\n'
    lock = threading.Lock()
 
    def __init__(self, filename):
        self.console = sys.stdout
        self.file = open(filename, 'a')
 
    def write(self, message):
        _my_lock = not self.lock.locked()
        if _my_lock: self.lock.acquire()
        try:     
            datetime_str = f'[{datetime.now()}] '
            if not (len(self.prev_str) > 0 and self.prev_str[-1] == '\n'):
                datetime_str = ''
            new_message = f'{datetime_str}{message}'
            self.console.write(new_message)
            self.file.write(new_message)
            self.file.flush()
            self.prev_str = message
        finally:
            if _my_lock: self.lock.release()
 
    def flush(self):
        self.console.flush()
        self.file.flush()

logger = Logger('log.txt')
sys.stdout = logger
		
def repo_updater_routine(path, wait_time):
    wait_time = 86400 if not wait_time else float(wait_time) # if not set, then default to 1 day
    wait_time = 86400 if not wait_time else wait_time
    print(f'Started a worker for repo {path} with sleep period {wait_time} sec.')
    while True:
        logger.lock.acquire()
        try:
            print(f'Attempting to commit path: {path}')
            try:
                os.chdir(path)
                now = datetime.now()
                msg = f'AutoGitCommit {now}'
                cmd = f'git commit -m "{msg}"'
                print(cmd)
                os.system('git add -A')
                os.system(cmd)
                print('Done.')
            except Exception as e:
                print(f'Path {path} failed: {e}')
            print()
        finally:
            logger.lock.release()
        time.sleep(wait_time)
        
repoPaths = None
print(f'\n\nLaunched AutoGitCommit instance, version: {version}\n')

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