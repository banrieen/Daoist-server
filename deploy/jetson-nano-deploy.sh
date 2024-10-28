#!/bin/sh

## Basement tool

audo apt install -y curl tmux  &&
sudo apt install -y build-essential libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev libffi-dev wget 

## Install python3.12

### https://tecadmin.net/how-to-install-python-3-12-on-ubuntu-18-04/
wget https://www.python.org/ftp/python/3.12.1/Python-3.12.2.tgz 
tar -xzf Python-3.12.2.tgz 
cd Python-3.12.2
./configure --enable-optimizations 
make -j$(nproc) ## The -j$(nproc) flag tells make to use all available CPU cores for faster compilation.
sudo make altinstall 

python3.12 -m ensurepip --upgrade
python3.12 -m pip  install virtualenv
python3.12 -m  virtualenv .venv
source  .venv/bin/activate
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.ini


## Install nu for pythonshell
### Install rust runtime at first
cargo install nu

## container 
sudo docker run -it -d --net=host --runtime nvidia -e DISPLAY=$DISPLAY -v ~/workspace:/home -v /tmp/.X11-unix/:/tmp/.X11-unix nvcr.io/nvidia/l4t-base:r32.4.3
