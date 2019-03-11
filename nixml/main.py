from . import generate
from sys import exit

try:
    import argparse
except ImportError:
    print("argparse not found. Please install argparse with 'pip install argparse'")
    exit(1)

def main(args=None):
    if args is None:
        from sys import argv
        args = argv[1:]
    import yaml
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cache-git", action="store_true",
            help="Cache git download: will be slow the first time, but will make it faster to switch between different snapshots")
    sp = parser.add_subparsers()
    parser_generate = sp.add_parser('generate', help='Generate .nix file')
    parser_generate.set_defaults(sub='generate')
    parser_shell = sp.add_parser('shell', help='Create a shell')
    parser_shell.set_defaults(sub='shell')
    parser_shell.add_argument('--pure', action='store_true',
            help='Run a pure shell, isolated from the rest of your system')

    opts = parser.parse_args(args)

    with open('env.nml') as ifile:
        data = yaml.load(ifile)

    nix_file = 'nixml.nix'
    with open(nix_file, 'w') as output:
        generate.write_nix(data, output, opts)
    if opts.sub == 'shell':
        import subprocess
        exit(subprocess.call(['nix-shell', nix_file]))

if __name__ == '__main__':
    from sys import argv
    main(argv[1:])
