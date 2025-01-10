# Multi-Cluster Deployment Using GitOps and Argo CD

multi-cluster deployment mechanisms with a focus on using GitOps practices and Argo CD. It compares traditional Continuous Deployment (CD) approaches, highlights their limitations, and explains how GitOps overcomes them. Additionally, it explores the hub-spoke and standalone models of Argo CD for managing Kubernetes clusters.

## Traditional vs. GitOps-Based CD Approaches

### Traditional (Legacy) CD

Traditional CD pipelines often utilize tools and scripts like:

Python scripts

Shell scripting 

Ansible

Jenkins plugins

These tools are used to deploy applications on Docker, Kubernetes, or other platforms. However, traditional methods have significant drawbacks:

Tracking Changes: Difficulty in tracking infrastructure or application changes.

Auditing: Limited auditing capabilities for deployments.

Auto-Healing: Lack of self-healing mechanisms.

Monitoring: Manual intervention for monitoring.

Reverting Changes: Complex rollback procedures.

### GitOps-Based CD

GitOps, with tools like Argo CD, addresses these drawbacks:

Centralized Source of Truth: Changes are tracked and audited via Git.

Automatic Syncing: Clusters sync automatically to the desired state defined in Git.

Self-Healing: If manual changes are made in clusters, Argo CD overrides them to match the Git state.

Improved Observability: Deployment state is visible in both Git and Argo CD dashboards.

### GitOps Workflow:

Git <--pull-- Argo CD --push--> Kubernetes Cluster

Multi-Cluster Deployment

Definition

In organizations, multiple Kubernetes clusters (e.g., dev, stage, QA, pre-prod, production, and feature-specific clusters) exist. Deploying a new application version across these clusters is referred to as multi-cluster deployment.

This mechanism often follows a hub-spoke model, where:

Hub: Centralized control.

Spokes: Individual clusters managed by the hub.

Benefits of Multi-Cluster Deployment

Environment Isolation: Different environments for testing, staging, and production.

Feature-Specific Clusters: Isolated clusters for specific features or teams.

Centralized Management: Simplifies deployment to multiple clusters.

Argo CD Deployment Models

### Argo CD supports two major deployment models:

1. Standalone Model

Each cluster has its own instance of Argo CD.

Advantages:

Dedicated Argo CD per cluster.

Independent cluster management.

Disadvantages:

Maintenance Overhead: Upgrades, configuration changes, or migrations must be done for each Argo CD instance.

Higher resource requirements for managing multiple Argo CD instances.

2. Hub-Spoke Model

A centralized Argo CD instance manages multiple clusters.

Advantages:

Easier to manage multiple clusters from a single location.

Suitable for organizations with centralized DevOps teams.

Disadvantages:

Resource Constraints: A single Argo CD instance manages multiple clusters, requiring adequate CPU, RAM, and other resources.

Potential Bottlenecks: Issues in the central instance can impact all managed clusters. Mitigated with high availability and dynamic sharding.

### Argo CD Features

Key Benefits

Automatic State Synchronization:

If any changes are manually made in a Kubernetes cluster, Argo CD automatically overrides them, ensuring that only Git-approved changes are applied.

Enhanced Observability:

Argo CD provides a visual dashboard to monitor and track deployments across all clusters.

Audit Trails:

All changes are logged in Git, ensuring complete traceability.

Scalability:

High availability configurations and sharding enable scaling for large infrastructures.

Declarative Configuration:

Deployments are defined in YAML/JSON files, stored in Git repositories.

### Best Practices for Multi-Cluster Deployment with Argo CD

Centralized Git Repository:

Maintain a single source of truth for all configurations.

Environment Segregation:

Use Git branches or folders to separate environments (e.g., dev, stage, prod).

Cluster Access Control:

Implement role-based access control (RBAC) to manage access to Argo CD and clusters.

Resource Monitoring:

Continuously monitor the resources of the centralized Argo CD instance in the hub-spoke model.

High Availability:

Enable high availability for critical clusters to avoid downtime.


-->Adopting GitOps and Argo CD for multi-cluster deployments streamlines the deployment process, enhances observability, and reduces manual intervention. Depending on organizational needs, you can choose between the standalone and hub-spoke models for Argo CD, ensuring scalability and efficiency in managing Kubernetes clusters.

-------------------------------------------------------------------------------------------------------------------------------------------------------------
# prerequisites

kubectl – A command line tool for working with Kubernetes clusters. For more information, see Installing or updating kubectl.
https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html

eksctl – A command line tool for working with EKS clusters that automates many individual tasks. For more information, see Installing or updating.
https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html

AWS CLI – A command line tool for working with AWS services, including Amazon EKS. For more information, see Installing, updating, and uninstalling the AWS CLI
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html in the AWS Command Line Interface User Guide. 

After installing the AWS CLI, I recommend that you also configure it. For more information, see Quick configuration with aws configure in the AWS Command Line Interface User Guide.
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config 

Argo CD CLI(Not the actual Argo CD Installation) - 
https://argo-cd.readthedocs.io/en/stable/cli_installation/#installation

## EKS Setup
### EKS Clusters Creation
eksctl create cluster --name hub-cluster --region us-west-1

eksctl create cluster --name spoke-cluster-1 --region us-west-1

eksctl create cluster --name spoke-cluster-2 --region us-west-1

### EKS Clusters Deletion
eksctl delete cluster --name hub-cluster --region us-west-1

eksctl delete cluster --name spoke-cluster-1 --region us-west-1

eksctl delete cluster --name spoke-cluster-2 --region us-west-1
________________________________________________________________________________________________________________________________________________
# Argo CD Setup

## Install Argo CD

```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## Run Argo CD in HTTP Mode(Insecure)

https://github.com/argoproj/argo-cd/blob/54f1572d46d8d611018f4854cf2f24a24a3ac088/docs/operator-manual/argocd-cmd-params-cm.yaml#L82

## Expose Argo CD Server Service in NodePort Mode

```
kubectl edit svc argocd-server -n argocd
```

and change the type to NodePort from ClusterIP


