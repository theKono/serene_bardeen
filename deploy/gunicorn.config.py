#!/usr/bin/env python

# standard library imports
import multiprocessing

# third party related imports

# local library imports


bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'egg:gunicorn#eventlet'
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
