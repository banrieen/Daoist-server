sudo apt install

# install pytorch only CPU
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
# ONNX runtime
 git clone --recursive https://github.com/Microsoft/onnxruntime.git
 cd onnxruntime
  python3 -m pip install cmake
  which cmake
# Cargo build dependence
cargo add pkg-config
sudo apt install libfontconfig1-dev

## Install postgresql

sudo apt install -y postgresql
sudo systemctl is-enabled postgresql
sudo systemctl status postgresql
### 启用远程连接
#### 使用以下 psql 命令登录 PostgreSQL shell。

sudo -u postgres psql

#### 现在执行以下查询来创建新的 PostgreSQL 用户和密码。在此示例中，您将创建一个新用户 alice，密码为 p4ssw0rd。

CREATE USER thomas with CREATEDB CREATEROLE;
ALTER USER thomas with PASSWORD 'thomas';
#### 使用以下查询验证 PostgreSQL 上的可用用户列表。如果成功，您应该会看到创建的用户 alice。
\du

## Install prometheus and grafana

sudo apt install -y prometheus 
# 192.168.56.2  
### grafana 需要添加安装源 


## 安装 SAM-2 
### 使用安装源安装python
pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple --trusted-host
### 配置 cuda PATH 
export LD_LIBRARY_PATH=/usr/local/cuda-12.4/lib64:$LD_LIBRARY_PATH
export PATH=/usr/local/cuda-12.4/bin:$PATH
### 启用 jupyter lab bash script
#!/bin/bash
# 启动本地环境中的Jupyter lab
cd /media/data/workspace-Li
source .venv/bin/activate
pip install jupyterlab
nohup jupyter lab --no-browser --ip=0.0.0.0 --port=8888 --allow-root &

#### 默认设置密码: thomas

############################################## 
## 机器学习环境配置
##

## Enable cuda
### [Nvidia Container Toolkit and Podman on Ubuntu 20.04](https://cognitivearchitect.com/2022/07/11/side-track-nvidia-container-toolkit-and-podman-on-ubuntu-20-04/)

## install Podman as usual:

sudo apt-get install -y curl wget gnupg2
source /etc/os-release
sudo sh -c "echo 'deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /' > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list"
wget -nv https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable/xUbuntu_${VERSION_ID}/Release.key -O- | sudo apt-key add -
sudo apt-get update && sudo apt-get install -y podman
podman -v

## install the Nvidia Container Toolkit as usual:

distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
 
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

## However, before you can start using both together you need to manually define the OCI hook:

sudo mkdir -p /usr/share/containers/oci/hooks.d/
 
cat << EOF | sudo tee /usr/share/containers/oci/hooks.d/oci-nvidia-hook.json
{
    "version": "1.0.0",
    "hook": {
        "path": "/usr/bin/nvidia-container-toolkit",
        "args": ["nvidia-container-toolkit", "prestart"],
        "env": [
            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
        ]
    },
    "when": {
        "always": true,
        "commands": [".*"]
    },
    "stages": ["prestart"]
}
EOF
 
sudo systemctl restart podman
 
## run container with cuda
podman run --name ml -it --rm -d --gpus all -p 8010:8010 --ipc=host -v /workspace:/workspace nvcr.io/nvidia/pytorch:23.10-py3 

## 参考
podman pull registry.opensuse.org/opensuse/mariadb:latest
podman pull registry.opensuse.org/opensuse/bci/rust:latest

# commit container 
podman commit -a "alex" e32910878b64 suse/rust:latest

# 容器 SSH 访问
# setup opensuse container sshd
## 按照ssh server
ssh-keygen -A 
passwd root # 设置密码 thomas
## 设置登录配置文件
/usr/etc/ssh/sshd_config
### sed -E 's/^#(PermitRootLogin )no/\1yes/' /usr/etc/ssh/sshd_config -i 
/usr/sbin/sshd &

## 调整 podman 文档存储路径 https://blog.csdn.net/witton/article/details/128497746
## 修改 /etc/containers/storage.conf

## windows 11 环境处理进程
列出所有端口的情况： netstat -ano
搜索指定端口、进程名称： netstat -ano | findstr $str
找到指定的进程是什么： tasklist | findstr $str  
根据需求，结束进程。


可以使用任务管理器-详细信息，查找PID终止进程。
可以使用命令终止进程。

通过进程名称结束进程： taskkill /f /t /im $name
通过PID结束进程： taskkill /f /t /pid $pid
说明：

/F                 指定强制终止进程。
/T                 终止指定的进程和由它启用的子进程。
/IM   imagename    指定要终止的进程的映像名称。通配符 '*'可用来指定所有任务或映像名称。
/PID  processid    指定要终止的进程的 PID。使用 TaskList 取得 PID。

## UI,UX 设计环境
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update -y && sudo apt install -y yarn 
yarn --version
curl -fsSL https://deno.land/install.sh | sh
deno --version

sudo systemctl restart networking

## 处理git for windows 无法显示中文的配置
git config --global core.quotepath false  		
git config --global gui.encoding utf-8			
git config --global i18n.commit.encoding utf-8	
git config --global i18n.logoutputencoding utf-8	
export LESSCHARSET=utf-8
