# NIX-ML : Easy, reproducible, environments with Nix + YAML


Simple, perfectly reproducible, environments with [nix](https://nixos.org)
specified using an YAML file.

Example, write to a file called `env.nml`:

    nixml: v0.0
    snapshot: stable-19.03
    packages:
      - lang: python
        version: 2
        modules:
          - numpy
          - scipy
          - matplotlib
          - mahotas
          - jupyter
          - scikitlearn

Now, run

```bash
nixml shell
```

and you will be dropped into an environment containing the packages listed
above, as was up to date in March 2019.


## Dependencies

- Python
- [nix](https://nixos.org)

## NIXML Format

It's a YaML file

`nixml`: version of nixml to use. Currently, only `v0.0` is supported.

`snapshot`: This is the package version to use. Currently, only `stable-19.03`
is available, but general syntax is `{stable,unstable}-{year}.{month}`.

`packages`: A list of packages, which are grouped into blocks

## Author

- [Luis Pedro Coelho](http://luispedro.org) (email: [luis@luispedro.org](mailto:luis@luispedro.org) on twitter: [@luispedrocoelho](https://twitter.com/luispedrocoelho))
