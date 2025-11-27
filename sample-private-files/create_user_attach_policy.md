# Create the user
aws iam create-user --user-name github-actions-mlops-deployer

# Create the policy from the JSON file
aws iam create-policy --policy-name GitHubActionsMLOpsDeployerPolicy --policy-document file://github-actions-policy.json

# Get your AWS Account ID programmatically
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Attach the policy to the user
aws iam attach-user-policy \
  --user-name github-actions-mlops-deployer \
  --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/GitHubActionsMLOpsDeployerPolicy

# Create an access key for the user
aws iam create-access-key --user-name github-actions-mlops-deployer

# Create a private ECR repository to store our Docker images
aws ecr create-repository \
  --repository-name mlops-iris-classifier \
  --image-scanning-configuration scanOnPush=true \
  --region ap-southeast-2

# Create a serverless ECS cluster using Fargate
aws ecs create-cluster --cluster-name mlops-production-cluster --region ap-southeast-2