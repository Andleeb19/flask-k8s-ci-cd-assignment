pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'flask-k8s-app:latest'
        KUBECONFIG = '/home/jenkins/.kube/config'
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh '''
                        docker build -t ${DOCKER_IMAGE} .
                        docker images | grep flask-k8s-app
                    '''
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo 'Deploying to Kubernetes cluster...'
                    sh '''
                        # Apply Kubernetes manifests
                        kubectl apply -f kubernetes/deployment.yaml
                        kubectl apply -f kubernetes/service.yaml
                        
                        echo "Deployment and Service created/updated"
                    '''
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                script {
                    echo 'Verifying deployment status...'
                    sh '''
                        # Check rollout status
                        kubectl rollout status deployment/flask-app-deployment \
                          --timeout=120s
                        
                        # Display pods
                        echo "\\n=== Pods Status ==="
                        kubectl get pods -l app=flask-app
                        
                        # Display services
                        echo "\\n=== Services ==="
                        kubectl get services flask-app-service
                        
                        # Display deployments
                        echo "\\n=== Deployments ==="
                        kubectl get deployments flask-app-deployment
                        
                        # Verify all pods are running
                        READY_PODS=$(kubectl get pods -l app=flask-app \
                          -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}' | grep -o "True" | wc -l)
                        TOTAL_PODS=$(kubectl get pods -l app=flask-app \
                          --no-headers | wc -l)
                        
                        echo "\\nReady Pods: $READY_PODS / $TOTAL_PODS"
                        
                        if [ "$READY_PODS" -eq "$TOTAL_PODS" ]; then
                            echo "✓ All pods are ready!"
                        else
                            echo "✗ Some pods are not ready"
                            exit 1
                        fi
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
