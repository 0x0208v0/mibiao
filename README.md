# mibiao

NodeSeek风格米表

**操作系统要求：**    
Linux系统；OSX系统

**最低硬件配置：**  
128MB内存；1GB硬盘空间

**推荐硬件配置：**  
256MB内存；2GB硬盘空间

**运行效果如下：**

![72285645556d26d35cff885c71e4389b.png](https://ice.frostsky.com/2024/12/01/72285645556d26d35cff885c71e4389b.png)

## 【‼️必装️】Python3 及相关依赖软件安装

[Alpine 安装 Python3 及相关依赖软件](./docs/alpine_install_python3.md)  
[Debian 安装 Python3 及相关依赖软件](./docs/debian_install_python3.md)

## 项目安装（需要 Python3 及相关依赖软件）

### 创建项目目录

    mkdir -p /opt/mibiao && cd /opt/mibiao

### 克隆项目代码

    git clone https://github.com/0x0208v0/mibiao.git /opt/mibiao 

### 创建项目数据目录（⚠️注意：用于存放项目的数据库和其他文件）

    mkdir -p /opt/mibiao/mibiao_data

### 【可选】查看当前路径是否正确（⚠️注意：确保此时在 /opt/mibiao 目录中）

    pwd

### 创建 Python3 虚拟环境（参考上面的 “Python3 相关软件安装”部分）

    python3 -m venv .venv

### 激活虚拟环境

    source /opt/mibiao/.venv/bin/activate

### 安装项目依赖包

    pip install --no-cache-dir -e .

### 后台运行项目（服务器重启后，项目将无法自动重启😭，自启请看“保活”相关文档）

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

## 【可选】配置 Supervisor 自启保活（推荐：服务器重启后，项目可以自动启动😎）

[Alpine 3.18 安装 Supervisor 并配置自启保活](./docs/alpine_install_supervisor.md)  
[Debian 12 安装 Supervisor 并配置自启保活](./docs/debian_install_supervisor.md)

## docker + docker-compose 方式安装项目

    docker-compose build
    
    docker-compose down && docker-compose up -d

## docker + docker compose 方式安装项目

    docker compose build

    docker compose down && docker-compose up -d

## 参考资料：

### Gunicorn：

[Gunicorn Settings¶](https://docs.gunicorn.org/en/latest/settings.html#settings)

### Supervisor：

[Supervisor Configuration File¶](http://supervisord.org/configuration.html)  
[Differences between reread, reload, restart, update? #720](https://github.com/Supervisor/supervisor/issues/720)  
[Supervisord: Restarting and Reloading](https://www.onurguzel.com/supervisord-restarting-and-reloading/)
