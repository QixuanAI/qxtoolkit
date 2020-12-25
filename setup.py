#! /usr/bin/env python
'''
Description : 
FilePath    : /cvutils/setup.py
Author      : qxsoftware@163.com
Date        : 2020-12-03 09:26:14
LastEditTime: 2020-12-25 13:55:43
Refer to    : https://github.com/QixuanAI
'''

from cvutils import __version__
from setuptools import setup, find_packages
setup(
    name="cvutils",
    version=__version__,
    keywords={"cvutils", "opencv"},
    description="Useful utils for opencv",
    long_description="Useful utils for opencv",
    license="GNU GENERAL PUBLIC LICENSE v3",
    url="https://github.com/QixuanAI/cvutils",
    author="LiuQixuan",
    author_email="qxairobot@163.com",
    packages=find_packages(exclude=["logs", "test*", "temp"]),
    install_requires=["numpy", "opencv-python"],
)