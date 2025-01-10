# Argo CD Setup 

## Core Components
### Application Controller

Handles **reconciliation**.Ensures the desired state in Git matches the actual state in the Kubernetes cluster.
### Repo Server

Interacts with Git repositories.Fetches manifests or Helm charts and provides them to the Application Controller.
### Redis

Acts as a cache to improve performance.Maintains the state of running processes.
### Server Component

Provides the Argo CD UI and API for CLI interactions.Manages user access and application views.

### Notification Controller

Sends alerts about application events (e.g., sync failures, successful deployments).
Works with tools like Slack, email, or Microsoft Teams.
Configurable to trigger notifications for specific events.
### ApplicationSet Controller

Creates and manages multiple applications automatically.
Uses templates and parameters for flexibility.
Ideal for deploying applications across multiple clusters or environments like dev, staging, and production.
### Dex (Authentication Provider)

Manages secure login for the Argo CD UI and CLI.
Supports integration with various identity providers such as:
LDAP
SAML
OIDC (e.g., Google or Okta)
GitHub
Provides Single Sign-On (SSO) capabilities.

## Installation Steps

### Using Kubernetes Manifest

Create a namespace for Argo CD:
~~~

kubectl create namespace argocd
~~~

Install Argo CD using the official manifest:
~~~

kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
~~~

### Using Helm Chart

Add the Argo CD Helm repository:
~~~
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
~~~
Create a namespace for Argo CD:
~~~
kubectl create namespace argocd
~~~
Install Argo CD using Helm:
~~~
helm install argocd argo/argo-cd -n argocd
~~~
## Exposing Argo CD Service

By default, the Argo CD server service is set to ClusterIP. To access it externally, you can change it to NodePort:

Edit the Argo CD server service:
~~~
kubectl edit svc argocd-server -n argocd
~~~
Change the type from ClusterIP to NodePort and save the changes.

To find the NodePort assigned, run:
~~~
kubectl get svc argocd-server -n argocd

Access the service using http://<NodeIP>:<NodePort>.
~~~
### Retrieving Argo CD Admin Password

Get the initial admin password:
~~~
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 --decode
~~~
The username is **admin**.

## Accessing the Argo CD UI

Open your browser and navigate to http://<NodeIP>:<NodePort>.

Log in using the username (admin) and the password retrieved in the previous step.

After logging in, you can create and manage applications directly from the UI.

Click New Application.

Fill in the required fields (e.g., application name, source repository, destination cluster/namespace).

Click Create to deploy your application.

## Using the CLI

Logging in

Install the Argo CD CLI: Download Instructions

Log in to Argo CD:
~~~
argocd login <ARGOCD_SERVER>
~~~
Replace <ARGOCD_SERVER> with the Argo CD server URL or IP.

Provide the username (admin) and the password.

Creating an Application

# Create an application using the CLI:
~~~
argocd app create <APP_NAME> \
--repo <REPO_URL> \
--path <APP_PATH> \
--dest-server <DEST_SERVER> \
--dest-namespace <NAMESPACE>
~~~
Replace placeholders with appropriate values:

<APP_NAME>: Name of the application.

<REPO_URL>: Git repository URL.

<APP_PATH>: Path to the application manifests in the repository.

<DEST_SERVER>: Kubernetes API server address.

<NAMESPACE>: Target namespace.

Viewing Applications

List all applications:
~~~
argocd app list
~~~
Syncing Applications

To synchronize an application (deploy changes):
~~~
argocd app sync <APP_NAME>
~~~
Checking Application Status

Get the status of an application:
~~~
argocd app get <APP_NAME>
~~~
## Reference Repositories and Documentation

Argo CD GitHub Repository: https://github.com/argoproj/argo-cd

Official Documentation: https://argo-cd.readthedocs.io/en/stable/

Helm Chart Documentation: https://github.com/argoproj/argo-helm

Argo CD CLI Commands: https://argo-cd.readthedocs.io/en/stable/cli/

acheivement --> reconciliation, it is not opinionated (Plain Kubernetes manifests,Helm charts,Customize templates etc) 
because each company will follow on owm farmat like helm , Customize etc
### Troubleshooting Tips

If the pods take time to initialize, check resource allocation on your cluster.

Use kubectl get pods -n argocd to monitor pod statuses.

For UI access issues, verify service type and tunneling configuration.

Base64 decode secrets using: echo <base64_secret> | base64 --decode.

