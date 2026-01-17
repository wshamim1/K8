# StatefulSets

This directory contains examples of Kubernetes StatefulSets for managing stateful applications.

## 📋 Overview

StatefulSet is a workload API object used to manage stateful applications. Unlike Deployments, StatefulSets maintain a sticky identity for each Pod, making them ideal for applications that require stable network identifiers, persistent storage, and ordered deployment/scaling.

## 📁 Files

- **statefulsets.yaml** - StatefulSet configuration example

## 🚀 Usage

### Create StatefulSet

```bash
# Apply StatefulSet configuration
kubectl apply -f statefulsets.yaml

# Create StatefulSet from command line
kubectl create -f - <<EOF
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: "nginx"
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
EOF
```

### Manage StatefulSets

```bash
# List StatefulSets
kubectl get statefulsets
kubectl get sts

# Get detailed information
kubectl describe statefulset <statefulset-name>

# View StatefulSet status
kubectl get statefulset <statefulset-name> -o wide

# Watch StatefulSet
kubectl get statefulset --watch
```

### Scale StatefulSets

```bash
# Scale up
kubectl scale statefulset <statefulset-name> --replicas=5

# Scale down
kubectl scale statefulset <statefulset-name> --replicas=2

# Edit replicas
kubectl edit statefulset <statefulset-name>
```

### Update StatefulSets

```bash
# Update image
kubectl set image statefulset/<statefulset-name> <container-name>=<new-image>

# Edit StatefulSet
kubectl edit statefulset <statefulset-name>

# Apply changes from file
kubectl apply -f statefulsets.yaml

# Check rollout status
kubectl rollout status statefulset/<statefulset-name>
```

### Delete StatefulSets

```bash
# Delete StatefulSet (keeps PVCs)
kubectl delete statefulset <statefulset-name>

# Delete StatefulSet and PVCs
kubectl delete statefulset <statefulset-name>
kubectl delete pvc -l app=<label>

# Delete without cascading (keeps pods)
kubectl delete statefulset <statefulset-name> --cascade=orphan
```

## 📝 StatefulSet Configuration

### Basic StatefulSet

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: "nginx"
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
          name: web
```

### StatefulSet with Persistent Storage

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None
  selector:
    app: nginx
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: "nginx"
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
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
```

### StatefulSet with Init Containers

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
spec:
  serviceName: mysql
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      initContainers:
      - name: init-mysql
        image: mysql:5.7
        command:
        - bash
        - "-c"
        - |
          set -ex
          # Generate mysql server-id from pod ordinal index
          [[ `hostname` =~ -([0-9]+)$ ]] || exit 1
          ordinal=${BASH_REMATCH[1]}
          echo [mysqld] > /mnt/conf.d/server-id.cnf
          echo server-id=$((100 + $ordinal)) >> /mnt/conf.d/server-id.cnf
        volumeMounts:
        - name: conf
          mountPath: /mnt/conf.d
      containers:
      - name: mysql
        image: mysql:5.7
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: "password"
        ports:
        - containerPort: 3306
          name: mysql
        volumeMounts:
        - name: data
          mountPath: /var/lib/mysql
        - name: conf
          mountPath: /etc/mysql/conf.d
      volumes:
      - name: conf
        emptyDir: {}
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
```

## 🎯 Key Features

### 1. Stable Network Identity

Each pod gets a persistent hostname:
- `<statefulset-name>-0`
- `<statefulset-name>-1`
- `<statefulset-name>-2`

DNS entries:
- `<pod-name>.<service-name>.<namespace>.svc.cluster.local`

### 2. Ordered Deployment and Scaling

- Pods are created sequentially (0, 1, 2, ...)
- Each pod must be Running and Ready before next is created
- Scaling down happens in reverse order (2, 1, 0, ...)

### 3. Stable Persistent Storage

- Each pod gets its own PersistentVolumeClaim
- PVCs persist even if pod is deleted
- Same PVC is reattached when pod is recreated

### 4. Ordered Updates

- Updates happen in reverse ordinal order
- Each pod must be updated and ready before next

## 💡 Use Cases

1. **Databases**: MySQL, PostgreSQL, MongoDB
2. **Distributed Systems**: Kafka, ZooKeeper, Elasticsearch
3. **Stateful Applications**: Redis clusters, Cassandra
4. **Message Queues**: RabbitMQ clusters
5. **Any application requiring**:
   - Stable network identifiers
   - Persistent storage
   - Ordered deployment/scaling

## 🔧 Update Strategies

### RollingUpdate (Default)

```yaml
spec:
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      partition: 0  # Update pods with ordinal >= partition
```

### OnDelete

```yaml
spec:
  updateStrategy:
    type: OnDelete  # Manual pod deletion required for updates
