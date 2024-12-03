# mibiao

NodeSeek风格米表，推荐部署在内存256MB以上的VPS。

运行效果如下：

![72285645556d26d35cff885c71e4389b.png](https://ice.frostsky.com/2024/12/01/72285645556d26d35cff885c71e4389b.png)

## 【⚠️必装️】Python3 相关软件安装

[Alpine 安装 Python3 及相关软件](./docs/alpine_install_python3.md)  
[Debian 安装 Python3 及相关软件](./docs/debian_install_python3.md)

## 项目安装

### 创建项目目录

    mkdir -p /opt/mibiao && cd /opt/mibiao

### 克隆项目代码

    git clone https://github.com/0x0208v0/mibiao.git /opt/mibiao 

### 创建项目数据目录

    mkdir -p /opt/mibiao/mibiao_data

### 【可选】查看当前路径是否正确（注意：确保此时应该在 /opt/mibiao 目录里）

    pwd

### 创建 Python3 虚拟环境（参考上面的 “Python3 相关软件安装”部分）

    python3 -m venv .venv

### 激活虚拟环境

    source /opt/mibiao/.venv/bin/activate

### 安装项目依赖包

    pip install --no-cache-dir -e .

### 后台运行项目（重启后，项目无法自动重启😭）

根据 VPS 情况，启动项目时监听 IPv4 或者 IPv6（下面三种方式选择一种即可）

#### 【方式一】只监听 ipv6

    # 运行命令后，可以用浏览器访问：
    # http://[2a01:4f8:201:2063::78c0:abcd]:15000/（改成你自己的IPv6地址）
    gunicorn -c gunicorn.conf.py -b '[::]:15000' -D mibiao.app:app

#### 【方式二】只监听 ipv4

    # 运行命令后，可以用浏览器访问：
    # http://239.23.23.42:15000/ （改成你自己的IPv4地址）
    gunicorn -c gunicorn.conf.py -b '0.0.0.0:15000' -D mibiao.app:app

#### 【方式三】只监听 ipv4 + ipv6

如果出现 `connection to ('::', 15000) failed: [Errno 98] Address already in use` 问题，
请看这个issue：https://github.com/benoitc/gunicorn/issues/1138

    gunicorn -c gunicorn.conf.py -b '0.0.0.0:15000' -b '[::]:15000' -D mibiao.app:app

### 检查是否已启动

    ps aux | grep gunicorn

看到下面的输出，则表示成功：

    (.venv) root@g4puxx72:/opt/mibiao# ps aux | grep gunicorn
    root        7265  0.0  9.0  39232 23720 ?        S    14:29   0:00 /opt/mibiao/.venv/bin/python3 /opt/mibiao/.venv/bin/gunicorn -c gunicorn.conf.py -b [::]:15000 -D mibiao.app:app
    root        7266  0.0 25.9 1133244 68040 ?       S    14:29   0:00 /opt/mibiao/.venv/bin/python3 /opt/mibiao/.venv/bin/gunicorn -c gunicorn.conf.py -b [::]:15000 -D mibiao.app:app

## 【可选】保活

[Supervisor 安装 + 配置 + 守护（推荐：重启后，项目可以自动重启😎）](./docs/supervisor_install.md)

## docker + docker-compose 部署

    docker-compose build
    
    docker-compose down && docker-compose up -d

## docker + docker compose 部署

    docker compose build

    docker compose down && docker-compose up -d

## 参考资料：

### Gunicorn：

[Gunicorn Settings¶](https://docs.gunicorn.org/en/latest/settings.html#settings)

### Supervisor：

[Supervisor Configuration File¶](http://supervisord.org/configuration.html)  
[Differences between reread, reload, restart, update? #720](https://github.com/Supervisor/supervisor/issues/720)  
[Supervisord: Restarting and Reloading](https://www.onurguzel.com/supervisord-restarting-and-reloading/)
