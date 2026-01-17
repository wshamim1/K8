# Namespaces

This directory contains Kubernetes Namespace configuration examples.

## 📋 Overview

Namespaces provide a mechanism for isolating groups of resources within a single cluster. They are intended for use in environments with many users spread across multiple teams or projects.

## 📁 Files

- **namespaces.yml** - Namespace definition examples

## 🚀 Usage

### Create Namespaces

```bash
# Apply namespace configuration
kubectl apply -f namespaces.yml

# Create namespace from command line
kubectl create namespace my-namespace

# Create namespace with labels
kubectl create namespace my-namespace --labels=env=dev,team=backend
```

### List Namespaces

```bash
# List all namespaces
kubectl get namespaces

# List with labels
kubectl get namespaces --show-labels

# Describe a namespace
kubectl describe namespace <namespace-name>
```

### Work with Namespaces

```bash
# Set default namespace for current context
kubectl config set-context --current --namespace=<namespace-name>

# View current namespace
kubectl config view --minify | grep namespace:

# Deploy resources to specific namespace
kubectl apply -f deployment.yaml -n <namespace-name>

# Get resources from specific namespace
kubectl get pods -n <namespace-name>

# Get resources from all namespaces
kubectl get pods --all-namespaces
# or
kubectl get pods -A
```

### Delete Namespaces

```bash
# Delete a namespace (deletes all resources within it)
kubectl delete namespace <namespace-name>

# Delete namespace from file
kubectl delete -f namespaces.yml
```

## 📝 Namespace Configuration

### Basic Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: development
  labels:
    environment: dev
    team: engineering
```

### Namespace with Resource Quotas

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: prod-quota
  namespace: production
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "50"
```

### Namespace with Limit Range

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: resource-limits
  namespace: production
spec:
  limits:
  - max:
      cpu: "2"
      memory: 4Gi
    min:
      cpu: "100m"
      memory: 128Mi
    default:
      cpu: "500m"
      memory: 512Mi
    defaultRequest:
      cpu: "200m"
      memory: 256Mi
    type: Container
```

## 💡 Use Cases

1. **Environment Separation**: dev, staging, production
2. **Team Isolation**: team-a, team-b, team-c
3. **Project Organization**: project-x, project-y
4. **Multi-tenancy**: customer-1, customer-2
5. **Resource Management**: Apply quotas and limits per namespace

## 🏷️ Default Namespaces

Kubernetes starts with four initial namespaces:

- **default**: Default namespace for objects with no other namespace
- **kube-system**: Namespace for objects created by Kubernetes system
- **kube-public**: Readable by all users, reserved for cluster usage
- **kube-node-lease**: Namespace for node lease objects

## 🔧 Resource Quotas

Limit resource consumption per namespace:

```bash
# Create resource quota
kubectl create quota my-quota \
  --hard=cpu=2,memory=4Gi,pods=10 \
  -n my-namespace

# View quotas
kubectl get resourcequota -n my-namespace

# Describe quota
kubectl describe resourcequota my-quota -n my-namespace
```

## 🎯 Network Policies

Isolate network traffic between namespaces:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-from-other-namespaces
  namespace: production
spec:
  podSelector:
    matchLabels: {}
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector: {}
```

## ⚠️ Best Practices

1. **Use Meaningful Names**: Choose descriptive namespace names
2. **Apply Resource Quotas**: Prevent resource exhaustion
3. **Set Limit Ranges**: Define default resource limits
4. **Use Labels**: Organize and filter namespaces
5. **Avoid Default Namespace**: Use specific namespaces for applications
6. **Document Purpose**: Add annotations describing namespace purpose
7. **RBAC Integration**: Combine with Role-Based Access Control
8. **Network Policies**: Implement network isolation when needed

## 🔍 Common Patterns

### Development Environment

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dev
  labels:
    environment: development
    cost-center: engineering
  annotations:
    description: "Development environment for testing"
```

### Production Environment

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: prod
  labels:
    environment: production
    cost-center: operations
  annotations:
    description: "Production environment - handle with care"
    contact: "ops-team@company.com"
```

## 🚫 Limitations

- Not all objects are in a namespace (e.g., nodes, persistentVolumes)
- Namespace names must be DNS-compatible
- Cannot nest namespaces
- Deleting a namespace deletes all resources within it

## 📊 Monitoring Namespaces

```bash
# View resource usage by namespace
kubectl top pods -n <namespace-name>

# View all resources in a namespace
kubectl get all -n <namespace-name>

# View events in a namespace
kubectl get events -n <namespace-name> --sort-by='.lastTimestamp'

# Count resources per namespace
kubectl get pods --all-namespaces | awk '{print $1}' | sort | uniq -c
```

## 🔗 Related Resources

- [RBAC](../rbac/) - Role-Based Access Control for namespaces
- [ConfigMaps](../ConfigMapsDemo/) - Namespace-scoped configuration
- [Secrets](../SecretsDemo/) - Namespace-scoped secrets
- [Services](../Services/) - Namespace-scoped services

## 📚 References

- [Kubernetes Namespaces Documentation](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
- [Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
- [Limit Ranges](https://kubernetes.io/docs/concepts/policy/limit-range/)