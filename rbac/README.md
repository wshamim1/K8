# RBAC (Role-Based Access Control)

This directory contains Kubernetes RBAC configuration examples for managing access control and permissions.

## 📋 Overview

RBAC (Role-Based Access Control) is a method of regulating access to computer or network resources based on the roles of individual users within an organization. In Kubernetes, RBAC uses the `rbac.authorization.k8s.io` API group to drive authorization decisions.

## 📁 Files

- **rbac.yaml** - RBAC configuration examples
- **roles.yaml** - Role and RoleBinding definitions

## 🚀 Usage

### Apply RBAC Configurations

```bash
# Apply RBAC configuration
kubectl apply -f rbac.yaml

# Apply roles configuration
kubectl apply -f roles.yaml
```

### View RBAC Resources

```bash
# List roles
kubectl get roles
kubectl get roles -A

# List cluster roles
kubectl get clusterroles

# List role bindings
kubectl get rolebindings
kubectl get rolebindings -A

# List cluster role bindings
kubectl get clusterrolebindings

# Describe a role
kubectl describe role <role-name> -n <namespace>

# Describe a cluster role
kubectl describe clusterrole <clusterrole-name>
```

### Check Permissions

```bash
# Check if you can perform an action
kubectl auth can-i create pods
kubectl auth can-i delete deployments --namespace=production

# Check permissions for another user
kubectl auth can-i list secrets --as=john@example.com

# Check all permissions for a user
kubectl auth can-i --list --as=john@example.com
```

## 📝 RBAC Components

### 1. Role (Namespace-scoped)

Defines permissions within a specific namespace.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

### 2. ClusterRole (Cluster-wide)

Defines permissions across the entire cluster.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "watch", "list"]
```

### 3. RoleBinding (Namespace-scoped)

Grants permissions defined in a Role to users or service accounts within a namespace.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: jane@example.com
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### 4. ClusterRoleBinding (Cluster-wide)

Grants permissions defined in a ClusterRole across the entire cluster.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: read-secrets-global
subjects:
- kind: Group
  name: manager
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

## 🎯 Common Verbs

- **get**: Read a specific resource
- **list**: List resources
- **watch**: Watch for changes
- **create**: Create new resources
- **update**: Update existing resources
- **patch**: Partially update resources
- **delete**: Delete resources
- **deletecollection**: Delete multiple resources

## 👥 Subject Types

1. **User**: Individual user accounts
2. **Group**: User groups
3. **ServiceAccount**: Service accounts for pods

## 📚 Common Use Cases

### Read-Only Access

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: viewer
rules:
- apiGroups: ["", "apps", "batch"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
```

### Developer Access

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: development
  name: developer
rules:
- apiGroups: ["", "apps", "batch"]
  resources: ["pods", "deployments", "services", "configmaps"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
```

### Admin Access (Namespace)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: namespace-admin
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]
```

### Service Account for Pods

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-service-account
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
  namespace: default
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-rolebinding
  namespace: default
subjects:
- kind: ServiceAccount
  name: app-service-account
  namespace: default
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io
```

## 🔐 Security Best Practices

1. **Principle of Least Privilege**: Grant only necessary permissions
2. **Use Namespaces**: Isolate resources and permissions
3. **Avoid Wildcards**: Be specific with resources and verbs
4. **Regular Audits**: Review and update permissions regularly
5. **Service Accounts**: Use dedicated service accounts for applications
6. **Separate Roles**: Create specific roles for different tasks
7. **Document Permissions**: Add annotations explaining role purposes
8. **Test Permissions**: Verify access before deploying

## 🛠️ Management Commands

### Create Resources

```bash
# Create service account
kubectl create serviceaccount my-sa -n my-namespace

# Create role
kubectl create role pod-reader --verb=get,list,watch --resource=pods -n my-namespace

# Create cluster role
kubectl create clusterrole secret-reader --verb=get,list --resource=secrets

# Create role binding
kubectl create rolebinding read-pods --role=pod-reader --user=jane@example.com -n my-namespace

# Create cluster role binding
kubectl create clusterrolebinding read-secrets --clusterrole=secret-reader --user=john@example.com
```

### Delete Resources

```bash
# Delete role
kubectl delete role <role-name> -n <namespace>

# Delete role binding
kubectl delete rolebinding <rolebinding-name> -n <namespace>

# Delete cluster role
kubectl delete clusterrole <clusterrole-name>

# Delete cluster role binding
kubectl delete clusterrolebinding <clusterrolebinding-name>
```

## 🔍 Troubleshooting

### Debug Permission Issues

```bash
# Check current user
kubectl auth whoami

# Test specific permission
kubectl auth can-i create deployments -n production

# View effective permissions
kubectl auth can-i --list

# Check as another user
kubectl auth can-i get pods --as=system:serviceaccount:default:my-sa

# View role details
kubectl describe role <role-name> -n <namespace>

# View binding details
kubectl describe rolebinding <rolebinding-name> -n <namespace>
```

### Common Issues

1. **Permission Denied**: Check role bindings and subjects
2. **Resource Not Found**: Verify namespace and resource names
3. **Verb Not Allowed**: Check role rules for required verbs
4. **Service Account Issues**: Ensure service account exists and is bound

## 📊 Built-in ClusterRoles

Kubernetes provides several built-in ClusterRoles:

- **cluster-admin**: Full cluster access
- **admin**: Full namespace access
- **edit**: Read/write access to most resources
- **view**: Read-only access to most resources

```bash
# List built-in cluster roles
kubectl get clusterroles | grep "system:"

# Use built-in role
kubectl create rolebinding admin-binding \
  --clusterrole=admin \
  --user=jane@example.com \
  -n production
```

## 🔗 Related Resources

- [Namespaces](../NameSpaces/) - Namespace isolation
- [Secrets](../SecretsDemo/) - Secure sensitive data
- [Service Accounts](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)

## 📚 References

- [Kubernetes RBAC Documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Authorization Overview](https://kubernetes.io/docs/reference/access-authn-authz/authorization/)
- [Service Accounts](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)