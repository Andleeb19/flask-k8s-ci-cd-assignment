"""
Flask Application for MLOps CI/CD Assignment
A simple Hello World application with Kubernetes deployment
"""
from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/')
def hello():
    """Main endpoint returning welcome message"""
    return jsonify({
        'message': 'Hello, World! MLOps CI/CD Pipeline',
        'status': 'running',
        'version': '1.0.0'
    })


@app.route('/health')
def health():
    """Health check endpoint for Kubernetes"""
    return jsonify({'status': 'healthy'}), 200


@app.route('/info')
def info():
    """Application information endpoint"""
    return jsonify({
        'app_name': 'Flask K8s CI/CD',
        'python_version': '3.9',
        'pod_name': os.getenv('HOSTNAME', 'local')
    })


def add_numbers(a, b):
    """Simple function for unit testing"""
    return a + b


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
