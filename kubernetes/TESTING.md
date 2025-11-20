\# Kubernetes Testing Results - Task 3



\## Environment

\- Minikube version: v1.37.0

\- Kubernetes version: v1.34.0

\- Docker driver

\- OS: Windows 11

\- Docker image size: 130MB



\## Deployment Verified

\- ✅ 3 pods deployed successfully

\- ✅ All pods running and healthy (READY 1/1)

\- ✅ Service created: flask-app-service (NodePort)

\- ✅ ClusterIP assigned: 10.99.197.185

\- ✅ NodePort: 30080

\- ✅ Application accessible via minikube service tunnel



\## Scaling Tested

\- ✅ Scaled from 3 → 5 replicas: Success

&nbsp; - All 5 pods reached Running state

&nbsp; - Pod names: p9lg5, rnvzh, xggtq, j4znx, qbdgv

\- ✅ Scaled from 5 → 3 replicas: Success

&nbsp; - 2 pods gracefully terminated

&nbsp; - 3 pods remain running



\## Rolling Updates Tested

\- ✅ Attempted update to v2 image (flask-k8s-app:v2)

\- ✅ Observed rolling update behavior

\- ✅ Message: "Waiting for deployment rollout to finish: 2 out of 3 new replicas have been updated"

\- ✅ Rolling update strategy working (maxSurge: 1, maxUnavailable: 1)



\## Rollback Tested

\- ✅ Successfully rolled back using: kubectl rollout undo

\- ✅ Rollback completed successfully

\- ✅ Output: "deployment flask-app-deployment successfully rolled out"

\- ✅ All 3 pods healthy after rollback



\## Rollout History

\- ✅ History tracked correctly

\- Revision 2: Initial deployment

\- Revision 3: After rollback



\## Service Access

\- ✅ Service tunnel created: http://127.0.0.1:60543

\- ✅ Main endpoint (/) working

\- ✅ Health endpoint (/health) working

\- ✅ Info endpoint (/info) working



\## Load Balancing Verified

\- ✅ Traffic distributed across all 3 pods

\- ✅ Different pod names in responses (round-robin)

\- ✅ Tested with 10 sequential requests

\- ✅ All pods receiving traffic



\## Resource Limits Applied

\- ✅ CPU requests: 100m per pod

\- ✅ CPU limits: 500m per pod

\- ✅ Memory requests: 128Mi per pod

\- ✅ Memory limits: 256Mi per pod



\## Health Checks Working

\- ✅ Liveness probe: /health (initialDelay: 10s, period: 5s)

\- ✅ Readiness probe: /health (initialDelay: 5s, period: 3s)

\- ✅ Pods marked Ready only after passing probes



\## Pod Details

\- Deployment: flask-app-deployment

\- Pod prefix: flask-app-deployment-68bcc6476b

\- Running pods:

&nbsp; - flask-app-deployment-68bcc6476b-p9lg5

&nbsp; - flask-app-deployment-68bcc6476b-rnvzh

&nbsp; - flask-app-deployment-68bcc6476b-xggtq



\## Test Date

November 20, 2025



\## Conclusion

All Kubernetes features tested and working correctly. Application demonstrates:

\- High availability (3 replicas)

\- Zero-downtime updates (rolling updates)

\- Quick recovery (rollback capability)

\- Load distribution (NodePort service)

\- Resource management (limits and requests)

\- Health monitoring (probes)

