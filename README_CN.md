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

## 例子

从终端启用录像工具：
```bash
python -m qxtoolkit
# or
python -m qxtoolkit.cam_record
```

从终端打开序列图像读取器：
```bash
python -m qxtoolkit.imgetter
```

对于如何在自己的python中使用这些工具，这里有一个绘制矩形选择框的例子可供参考：
```bash
# cd to qxtoolkit/
python ./Example/selector.py
```
查看[./Example/selector.py](https://github.com/QixuanAI/qxtoolkit/blob/master/Example/selector.py)
