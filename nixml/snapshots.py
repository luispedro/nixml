from collections import namedtuple
Snapshot = namedtuple('Snapshot', ['rev', 'sha256'])

GITHUB_URL = 'https://raw.githubusercontent.com/luispedro/nixml/master/nixml/data/snapshots.tsv'

def get_snapshot(snapshot):
    '''Retrieve snapshot'''
    # Check in order
    # 1. Data shipped with the package
    # 2. Data previously downloaded
    # 3. Data updated from github
    
    from os import path
    import re
    if not re.match(r'^(stable|unstable)-\d{2}\.\d{2}$', snapshot):
        raise ValueError("Illegal snapshot value '{}'".format(snapshot))

    try:
        data_paths = [path.join(
                        path.dirname(path.abspath(__file__)),
                        'data',
                        'snapshots.tsv')]
    except NameError:
        data_paths = []
    data_paths.append(snapshot_cache(True))
    for p in data_paths:
        if p is None:
            continue
        snaps = load_snapshot_data_from(p)
        r = snaps.get(snapshot)
        if r:
            return r
    print("Snapshot not found locally. Updating snapshot data...")
    snaps = load_snapshot_data_from(update_snapshot_data())
    r = snaps.get(snapshot)
    if r:
        return r
    raise ValueError("Snapshot '{}' not found".format(snapshot))
    

def load_snapshot_data_from(data_file):
    snapshots = {}
    for line in open(data_file):
        name, rev, sha256 = line.strip().split('\t')
        snapshots[name] = Snapshot(rev=rev, sha256=sha256)
    return snapshots

def snapshot_cache(check_exists):
    '''Returns location of snapshot file'''
    from os import path, makedirs
    cache_directory = path.expanduser("~/.cache/nixml/")
    cache_file = cache_directory + "snapshots.tsv"
    if check_exists and not path.exists(cache_file):
        return None
    makedirs(cache_directory, exist_ok=True)
    return cache_file

def update_snapshot_data():
    import requests
    r = requests.get(GITHUB_URL)
    ofile = snapshot_cache(False)
    with open(ofile, 'wt') as output:
        output.write(r.text)
    return ofile


