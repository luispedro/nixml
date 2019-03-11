# NIX-ML : Easy, reproducible, environments with Nix + YAML


Simple, perfectly reproducible, environments with [nix](https://nixos.org)
specified using an YAML file.

Example:

    nixml: v0.0
    snapshot: stable-19.03
    packages:
      - lang: python
        version: 2
        modules:
          - numpy
          - scipy
          - matplotlib
          - jupyter
          - scikitlearn


## Dependencies

- Python
- [nix](https://nixos.org)

## Author

- [Luis Pedro Coelho](http://luispedro.org) (email: [luis@luispedro.org](mailto:luis@luispedro.org) on twitter: [@luispedrocoelho](https://twitter.com/luispedrocoelho))
