#! /usr/bin/env python
'''
Description : 
FilePath    : /qxtoolkit/qxtoolkit/__main__.py
Author      : qxsoftware@163.com
Date        : 2021-06-15 11:01:59
LastEditTime: 2021-07-14 10:27:39
Refer to    : https://github.com/QixuanAI
'''
from __future__ import absolute_import

if __name__ == "__main__":
    import os
    import sys
    if len(sys.argv)>1 and os.path.isfile(sys.argv[1]):
        from qxtoolkit.imgetter import run
        run(sys.argv[1:])
    else:
        from qxtoolkit.cam_record import cam_record_cmd
        cam_record_cmd()
