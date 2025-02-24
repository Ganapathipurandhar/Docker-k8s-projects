# Kubernetes Problems and Troubleshooting Guide

## K8s Troubleshooting Scenarios:

- Crashing/Pending Pods
- Case of the Missing Pods
- Schrödinger's Deployment
- Container Errors
- EnableServiceLinks
- Leaky Network Policies
- What the Ingress?
- Interns can see our secrets!
- Multi-attach Volume Errors

## Basic `kubectl` Commands for Troubleshooting

- describe
- logs
- explain
- exec
- port-forward
- top node
- diff
- auth-can-i
- get

---

# Kubernetes `kubectl` Commands Cheat Sheet

This document provides a comprehensive list of commonly used `kubectl` commands for managing Kubernetes clusters.

## `kubectl get` Command

```bash
alias k=kubectl
k get all                  # Shows all resources in the default namespace
k get all -A               # Shows all resources in all namespaces
k get ns                   # Lists all namespaces
k get -n uat deployment.apps  # Lists deployments in the `uat` namespace
k get -n uat deployment.apps notes-app-deployment -o yaml  # Gets YAML output for the deployment
k get -n uat deployment.apps notes-app-deployment -o=jsonpath='{.spec.replicas}'  # Extracts replica count
```

## `kubectl describe`

```bash
k get nodes                # Lists all nodes
k describe node node-name  # Provides detailed information about a node (CPU, memory, disk space, etc.)
k describe -n monitoring pod/grafana-68z58cd678-j456  # Provides pod details (readiness, liveness probes, events, etc.)
```

## `kubectl logs`

```bash
k logs -n <namespace-name> <pod-name>  # Shows logs for a specific pod
k logs -n <namespace-name> <pod-name> --all-containers  # Shows logs for all containers in a pod
k logs -n <namespace-name> <pod-name> -c <container-name>  # Shows logs for a specific container
k logs -n uat <pod-name> --timestamps  # Adds timestamps to logs
k logs -n uat <pod-name> --since=30s   # Shows logs from the last 30 seconds
k logs -n uat <pod-name> -f  # Follows logs dynamically (useful for debugging)
```

## `kubectl exec`

```bash
k exec -n dev nginx -- ls  # Executes a command (`ls`) in a running container
k exec -n dev nginx -it -- /bin/bash  # Opens an interactive shell in a container
```

## `kubectl port-forward`

```bash
k get svc -A  # Lists all services
k port-forward -n uat svc/notes-app-deployment 8000:80  # Forwards local port 8000 to the pod's port 80
curl localhost:8000  # Accesses the service locally
```

## `kubectl auth can-i`

```bash
k auth can-i list pods -n monitoring  # Checks if the user can list pods in the `monitoring` namespace
k auth whoami  # Shows the current user
k get role pod-reader -o yaml  # Shows details of a specific role
k get rolebindings  # Lists all role bindings
```

## `kubectl top`

```bash
k top nodes  # Shows resource usage for nodes
k top pods   # Shows resource usage for pods
```

## `kubectl explain`

```bash
k explain pod  # Explains the `pod` resource
k explain pod.spec.securityContext --recursive  # Explains the `securityContext` field recursively
```

## `kubectl diff`

```bash
cat redis.yaml
k apply -f redis.yaml
k diff -f redis.yaml  # Shows the differences between the current state and the desired state
```

# Kubectl Debug

## Why Use `kubectl debug`?

- **Minimize Pod Disruptions**: Avoid accidental disruptions in production environments by attaching another container to an existing container without causing disruptions.
- **Distroless Images**: 
  - These images do not have extra dependencies or packages.
  - Improve security by reducing the attack surface of the container.
  - Lightweight, making them faster.
- **Crashed Container**: Helps investigate a crashing container.

---

## `kubectl exec` Limitation

We cannot use the `exec` command on distroless images.

```sh
k get pods
k exec -it destro-debug-pod -- /bin/bash  # Throws error: internal error occurred
```

Instead, use `kubectl debug`:

```sh
k debug destroless-debug-pod -it --image=busybox  # Uses nettools image
```

**Note**: Resources used by the ephemeral container are shared by the entire pod.

---

## `--target` Option

You can use `--target` to specify the main container you want to debug.

```sh
k apply -f nginx.yaml  # Creates an Nginx container
k debug nginx-pod -it --image=busybox  # Running 'ps aux' inside will execute on busybox

k debug -it nginx-pod --image=busybox --target=nginx
# Now, running 'ps aux' will execute on nginx
```

You can navigate through other containers using the process filesystem:

```sh
cd /proc
cd 1
ls
cd root
ls
cd etc/nginx
cat nginx.config
```

---

## `--copy-to` Option

Create a new pod by combining the `busybox` container with `nginx-pod`:

```sh
k debug nginx-pod -it --image=busybox --copy-to=debugging-pod --share-processes
```

Now, list the pods:

```sh
k get pods  # You will see a new container
```

To describe the newly created pod:

```sh
k describe pod debugging-pod  # In this case, busybox is not an ephemeral container
```

**Note**: If a service is forwarding traffic to the pod, the new pod will not be owned by the deployment and will not share labels with the original pod, preventing unintended traffic.

