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
    py_version = str(data['version'])
    py_version = {
            '2.7': '2',
            '3': '36',
            '3.4': '34',
            '3.5': '35',
            '3.6': '36',
            '3.7': '37',
            '3.8': '38',
            }.get(py_version, py_version)
    packages = '\n    '.join(data['modules'])
    output.write(python_group.format(py_version=py_version, packages=packages))
    return ['pwp']
