# QXToolKit

Some useful utils for computer vision works.

[HomePage](https://github.com/QixuanAI/qxtoolkit)|[中文](https://github.com/QixuanAI/qxtoolkit/blob/master/README_CN.md)

## Prequest

* python
* pip
* numpy
* python-opencv


## Install

It is easy to install this package, you just need to clone the repo and run one-click script.
```bash
git clone https://github.com/QixuanAI/qxtoolkit.git
cd qxtoolkit
# Install with script
bash ./pip_install_atonce.sh
```
Or if you want to take full control of installation, please refer to the content of [pip_install_atonce.sh](https://github.com/QixuanAI/qxtoolkit/blob/master/pip_install_atonce.sh).

## Example

Run camera recorder example from terminal:
```bash
python -m qxtoolkit
# or
python -m qxtoolkit.cam_record
```

Run image getter example from terminal:
```bash
python -m qxtoolkit.imgetter
```

For how to use these utils in your code, here is an reference of drawing rectangle selector:
```bash
# cd to qxtoolkit/
python ./Example/selector.py
```
View[./Example/selector.py](https://github.com/QixuanAI/qxtoolkit/blob/master/Example/selector.py)