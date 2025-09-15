# FastAPI Production Deployment with Gunicorn + Uvicorn

A complete guide and setup for deploying FastAPI applications in production using Gunicorn as a process manager with Uvicorn workers.

---


## 📁 Project Structure

```
fastapi-production-deployment/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   └── routes/
│       ├── __init__.py
│       ├── items.py
│       └── users.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_routes.py
├── gunicorn_conf.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Features

- 🚀 Production-grade FastAPI deployment
- 🔧 Gunicorn + Uvicorn worker configuration
- 📦 Docker containerization
- 🔒 Environment-based configuration
- 📊 Health checks and monitoring endpoints
- 🧪 Test suite with pytest
- 📝 Comprehensive logging
- 🔄 Process management and auto-reload

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- pip
- Docker and Docker Compose (optional, for containerized deployment)

---

### 1. Clone and Set Up the Project

```bash
mkdir fastapi-production-deployment
cd fastapi-production-deployment

python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt

# For development (testing, linting, etc.):
pip install -r requirements-dev.txt
```

**Potential Errors & Solutions:**
- **Error:** `Failed building wheel for cryptography`  
  - Ubuntu/Debian: `sudo apt-get install build-essential libssl-dev libffi-dev python3-dev`
  - Windows: Install Visual Studio Build Tools
  - macOS: `xcode-select --install`

---

### 3. Configure Environment Variables

```bash
cp .env.example .env
```
Edit `.env` with your configuration (e.g., `DATABASE_URL`, `DEBUG`, `WORKERS`).

---

### 4. Run the Application

#### Development Mode (with auto-reload):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Production Mode with Gunicorn:

```bash
gunicorn -c gunicorn_conf.py app.main:app
```

#### Using Docker:

```bash
docker-compose up --build

# Or build and run individually:
docker build -t fastapi-app .
docker run -p 8000:80 fastapi-app
```

---

## ⚙️ Configuration

### Gunicorn (`gunicorn_conf.py`)

- Worker processes: calculated by CPU cores or override via env
- Worker class: Uvicorn workers for async support
- Port: default 8000
- Logging: logs to stdout
- Preload app and graceful timeouts

### Environment Variables

Edit `.env` (see `.env.example`):

```ini
DEBUG=False
HOST=0.0.0.0
PORT=8000
WORKERS=4
LOG_LEVEL=info
DATABASE_URL=sqlite:///./test.db
```

---

## 🔗 API Endpoints

| Method | Endpoint           | Description      |
|--------|--------------------|------------------|
| GET    | `/`                | Welcome message  |
| GET    | `/health`          | Health check     |
| GET    | `/items/`          | List items       |
| POST   | `/items/`          | Create item      |
| GET    | `/items/{item_id}` | Get item by ID   |
| GET    | `/users/`          | List users       |
| POST   | `/users/`          | Create user      |
| GET    | `/users/{user_id}` | Get user by ID   |

---

## 🚀 Production Deployment

### 1. Traditional Server

```bash
pip install -r requirements.txt
gunicorn -c gunicorn_conf.py app.main:app
# Or specify number of workers:
gunicorn -c gunicorn_conf.py app.main:app --workers 8
```

### 2. Docker

```bash
docker build -t my-fastapi-app .
docker run -p 8000:80 my-fastapi-app

# Or with environment file
docker run -p 8000:80 --env-file .env my-fastapi-app
```

### 3. Docker Compose

```bash
docker-compose up -d
docker-compose logs -f
docker-compose up -d --scale web=4
```

### 4. Kubernetes (example)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: fastapi-app
        image: my-fastapi-app:latest
        ports:
        - containerPort: 80
        envFrom:
        - configMapRef:
            name: fastapi-config
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  selector:
    app: fastapi-app
  ports:
  - port: 80
    targetPort: 80
```

---

## ⚡ Performance Tuning

- **Workers:**  
  `workers = (2 * CPU cores) + 1` (default in `gunicorn_conf.py`)
- **Monitoring:**  
  `curl http://localhost:8000/health`
- **Load Testing:**  
  Install and run `locust`:
  ```bash
  pip install locust
  locust -f locustfile.py
  ```
  Open [http://localhost:8089](http://localhost:8089) to start testing.

---

## 🩺 Health Checks & Monitoring

- `/health`: Basic health check
- `/health/detailed`: System info (requires `psutil`)
- `/metrics`: Application metrics (if configured with Prometheus)

---

## 📝 Logging

- Logs output to stdout (JSON or plain text)
- Example:
  ```json
  {
    "timestamp": "2023-01-01T12:00:00.000Z",
    "level": "INFO",
    "message": "Request completed",
    "method": "GET",
    "path": "/health",
    "status_code": 200,
    "duration": 0.002
  }
  ```

---

## 🔒 Security Considerations

1. Never commit sensitive data to version control
2. Update dependencies regularly
3. Use non-root users in Docker containers
4. Always use HTTPS in production (with a reverse proxy)
5. Set CORS properly for your frontend domains

---

## 🐞 Troubleshooting

- **Port already in use:**  
  Find and kill the process or use a different port:
  ```bash
  lsof -ti:8000 | xargs kill -9
  gunicorn -c gunicorn_conf.py app.main:app --bind 0.0.0.0:8001
  ```
- **Worker timeout errors:**  
  Increase timeout in `gunicorn_conf.py` (`timeout = 120`)
- **Memory issues:**  
  Reduce number of workers or use connection pooling
- **Database connection issues:**  
  Check `DATABASE_URL` and connectivity

- **Debug mode:**  
  Set `DEBUG=True` in `.env` and run:
  ```bash
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```

---

## 🛠️ Fixing Circular Import Error

If you see an error about circular imports (e.g. `from app.main import app` in `app/main.py`):

- **Remove any line like:**  
  `from app.main import app`  
  from `app/main.py`.

- The FastAPI app should be defined directly in `app/main.py`:
  ```python
  from fastapi import FastAPI
  app = FastAPI()
  ```

- For running with `uvicorn`, use:
  ```bash
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```

**Optional:** Create a `run.py` in root for manual running:
```python
# run.py
import uvicorn
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL
    )
```
Run: `python run.py`

- For `/health/detailed` endpoint, ensure `psutil` is installed:
  ```bash
  pip install psutil
  ```

---

## 📝 License

MIT License – Free to use for learning and production deployments.

---

**This setup provides a robust, production-ready FastAPI app with Gunicorn+Uvicorn, Docker, environment-based config, and modern deployment best practices.**
