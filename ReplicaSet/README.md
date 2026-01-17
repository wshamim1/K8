# ReplicaSets and Replication Controllers

This directory contains examples of Kubernetes ReplicaSets and ReplicationControllers for maintaining pod replicas.

## 📋 Overview

**ReplicaSet** ensures that a specified number of pod replicas are running at any given time. It's the next-generation ReplicationController with more expressive pod selectors.

**ReplicationController** is the older mechanism for ensuring pod availability (now superseded by ReplicaSets and Deployments).

## 📁 Files

- **ReplicaSetSample.yaml** - ReplicaSet configuration example
- **ReplicationControllerDemo.yaml** - ReplicationController configuration example

## 🚀 Usage

### ReplicaSet

#### Create ReplicaSet

```bash
# Apply ReplicaSet configuration
kubectl apply -f ReplicaSetSample.yaml

# Create ReplicaSet from command line
kubectl create -f - <<EOF
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:1.14
EOF
```

#### Manage ReplicaSets

```bash
# List ReplicaSets
kubectl get replicasets
kubectl get rs

# Get detailed information
kubectl describe replicaset <replicaset-name>

# View ReplicaSet YAML
kubectl get replicaset <replicaset-name> -o yaml

# Scale ReplicaSet
kubectl scale replicaset <replicaset-name> --replicas=5

# Delete ReplicaSet
kubectl delete replicaset <replicaset-name>

# Delete ReplicaSet but keep pods
kubectl delete replicaset <replicaset-name> --cascade=orphan
```

### ReplicationController

#### Create ReplicationController

```bash
# Apply ReplicationController configuration
kubectl apply -f ReplicationControllerDemo.yaml

# List ReplicationControllers
kubectl get replicationcontrollers
kubectl get rc

# Scale ReplicationController
kubectl scale rc <rc-name> --replicas=4
```

## 📝 ReplicaSet Configuration

### Basic ReplicaSet

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx-replicaset
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.19
        ports:
        - containerPort: 80
```

### ReplicaSet with Advanced Selectors

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: advanced-replicaset
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
    matchExpressions:
    - key: tier
      operator: In
      values:
      - frontend
      - backend
    - key: environment
      operator: NotIn
      values:
      - dev
  template:
    metadata:
      labels:
        app: myapp
        tier: frontend
        environment: prod
    spec:
      containers:
      - name: app
        image: myapp:1.0
```

## 📝 ReplicationController Configuration

### Basic ReplicationController

```yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name: nginx-rc
spec:
  replicas: 3
  selector:
    app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.19
        ports:
        - containerPort: 80
```

## 🔄 ReplicaSet vs ReplicationController

| Feature | ReplicaSet | ReplicationController |
|---------|-----------|----------------------|
| API Version | apps/v1 | v1 |
| Selector | Set-based (matchLabels, matchExpressions) | Equality-based only |
| Status | Current standard | Legacy (deprecated) |
| Used By | Deployments | Older workloads |
| Recommendation | ✅ Use this | ❌ Avoid for new workloads |

## 💡 Key Features

### ReplicaSet Features

1. **Self-Healing**: Automatically replaces failed pods
2. **Scaling**: Easy horizontal scaling
3. **Label Selectors**: Advanced pod selection
4. **Rolling Updates**: When used with Deployments
5. **Pod Template**: Defines pod specifications

### How It Works

1. ReplicaSet monitors pods matching its selector
2. If pod count < desired replicas, creates new pods
3. If pod count > desired replicas, deletes excess pods
4. Continuously maintains desired state

## 🎯 Use Cases

1. **High Availability**: Ensure multiple pod replicas
2. **Load Distribution**: Spread load across replicas
3. **Fault Tolerance**: Replace failed pods automatically
4. **Scaling**: Adjust capacity based on demand

## ⚠️ Important Notes

### When to Use

- **Use Deployments** instead of ReplicaSets directly (Deployments manage ReplicaSets)
- **Use ReplicaSets** only when you need custom update orchestration
- **Avoid ReplicationControllers** for new applications

### Limitations

- ReplicaSets don't support rolling updates directly (use Deployments)
- Changing pod template doesn't update existing pods
- No built-in rollback mechanism (use Deployments)

## 🔧 Common Operations

### Scaling

```bash
# Scale up
kubectl scale rs <replicaset-name> --replicas=10

# Scale down
kubectl scale rs <replicaset-name> --replicas=2

# Autoscale (requires metrics-server)
kubectl autoscale rs <replicaset-name> --min=2 --max=10 --cpu-percent=80
```

### Monitoring

```bash
# Watch ReplicaSet status
kubectl get rs --watch

# View events
kubectl describe rs <replicaset-name>

# Check pod status
kubectl get pods -l app=<label-value>

# View logs from all pods
kubectl logs -l app=<label-value> --all-containers=true
```

### Updating

```bash
# Update image (creates new pods)
kubectl set image rs/<replicaset-name> <container-name>=<new-image>

# Edit ReplicaSet
kubectl edit rs <replicaset-name>

# Note: Existing pods won't be updated automatically
# You need to delete old pods manually or use a Deployment
```

## 🔍 Troubleshooting

### Common Issues

1. **Pods Not Starting**
   ```bash
   kubectl describe rs <replicaset-name>
   kubectl describe pod <pod-name>
   kubectl logs <pod-name>
   ```

2. **Wrong Number of Replicas**
   ```bash
   kubectl get rs <replicaset-name>
   kubectl describe rs <replicaset-name>
   # Check for resource constraints or node issues
   ```

3. **Selector Mismatch**
   ```bash
   # Ensure pod labels match ReplicaSet selector
   kubectl get pods --show-labels
   ```

### Debug Commands

```bash
# Check ReplicaSet status
kubectl get rs <replicaset-name> -o wide

# View ReplicaSet events
kubectl get events --field-selector involvedObject.name=<replicaset-name>

# Check pod ownership
kubectl get pods -o jsonpath='{.items[*].metadata.ownerReferences[*].name}'

# Force delete stuck ReplicaSet
kubectl delete rs <replicaset-name> --grace-period=0 --force
```

## 📊 Best Practices

1. **Use Deployments**: Prefer Deployments over bare ReplicaSets
2. **Label Consistency**: Ensure pod labels match selector
3. **Resource Limits**: Define CPU and memory limits
4. **Health Checks**: Add liveness and readiness probes
5. **Meaningful Names**: Use descriptive names for ReplicaSets
6. **Version Tags**: Use specific image versions, not `latest`
7. **Monitoring**: Set up alerts for replica count mismatches

## 🔗 Related Resources

- [Deployments](../Deployments/) - Recommended over ReplicaSets
- [StatefulSets](../StatefulSets/) - For stateful applications
- [Services](../Services/) - Expose ReplicaSet pods
- [HPA](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) - Horizontal Pod Autoscaling

## 📚 References

- [Kubernetes ReplicaSet Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
- [ReplicationController Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/)
- [Deployments vs ReplicaSets](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)