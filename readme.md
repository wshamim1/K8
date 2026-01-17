# Kubernetes (K8s) Learning Repository

A comprehensive collection of Kubernetes configuration files, examples, and demonstrations for learning and reference purposes.

## 📁 Repository Structure

### Core Concepts

- **[ConfigMapsDemo/](ConfigMapsDemo/)** - ConfigMap examples for application configuration management
- **[SecretsDemo/](SecretsDemo/)** - Secret management examples for sensitive data
- **[NameSpaces/](NameSpaces/)** - Namespace configuration and isolation examples
- **[Volumes/](Volumes/)** - Persistent storage configurations (PV, PVC)

### Workload Resources

- **[Deployments/](Deployments/)** - Deployment configurations for various applications (MySQL, Nginx, Redis)
- **[ReplicaSet/](ReplicaSet/)** - ReplicaSet and ReplicationController examples
- **[StatefulSets/](StatefulSets/)** - StatefulSet configurations for stateful applications
- **[Jobs/](Jobs/)** - Job and CronJob examples for batch processing

### Networking & Access

- **[Services/](Services/)** - Service types: ClusterIP, NodePort, and LoadBalancer
- **[rbac/](rbac/)** - Role-Based Access Control configurations

### Examples

- **[examples/](examples/)** - Real-world application examples
  - Flask Application
  - Kafka deployment
  - MySQL complete setup

### Tools

- **[kubectl/](kubectl/)** - kubectl command reference and cheat sheets
- **[cdrs/](cdrs/)** - Custom Resource Definitions

## 🚀 Getting Started

### Prerequisites

- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl CLI tool installed
- Basic understanding of containerization and Docker

### Quick Start

1. Clone this repository:
```bash
git clone <repository-url>
cd K8
```

2. Start with basic concepts:
```bash
# Create a namespace
kubectl apply -f NameSpaces/namespaces.yml

# Deploy a simple application
kubectl apply -f Deployments/nginx_deploymentwithServices.yaml
```

3. Explore each directory for specific examples and use cases

## 📚 Learning Path

1. **Basics**: Start with Namespaces and ConfigMaps
2. **Workloads**: Learn Deployments, ReplicaSets, and StatefulSets
3. **Storage**: Understand Volumes and Persistent Storage
4. **Networking**: Explore Services and their types
5. **Security**: Study Secrets and RBAC
6. **Advanced**: Jobs, CronJobs, and Custom Resources

## 🛠️ Common Commands

```bash
# Apply a configuration
kubectl apply -f <file.yaml>

# Get resources
kubectl get pods
kubectl get services
kubectl get deployments

# Describe a resource
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>

# Delete resources
kubectl delete -f <file.yaml>
```

## 📖 Documentation

Each subdirectory contains its own README.md with specific examples and explanations.

## 🤝 Contributing

Feel free to add more examples, improve documentation, or fix issues.

## 📝 License

This repository is for educational purposes.

## 🔗 Resources

- [Official Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes GitHub](https://github.com/kubernetes/kubernetes)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
