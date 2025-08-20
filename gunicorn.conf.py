import os
import sys

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(__file__))

# Gunicorn配置
bind = "0.0.0.0:5000"
timeout = 300
graceful_timeout = 300
workers = 2
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# 日志配置
accesslog = "-"
errorlog = "-"
loglevel = "info"
capture_output = True
enable_stdio_inheritance = True