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

def generate(data, output, _):
    '''
    Generate a Python group
    '''
    packages = '\n    '.join(data['modules'])
    output.write(python_group.format(py_version=data['version'], packages=packages))
    return ['pwp']
