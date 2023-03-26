from datetime import datetime
import os
import sys

version = '0.3'

class Logger:
    prev_str = '\n'
 
    def __init__(self, filename):
        self.console = sys.stdout
        self.file = open(filename, 'a')
 
    def write(self, message):
        datetime_str = f'[{datetime.now()}] '
        if not (len(self.prev_str) > 0 and self.prev_str[-1] == '\n'):
            datetime_str = ''
        new_message = f'{datetime_str}{message}'
        self.console.write(new_message)
        self.file.write(new_message)
        self.prev_str = message
 
    def flush(self):
        self.console.flush()
        self.file.flush()
		

sys.stdout = Logger('log.txt')		
repoPaths = None
print(f'\nLaunched AutoGitCommit instance, version: {version}')

with open('repos.txt','r') as f:
    repoPaths = f.readlines()
for _path in repoPaths:
    path = _path[:-1] if _path[-1] == '\n' else _path # strip newline
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
        