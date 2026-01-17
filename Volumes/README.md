# Volumes

This directory contains examples of Kubernetes persistent storage configurations including PersistentVolumes (PV), PersistentVolumeClaims (PVC), and Pod volume usage.

## 📋 Overview

Kubernetes Volumes provide persistent storage for containers. Unlike container filesystems which are ephemeral, volumes persist data beyond the container lifecycle and can be shared between containers in a pod.

## 📁 Files

- **persistentVolume.yaml** - PersistentVolume (PV) definitions
- **persistentVolumeClaim.yaml** - PersistentVolumeClaim (PVC) definitions
- **pod_PVC.yaml** - Pod using PVC for storage

## 🚀 Usage

### Create Storage Resources

```bash
# Create PersistentVolume
kubectl apply -f persistentVolume.yaml

# Create PersistentVolumeClaim
kubectl apply -f persistentVolumeClaim.yaml

# Create Pod with PVC
kubectl apply -f pod_PVC.yaml
```

### Manage Volumes

```bash
# List PersistentVolumes
kubectl get pv

# List PersistentVolumeClaims
kubectl get pvc

# Describe PV
kubectl describe pv <pv-name>

# Describe PVC
kubectl describe pvc <pvc-name>

# Check PVC status
kubectl get pvc <pvc-name> -o wide
```

### Delete Resources

```bash
# Delete Pod (PVC remains)
kubectl delete pod <pod-name>

# Delete PVC
kubectl delete pvc <pvc-name>

# Delete PV
kubectl delete pv <pv-name>
```

## 📝 Storage Components

### 1. PersistentVolume (PV)

A piece of storage in the cluster provisioned by an administrator or dynamically using Storage Classes.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-example
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: standard
  hostPath:
    path: /mnt/data
```

### 2. PersistentVolumeClaim (PVC)

A request for storage by a user. Claims can request specific size and access modes.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-example
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
```

### 3. Pod Using PVC

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-pvc
spec:
  containers:
  - name: app
    image: nginx
    volumeMounts:
    - name: storage
      mountPath: /usr/share/nginx/html
  volumes:
  - name: storage
    persistentVolumeClaim:
      claimName: pvc-example
```

## 🔑 Access Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **ReadWriteOnce (RWO)** | Volume mounted as read-write by single node | Most common, databases |
| **ReadOnlyMany (ROX)** | Volume mounted as read-only by many nodes | Shared configuration |
| **ReadWriteMany (RWX)** | Volume mounted as read-write by many nodes | Shared storage, NFS |
| **ReadWriteOncePod (RWOP)** | Volume mounted as read-write by single pod | Kubernetes 1.22+ |

## 🔄 Reclaim Policies

Defines what happens to PV when PVC is deleted:

| Policy | Description |
|--------|-------------|
| **Retain** | Manual reclamation (data preserved) |
| **Delete** | PV and underlying storage deleted |
| **Recycle** | Basic scrub (deprecated) |

```yaml
spec:
  persistentVolumeReclaimPolicy: Retain  # or Delete
```

## 💾 Volume Types

### 1. EmptyDir

Temporary storage, deleted when pod is removed.

```yaml
volumes:
- name: cache
  emptyDir: {}
```

### 2. HostPath

Mounts file/directory from host node (not recommended for production).

```yaml
volumes:
- name: host-volume
  hostPath:
    path: /data
    type: Directory
```

### 3. NFS

Network File System storage.

```yaml
volumes:
- name: nfs-volume
  nfs:
    server: nfs-server.example.com
    path: /exported/path
```

### 4. ConfigMap

Mount ConfigMap as volume.

```yaml
volumes:
- name: config
  configMap:
    name: app-config
```

### 5. Secret

Mount Secret as volume.

```yaml
volumes:
- name: secret
  secret:
    secretName: app-secret
```

### 6. Cloud Provider Volumes

#### AWS EBS

```yaml
volumes:
- name: aws-ebs
  awsElasticBlockStore:
    volumeID: vol-12345678
    fsType: ext4
```

#### GCE Persistent Disk

```yaml
volumes:
- name: gce-pd
  gcePersistentDisk:
    pdName: my-disk
    fsType: ext4
```

#### Azure Disk

```yaml
volumes:
- name: azure-disk
  azureDisk:
    diskName: myDisk
    diskURI: /subscriptions/.../myDisk
```

## 🏗️ Storage Classes

Dynamic provisioning of PersistentVolumes.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-storage
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iopsPerGB: "10"
  encrypted: "true"
reclaimPolicy: Delete
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

### Use StorageClass in PVC

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast-storage
  resources:
    requests:
      storage: 20Gi
```

