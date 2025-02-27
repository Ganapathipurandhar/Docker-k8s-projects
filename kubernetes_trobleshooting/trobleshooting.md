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

# Create the markdown content as a string
markdown_content = """
# Exit Codes and Their Meanings

| **Exit Code** | **Reason**                                                                 | **Range**    |
|---------------|-----------------------------------------------------------------------------|--------------|
| **0**         | Successful execution. The program has completed its task without errors.    | Success      |
| **1**         | General error. The command failed, but no specific reason is provided.       | Error        |
| **2**         | Misuse of shell built-ins or syntax error.                                  | Error        |
| **126**       | Command invoked cannot execute (e.g., missing execute permissions).         | Error        |
| **127**       | Command not found. The shell cannot find the command in the PATH.           | Error        |
| **128**       | Invalid argument to exit.                                                   | Error        |
| **130**       | Script terminated by Control-C (SIGINT).                                    | Error        |
| **137**       | Process terminated by signal 9 (SIGKILL).                                  | Error        |
| **139**       | Segmentation fault (SIGSEGV).                                               | Error        |
| **200**       | OK. The operation completed successfully with some non-fatal issues.        | Success      |
| **201**       | Partial success. Some tasks completed, but others did not.                  | Warning      |
| **202**       | Task completed with warnings.                                               | Warning      |
| **300**       | Resource unavailable. Typically used for unavailable service or network.   | Warning/Error|
| **301**       | Invalid user input. The provided input was not in the expected format.      | Error        |
| **302**       | Command timed out due to network or resource issues.                        | Error        |
| **400**       | Client-side error (bad request). The client made a request that the server could not process due to an error in the request. | Error        |
| **401**       | Unauthorized access. The operation requires authentication.                | Error        |
| **402**       | Payment required. Typically used for subscription-based services.          | Error        |
| **403**       | Forbidden. The server understands the request but refuses to authorize it. | Error        |
| **404**       | Not found. The requested resource could not be found on the server.         | Error        |
| **405**       | Method not allowed. The HTTP method used is not allowed for the requested resource. | Error        |
| **500**       | Internal server error. The server encountered an unexpected condition.     | Error        |
| **501**       | Not implemented. The server does not support the functionality required to fulfill the request. | Error        |
| **502**       | Bad gateway. The server received an invalid response from the upstream server. | Error        |
| **503**       | Service unavailable. The server is currently unavailable, typically due to being overloaded. | Error        |
| **504**       | Gateway timeout. The server did not receive a timely response from an upstream server. | Error        |
| **505**       | HTTP version not supported. The server does not support the HTTP protocol version used in the request. | Error        |
"""

# Save it as a markdown file
file_path = "/mnt/data/exit_codes.md"
with open(file_path, "w") as file:
    file.write(markdown_content)

file_path


