# mibiao

NodeSeek风格米表，推荐部署在内存256MB以上的VPS。

运行效果如下：

![72285645556d26d35cff885c71e4389b.png](https://ice.frostsky.com/2024/12/01/72285645556d26d35cff885c71e4389b.png)

## Debian 12 部署

    # 创建项目目录
    mkdir -p /opt/mibiao && cd /opt/mibiao
    
    # 安装必备软件
    apt update && apt upgrade -y && apt install -y git
    
    # 克隆项目代码
    git clone https://github.com/0x0208v0/mibiao.git
    
    # 进入项目所在目录
    cd mibiao

    # 【可选】查看当前路径是否正确（注意：确保此时应该在 /opt/mibiao/mibiao 目录里）
    pwd

    # 安装 Python3 相关软件
    apt install -y python3 python3-pip python3-venv
    
    # 创建Python3.12虚拟环境
    python3 -m venv .venv
    
    # 激活虚拟环境
    source /opt/mibiao/mibiao/.venv/bin/activate
    
    # 安装项目依赖包
    pip install e .
    
    # 根据 VPS 情况，监听 IPv4 或者 IPv6（下面三种方式选择一种即可）
    
    # 【方式一】只监听 ipv6
    gunicorn -c gunicorn.conf.py -b '[::]:15000' -D mibiao.app:app
    
    # 【方式二】只监听 ipv4
    gunicorn -c gunicorn.conf.py -b '0.0.0.0:15000' -D mibiao.app:app
    
    # 【方式三】只监听 ipv4 + ipv6
    gunicorn -c gunicorn.conf.py -b '0.0.0.0:15000' -b '[::]:15000' -D mibiao.app:app

## 【可选】Supervisor 安装 + 配置 + 后台守护

### Debian 12 安装 Supervisor

    # 安装软件
    apt update && apt upgrade -y && apt install -y supervisor
    
    # 进入配置目录
    cd /etc/supervisor/conf.d
    
    # 确认是否安装成功（成功则能看见 conf.d 和 supervisord.conf）
    ls /etc/supervisor

### 其他环节

    # todo
    echo todo

### 配置 + 后台守护

    # todo
    echo todo

## 无 docker 部署

## docker + docker-compose 部署

    docker-compose build
    
    docker-compose down && docker-compose up -d

## docker + docker compose 部署

        docker compose build
    
        docker compose down && docker-compose up -d
