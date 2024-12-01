workers = 1
worker_class = 'gevent'
worker_connections = 1024
timeout = 10

loglevel = 'info'
errorlog = '-'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
capture_output = True

# 命令行启动
# gunicorn -c gunicorn.conf.py -b '0.0.0.0:15000' -b '[::]:15000'  mibiao.app:app
# gunicorn -c gunicorn.conf.py -b '[::]:15000'  mibiao.app:app
