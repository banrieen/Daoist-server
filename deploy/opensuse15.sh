#!bin/sh
# openSUSE 15.5

## [] 1. Install  build dependencies
sudo zypper install gcc automake bzip2 libbz2-devel xz xz-devel openssl-devel ncurses-devel \
readline-devel zlib-devel tk-devel libffi-devel sqlite3-devel make

sudo zypper install -t pattern devel_basis 

## [] 2. tmux 多个session
sudo zypper install -y tmux

## [] 4. 安装 mariadb 数据库
sudo zypper install mariadb

### 创建一个账号
CREATE USER 'thomas'@'%' IDENTIFIED BY 'thomas';  
GRANT ALL PRIVILEGES ON *.* TO 'thomas'@'%' WITH GRANT OPTION;
select user,host from mysql.user where user='thomas';
FLUSH PRIVILEGES;
### 允许远程访问
sudo vim /etc/my.cnf
bind-address = 0.0.0.0
### 启用数据库
sudo systemctl enable --now mariadb
sudo systemctl start --now mariadb

## [] 5. 安装和启用存储服务

### 参考链接：https://min.io/docs/minio/linux/operations/install-deploy-manage/deploy-minio-single-node-single-drive.html

sudo groupadd -r minio-user && 
useradd -M -r -g minio-user minio-user
sudo mkdir /mnt/data
sudo chown minio-user:minio-user /mnt/data
sudo systemctl start minio.service
sudo systemctl enable minio.service

### MinIO on podman
dataDir=/mnt/c/Users/bian.haiyuan/workspace
sudo podman run -d --name dataServer -p 9000:9000 -p 9001:9001 -v $dataDir:/data minio/minio server /data --console-address ":9001" 
defaultAccour: minioadmin:minioadmin

## [] 6. 数据标注
cd /mnt/c/Users/bian.haiyuan/workspace
mkdir -p `pwd`/VPG/lablestudio
sudo podman run -it -d -p 8010:8080 -v `pwd`/VPG/lablestudio:/label-studio/data heartexlabs/label-studio:latest
account=2779026762@qq.com/12345678

## [] 7. 本地缓存
sudo zypper install redis
sudo cp /etc/redis/default.conf.example /etc/redis/redis.conf
sudo vim /etc/redis/redis.conf

sudo chown root.redis /etc/redis/redis.conf
sudo vim /etc/systemd/system/redis.service
'''
[Unit]
Description=Redis In-Memory Data Store
After=network.target 

[Service] 
User=redis
Group=redis 
ExecStart=/usr/sbin/redis-server /etc/redis/redis.conf 
LimitNOFILE=10240 
ExecStop=/usr/bin/redis-cli shutdown 
Restart=always 

[Install] 
WantedBy=multi-user.target
'''

sudo systemctl start redis
sudo systemctl enable redis
sudo systemctl status redis
#### journalctl -u redis.service

### redis-cli
set key-test local
get key-test

## [] 8. Nginx 托管本地静态 html
workspace=/mnt/c/Users/bian.haiyuan/workspace/VPG/nginx
staticHtml=/mnt/c/Users/bian.haiyuan/workspace/产品/三安AOI一期/芜湖三安/芜湖定制需求原型-HTML-v04
mkdir -p VPG/nginx
echo """
worker_processes  4;
worker_rlimit_nofile 8192;
events{
worker_connections 1024;
}

http{
  include    mime.types;
  default_type application/octet_stream;
  sendfile on;
  keepalive_timeout 65;
  server {
    listen 8000;
    location / {
      root html;
      index index.html index.htm;
     }
  }
}
""" > nginx/nginx.conf
sudo podman run -it -d --name yuanxing-nginx -p 8000:8000 \
    -v $workspace/nginx.conf:/etc/nginx/nginx.conf \
    -v $staticHtml:/usr/share/nginx/html:ro -d nginx

### Install podman 
. /etc/os-release
echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
curl -L "https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/Release.key" | sudo apt-key add -
sudo apt update && sudo apt install -y podman 
workspace=/home/yuanxing/nginx
staticHtml=/home/yuanxing/芜湖定制需求原型-HTML-v04
sudo docker run -it -d --name sanan-wuhu-v01 -p 8020:8000 \
    -v $workspace/nginx.conf:/etc/nginx/nginx.conf \
    -v $staticHtml:/usr/share/nginx/html:ro -d nginx

## 搭建本地 Gitlab
### refer: https://docs.gitlab.com/ee/install/docker.html
GITLAB_HOME=/mnt/c/Users/bian.haiyuan/workspace/gitlabSpace
mkdir -p $GITLAB_HOME
mkdir -p  $GITLAB_HOME/config
mkdir -p  $GITLAB_HOME/logs
mkdir -p  $GITLAB_HOME/data
export GITLAB_HOME=$GITLAB_HOME
sudo podman run --detach \
  --hostname gitlab.local.com \
  --publish 8443:443 --publish 8010:80 --publish 8022:22 \
  --name gitlab \
  --restart always \
  --volume $GITLAB_HOME/config:/etc/gitlab \
  --volume $GITLAB_HOME/logs:/var/log/gitlab \
  --volume $GITLAB_HOME/data:/var/opt/gitlab \
  --shm-size 512m \
  gitlab/gitlab-ee:latest

## 案例制作 Jupyterlab
pip install jupyterlab voila
    To access the server, open this file in a browser:
        file:///home/yijie/.local/share/jupyter/runtime/jpserver-7774-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/lab?token=229195e3f2397f6e9328b32ea737863407905bb5f490c629
     or http://127.0.0.1:8888/lab?token=229195e3f2397f6e9328b32ea737863407905bb5f490c629
Jupyter-lab &
voila &

## 部署工具
https://github.com/saltstack
https://saltproject.io/


## Linux 基础依赖
nushell
uv (pip)

Mariadb
rust
python 3.11
gradio
label-studio
langflow

##  run langflow
langflow run --port 7860 --workers 2 --timeout 180  --cache InMemoryCache --log-level critical