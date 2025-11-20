\# Jenkins Pipeline Configuration - Task 4



\## Overview

This document describes the Jenkins CI/CD pipeline configured for automated Kubernetes deployment.



\## Pipeline Structure



\### Stage 1: Build Docker Image

\- Builds the Flask application Docker image

\- Tags as `flask-k8s-app:latest`

\- Verifies image creation



\### Stage 2: Deploy to Kubernetes

\- Applies `kubernetes/deployment.yaml` (3 replicas)

\- Applies `kubernetes/service.yaml` (NodePort)

\- Uses `kubectl apply` commands



\### Stage 3: Verify Deployment

\- Checks rollout status (120s timeout)

\- Displays pods status

\- Shows services configuration

\- Lists deployment details

\- Verifies all pods are ready



\## Environment Variables

\- `DOCKER\_IMAGE`: flask-k8s-app:latest

\- `KUBECONFIG`: /home/jenkins/.kube/config



\## Post-Build Actions

\- Success: Logs completion message

\- Failure: Logs failure details



\## Kubernetes Resources

\- \*\*Deployment:\*\* flask-app-deployment (3 replicas)

\- \*\*Service:\*\* flask-app-service (NodePort 30080)

\- \*\*Selector:\*\* app=flask-app



\## Task 4 Requirements Met

✅ Jenkinsfile with 3+ stages created

✅ Stage 1: Build Docker Image

✅ Stage 2: Deploy using kubectl apply

✅ Stage 3: Verify deployment with rollout status

✅ Declarative pipeline syntax used

✅ Ready for Jenkins job configuration

