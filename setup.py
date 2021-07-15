#! /usr/bin/env python
'''
Description : 
FilePath    : /qxtoolkit/setup.py
Author      : qxsoftware@163.com
Date        : 2020-12-03 09:26:14
LastEditTime: 2021-07-14 16:51:45
Refer to    : https://github.com/QixuanAI/qxtoolkit
'''

from qxtoolkit import __version__
from setuptools import setup, find_packages
setup(
    name="qxtoolkit",
    version=__version__,
    keywords=["qxtoolkit", "qx", "toolkit", "opencv"],
    description="Useful utils for cv working",
    long_description="Useful utils for cv working",
    license="BSD 3-Clause License",
    url="https://github.com/QixuanAI/qxtoolkit",
    author="LiuQixuan",
    author_email="qxairobot@163.com",
    packages=find_packages(exclude=["logs", "test*", "temp"]),
    install_requires=["numpy", "opencv-python"],
)
