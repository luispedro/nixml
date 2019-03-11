import generate

try:
    import argparse
except ImportError:
    print("argparse not found. Please install argparse with 'pip install argparse'")
    sys.exit(1)

def main(args):
    import yaml
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cache-git", action="store_true",
            help="Cache git download: will be slow the first time, but will make it faster to switch between different snapshots")
    opts = parser.parse_args(args)
    with open('env.nml') as ifile:
        data = yaml.load(ifile)
    with open('nixml.nix', 'w') as output:
        generate.write_nix(data, output, opts)

if __name__ == '__main__':
    from sys import argv
    main(argv[1:])
