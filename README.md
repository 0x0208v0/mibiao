# mibiao

NodeSeek风格米表，推荐部署在内存256MB以上的VPS。

运行效果如下：

![72285645556d26d35cff885c71e4389b.png](https://ice.frostsky.com/2024/12/01/72285645556d26d35cff885c71e4389b.png)

## Debian 12 部署

    # 创建项目目录
    mkdir -p /opt/mibiao && cd /opt/mibiao
    
    # 安装必备软件
    apt update && apt upgrade -y && apt install -y curl wget git supervisor
    
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
    source  /opt/mibiao/mibiao/.venv/bin/activate
    
    # 安装项目依赖包
    pip install e .

## Supervisor 配置

    cd /etc/supervisor/conf.d

## 无 docker 部署

    # ipv4
    gunicorn \
    --log-level=INFO \
    --capture-output \
    --access-logfile - \
    --error-logfile - \
    -b 0.0.0.0:15000 \
    -k gevent \
    -w 1 \
    -t 10 \
    --max-requests 1000 \
    mibiao.app:app
    
    # ipv6
    gunicorn \
    --log-level=INFO \
    --capture-output \
    --access-logfile - \
    --error-logfile - \
    -b '[::]:15000' \
    -k gevent \
    -w 1 \
    -t 10 \
    --max-requests 1000 \
    mibiao.app:app

## docker + docker-compose 部署

    docker-compose build
    
    docker-compose down && docker-compose up -d

## docker + docker compose 部署

        docker compose build
    
        docker compose down && docker-compose up -d
