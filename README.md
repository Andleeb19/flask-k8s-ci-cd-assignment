# Flask Kubernetes CI/CD Assignment

## Project Overview

This project demonstrates a complete **CI/CD pipeline** for a Flask web application using:
- **GitHub Actions** for Continuous Integration (automated testing)
- **Jenkins** for Continuous Delivery (automated deployment)
- **Docker** for containerization
- **Kubernetes (minikube)** for orchestration and scaling

### Application Features
- Simple Flask REST API with multiple endpoints
- Health check endpoint for Kubernetes probes
- Automated testing with pytest and flake8
- Docker multi-stage build for optimized images

### Kubernetes Features Used
1. **Automated Rollouts**: Rolling update strategy with zero downtime
2. **Scaling**: Multiple replicas (3 pods) for high availability
3. **Load Balancing**: NodePort service distributes traffic across pods
4. **Resource Management**: CPU and memory limits/requests
5. **Health Monitoring**: Liveness and readiness probes

---

## Prerequisites

### Required Software
- Git
- Docker Desktop
- Python 3.9+
- Minikube
- kubectl
- Jenkins

### Installation Links
- **Docker**: https://www.docker.com/products/docker-desktop
- **Minikube**: https://minikube.sigs.k8s.io/docs/start/
- **kubectl**: https://kubernetes.io/docs/tasks/tools/

---

## Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/flask-k8s-ci-cd-assignment.git
cd flask-k8s-ci-cd-assignment
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application Locally
```bash
python app.py
```
Access the app at: http://localhost:5000

### 4. Run Tests
```bash
# Run unit tests
pytest test_app.py -v

# Run linting
flake8 . --max-line-length=90
```

---

## Docker Setup

### Build the Docker Image
```bash
docker build -t flask-k8s-app:latest .
```

### Run the Container
```bash
docker run -d -p 5000:5000 --name flask-app flask-k8s-app:latest
```

### Test the Container
```bash
curl http://localhost:5000
```

### Stop and Remove Container
```bash
docker stop flask-app
docker rm flask-app
```

---

## Kubernetes Deployment

### 1. Start Minikube
```bash
minikube start --driver=docker
```

### 2. Load Docker Image to Minikube
```bash
# Build image in minikube's Docker environment
eval $(minikube docker-env)
docker build -t flask-k8s-app:latest .
```

### 3. Deploy to Kubernetes
```bash
# Apply manifests
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml

# Verify deployment
kubectl get pods
kubectl get services
kubectl get deployments
```

### 4. Access the Application
```bash
# Get minikube IP and service URL
minikube service flask-app-service --url

# Or use port forwarding
kubectl port-forward service/flask-app-service 8080:80
```
Then visit: http://localhost:8080

### 5. Test Kubernetes Features

#### Scaling
```bash
# Scale to 5 replicas
kubectl scale deployment flask-app-deployment --replicas=5

# Verify
kubectl get pods
```

#### Rolling Update
```bash
# Update the image (simulate new version)
kubectl set image deployment/flask-app-deployment \
  flask-container=flask-k8s-app:v2

# Watch the rollout
kubectl rollout status deployment/flask-app-deployment
```

#### Rollback
```bash
# Rollback to previous version
kubectl rollout undo deployment/flask-app-deployment

# Check rollout history
kubectl rollout history deployment/flask-app-deployment
```

#### Load Balancing Test
```bash
# Send multiple requests and see different pod responses
for i in {1..10}; do
  curl http://$(minikube ip):30080/info | grep pod_name
done
```

---

## Jenkins Pipeline Setup

### 1. Start Jenkins
```bash
docker run -d -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name jenkins jenkins/jenkins:lts
```

### 2. Initial Jenkins Setup
```bash
# Get initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```
- Open http://localhost:8080
- Enter the password
- Install suggested plugins
- Create admin user

### 3. Install Required Plugins
Go to: **Manage Jenkins → Plugins → Available Plugins**
- Git Plugin
- Pipeline Plugin
- Docker Pipeline Plugin
- Kubernetes CLI Plugin

### 4. Configure Kubernetes Access in Jenkins
```bash
# Copy minikube config to Jenkins
docker exec -it jenkins mkdir -p /var/jenkins_home/.kube
docker cp ~/.kube/config jenkins:/var/jenkins_home/.kube/config
docker exec jenkins chmod 600 /var/jenkins_home/.kube/config
```

### 5. Create Pipeline Job
1. Click "New Item" → Enter name → Select "Pipeline"
2. Under "Pipeline" section:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: Your GitHub repo URL
   - **Branch**: main
   - **Script Path**: Jenkinsfile
3. Save and click "Build Now"

---

## CI/CD Workflow

### GitHub Actions (CI)
Automatically runs on every push:
1. Sets up Python environment
2. Installs dependencies
3. Runs flake8 linting (max 90 chars per line)
4. Runs pytest unit tests
5. Builds Docker image

### Jenkins Pipeline (CD)
Runs when code is merged to main:
1. **Build Stage**: Creates Docker image
2. **Deploy Stage**: Applies Kubernetes manifests
3. **Verify Stage**: Checks deployment status and pod health

---

## Project Structure
```
flask-k8s-ci-cd-assignment/
├── app.py                      # Flask application
├── test_app.py                 # Unit tests
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Multi-stage Docker build
├── Jenkinsfile                 # Jenkins pipeline definition
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions workflow
├── kubernetes/
│   ├── deployment.yaml        # Kubernetes deployment manifest
│   └── service.yaml           # Kubernetes service manifest
└── README.md                  # This file
```

---

## Kubernetes Rollout Strategy Explained

### Rolling Update Strategy
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1        # Max 1 extra pod during update
    maxUnavailable: 1  # Max 1 pod can be unavailable
```

**How it works:**
1. With 3 replicas, during update:
   - First, creates 1 new pod (total: 4 pods)
   - Waits for new pod to be ready
   - Terminates 1 old pod (back to 3 pods)
   - Repeats until all pods are updated
2. **Zero downtime**: Service always has running pods
3. **Gradual rollout**: Issues caught early, can rollback easily

### Load Balancing
The NodePort service distributes incoming traffic across all healthy pods:
- Uses round-robin algorithm by default
- Only routes to pods that pass health checks
- Automatically removes failed pods from rotation

### Resource Management
```yaml
resources:
  requests:
    memory: "128Mi"  # Guaranteed minimum
    cpu: "100m"      # 0.1 CPU cores
  limits:
    memory: "256Mi"  # Maximum allowed
    cpu: "500m"      # 0.5 CPU cores
```
Ensures pods don't consume excessive resources.

---

## Troubleshooting

### Minikube Issues
```bash
# Stop and restart minikube
minikube stop
minikube start

# Delete and recreate cluster
minikube delete
minikube start
```

### Pod Not Starting
```bash
# Check pod logs
kubectl logs <pod-name>

# Describe pod for events
kubectl describe pod <pod-name>
```

### Jenkins Build Fails
```bash
# Check Jenkins has kubectl access
docker exec jenkins kubectl version

# Verify Docker socket access
docker exec jenkins docker ps
```

---

## Team Members
- **Member A (Admin)**: Andleeb
- **Member B (Developer)**: Maria
---

## References
- Flask Documentation: https://flask.palletsprojects.com/
- Kubernetes Documentation: https://kubernetes.io/docs/
- Docker Documentation: https://docs.docker.com/
- Jenkins Documentation: https://www.jenkins.io/doc/

---

## License
This project is for educational purposes as part of MLOps coursework.
