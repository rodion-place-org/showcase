"""Gunicorn configuration for x402 forecast endpoint."""
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '5001')}"
backlog = 2048

# Worker processes
workers = int(os.environ.get('WORKERS', '2'))
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests (prevent memory leaks)
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get('LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "x402-forecast"

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# SSL (handled by reverse proxy)
keyfile = None
certfile = None

# Security
limit_request_fields = 100
limit_request_field_size = 8190
limit_request_line = 4094

# Preload app for faster startup and memory savings
preload_app = True

# Worker lifecycle
def on_starting(server):
    server.log.info("Starting x402 forecast endpoint")

def on_reload(server):
    server.log.info("Reloading x402 forecast endpoint")

def worker_int(worker):
    worker.log.info("Worker received INT signal")

def pre_fork(server, worker):
    server.log.info(f"Spawning worker {worker.pid}")

def post_fork(server, worker):
    worker.log.info(f"Worker {worker.pid} spawned")

def post_worker_init(worker):
    worker.log.info(f"Worker {worker.pid} initialized")

def worker_abort(worker):
    worker.log.info(f"Worker {worker.pid} aborted")

def pre_exec(server):
    server.log.info("Forked child, re-executing")

def when_ready(server):
    server.log.info("Server ready, accepting connections")