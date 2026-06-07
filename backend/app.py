from flask import Flask, jsonify
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)