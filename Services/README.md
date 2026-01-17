# Services

This directory contains examples of different Kubernetes Service types for exposing applications.

## 📋 Overview

A Service in Kubernetes is an abstraction that defines a logical set of Pods and a policy to access them. Services enable loose coupling between dependent Pods and provide stable networking endpoints.

## 📁 Files

- **Services_ClusterIP_Sample.yaml** - ClusterIP service example (internal access)
- **Services_NodePortSample.yaml** - NodePort service example (external access via node)
- **Services_LoadBalancerSample.yaml** - LoadBalancer service example (cloud load balancer)

## 🚀 Usage

### Apply Service Configurations

```bash
# Apply ClusterIP service
kubectl apply -f Services_ClusterIP_Sample.yaml

# Apply NodePort service
kubectl apply -f Services_NodePortSample.yaml

# Apply LoadBalancer service
kubectl apply -f Services_LoadBalancerSample.yaml
```

### Manage Services

```bash
# List all services
kubectl get services
kubectl get svc

# Get service details
kubectl describe service <service-name>

# Get service endpoints
kubectl get endpoints <service-name>

# Delete a service
kubectl delete service <service-name>
```

### Test Services

```bash
# Get service URL (for NodePort)
kubectl get service <service-name> -o wide

# Port forward to local machine
kubectl port-forward service/<service-name> 8080:80

# Test service from within cluster
kubectl run test-pod --image=busybox -it --rm -- wget -O- http://<service-name>
```

## 📝 Service Types

### 1. ClusterIP (Default)

Exposes service on an internal IP within the cluster. Only accessible from within the cluster.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-clusterip-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```

**Use Cases**:
- Internal microservices communication
- Database services
- Backend APIs not exposed externally

**Access**:
```bash
# From within cluster
curl http://my-clusterip-service:80

# From local machine (port-forward)
kubectl port-forward service/my-clusterip-service 8080:80
curl http://localhost:8080
```

### 2. NodePort

Exposes service on each Node's IP at a static port (30000-32767 range).

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-nodeport-service
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
    nodePort: 30080  # Optional, auto-assigned if not specified
```

**Use Cases**:
- Development and testing
- Direct access to services
- When LoadBalancer is not available

**Access**:
```bash
# Get node IP
kubectl get nodes -o wide

# Access service
curl http://<node-ip>:30080
```

### 3. LoadBalancer

Exposes service externally using a cloud provider's load balancer.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-loadbalancer-service
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```

**Use Cases**:
- Production web applications
- Public-facing APIs
- Services requiring high availability

**Access**:
```bash
# Get external IP
kubectl get service my-loadbalancer-service

# Access service
curl http://<external-ip>:80
```

### 4. ExternalName

Maps service to a DNS name (not covered in files, but useful to know).

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-external-service
spec:
  type: ExternalName
  externalName: api.example.com
```

**Use Cases**:
- Accessing external services
- Service migration
- DNS aliasing

## 🎯 Service Discovery

### DNS-Based Discovery

Services are automatically assigned DNS names:

```
<service-name>.<namespace>.svc.cluster.local
```

**Examples**:
```bash
# Same namespace
curl http://my-service

# Different namespace
curl http://my-service.production.svc.cluster.local

# Full FQDN
curl http://my-service.production.svc.cluster.local:80
```

### Environment Variables

Kubernetes injects service information as environment variables:

```bash
# Service host
<SERVICE_NAME>_SERVICE_HOST

# Service port
<SERVICE_NAME>_SERVICE_PORT
```

## 🔧 Advanced Configurations

### Session Affinity

Maintain client session to same pod:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: sticky-service
spec:
  type: ClusterIP
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
```

### Headless Service

For direct pod access without load balancing:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: headless-service
spec:
  clusterIP: None
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
```

### Multi-Port Service

Expose multiple ports:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: multi-port-service
spec:
  selector:
    app: myapp
  ports:
  - name: http
    protocol: TCP
    port: 80
    targetPort: 8080
  - name: https
    protocol: TCP
    port: 443
    targetPort: 8443
```

### External IPs

Specify external IPs manually:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-ip-service
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
  externalIPs:
  - 192.168.1.100
```

## 📊 Service Comparison

| Feature | ClusterIP | NodePort | LoadBalancer |
|---------|-----------|----------|--------------|
| Accessibility | Internal only | External via Node IP | External via LB |
| Port Range | Any | 30000-32767 | Any |
| Cost | Free | Free | Cloud provider cost |
| Use Case | Internal services | Dev/Test | Production |
| HA | Yes | Limited | Yes |

## 💡 Best Practices

1. **Use ClusterIP by Default**: For internal services
2. **LoadBalancer for Production**: External-facing services
3. **Meaningful Names**: Use descriptive service names
4. **Label Selectors**: Ensure correct pod selection
5. **Health Checks**: Configure readiness probes
6. **Resource Limits**: Set appropriate timeouts
7. **Security**: Use NetworkPolicies with services
8. **Monitoring**: Track service metrics and endpoints

## 🔍 Troubleshooting

### Service Not Working

```bash
# Check service exists
kubectl get service <service-name>

# Check endpoints
kubectl get endpoints <service-name>

# Verify pod labels match selector
kubectl get pods --show-labels
kubectl describe service <service-name>

# Check service events
kubectl describe service <service-name>

# Test connectivity
kubectl run test --image=busybox -it --rm -- wget -O- http://<service-name>
```

### No Endpoints

```bash
# Check if pods are running
kubectl get pods -l app=<label>

# Verify pod labels
kubectl get pods --show-labels

# Check pod readiness
kubectl get pods -o wide

# Describe service
kubectl describe service <service-name>
```

### LoadBalancer Pending

```bash
# Check service status
kubectl get service <service-name>

# Describe service for events
kubectl describe service <service-name>

# Verify cloud provider integration
kubectl get events --sort-by=.metadata.creationTimestamp
```

## 🛠️ Common Commands

```bash
# Create service from command line
kubectl expose deployment <deployment-name> --type=LoadBalancer --port=80

# Get service URL (minikube)
minikube service <service-name> --url

# Edit service
kubectl edit service <service-name>

# Scale deployment behind service
kubectl scale deployment <deployment-name> --replicas=5

# View service logs (via pods)
kubectl logs -l app=<label> --all-containers=true

# Delete service
kubectl delete service <service-name>
```

## 🔗 Service Mesh Integration

For advanced traffic management, consider service meshes:
- **Istio**: Traffic management, security, observability
- **Linkerd**: Lightweight service mesh
- **Consul**: Service discovery and mesh

## 📈 Monitoring Services

```bash
# Watch service status
kubectl get services --watch

# Check service endpoints
kubectl get endpoints

# View service metrics (requires metrics-server)
kubectl top pods -l app=<label>

# Service logs
kubectl logs -l app=<label> --tail=100 -f
```

## 🔗 Related Resources

- [Deployments](../Deployments/) - Deploy applications behind services
- [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) - HTTP/HTTPS routing
- [NetworkPolicies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) - Network security
- [DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) - Service discovery

## 📚 References

- [Kubernetes Services Documentation](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Service Types](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)
- [DNS for Services](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)