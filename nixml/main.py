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

    parser_run = sp.add_parser('run', help='Run a command in the shell')
    parser_run.add_argument('--command', action='store')
    parser_run.add_argument('--pure', action='store_true',
            help='Run a pure shell, isolated from the rest of your system')
    parser_run.set_defaults(sub='run')

    opts = parser.parse_args(args)

    with open('env.nml') as ifile:
        data = yaml.safe_load(ifile)

    actions = {
            'shell': ['generate', 'shell'],
            'generate': ['generate'],
            'run': ['generate', 'run'],
            'no-sub': ['error-no-sub']
            }.get(getattr(opts, 'sub', 'no-sub'))

    if actions is None:
        from sys import stderr
        stderr.write("Unknown subcommand '{}'\n".format(opts.sub))
        exit(1)
    if 'error-no-sub' in actions:
        from sys import stderr
        stderr.write("You must use a subcommand as argument to nixml.\n\nUse --help for a list of subcommands.\n")
        exit(1)


    nix_file = 'nixml.nix'
    if 'generate' in actions:
        with open(nix_file, 'w') as output:
            generate.write_nix(data, output, opts)
    if 'shell' in actions or 'run' in actions:
        import subprocess
        nix_shell_args = ['nix-shell', nix_file]
        if opts.pure:
            nix_shell_args.append('--pure')
        if 'run' in actions:
            nix_shell_args.append('--command')
            nix_shell_args.append(opts.command)
        exit(subprocess.call(nix_shell_args))

if __name__ == '__main__':
    from sys import argv
    main(argv[1:])
