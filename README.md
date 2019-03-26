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
above, as was up to date in March 2019. Conceptually, the environment will
always be generated from scratch, but caching means that the first time will
take significantly longer (including, it will download all dependencies).
Afterwards, it should take a few seconds at most.

This environment will be like a typical _conda/pip/virtualenv/..._ environment:
if will place the corresponding binaries at the front of the `PATH` so that
they are picked with high priority, but, alternatively, you can generate a
_pure environment_, which will contain **only the packages that you specify**.
This avoids accidental use of packages that are not part of the environment:

```bash
nixml shell --pure
```

Finally, you can run

```bash
nixml generate
```

to just create the `nixml.nix` corresponding to the enviroment.

## Dependencies

- Python
- [nix](https://nixos.org)

## NIXML Format

It's a YaML file

`nixml`: version of nixml to use. Currently, only `v0.0` is supported.

`snapshot`: This is the package version to use. Currently, only `stable-19.03`
is available, but general syntax is `{stable,unstable}-{year}.{month}`.

`packages`: A list of packages, which are grouped into language blocks.
Currently supported:

- `python`: Python language environment, specify the version (`version`) and `modules`.
- `texlive`: Texlive packages
- `nix`: Generic packages (i.e., `vim` or `bash`)

## Author

- [Luis Pedro Coelho](http://luispedro.org) (email: [luis@luispedro.org](mailto:luis@luispedro.org) on twitter: [@luispedrocoelho](https://twitter.com/luispedrocoelho))
