from datetime import datetime
import os

repoPaths = None
with open('repos.txt','r') as f:
    repoPaths = f.readlines()

for _path in repoPaths:
    path = _path[:-1] if _path[-1] == '\n' else _path # strip newline
    print(f'Attempting to commit {path}')
    try:
        os.chdir(path)
        now = datetime.now()
        msg = f'AutoGitCommit {now}'
        cmd = f'git commit -m "{msg}"'
        print(cmd)
        os.system('git add -A')
        os.system(cmd)
    except Exception as e:
        print(f'Path {path} failed: {e}')
    print()
        