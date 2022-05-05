try:
    from git import Repo
except ImportError:
    print("import git failed")
    print("GiPython is needed: https://gitpython.readthedocs.io/")
    print("\t\tpip install GitPython")
    raise

from datetime import datetime
from sys import argv
import subprocess

y2 = int(argv[1])
month = int(argv[2])
t = datetime(2000 + y2, month, 1).timestamp()


# We only check commits in the last year
min_t = datetime(2000 + y2 - 1, month , 1).timestamp()
r = Repo('.')

def iter_after(c, min_t):
    seen = set()
    stack = [c]
    while stack:
        c = stack.pop()
        if c.hexsha in seen:
            continue
        if c.authored_date < min_t:
            continue
        yield c
        seen.add(c.hexsha)
        stack.extend(c.parents)

for nixml_name, branch_name in [
        ('unstable', 'master'),
        ('stable', '20.09'),
        ]:
    [head] = [b for b in r.branches if b.name == branch_name]
    candidates = [c for c in iter_after(head.commit, min_t) if c.authored_date >= t]
    candidates.sort(key=lambda c : c.authored_date)
    h = candidates[0].hexsha
    s = subprocess.check_output(['nix-prefetch-url', '--type', 'sha256', '--unpack', f'https://github.com/nixos/nixpkgs/archive/{h}.tar.gz'])
    s = s.decode('ascii').strip()
    print(f'{nixml_name}-{y2}.{month:02}\t{h}\t{s}')
