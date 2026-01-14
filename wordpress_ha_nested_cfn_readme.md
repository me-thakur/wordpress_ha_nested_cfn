# WordPress HA using Nested CloudFormation (JSON only)

This repo contains Nested CloudFormation JSON templates to deploy a Highly Available WordPress architecture.

## Architecture
- VPC with 2 Public + 2 Private Subnets (Multi-AZ)
- Internet Gateway + NAT Gateway + Route Tables
- Application Load Balancer (ALB)
- Auto Scaling Group (ASG) with Launch Template
- WordPress installed from scratch on Amazon Linux 2023 (kernel 6.12)
- Shared storage using EFS mounted at `/var/www/html`
- MySQL backend using RDS in private subnet

## Repo Structure

wordpress-ha-nested-cfn-json/
├── root-stack.json
└── stacks/
    ├── 01-network.json
    ├── 02-security.json
    ├── 03-storage.json
    └── 04-app.json

## Pre-requisites
1. S3 bucket created (example: `cf-resource-deploy`)
2. Nested templates already uploaded to S3 at:

s3://cf-resource-deploy/stacks/01-network.json
s3://cf-resource-deploy/stacks/02-security.json
s3://cf-resource-deploy/stacks/03-storage.json
s3://cf-resource-deploy/stacks/04-app.json

3. Root template uploaded to S3:

s3://cf-resource-deploy/root-stack.json

4. Create an EC2 keypair (for SSH if required)
5. IAM CloudFormation execution role configured properly

## Deployment (AWS Console)

### Step 1: Open CloudFormation
AWS Console → CloudFormation → Create stack

### Step 2: Choose Template
Select:
- Template is ready
- Amazon S3 URL

Paste:

https://cf-resource-deploy.s3.us-east-1.amazonaws.com/root-stack.json

### Step 3: Provide Parameters
Fill:
- TemplateBucket = cf-resource-deploy
- KeyName = <your-keypair>
- DBName = wordpressdb
- DBUser = admin
- DBPassword = ********

### Step 4: Create Stack
Click Create stack and wait for CREATE_COMPLETE.

## Outputs
After stack finishes:
CloudFormation → Outputs

- WordPressURL = ALB DNS (open in browser)

Example:
http://xxxxx.us-east-1.elb.amazonaws.com

## Automation (Already created via Console)
Lambda function and EventBridge Scheduler have been created manually using AWS console.

Lambda triggers:
- START action at 9 AM IST
- STOP action at 5 PM IST

Lambda Destinations configured to SNS topic for notifications.

## Notes
- NAT Gateway is chargeable (hourly)
- RDS stop/start supported for non-Aurora DB engines
- ELB connection draining can delay instance termination
