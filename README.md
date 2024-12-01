# mibiao

NodeSeek风格米表，效果如下：

![72285645556d26d35cff885c71e4389b.png](https://ice.frostsky.com/2024/12/01/72285645556d26d35cff885c71e4389b.png)

## LXC Debian 12 部署

    apt update

    apt upgrade 

    apt install -y curl wget supervisor

    apt install python3.12-venv python3.12-venv

    python3.12 -m venv .venv

    source .venv/bin/activate
    
## 无 docker 部署

    gunicorn \
    --log-level=INFO \
    --capture-output \
    --access-logfile - \
    --error-logfile - \
    -b 0.0.0.0:15000 \
    -k gevent \
    -w 1 \
    -t 10 \
    --max-requests 10000 \
    mibiao.app:app

## docker + docker-compose 部署

    docker-compose build
    
    docker-compose down && docker-compose up -d

## docker + docker compose 部署

        docker compose build
    
        docker compose down && docker-compose up -d
