1. Create the Application Load Balancer (ALB)
1.1 Create a Security Group for the ALB

This SG allows public inbound traffic on port 80:

```
aws ec2 create-security-group \
  --group-name mlops-alb-sg \
  --description "Security Group for ALB"

```

Allow HTTP inbound:

```
aws ec2 authorize-security-group-ingress \
  --group-name mlops-alb-sg \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0
```

1.2 Create the ALB

Replace <vpc-id> with your actual VPC.

```
aws elbv2 create-load-balancer \
  --name mlops-iris-alb \
  --subnets <subnet-1> <subnet-2> \
  --security-groups <alb-sg-id> \
  --type application
```
Save the ALB ARN and DNS name that the command returns.

1.3 Create a Target Group

This target group receives traffic from the ALB and sends it to ECS tasks.

It expects the app on port 8080 and a /health endpoint.
```
aws elbv2 create-target-group \
  --name iris-tg \
  --protocol HTTP \
  --port 8080 \
  --target-type ip \
  --vpc-id <vpc-id> \
  --health-check-protocol HTTP \
  --health-check-path "/health" \
  --health-check-interval-seconds 15 \
  --health-check-timeout-seconds 5 \
  --healthy-threshold-count 2 \
  --unhealthy-threshold-count 2
```

1.4 Create a Listener for the ALB

Route all inbound HTTP to the target group.

```
aws elbv2 create-listener \
  --load-balancer-arn <alb-arn> \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=<target-group-arn>
```