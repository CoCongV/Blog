import multiprocessing

bind = '127.0.0.1:8080'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
backlog = 2048
debug = True
proc_name = 'gunicorn.pid'
pidfile = './tmp/log/gunicorn/debug.log'
loglevel = 'debug'
