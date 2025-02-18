# Kubernetes Problems and Troubleshooting Guide

This guide provides structured troubleshooting steps for common Kubernetes problems, highlighting specific error messages.

---

## 1. Image Pull Error (`ImagePullBackOff`, `ErrImagePull`)

### Scenario
A pod fails to start because Kubernetes cannot pull the specified container image.

### Possible Causes
- Incorrect image name or tag.
- Image hosted in a private registry, but authentication is missing.
- Image does not exist in the repository.
- Network issues preventing the image pull.

### Troubleshooting Steps
1. **Check Pod Events:**
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```
2. **Verify Image Exists:**
   ```bash
   docker pull <image-name>:<tag>
   ```
3. **Check Registry Authentication:**
   ```bash
   kubectl get secret -n <namespace>
   ```
4. **Manually Set Image Credentials (if needed):**
   ```bash
   kubectl create secret docker-registry my-secret \
     --docker-server=<registry-server> \
     --docker-username=<username> \
     --docker-password=<password> \
     --namespace=<namespace>
   ```

---

## 2. Crashing Pods (`CrashLoopBackOff`)

### Scenario
A pod keeps restarting or failing after launching.

### Possible Causes
- The application inside the container is failing due to a misconfiguration.
- Readiness or liveness probes are incorrectly defined.
- The pod is running out of memory or CPU.
- Required environment variables or secrets are missing.

### Troubleshooting Steps
1. **Check Pod Logs:**
   ```bash
   kubectl logs <pod-name> -n <namespace>
   ```
2. **Describe the Pod to View Events:**
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```
3. **Check Resource Requests and Limits:**
   ```bash
   kubectl get pod <pod-name> -o=jsonpath='{.spec.containers[*].resources}'
   ```
4. **Adjust Resources If Needed:**
   ```bash
   kubectl edit deployment <deployment-name> -n <namespace>
   ```

---

## 3. Pending Pods (`Pending`)

### Scenario
A pod stays in the "Pending" state and never transitions to "Running".

### Possible Causes
- No nodes are available with enough resources.
- Node selector or taints are misconfigured.
- Persistent volume claims are not bound.
- The scheduler cannot find a suitable node.

### Troubleshooting Steps
1. **Check Events and Scheduling Issues:**
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```
2. **Check Available Nodes:**
   ```bash
   kubectl get nodes -o wide
   ```
3. **Review Taints and Tolerations:**
   ```bash
   kubectl describe node <node-name>
   ```

---

## 4. Missing Pods

### Scenario
A deployment has been applied, but the expected pods are not running.

### Possible Causes
- Incorrect deployment configurations causing pod failures.
- A higher-priority workload is evicting the pods.
- The cluster autoscaler removed nodes unexpectedly.

### Troubleshooting Steps
1. **List All Pods:**
   ```bash
   kubectl get pods -A
   ```
2. **Check Deployment Status:**
   ```bash
   kubectl describe deployment <deployment-name> -n <namespace>
   ```
3. **Investigate Node Autoscaler Logs:**
   ```bash
   kubectl get events --sort-by=.metadata.creationTimestamp
   ```

---

## 5. Schrödinger’s Deployment (Deployment Exists but Doesn’t Work)

### Scenario
A deployment appears to exist but is unresponsive or inconsistently reported.

### Possible Causes
- A network partition causes Kubernetes control plane desynchronization.
- The controller-manager is malfunctioning.

### Troubleshooting Steps
1. **Restart Affected Nodes:**
   ```bash
   kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
   ```
2. **Verify Controller-Manager Status:**
   ```bash
   kubectl get componentstatuses
   ```
3. **Force Redeploy:**
   ```bash
   kubectl delete deployment <deployment-name> -n <namespace>
   kubectl apply -f <deployment.yaml>
   ```

---

## 6. Multi-Attached Volume Errors (`Multi-Attach Error for Volume`)

### Scenario
A pod using a Persistent Volume Claim (PVC) fails due to a multi-attach error.

### Possible Causes
- The volume is already attached to another node.
- The storage class does not allow multiple read-write nodes.
- Pod scheduling on a different node than its volume.

### Troubleshooting Steps
1. **Check PVC Status:**
   ```bash
   kubectl get pvc -n <namespace>
   ```
2. **Verify Node Attachment:**
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```
3. **Unmount and Reattach the Volume:**
   ```bash
   kubectl delete pod <pod-name> -n <namespace>
   ```

---

## 7. RBAC Issues (`Forbidden Errors`)

### Scenario
A user or service account cannot perform an expected action in the cluster.

### Possible Causes
- Incorrect role or role binding.
- Missing permissions.

### Troubleshooting Steps
1. **Check User Permissions:**
   ```bash
   kubectl auth can-i get pods -n <namespace>
   ```
2. **View Role Bindings:**
   ```bash
   kubectl get rolebindings -A
   ```
3. **Review and Edit Role Configurations:**
   ```bash
   kubectl describe role <role-name> -n <namespace>
   ```
