from collections import namedtuple

Snapshot = namedtuple('Snapshot', ['rev', 'sha256'])

snapshots = {
    'stable-19.03':
        Snapshot(rev='c42f391c0c87429dafd059c2da2aff66edb00357',
                 sha256='0yh8wmyws63lc757akgwclvjgl5hk763ci26ndz04dpw6frsrlkq'),
}

import_nixpkgs_nocache = '''
with (import (builtins.fetchTarball {{
  name = "nixml-{name}";
  url = https://github.com/nixos/nixpkgs/archive/{rev}.tar.gz;
  sha256 = "{sha256}";
}}) {{}});
'''

import_nixpkgs_cache = '''
with (import (builtins.fetchGit {{
  name = "nixml-{name}";
  url = https://github.com/nixos/nixpkgs/;
  rev = "{rev}";
}}) {{}});
'''

python_group = '''
let
  pwp = python{py_version}.buildEnv.override {{
    extraLibs = (with python{py_version}Packages; [
        {packages}
    ]);
    ignoreCollisions = true;
 }};

in
'''

mkDerivation = '''
stdenv.mkDerivation {{
  name = "{name}";
  buildInputs = [
    {buildInputs}
  ];
}}
'''

def write_nix(data, output, options):
    '''
    Write .nix encoding of the 
    '''
    nixml_version = data['nixml']
    if nixml_version != 'v0.0':
        raise NotImplementedError('Only nixml v0.0 is currently supported')
    sn = snapshots[data['snapshot']]
    import_nixpkgs = (import_nixpkgs_cache
                        if options.cache_git
                        else import_nixpkgs_nocache)
    output.write(import_nixpkgs.format(name=data['snapshot'], rev=sn.rev, sha256=sn.sha256))
    buildInputs = []
    for p in data['packages']:
        if p['lang'] == 'python':
            output.write(python_group.format(py_version=p['version'],
                                packages='\n    '.join(p['modules']))
            )                    
            buildInputs.append('pwp')
        else:
            raise NotImplementedError("Only Python lang for now")
    name = p.get('name', 'pynix-env')
    output.write(mkDerivation.format(name=name, buildInputs=' '.join(buildInputs)))
