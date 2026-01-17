# Examples

This directory contains real-world application examples deployed on Kubernetes.

## 📋 Overview

These examples demonstrate complete application deployments with all necessary Kubernetes resources including deployments, services, storage, and configuration.

## 📁 Projects

### 🐍 Flask Application
A Python Flask web application example with HTML templates.

**Location**: `FlaskAPP/`

**Components**:
- `main.py` - Flask application code
- `templates/index.html` - Web interface

**Features**:
- Simple web application
- Template rendering
- Ready for containerization

### 📨 Kafka
Apache Kafka deployment for distributed streaming platform.

**Location**: `kafka/`

**Components**:
- `kafka.yaml` - Kafka deployment configuration

**Use Cases**:
- Event streaming
- Message queuing
- Real-time data pipelines
- Log aggregation

### 🗄️ MySQL
Complete MySQL database deployment with all necessary Kubernetes resources.

**Location**: `mysql/`

**Components**:
- `mysql-deployment.yaml` - MySQL deployment
- `mysql-namespace.yaml` - Dedicated namespace
- `mysql-secret.yaml` - Database credentials
- `mysql-services.yaml` - Service configuration
- `mysql-storage.yaml` - Persistent storage

**Features**:
- Persistent data storage
- Secure credential management
- Service exposure
- Namespace isolation

## 🚀 Quick Start

### Deploy Flask Application

```bash
# Build Docker image (create Dockerfile first)
docker build -t flask-app:1.0 examples/FlaskAPP/

# Create deployment (create deployment.yaml first)
kubectl apply -f examples/FlaskAPP/deployment.yaml
```

### Deploy Kafka

```bash
# Apply Kafka configuration
kubectl apply -f examples/kafka/kafka.yaml

# Verify deployment
kubectl get pods -l app=kafka
```

### Deploy MySQL

```bash
# Deploy in order
kubectl apply -f examples/mysql/mysql-namespace.yaml
kubectl apply -f examples/mysql/mysql-secret.yaml
kubectl apply -f examples/mysql/mysql-storage.yaml
kubectl apply -f examples/mysql/mysql-deployment.yaml
kubectl apply -f examples/mysql/mysql-services.yaml

# Verify deployment
kubectl get all -n mysql
```

## 💡 Usage Tips

### Flask Application
1. Create a Dockerfile for the Flask app
2. Build and push to container registry
3. Create Kubernetes deployment and service manifests
4. Deploy to cluster

### Kafka
- Ensure sufficient resources for Kafka brokers
- Configure persistent storage for data retention
- Set up ZooKeeper if required
- Configure appropriate resource limits

### MySQL
- Always use Secrets for passwords
- Configure persistent volumes for data
- Set resource limits appropriately
- Use StatefulSets for production deployments
- Configure backups

## 📝 Creating Your Own Examples

When adding new examples, include:

1. **Application Code** - Source files
2. **Dockerfile** - Container image definition
3. **Kubernetes Manifests**:
   - Deployment
   - Service
   - ConfigMap (if needed)
   - Secret (if needed)
   - PersistentVolume (if needed)
4. **README.md** - Specific instructions

## 🔍 Example Structure

```
examples/
├── your-app/
│   ├── README.md
│   ├── Dockerfile
│   ├── app-code/
│   ├── k8s/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   └── secret.yaml
│   └── docs/
```

## ⚠️ Important Notes

- **Secrets**: Never commit actual secret values to version control
- **Images**: Use specific version tags, not `latest`
- **Resources**: Always define resource requests and limits
- **Health Checks**: Implement liveness and readiness probes
- **Namespaces**: Use namespaces for isolation

## 🔗 Related Resources

- [Deployments](../Deployments/) - Deployment patterns
- [Services](../Services/) - Service configurations
- [Secrets](../SecretsDemo/) - Secret management
- [Volumes](../Volumes/) - Storage configuration

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [MySQL on Kubernetes](https://kubernetes.io/docs/tasks/run-application/run-single-instance-stateful-application/)