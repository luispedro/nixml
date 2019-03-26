tex_group = '''
let
  tex = pkgs.texlive.combine {{
    inherit (pkgs.texlive)
        {packages};
  }};
in
'''

def generate(data, output, _):
    '''
    Generate a TeXLive group
    '''
    packages = '\n    '.join(data['modules'])
    output.write(tex_group.format(packages=packages))
    return ['tex']
