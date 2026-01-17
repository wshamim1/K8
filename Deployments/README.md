# Deployments

This directory contains Kubernetes Deployment examples for various applications and services.

## 📋 Overview

Deployments provide declarative updates for Pods and ReplicaSets. They manage the deployment and scaling of a set of Pods and provide guarantees about the ordering and uniqueness of these Pods.

## 📁 Files

- **DeploymentDemo.yaml** - Basic deployment example
- **mysql_deploymentwithServices.yaml** - MySQL deployment with service configuration
- **nginx_deploymentwithServices.yaml** - Nginx deployment with service configuration
- **redisDeployment.yaml** - Redis deployment example

## 🚀 Usage

### Deploy an Application

```bash
# Deploy Nginx
kubectl apply -f nginx_deploymentwithServices.yaml

# Deploy MySQL
kubectl apply -f mysql_deploymentwithServices.yaml

# Deploy Redis
kubectl apply -f redisDeployment.yaml

# Deploy basic demo
kubectl apply -f DeploymentDemo.yaml
```

### Manage Deployments

```bash
# List all deployments
kubectl get deployments

# Get detailed information
kubectl describe deployment <deployment-name>

# Check rollout status
kubectl rollout status deployment/<deployment-name>

# View deployment history
kubectl rollout history deployment/<deployment-name>
```

### Scale Deployments

```bash
# Scale to specific number of replicas
kubectl scale deployment <deployment-name> --replicas=5

# Autoscale based on CPU
kubectl autoscale deployment <deployment-name> --min=2 --max=10 --cpu-percent=80
```

### Update Deployments

```bash
# Update image
kubectl set image deployment/<deployment-name> <container-name>=<new-image>

# Edit deployment
kubectl edit deployment <deployment-name>

# Apply changes from file
kubectl apply -f <deployment-file.yaml>
```

### Rollback Deployments

```bash
# Rollback to previous version
kubectl rollout undo deployment/<deployment-name>

# Rollback to specific revision
kubectl rollout undo deployment/<deployment-name> --to-revision=2

# Pause/Resume rollout
kubectl rollout pause deployment/<deployment-name>
kubectl rollout resume deployment/<deployment-name>
```

## 💡 Key Features

1. **Rolling Updates**: Update Pods gradually without downtime
2. **Rollback**: Revert to previous versions if issues occur
3. **Scaling**: Easily scale applications up or down
4. **Self-Healing**: Automatically replace failed Pods
5. **Declarative Updates**: Define desired state, Kubernetes handles the rest

## 📝 Deployment Structure

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app:1.0
        ports:
        - containerPort: 80
```

## 🔍 Examples in This Directory

### Nginx Deployment
- Web server deployment
- Includes LoadBalancer service
- Multiple replicas for high availability

### MySQL Deployment
- Database deployment
- Persistent storage configuration
- Service for database access

### Redis Deployment
- In-memory data store
- Cache layer deployment
- Fast data access configuration

## ⚠️ Best Practices

1. **Always specify resource limits** (CPU, memory)
2. **Use health checks** (liveness and readiness probes)
3. **Set appropriate replica counts** for high availability
4. **Use labels and selectors** consistently
5. **Version your container images** (avoid `latest` tag)
6. **Configure rolling update strategy** for zero-downtime deployments

## 🔗 Related Resources

- [Services](../Services/) - Expose deployments via services
- [ConfigMaps](../ConfigMapsDemo/) - Configuration management
- [Secrets](../SecretsDemo/) - Sensitive data management
- [Volumes](../Volumes/) - Persistent storage

## 📚 References

- [Kubernetes Deployments Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Deployment Strategies](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy)