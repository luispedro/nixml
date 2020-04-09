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

synonyms = {
    'keras': ('Keras', 'package names are case sensitive'),

    # Be nice to users
    'sklearn': ('scikitlearn', None),
    'scikit-learn': ('scikitlearn', None),
}

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
    packages = []
    for p in data['modules']:
        if p in synonyms:
            np,note = synonyms[p]
            if note is not None:
                message = "Replacing package '{}' by '{}' ({}).".format(p, np, note)
            else:
                message = "Replacing package '{}' by its canonical name '{}'.".format(p, np)
            print(message)
            packages.append(np)
        else:
            packages.append(p)
    packages = '\n    '.join(packages)
    output.write(python_group.format(py_version=py_version, packages=packages))
    return ['pwp']
