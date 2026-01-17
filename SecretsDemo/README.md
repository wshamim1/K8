# Secrets Demo

This directory contains examples of Kubernetes Secrets for managing sensitive information.

## 📋 Overview

Secrets are Kubernetes objects that store sensitive data such as passwords, OAuth tokens, SSH keys, and other confidential information. They help you avoid putting sensitive data directly in Pod specifications or container images.

## 📁 Files

- **SecretsDemo.yml** - Secret definition examples
- **mysql-secret.properties** - MySQL database credentials (example)
- **ui-secrets.properties** - UI application secrets (example)

## 🚀 Usage

### Create Secrets

#### From YAML File

```bash
# Apply secret configuration
kubectl apply -f SecretsDemo.yml
```

#### From Literal Values

```bash
# Create secret from literal values
kubectl create secret generic db-credentials \
  --from-literal=username=admin \
  --from-literal=password=secretpassword123

# Create secret with multiple key-value pairs
kubectl create secret generic app-secrets \
  --from-literal=api-key=abc123 \
  --from-literal=api-secret=xyz789
```

#### From Files

```bash
# Create secret from properties file
kubectl create secret generic mysql-secret \
  --from-file=mysql-secret.properties

# Create secret from multiple files
kubectl create secret generic ui-secrets \
  --from-file=ui-secrets.properties \
  --from-file=api-config.json

# Create secret from directory
kubectl create secret generic app-config --from-file=./config-dir/
```

#### From Environment File

```bash
# Create secret from .env file
kubectl create secret generic env-secrets --from-env-file=.env
```

### View Secrets

```bash
# List all secrets
kubectl get secrets

# Get secret details (values are base64 encoded)
kubectl get secret <secret-name> -o yaml

# Describe secret (doesn't show values)
kubectl describe secret <secret-name>

# Decode secret value
kubectl get secret <secret-name> -o jsonpath='{.data.password}' | base64 --decode
```

### Delete Secrets

```bash
# Delete a secret
kubectl delete secret <secret-name>

# Delete from file
kubectl delete -f SecretsDemo.yml
```

## 📝 Secret Types

### 1. Opaque (Generic)

Default type for arbitrary user-defined data.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  username: YWRtaW4=        # base64 encoded "admin"
  password: cGFzc3dvcmQ=    # base64 encoded "password"
```

### 2. Docker Registry

For storing Docker registry credentials.

```bash
kubectl create secret docker-registry regcred \
  --docker-server=<registry-server> \
  --docker-username=<username> \
  --docker-password=<password> \
  --docker-email=<email>
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: regcred
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-encoded-docker-config>
```

### 3. TLS

For storing TLS certificates and keys.

```bash
kubectl create secret tls tls-secret \
  --cert=path/to/cert.crt \
  --key=path/to/key.key
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-cert>
  tls.key: <base64-encoded-key>
```

### 4. Basic Authentication

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: basic-auth
type: kubernetes.io/basic-auth
stringData:
  username: admin
  password: secretpassword
```

### 5. SSH Authentication

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ssh-key
type: kubernetes.io/ssh-auth
data:
  ssh-privatekey: <base64-encoded-private-key>
```

## 💡 Using Secrets in Pods

### As Environment Variables

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-env-pod
spec:
  containers:
  - name: myapp
    image: myapp:1.0
    env:
    - name: DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: password
```

### As Volume Mounts

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-volume-pod
spec:
  containers:
  - name: myapp
    image: myapp:1.0
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: db-credentials
```

### All Keys as Environment Variables

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-envfrom-pod
spec:
  containers:
  - name: myapp
    image: myapp:1.0
    envFrom:
    - secretRef:
        name: db-credentials
```

## 🔐 Security Best Practices

1. **Enable Encryption at Rest**: Encrypt secrets in etcd
2. **Use RBAC**: Restrict access to secrets
3. **Avoid Logging**: Don't log secret values
4. **Rotate Regularly**: Update secrets periodically
5. **Use External Secret Managers**: Consider HashiCorp Vault, AWS Secrets Manager
6. **Limit Scope**: Use namespace-specific secrets
7. **Immutable Secrets**: Mark secrets as immutable when possible
8. **Audit Access**: Monitor secret access patterns

## 🔒 Immutable Secrets

Prevent accidental updates (Kubernetes 1.21+):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: immutable-secret
type: Opaque
immutable: true
data:
  key: dmFsdWU=
```

## 🛠️ Advanced Operations

### Update Secret

```bash
# Edit secret
kubectl edit secret <secret-name>

# Patch secret
kubectl patch secret <secret-name> -p '{"data":{"password":"bmV3cGFzc3dvcmQ="}}'

# Replace secret from file
kubectl create secret generic <secret-name> --from-file=config.json --dry-run=client -o yaml | kubectl apply -f -
```

### Base64 Encoding/Decoding

```bash
# Encode
echo -n "mypassword" | base64

# Decode
echo "bXlwYXNzd29yZA==" | base64 --decode
```

### Copy Secret to Another Namespace

```bash
kubectl get secret <secret-name> -n source-namespace -o yaml | \
  sed 's/namespace: source-namespace/namespace: target-namespace/' | \
  kubectl apply -f -
```

## ⚠️ Important Notes

- Secrets are **base64 encoded**, not encrypted by default
- Secrets are stored in etcd (enable encryption at rest)
- Maximum size: 1MB per secret
- Secrets are namespace-scoped
- Pods must exist in the same namespace as secrets
- Changes to secrets don't automatically update running pods
- Use `stringData` for plain text (automatically encoded)

## 🔍 Troubleshooting

### Common Issues

```bash
# Secret not found
kubectl get secrets -A | grep <secret-name>

# Check secret format
kubectl get secret <secret-name> -o yaml

# Verify base64 encoding
kubectl get secret <secret-name> -o jsonpath='{.data.key}' | base64 --decode

# Check pod events
kubectl describe pod <pod-name>

# Verify RBAC permissions
kubectl auth can-i get secrets
```

### Debug Commands

```bash
# List all secrets with details
kubectl get secrets -o wide

# Show secret keys (not values)
kubectl get secret <secret-name> -o jsonpath='{.data}'

# Check which pods use a secret
kubectl get pods -o json | jq '.items[] | select(.spec.volumes[]?.secret.secretName=="<secret-name>") | .metadata.name'
```

## 📊 Secret vs ConfigMap

| Feature | Secret | ConfigMap |
|---------|--------|-----------|
| Purpose | Sensitive data | Configuration data |
| Encoding | Base64 | Plain text |
| Size Limit | 1MB | 1MB |
| Encryption | Optional (at rest) | No |
| Use Case | Passwords, tokens | App settings |

## 🔗 Related Resources

- [ConfigMaps](../ConfigMapsDemo/) - For non-sensitive configuration
- [RBAC](../rbac/) - Access control for secrets
- [Deployments](../Deployments/) - Using secrets in deployments
- [Volumes](../Volumes/) - Mounting secrets as volumes

## 📚 References

- [Kubernetes Secrets Documentation](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Encrypting Secret Data at Rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/)
- [External Secrets Operator](https://external-secrets.io/)