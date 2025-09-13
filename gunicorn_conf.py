import multiprocessing
import os
from dotenv import load_dotenv

load_dotenv()

# Server socket
bind = os.getenv("HOST", "0.0.0.0") + ":" + os.getenv("PORT", "8000")

# Worker processes
workers = int(os.getenv("WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "uvicorn.workers.UvicornWorker"

# Worker configuration
threads = 1
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 120
graceful_timeout = 30
keepalive = 5

# Server mechanics
preload_app = True

# Logging
accesslog = "-"  # Print access logs to stdout
errorlog = "-"   # Print error logs to stdout
loglevel = os.getenv("LOG_LEVEL", "info")

# Process naming
proc_name = "fastapi-production-app"

# Server hooks
def on_starting(server):
    """Execute code when the server starts"""
    print("🚀 Starting Gunicorn server with Uvicorn workers")

def when_ready(server):
    """Execute code when the server is ready to accept connections"""
    print(f"✅ Server is ready. Listening on {bind} with {workers} workers")

def on_exit(server):
    """Execute code when the server is exiting"""
    print("🛑 Server is shutting down")