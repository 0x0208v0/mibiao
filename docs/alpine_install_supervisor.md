## Alpine 3.18 安装 Supervisor 并配置自启保活

### 安装软件

    apk add supervisor

### 确认是否安装成功（成功则能看见配置文件内容）

    cat /etc/supervisord.conf

### 创建并进入配置目录

    mkdir -p /etc/supervisor.d && cd /etc/supervisor.d 

### 从项目里复制一份 Supervisor 配置文件

    cp /opt/mibiao/supervisor.conf /etc/supervisor.d/supervisor.ini

### 启动 Supervisor

    supervisord -c /etc/supervisord.conf

### 检查是否已启动

    ps aux | grep gunicorn

看到下面的输出，则表示成功：

    (.venv) test:/etc/supervisor.d# ps aux | grep gunicorn
     1201 root      0:00 {gunicorn} /opt/mibiao/.venv/bin/python3 /opt/mibiao/.venv/bin/gunicorn -c /opt/mibiao/gunicorn.conf.py -b [::]:15000 mibiao.app:app
     1202 root      0:00 {gunicorn} /opt/mibiao/.venv/bin/python3 /opt/mibiao/.venv/bin/gunicorn -c /opt/mibiao/gunicorn.conf.py -b [::]:15000 mibiao.app:app

### 停止项目

    supervisorctl stop mibiao

### 启动项目

    supervisorctl start mibiao