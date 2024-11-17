# mibiao

    gunicorn \
    --log-level=INFO \
    --capture-output \
    --access-logfile - \
    --error-logfile - \
    -b 0.0.0.0:15000 \
    -k gevent \
    -w 1 \
    -t 30 \
    --max-requests 10000 \
    mibiao.app:app