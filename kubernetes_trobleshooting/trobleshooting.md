# K8s Troubleshooting Scenarios:

- Crashing/Pending Pods
- Case of the Missing Pods
- Schrödinger's Deployment
- Container Errors
- EnableServiceLinks
- Leaky Network Policies
- What the Ingress?
- Interns can see our secrets!
- Multi-attach Volume Errors

### basic commands kubectl for trobleshooting
- describe
- logs
- explain
- exec
- port-forward
- top node
- diff
- auth-can-i
- get

# Kubernetes `kubectl` Commands Cheat Sheet

This document provides a comprehensive list of commonly used `kubectl` commands for managing Kubernetes clusters.

---

## `kubectl get` Command

```bash
alias k=kubectl
k get all                  # Shows all resources in the default namespace
k get all -A               # Shows all resources in all namespaces
k get ns                   # Lists all namespaces
k get -n uat deployment.apps  # Lists deployments in the `uat` namespace
k get -n uat deployment.apps notes-app-deployment -o yaml  # Gets YAML output for the deployment
k get -n uat deployment.apps notes-app-deployment -o yaml | grep replicas  # Filters YAML to show replicas

# JSON Output
k get -n uat deployment.apps notes-app-deployment -o=jsonpath='{.spec.replicas}'  # Extracts replica count
k get -n uat deployment.apps notes-app-deployment -o=jsonpath='{.spec.template.spec.containers}'  # Extracts container details

# kubectl describe
k get nodes                # Lists all nodes
k describe node node-name  # Provides detailed information about a node (CPU, memory, disk space, etc.)
k describe -n monitoring pod/grafana-68z58cd678-j456  # Provides pod details (readiness, liveness probes, events, etc.)

# kubectl get events
k get events -n monitoring  # Shows events in the `monitoring` namespace (types: Normal, Warning, etc.)
# kubectl logs
k logs -n <namespace-name> <pod-name>  # Shows logs for a specific pod
k logs -n <namespace-name> <pod-name> --all-containers  # Shows logs for all containers in a pod
k logs -n <namespace-name> <pod-name> -c <container-name>  # Shows logs for a specific container
k logs -n <namespace-name> <pod-name> --all-containers -o=jsonpath='{.spec.containers}' | jq  # Converts logs to JSON format

# Using Labels
k logs deployments.apps -n uat notes-app-deployment -o yaml | grep labels -A5  # Extracts labels from a deployment
k logs -n uat -l app=notes-app  # Shows logs for all pods with the label `app=notes-app`

# Timestamps and Time Range

k logs -n uat <pod-name> --timestamps  # Adds timestamps to logs
k logs -n uat <pod-name> --since=30s   # Shows logs from the last 30 # # seconds
# Follow Logs

k logs -n uat <pod-name> -f  # Follows logs dynamically (useful for debugging)
# kubectl exec

k exec -n dev nginx -- ls  # Executes a command (`ls`) in a running container
k exec -n dev nginx -it -- /bin/bash  # Opens an interactive shell in a container
# kubectl port-forward
Port-forwarding is useful for accessing internal cluster resources from your local network.

~~~
k get svc -A  # Lists all services
k port-forward -n uat svc/notes-app-deployment 8000:80  # Forwards local port 8000 to the pod's port 80
curl localhost:8000  # Accesses the service locally

k port-forward -n kubernetes-dashboard svc/kubernetes-dashboard-web 8000:8000  # Forwards the Kubernetes Dashboard
~~~
Access in browser: http://localhost:8000

# kubectl auth can-i
This command checks permissions under RBAC (Role-Based Access Control).

~~~
k auth can-i list pods -n monitoring  # Checks if the user can list pods in the `monitoring` namespace
k auth whoami  # Shows the current user
k get role pod-reader -o yaml  # Shows details of a specific role
k get rolebindings  # Lists all role bindings
k get rolebinding <name-of-rolebinding> -o yaml  # Shows details of a specific role binding
k auth can-i get pods --as=jane  # Checks if user `jane` can get pods
k auth can-i delete pods --as=jane  # Checks if user `jane` can delete pods
k auth can-i get pods --as=system:serviceaccount:default:default  # Checks if the default service account can get pods
k auth can-i delete pods --as=system:serviceaccount:default:default  # Checks if the default service account can delete pods
~~~

# Verbose Output
~~~
k auth can-i get pods --as=jane --v=10  # Provides detailed information about the permission check
~~~
# kubectl top
This command shows resource usage (CPU, memory) for nodes and pods. It requires the Metrics Server.
~~~
k top nodes  # Shows resource usage for nodes
k top pods   # Shows resource usage for pods
~~~
# kubectl explain
This command provides documentation for Kubernetes API resources.
~~~
k explain pod  # Explains the `pod` resource
k explain pod.spec.securityContext --recursive  # Explains the `securityContext` field recursively
~~~
# kubectl diff
This command verifies changes before applying them.
~~~
cat redis.yaml
k apply -f redis.yaml
# Accidentally change replicas from 2 to 3
k diff -f redis.yaml  # Shows the differences between the current state and the desired state
~~~
# kubectl debug
This command is used to debug pods without disrupting them, especially useful for distroless images.


k get pods  # Lists all pods
k debug <pod-name>  # Attaches a debug container to a running pod
# Debugging Distroless Images

k exec -it distroless-debug-pod -- /bin/bash  # This will fail for distroless images
k debug <pod-name> --image=busybox --target=<container-name>  # Attaches a debug container to a distroless pod
Save this file as kubectl-cheatsheet.md for easy reference!






