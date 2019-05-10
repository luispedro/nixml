from . import languages, snapshots

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
    sn = snapshots.get_snapshot(data['snapshot'])
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
