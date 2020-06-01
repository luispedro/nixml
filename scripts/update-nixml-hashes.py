from git import Repo
from datetime import datetime
from sys import argv
import subprocess

y2 = int(argv[1])
month = int(argv[2])
t = datetime(2000 + y2, month, 1).timestamp()
r = Repo('.')

for nixml_name, branch_name in [
        ('unstable', 'master'),
        ('stable', 'nixos-20.03'),
        ]:
    [head] = [b for b in r.branches if b.name == branch_name]
    after_target = [c for c in head.commit.iter_parents() if c.authored_date > t]
    h = after_target[-1].hexsha
    s = subprocess.check_output(['nix-prefetch-url', '--type', 'sha256', '--unpack', f'https://github.com/nixos/nixpkgs/archive/{h}.tar.gz'])
    s = s.decode('ascii').strip()
    print(f'{nixml_name}-{y2}.{month:02}\t{h}\t{s}')
