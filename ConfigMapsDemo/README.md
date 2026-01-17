# ConfigMaps Demo

This directory contains examples of Kubernetes ConfigMaps for managing application configuration data.

## 📋 Overview

ConfigMaps allow you to decouple configuration artifacts from image content to keep containerized applications portable. They store non-confidential data in key-value pairs.

## 📁 Files

- **configmap.yml** - ConfigMap definition file
- **appdetails.properties** - Application configuration properties
- **uidetails.properties** - UI configuration properties

## 🚀 Usage

### Create ConfigMap from Properties Files

```bash
# Create ConfigMap from appdetails.properties
kubectl create configmap app-config --from-file=appdetails.properties

# Create ConfigMap from uidetails.properties
kubectl create configmap ui-config --from-file=uidetails.properties
```

### Apply ConfigMap from YAML

```bash
kubectl apply -f configmap.yml
```

### View ConfigMaps

```bash
# List all ConfigMaps
kubectl get configmaps

# Describe a specific ConfigMap
kubectl describe configmap <configmap-name>

# View ConfigMap data
kubectl get configmap <configmap-name> -o yaml
```

## 💡 Use Cases

1. **Environment Variables**: Inject configuration as environment variables
2. **Command-line Arguments**: Pass configuration as command arguments
3. **Configuration Files**: Mount ConfigMaps as files in volumes
4. **Application Settings**: Store application-specific settings

## 📝 Example: Using ConfigMap in a Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: configmap-demo-pod
spec:
  containers:
  - name: demo
    image: nginx
    env:
    - name: APP_CONFIG
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: app.property
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: ui-config
```

## ⚠️ Important Notes

- ConfigMaps are **not** suitable for sensitive data (use Secrets instead)
- Maximum size: 1MB per ConfigMap
- ConfigMaps must exist before Pods that reference them
- Changes to ConfigMaps don't automatically update running Pods (requires restart)

## 🔗 Related Resources

- [Secrets](../SecretsDemo/) - For sensitive configuration data
- [Deployments](../Deployments/) - For deploying applications with ConfigMaps

## 📚 References

- [Kubernetes ConfigMaps Documentation](https://kubernetes.io/docs/concepts/configuration/configmap/)