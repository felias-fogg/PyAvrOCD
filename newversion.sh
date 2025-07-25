#!/bin/bash
arch=x86_64-apple-darwin
poetry install
rm -rf build
poetry run pyinstaller -y intel-apple-pyavrocd.spec
rm -rf ../felias-fogg.github.io/binaries/${arch}/pyavrocd*
mv dist/pyavrocd/pyavrocd* ../felias-fogg.github.io/binaries/${arch}/
../felias-fogg.github.io/binaries/${arch}/pyavrocd -V
