#! /usr/bin/env bash
rm -rv build/ dist/ qxtoolkit.egg-info/
python3 setup.py bdist_wheel
if [[ $? != 0 ]]
then
    echo -e "\033[1m\033[31mFailed to build qxtoolkit\033[0m"
    exit 1
fi
pip3 install -U dist/qxtoolkit*.whl
if [[ $? != 0 ]]
then
    echo -e "\033[1m\033[31mFailed to install qxtoolkit\033[0m"
    exit 1
fi
rm -rv build/ dist/ qxtoolkit.egg-info/
echo
echo -e "\033[1m\033[32mSuccessfully installed qxtoolkit\033[0m"