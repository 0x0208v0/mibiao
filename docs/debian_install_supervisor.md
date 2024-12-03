## Debian 12 安装 Supervisor 并配置自启保活

### 安装软件

    apt update && apt upgrade -y && apt install -y supervisor

### 确认是否安装成功（成功则能看见 conf.d 和 supervisord.conf）

    ls /etc/supervisor

### 进入配置目录

    cd /etc/supervisor/conf.d

### 从项目里复制一份 Supervisor 配置文件

    cp /opt/mibiao/supervisor.conf /etc/supervisor/conf.d/mibiao.conf

### 让 Supervisor 重新加载配置文件，并启动项目

    supervisorctl update

看到下面的输出，则表示配置已添加

    (.venv) root@g4puxx72:/etc/supervisor/conf.d# supervisorctl update
    mibiao: added process group

### 启动 Supervisor

    supervisorctl update

看到下面的输出，则表示配置已添加

    (.venv) root@g4puxx72:/etc/supervisor/conf.d# supervisorctl update
    mibiao: added process group

### 检查是否已启动

    ps aux | grep gunicorn

看到下面的输出，则表示成功：

    root@g4puxx72:/etc/supervisor/conf.d# ps aux | grep gunicorn
    root        7931  0.0 10.9  39248 28672 ?        S    14:54   0:00 /opt/mibiao/.venv/bin/python3 /opt/mibiao/.venv/bin/gunicorn -c /opt/mibiao/gunicorn.conf.py -b 0.0.0.0:15000 mibiao.app:app
    root        7932  0.0 26.0 1133184 68312 ?       S    14:54   0:00 /opt/mibiao/.venv/bin/python3 /opt/mibiao/.venv/bin/gunicorn -c /opt/mibiao/gunicorn.conf.py -b 0.0.0.0:15000 mibiao.app:app

### 停止项目

    supervisorctl stop mibiao

### 启动项目

    supervisorctl start mibiao