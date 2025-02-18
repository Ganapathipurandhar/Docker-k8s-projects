# Kubernetes Problems and Troubleshooting Guide

This guide provides structured troubleshooting steps for common Kubernetes problems, highlighting specific error messages.

---

## 1. Image Pull Error (`ImagePullBackOff`, `ErrImagePull`)

### Scenario:
A pod fails to start because Kubernetes cannot pull the specified container image.

### Possible Causes:
- The image name or tag is incorrect.
- The image is hosted in a private registry, and authentication is missing.
- The image does not exist in the repository.
- Network issues prevent the image pull.

### Troubleshooting Steps:
1. **Check Pod Events:**
   ```bash
   kubectl describe pod <pod-name> -n <namespace>

Kubernetes Problems and Troubleshooting Guide

1. Image Pull Error (ImagePullBackOff, ErrImagePull)

Scenario:

A pod fails to start because Kubernetes cannot pull the specified container image.

Possible Causes:

The image name or tag is incorrect.

The image is hosted in a private registry, and authentication is missing.

The image does not exist in the repository.

Network issues prevent the image pull.

Troubleshooting Steps:

Check Pod Events:

kubectl describe pod <pod-name> -n <namespace>

Verify Image Exists:

docker pull <image-name>:<tag>

Check Registry Authentication:

kubectl get secret -n <namespace>

Manually Set Image Credentials (if needed):

kubectl create secret docker-registry my-secret --docker-server=<registry-server> --docker-username=<username> --docker-password=<password> --namespace=<namespace>

2. Crashing Pods (CrashLoopBackOff)

Scenario:

A pod keeps restarting or failing after launching.

Possible Causes:

The application inside the container is failing due to a misconfiguration.

Readiness or liveness probes are incorrectly defined.

The pod is running out of memory or CPU.

Required environment variables or secrets are missing.

Troubleshooting Steps:

Check Pod Logs:

kubectl logs <pod-name> -n <namespace>

Describe the Pod to View Events:

kubectl describe pod <pod-name> -n <namespace>

Check Resource Requests and Limits:

kubectl get pod <pod-name> -o=jsonpath='{.spec.containers[*].resources}'

Adjust Resources If Needed:

kubectl edit deployment <deployment-name> -n <namespace>

3. Pending Pods (Pending)

Scenario:

A pod stays in the "Pending" state and never transitions to "Running".

Possible Causes:

No nodes are available with enough resources.

Node selector or taints are misconfigured.

Persistent volume claims are not bound.

The scheduler cannot find a suitable node.

Troubleshooting Steps:

Check Events and Scheduling Issues:

kubectl describe pod <pod-name> -n <namespace>

Check Available Nodes:

kubectl get nodes -o wide

Review Taints and Tolerations:

kubectl describe node <node-name>

4. Missing Pods

Scenario:

A deployment has been applied, but the expected pods are not running.

Possible Causes:

The deployment has incorrect configurations causing pod failures.

A higher-priority workload is evicting the pods.

The cluster autoscaler removed nodes unexpectedly.

Troubleshooting Steps:

List All Pods:

kubectl get pods -A

Check Deployment Status:

kubectl describe deployment <deployment-name> -n <namespace>

Investigate Node Autoscaler Logs:

kubectl get events --sort-by=.metadata.creationTimestamp

5. Schrödinger’s Deployment (Deployment Exists but Doesn’t Work)

Scenario:

A deployment appears to exist but is unresponsive or inconsistently reported.

Possible Causes:

A network partition causes Kubernetes control plane desynchronization.

The controller-manager is malfunctioning.

Troubleshooting Steps:

Restart Affected Nodes:

kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

Verify Controller-Manager Status:

kubectl get componentstatuses

Force Redeploy:

kubectl delete deployment <deployment-name> -n <namespace>
kubectl apply -f <deployment.yaml>

6. Multi-Attached Volume Errors (Multi-Attach Error for Volume)

Scenario:

A pod using a Persistent Volume Claim (PVC) fails due to a multi-attach error.

Possible Causes:

The volume is already attached to another node.

The storage class does not allow multiple read-write nodes.

Pod scheduling on a different node than its volume.

Troubleshooting Steps:

Check PVC Status:

kubectl get pvc -n <namespace>

Verify Node Attachment:

kubectl describe pod <pod-name> -n <namespace>

Unmount and Reattach the Volume:

kubectl delete pod <pod-name> -n <namespace>

7. RBAC Issues (Forbidden Errors)

Scenario:

A user or service account cannot perform an expected action in the cluster.

Possible Causes:

Incorrect role or role binding.

Missing permissions.

Troubleshooting Steps:

Check User Permissions:

kubectl auth can-i get pods -n <namespace>

View Role Bindings:

kubectl get rolebindings -A

Review and Edit Role Configurations:

kubectl describe role <role-name> -n <namespace>

This guide provides structured troubleshooting steps for common Kubernetes problems, highlighting specific error messages. Let me know if additional scenarios or commands need to be included!