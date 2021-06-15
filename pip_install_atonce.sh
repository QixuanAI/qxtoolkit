#! /usr/bin/env bash
rm -rv build/ dist/ qxtoolkit.egg-info/
python3 setup.py bdist_wheel
pip3 install -U dist/qxtoolkit*.whl
rm -rv build/ dist/ qxtoolkit.egg-info/
echo
echo  -e "\033[1m\033[31mSuccessfully installed qxtoolkit\033[0m"