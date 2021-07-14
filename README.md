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

## Usage
Get usage from command line:
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
The help doc is under construction, please refer to Examples and source codes first, thanks:>

## Example

Run camera recorder example from terminal:
```bash
python -m qxtoolkit         # enumerate all available cameras
```
This command will enumerate all available cameras on current machine. 

If you want to run with specified camera id, just put the id follow the command:
```bash
python -m qxtoolkit 0       # open camera 0
python -m qxtoolkit 0 1 2   # open camera 0,1,2
```

If you want to preview a video or a folder of sequence images, just put the path follow the command:
```bash
python -m qxtoolkit /path/to/video.mp4      # preview video file
python -m qxtoolkit /path/to/images/folder  # preview images
```

For how to use these utils in your code, here is an reference of drawing rectangle selector:
```bash
# cd to qxtoolkit/
python ./Example/selector.py
```
View[./Example/selector.py](https://github.com/QixuanAI/qxtoolkit/blob/master/Example/selector.py)