## 📊 Volume Lifecycle

1. **Provisioning**: PV created (static or dynamic)
2. **Binding**: PVC bound to PV
3. **Using**: Pod mounts PVC
4. **Releasing**: PVC deleted
5. **Reclaiming**: PV reclaimed based on policy

## 💡 Common Patterns

### Database with Persistent Storage

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
  storageClassName: standard
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
spec:
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: password
        volumeMounts:
        - name: mysql-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-storage
        persistentVolumeClaim:
          claimName: mysql-pvc
```

### Shared Storage Between Pods

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: shared-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
  storageClassName: nfs
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx
        volumeMounts:
        - name: shared-data
          mountPath: /usr/share/nginx/html
      volumes:
      - name: shared-data
        persistentVolumeClaim:
          claimName: shared-pvc
```

### Multiple Volumes in Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-volume-pod
spec:
  containers:
  - name: app
    image: myapp
    volumeMounts:
    - name: data
      mountPath: /data
    - name: config
      mountPath: /config
    - name: cache
      mountPath: /cache
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: data-pvc
  - name: config
    configMap:
      name: app-config
  - name: cache
    emptyDir: {}
```

## 🔧 Volume Expansion

Expand existing PVC (requires StorageClass with `allowVolumeExpansion: true`):

```bash
# Edit PVC to increase size
kubectl edit pvc <pvc-name>

# Or patch PVC
kubectl patch pvc <pvc-name> -p '{"spec":{"resources":{"requests":{"storage":"50Gi"}}}}'

# Check expansion status
kubectl describe pvc <pvc-name>
```

## 🔍 Troubleshooting

### PVC Pending

```bash
# Check PVC status
kubectl describe pvc <pvc-name>

# Check available PVs
kubectl get pv

# Check StorageClass
kubectl get storageclass

# View events
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Pod Can't Mount Volume

```bash
# Check pod events
kubectl describe pod <pod-name>

# Verify PVC is bound
kubectl get pvc

# Check node where pod is scheduled
kubectl get pod <pod-name> -o wide

# Check volume attachment
kubectl get volumeattachment
```

### Storage Full

```bash
# Check PVC usage (requires metrics-server)
kubectl top pods

# Exec into pod to check disk usage
kubectl exec -it <pod-name> -- df -h

# Check PV capacity
kubectl get pv <pv-name> -o yaml
```

### Permission Issues

```bash
# Check pod security context
kubectl get pod <pod-name> -o yaml | grep -A 10 securityContext

# Verify volume permissions
kubectl exec -it <pod-name> -- ls -la /mount/path
```

## ⚠️ Best Practices

1. **Use StorageClasses**: Enable dynamic provisioning
2. **Set Resource Requests**: Specify storage requirements
3. **Choose Correct Access Mode**: Match your use case
4. **Plan for Backups**: Regular backup strategy
5. **Monitor Usage**: Track storage consumption
6. **Set Reclaim Policy**: Understand data retention
7. **Use Labels**: Organize PVs and PVCs
8. **Security**: Set appropriate permissions
9. **Performance**: Choose right storage type
10. **Cost Management**: Monitor cloud storage costs

## 📈 Monitoring

```bash
# Check PV status
kubectl get pv -o wide

# Check PVC status
kubectl get pvc -o wide

# View storage capacity
kubectl get pv -o custom-columns=NAME:.metadata.name,CAPACITY:.spec.capacity.storage,STATUS:.status.phase

# Check volume usage (requires metrics-server)
kubectl top pods

# View PV/PVC events
kubectl get events --field-selector involvedObject.kind=PersistentVolume
kubectl get events --field-selector involvedObject.kind=PersistentVolumeClaim
```

## 🔐 Security Considerations

### Volume Security Context

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    fsGroup: 2000
    runAsUser: 1000
    runAsNonRoot: true
  containers:
  - name: app
    image: myapp
    volumeMounts:
    - name: data
      mountPath: /data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: secure-pvc
```

## 🔗 Related Resources

- [StatefulSets](../StatefulSets/) - Stateful applications with persistent storage
- [Deployments](../Deployments/) - Deploying applications with volumes
- [ConfigMaps](../ConfigMapsDemo/) - Configuration as volumes
- [Secrets](../SecretsDemo/) - Sensitive data as volumes

## 📚 References

- [Kubernetes Volumes Documentation](https://kubernetes.io/docs/concepts/storage/volumes/)
- [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
- [Dynamic Volume Provisioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/)