from collections import namedtuple
from . import languages

Snapshot = namedtuple('Snapshot', ['rev', 'sha256'])

snapshots = {
    'stable-19.04':
        Snapshot(rev='37694c8cc0e9ecab60d06f1d9a2fd0073bcc5fa3',
                 sha256='1ibjg6ln2y764wfg0yd0v055jm4xzhmxy5lfz63m6jr3y16jdmzb'),
    'stable-19.03':
        Snapshot(rev='c42f391c0c87429dafd059c2da2aff66edb00357',
                 sha256='0yh8wmyws63lc757akgwclvjgl5hk763ci26ndz04dpw6frsrlkq'),


    'unstable-19.04':
        Snapshot(rev='54bb7ed9270a8b16b2dd56fd52cbf31562b2bf4a',
                 sha256='0qwhddz0vl8jib8imc8l9m5cddxpycvc5qly4gniy0iqvfiyx84j'),
    'unstable-19.03':
        Snapshot(rev='d64d42f12d253d4b0fde2b63e14d1f7d322b754c',
                 sha256='1l8i523paqmhzgcn1v8z5jssry5ww46qnfrhj7832drgh1h7bxdx'),
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
        langmod = {
                'python': languages.python,
                'texlive': languages.texlive,
                'nix': languages.nix,
                }.get(p['lang'])
        if langmod is None:
            raise NotImplementedError("Unsupported lang '{}' (currently supported: 'python', 'texlive', 'nix')".format(p['lang']))
        else:
            buildInputs.extend(langmod.generate(p, output, options))
    name = p.get('name', 'pynix-env')
    output.write(mkDerivation.format(name=name, buildInputs=' '.join(buildInputs)))
