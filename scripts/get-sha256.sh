#!/usr/bin/env bash

set -e
rev=$1

exec nix-prefetch-url --type sha256 --unpack https://github.com/nixos/nixpkgs/archive/${rev}.tar.gz
