# QXToolKit

一些在机器视觉工作中用得上的小玩意。

[主页 / English HomePage](https://github.com/QixuanAI/qxtoolkit)

## 依赖项

* python
* pip
* numpy
* python-opencv

## 安装

这个工具包安装起来非常简单，你只需要克隆这个仓库，然后运行一键安装脚本就行（当然前提是您已经配置好了python与pip）。
```bash
git clone https://github.com/QixuanAI/qxtoolkit.git
cd qxtoolkit
# Install with script
bash ./pip_install_atonce.sh
```
如果你想更好地把握安装过程，可以直接打开安装脚本查看：[pip_install_atonce.sh](https://github.com/QixuanAI/qxtoolkit/blob/master/pip_install_atonce.sh)

## 使用
使用命令行获取帮助：
```bash
python -m qxtoolkit -h
```
```text
usage: python -m qxtoolkit [-h] [-r] [-t SAVETO] [-q {small,normal,lossless}] [-i INTERVAL] [-f] [-s] [-V] [cam_ids [cam_ids ...]]

A simple camera recorder, support Windows, MacOS and Linux.

positional arguments:
  cam_ids               The camera's device IDs, can be either a nuber or serveral numbers separated by space.

optional arguments:
  -h, --help            show this help message and exit
  -r, --record          Whether to record video to a file or not.
  -t SAVETO, --saveto SAVETO
                        Where to save the result.
  -q {small,normal,lossless}, --quality {small,normal,lossless}
                        The quality of saved video file, default is lossless.
  -i INTERVAL, --interval INTERVAL
                        Interval milliseconds between two frames.
  -f, --flip            Flip video around vertical axes.
  -s, --fixedsize       Fixed preview windows in original size rather than fit the screen.
  -V, --version         Show version.
```
更多帮助文档还在建设中，请先参阅例子、源码注释，望海涵～

## 例子

从终端启用录像工具：
```bash
python -m qxtoolkit         # 遍历所有可用的相机
```
这个命令会遍历当前设备上所有可用的相机。

如果你想指定使用某台相机而非遍历所有相机，只需要把指定相机ID放在命令后即可：
```bash
python -m qxtoolkit 0       # 打开0号相机
python -m qxtoolkit 0 1 2   # 打开0号、1号、2号共三个相机
```

如果你想预览一段视频或者一个文件夹下的所有图片，只需要把相应路径放在命令后即可：
```bash
python -m qxtoolkit /path/to/video.mp4      # 预览一段视频
python -m qxtoolkit /path/to/images/folder  # 浏览文件夹下的图片
```

对于如何在自己的python中使用这些工具，这里有一个绘制矩形选择框的例子可供参考：
```bash
# cd to qxtoolkit/
python ./Example/selector.py
```
查看[./Example/selector.py](https://github.com/QixuanAI/qxtoolkit/blob/master/Example/selector.py)