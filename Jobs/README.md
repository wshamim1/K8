# Jobs and CronJobs

This directory contains examples of Kubernetes Jobs and CronJobs for batch processing and scheduled tasks.

## 📋 Overview

**Jobs** create one or more Pods and ensure that a specified number of them successfully terminate. Jobs track the successful completions and when a specified number of successful completions is reached, the Job is complete.

**CronJobs** create Jobs on a repeating schedule, similar to Unix cron jobs.

## 📁 Files

- **jobsDemo.yaml** - Basic Job example
- **cronJobDemo.yaml** - CronJob example for scheduled tasks

## 🚀 Usage

### Jobs

#### Create a Job

```bash
# Apply Job configuration
kubectl apply -f jobsDemo.yaml

# Create Job from command line
kubectl create job my-job --image=busybox -- echo "Hello World"
```

#### Monitor Jobs

```bash
# List all jobs
kubectl get jobs

# Get job details
kubectl describe job <job-name>

# View job logs
kubectl logs job/<job-name>

# Watch job status
kubectl get jobs --watch
```

#### Manage Jobs

```bash
# Delete a job
kubectl delete job <job-name>

# Delete job and its pods
kubectl delete job <job-name> --cascade=foreground

# Delete completed jobs
kubectl delete jobs --field-selector status.successful=1
```

### CronJobs

#### Create a CronJob

```bash
# Apply CronJob configuration
kubectl apply -f cronJobDemo.yaml

# Create CronJob from command line
kubectl create cronjob my-cron --image=busybox --schedule="*/5 * * * *" -- echo "Hello"
```

#### Monitor CronJobs

```bash
# List all cronjobs
kubectl get cronjobs

# Get cronjob details
kubectl describe cronjob <cronjob-name>

# View recent jobs created by cronjob
kubectl get jobs --selector=job-name=<cronjob-name>
```

#### Manage CronJobs

```bash
# Suspend a cronjob
kubectl patch cronjob <cronjob-name> -p '{"spec":{"suspend":true}}'

# Resume a cronjob
kubectl patch cronjob <cronjob-name> -p '{"spec":{"suspend":false}}'

# Delete a cronjob
kubectl delete cronjob <cronjob-name>
```

## 📝 Job Configuration

### Basic Job Example

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: example-job
spec:
  template:
    spec:
      containers:
      - name: job-container
        image: busybox
        command: ["echo", "Job completed successfully"]
      restartPolicy: Never
  backoffLimit: 4
  completions: 1
  parallelism: 1
```

### CronJob Example

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: example-cronjob
spec:
  schedule: "0 */6 * * *"  # Every 6 hours
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: cron-container
            image: busybox
            command: ["echo", "Scheduled task executed"]
          restartPolicy: OnFailure
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
```

## ⏰ Cron Schedule Format

```
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
# │ │ │ │ │
# * * * * *
```

### Common Schedules

- `*/5 * * * *` - Every 5 minutes
- `0 * * * *` - Every hour
- `0 0 * * *` - Daily at midnight
- `0 0 * * 0` - Weekly on Sunday at midnight
- `0 0 1 * *` - Monthly on the 1st at midnight
- `0 9 * * 1-5` - Weekdays at 9 AM

## 💡 Use Cases

### Jobs
- Data processing tasks
- Batch computations
- Database migrations
- One-time administrative tasks
- Report generation
- Backup operations

### CronJobs
- Scheduled backups
- Regular data cleanup
- Periodic report generation
- Health checks
- Log rotation
- Certificate renewal

## 🔧 Key Parameters

### Job Parameters

- **completions**: Number of successful pod completions needed
- **parallelism**: Maximum number of pods running in parallel
- **backoffLimit**: Number of retries before marking job as failed
- **activeDeadlineSeconds**: Maximum duration for job execution
- **ttlSecondsAfterFinished**: Automatic cleanup after completion

### CronJob Parameters

- **schedule**: Cron expression for scheduling
- **successfulJobsHistoryLimit**: Number of successful jobs to keep
- **failedJobsHistoryLimit**: Number of failed jobs to keep
- **concurrencyPolicy**: How to handle concurrent executions (Allow, Forbid, Replace)
- **startingDeadlineSeconds**: Deadline for starting the job if missed

## ⚠️ Best Practices

1. **Set Resource Limits**: Define CPU and memory limits
2. **Use Appropriate Restart Policies**: Never or OnFailure for Jobs
3. **Configure Backoff Limits**: Prevent infinite retry loops
4. **Set TTL for Cleanup**: Automatically remove completed jobs
5. **Monitor Job Status**: Set up alerts for failed jobs
6. **Use Idempotent Operations**: Jobs may be retried
7. **Handle Concurrency**: Configure concurrencyPolicy for CronJobs
8. **Set Deadlines**: Use activeDeadlineSeconds to prevent hanging jobs

## 🔍 Troubleshooting

```bash
# Check job status
kubectl get jobs
kubectl describe job <job-name>

# View pod logs
kubectl logs <pod-name>

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp

# Debug failed jobs
kubectl get pods --selector=job-name=<job-name>
kubectl logs <failed-pod-name>
```

## 🔗 Related Resources

- [Deployments](../Deployments/) - For long-running applications
- [ConfigMaps](../ConfigMapsDemo/) - Configuration for jobs
- [Secrets](../SecretsDemo/) - Sensitive data for jobs

## 📚 References

- [Kubernetes Jobs Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
- [Kubernetes CronJobs Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)
- [Cron Expression Format](https://en.wikipedia.org/wiki/Cron)