```

## 🔄 Pod Management Policies

### OrderedReady (Default)

Pods are created/deleted in order, waiting for each to be ready.

```yaml
spec:
  podManagementPolicy: OrderedReady
```

### Parallel

Pods are created/deleted in parallel (faster but less controlled).

```yaml
spec:
  podManagementPolicy: Parallel
```

## 📊 StatefulSet vs Deployment

| Feature | StatefulSet | Deployment |
|---------|-------------|------------|
| Pod Identity | Stable, unique | Random |
| Pod Names | Predictable (web-0, web-1) | Random hash |
| Storage | Persistent per pod | Shared or ephemeral |
| Scaling | Ordered | Parallel |
| Updates | Ordered | Rolling |
| Use Case | Stateful apps | Stateless apps |
| DNS | Stable per pod | Service-level only |

## ⚠️ Important Considerations

1. **Headless Service Required**: StatefulSets need a headless service (clusterIP: None)
2. **PVC Deletion**: PVCs are not automatically deleted when StatefulSet is deleted
3. **Ordered Operations**: Scaling and updates are sequential (can be slow)
4. **Storage Class**: Ensure appropriate StorageClass is available
5. **Pod Disruption Budget**: Consider setting PDB for production
6. **Backup Strategy**: Plan for data backup and recovery

## 🛠️ Advanced Operations

### Access Individual Pods

```bash
# Access specific pod
kubectl exec -it <statefulset-name>-0 -- /bin/bash

# Access via DNS
kubectl run -it --rm debug --image=busybox --restart=Never -- \
  nslookup <statefulset-name>-0.<service-name>
```

### Partition Updates

Update only pods with ordinal >= partition:

```bash
kubectl patch statefulset <statefulset-name> -p \
  '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":2}}}}'
```

### Force Delete Stuck Pod

```bash
# Delete pod forcefully
kubectl delete pod <pod-name> --grace-period=0 --force

# StatefulSet will recreate it
```

### Manual PVC Management

```bash
# List PVCs for StatefulSet
kubectl get pvc -l app=<label>

# Delete specific PVC
kubectl delete pvc <pvc-name>

# Backup PVC data before deletion
```

## 🔍 Troubleshooting

### Pod Not Starting

```bash
# Check pod status
kubectl get pods -l app=<label>

# Describe pod
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp

# Check PVC status
kubectl get pvc
```

### PVC Issues

```bash
# Check PVC status
kubectl get pvc

# Describe PVC
kubectl describe pvc <pvc-name>

# Check PV
kubectl get pv

# Verify StorageClass
kubectl get storageclass
```

### Scaling Issues

```bash
# Check StatefulSet status
kubectl describe statefulset <statefulset-name>

# View pod conditions
kubectl get pods -o wide

# Check resource availability
kubectl describe nodes
```

### Update Stuck

```bash
# Check rollout status
kubectl rollout status statefulset/<statefulset-name>

# View update history
kubectl rollout history statefulset/<statefulset-name>

# Rollback if needed
kubectl rollout undo statefulset/<statefulset-name>
```

## 📈 Monitoring

```bash
# Watch StatefulSet status
kubectl get statefulset --watch

# Monitor pods
kubectl get pods -l app=<label> --watch

# Check resource usage
kubectl top pods -l app=<label>

# View logs from all pods
kubectl logs -l app=<label> --all-containers=true --tail=100
```

## 🔐 Best Practices

1. **Use Headless Service**: Always create a headless service
2. **Set Resource Limits**: Define CPU and memory limits
3. **Configure Health Checks**: Add liveness and readiness probes
4. **Plan Storage**: Choose appropriate storage class and size
5. **Pod Disruption Budget**: Protect against voluntary disruptions
6. **Backup Strategy**: Regular backups of persistent data
7. **Monitoring**: Track pod and storage metrics
8. **Testing**: Test scaling and updates in non-production first
9. **Documentation**: Document pod roles and dependencies
10. **Security**: Use RBAC and network policies

## 🔗 Related Resources

- [Volumes](../Volumes/) - Persistent storage configuration
- [Services](../Services/) - Headless service setup
- [Deployments](../Deployments/) - For stateless applications
- [PersistentVolumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)

## 📚 References

- [Kubernetes StatefulSets Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
- [StatefulSet Basics Tutorial](https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/)
- [Run Replicated Stateful Application](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/)