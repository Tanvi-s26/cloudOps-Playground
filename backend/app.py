from prometheus_client import Counter
from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from flask import Flask, jsonify, render_template
import psutil
import socket
import platform

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "project": "CloudOps Playground",
        "status": "running"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

@app.route("/api/cpu")
def cpu_usage():
    return jsonify({
        "cpu_percent": psutil.cpu_percent(interval=1)
    })

@app.route("/api/memory")
def memory_usage():
    memory = psutil.virtual_memory()

    return jsonify({
        "total": memory.total,
        "used": memory.used,
        "available": memory.available,
        "percent": memory.percent
    })

@app.route("/api/disk")
def disk_usage():
    disk = psutil.disk_usage('/')

    return jsonify({
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent
    })

@app.route("/api/metrics")
def metrics():

    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return jsonify({
        "cpu": psutil.cpu_percent(interval=1),
        "memory": memory.percent,
        "disk": disk.percent
    })


@app.route("/db-health")
def db_health():

    try:
        test_connection()

        return {
            "database": "connected"
        }

    except Exception as e:

        return {
            "database": "failed",
            "error": str(e)
        }

@app.route("/api/system")
def system_info():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return jsonify({
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": memory.percent,
        "disk_percent": disk.percent
    })

@app.route("/dashboard")
def dashboard():

    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    data = {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "cpu": psutil.cpu_percent(interval=1),
        "memory": memory.percent,
        "disk": disk.percent
    }

    return render_template(
        "dashboard.html",
        data=data
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)