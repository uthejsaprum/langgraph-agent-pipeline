'# Terraform From Scratch Roadmap

## Goal

You want to implement Terraform from scratch using

:| Component | Tool |
|---|---|
| CI/CD Pipeline | Azure DevOps |
| Terraform State Storage | Terraform Cloud |
| Cloud Provider | AWS |
| IaC Tool | Terraform |

---

# 1. High-Level Architecture

```text
Developer
   |
   | Push Terraform code
   v
Azure Repos / GitHub Repo
   |
   | Trigger Pipeline
   v
Azure DevOps Pipeline
   |
   | terraform init / plan / apply
   v
Terraform Cloud
   |
   | Stores Terraform state remotely
   v
AWS
   |
   | Creates / Updates / Deletes infrastructure
```

---

# 2. What You Need Before Starting

## Accounts Required

You need access to

:```text
1. AWS Account
2. Terraform Cloud Account
3. Azure DevOps Organization
4. Git Repository
```

---

## Tools Required Locally

Install these on your laptop

:```text
1. Terraform CLI
2. AWS CLI
3. Git
4. VS Code or any editor
```

---

## Install Terraform

Download Terraform

:```text
https://developer.hashicorp.com/terraform/downloads
```

Check installation

:```bash
terraform version
```

---

## Install AWS CLI

Download AWS CLI

:```text
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
```

Check installation

:```bash
aws --version
```

---

## Install Git

Check Git

:```bash
git --version
```

---

# 3. Basic Terraform Concepts

## Terraform Provider

A provider allows Terraform to talk to a cloud platform.

For AWS

:```hcl
provider "aws" {
  region = "us-east-1"
}
```

---

## Terraform State

Terraform state tracks resources created by Terraform.

Example

:```text
Terraform Code says
:Create 1 S3 bucket

Terraform State remembers
:S3 bucket named my-demo-bucket exists in AWS
```

Without state, Terraform cannot properly manage infrastructure.

---

## Terraform Cloud State

Instead of storing state locally like this

:```text
terraform.tfstate
```

You will store it remotely in Terraform Cloud.

Benefits

:```text
1. Centralized state storage
2. State locking
3. Team collaboration
4. Safer than local state
5. State history
```

---

# 4. Recommended Repository Structure

Use this structure

:```text
terraform-aws-infra/
│
├── azure-pipelines.yml
│
├── README.md
│
└── terraform/
    │
    ├── modules/
    │   └── s3-bucket/
    │       ├── main.tf
    │       ├── variables.tf
    │       └── outputs.tf
    │
    └── environments/
        ├── dev/
        │   ├── versions.tf
        │   ├── provider.tf
        │   ├── main.tf
        │   ├── variables.tf
        │   ├── terraform.tfvars
        │   └── outputs.tf
        │
        ├── stage/
        │   ├── versions.tf
        │   ├── provider.tf
        │   ├── main.tf
        │   ├── variables.tf
        │   ├── terraform.tfvars
        │   └── outputs.tf
        │
        └── prod/
            ├── versions.tf
            ├── provider.tf
            ├── main.tf
            ├── variables.tf
            ├── terraform.tfvars
            └── outputs.tf
```

---

# 5. Terraform Cloud Setup

## Step 1: Create Terraform Cloud Account

Go to

:```text
https://app.terraform.io
```

Create an account or log in.

---

## Step 2: Create Organization

Example organization name

:```text
my-company-org
```

---

## Step 3: Create Workspaces

Create one workspace per environment.

Example

:```text
aws-dev
aws-stage
aws-prod
```

For each workspace

:```text
Execution Mode: Local
```

Very important.

Because Azure DevOps will run Terraform commands, but Terraform Cloud will store the state.

---

## Step 4: Create Terraform Cloud API Token

Go to

:```text
User Settings > Tokens > Create an API token
```

Copy the token.

It will look like

:```text
xxxxxxxx.atlasv1.xxxxxxxxxxxxxxxxxxxxx
```

You will store this token in Azure DevOps.

---

# 6. AWS Setup

## Option 1: Simple Setup Using IAM User

For beginners, create an IAM user for Terraform.

Later, in production, you should move to IAM Role/OIDC-based authentication.

---

## Step 1: Create IAM User

In AWS Console

:```text
IAM > Users > Create User
```

Example username

:```text
terraform-azuredevops-user
```

Enable

:```text
Programmatic access
```

---

## Step 2: Attach Permissions

For learning or initial setup, you can attach

:```text
AdministratorAccess
```

But for production, always use least privilege.

---

## Step 3: Create Access Key

Create access key and copy

:```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

These will be stored securely in Azure DevOps.

---

# 7. Azure DevOps Setup

## Step 1: Create Project

Go to Azure DevOps

:```text
https://dev.azure.com
```

Create a project

:```text
terraform-aws-project
```

---

## Step 2: Create Repository

You can use

:```text
Azure Repos
```

or connect GitHub.

Example repo name

:```text
terraform-aws-infra
```

---

## Step 3: Add Secret Variables

Go to

:```text
Pipelines > Library > Variable Groups
```

Create a variable group

:```text
terraform-secrets
```

Add these variables

:| Variable Name | Value | Secret |
|---|---|---|
| `TFC_TOKEN` | Terraform Cloud API token | Yes |
| `AWS_ACCESS_KEY_ID` | AWS access key | Yes |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Yes |
| `AWS_REGION` | Example: `us-east-1` | No |

---

## Step 4: Allow Pipeline Access

Inside the variable group, enable

:```text
Allow access to all pipelines
```

Or explicitly authorize your pipeline when prompted.

---

# 8. Terraform Code

## Module: S3 Bucket

Create

:```text
terraform/modules/s3-bucket/main.tf
```

```hcl
resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name

  tags = var.tags
}

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id

  versioning_configuration {
    status = var.versioning_enabled ? "Enabled" : "Suspended"
  }
}
```

---

Create

:```text
terraform/modules/s3-bucket/variables.tf
```

```hcl
variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "versioning_enabled" {
  description = "Enable or disable bucket versioning"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags for the S3 bucket"
  type        = map(string)
  default     = {}
}
```

---

Create

:```text
terraform/modules/s3-bucket/outputs.tf
```

```hcl
output "bucket_id" {
  description = "S3 bucket ID"
  value       = aws_s3_bucket.this.id
}

output "bucket_arn" {
  description = "S3 bucket ARN"
  value       = aws_s3_bucket.this.arn
}
```

---

# 9. Dev Environment Code

Create

:```text
terraform/environments/dev/versions.tf
```

```hcl
terraform {
  required_version = ">= 1.6.0"

  cloud {
    organization = "my-company-org"

    workspaces {
      name = "aws-dev"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

Replace

:```text
my-company-org
```

with your actual Terraform Cloud organization name.

---

Create

:```text
terraform/environments/dev/provider.tf
```

```hcl
provider "aws" {
  region = var.aws_region
}
```

Do not hardcode AWS credentials here.

Terraform will get AWS credentials from environment variables

:```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
```

---

Create

:```text
terraform/environments/dev/variables.tf
```

```hcl
variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "bucket_name" {
  description = "S3 bucket name"
  type        = string
}
```

---

Create

:```text
terraform/environments/dev/main.tf
```

```hcl
module "app_bucket" {
  source = "../../modules/s3-bucket"

  bucket_name        = var.bucket_name
  versioning_enabled = true

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = "Terraform-AWS-Demo"
  }
}
```

---

Create

:```text
terraform/environments/dev/outputs.tf
```

```hcl
output "bucket_id" {
  value = module.app_bucket.bucket_id
}

output "bucket_arn" {
  value = module.app_bucket.bucket_arn
}
```

---

Create

:```text
terraform/environments/dev/terraform.tfvars
```

```hcl
aws_region  = "us-east-1"
environment = "dev"
bucket_name = "my-company-dev-demo-bucket-001"
```

Important

:S3 bucket names must be globally unique.

Change the bucket name to something unique.

---

# 10. Local Terraform Test

Before pipeline setup, test locally.

## Step 1: Login to Terraform Cloud

```bash
terraform login
```

Paste your Terraform Cloud token.

---

## Step 2: Configure AWS CLI

```bash
aws configure
```

Enter

:```text
AWS Access Key ID
AWS Secret Access Key
Default Region
Output Format
```

Example

:```text
Default Region: us-east-1
Output Format: json
```

---

## Step 3: Go to Dev Environment Folder

```bash
cd terraform/environments/dev
```

---

## Step 4: Initialize Terraform

```bash
terraform init
```

Expected result

:```text
Terraform has been successfully initialized!
```

---

## Step 5: Format Code

```bash
terraform fmt
```

---

## Step 6: Validate Code

```bash
terraform validate
```

Expected result

:```text
Success! The configuration is valid.
```

---

## Step 7: Run Plan

```bash
terraform plan
```

---

## Step 8: Apply

```bash
terraform apply
```

Type

:```text
yes
```

Terraform should create the S3 bucket in AWS.

---

## Step 9: Destroy Test Resource If Needed

```bash
terraform destroy
```

---

# 11. Azure DevOps Pipeline

Create this file in the root of your repo

:```text
azure-pipelines.yml
```

```yaml
trigger
:  branches
:    include
:      - main
  paths
:    include
:      - terraform/*
      - azure-pipelines.yml

pr
:  branches
:    include
:      - "*"

variables
:  - group: terraform-secrets

  - name: TERRAFORM_VERSION
    value: "1.8.5"

  - name: WORKING_DIR
    value: "terraform/environments/dev"

  - name: TF_IN_AUTOMATION
    value: "true"

  - name: TF_INPUT
    value: "false"

stages
:  - stage: Validate_And_Plan
    displayName: "Terraform Validate and Plan"
    jobs
:      - job: terraform_plan
        displayName: "Terraform Plan"
        pool
:          vmImage: "ubuntu-latest"

        steps
:          - checkout: self

          - script: |
              echo "Installing Terraform version $(TERRAFORM_VERSION)"
              sudo apt-get update
              sudo apt-get install -y wget unzip

              wget https://releases.hashicorp.com/terraform/$(TERRAFORM_VERSION)/terraform_$(TERRAFORM_VERSION)_linux_amd64.zip
              unzip terraform_$(TERRAFORM_VERSION)_linux_amd64.zip
              sudo mv terraform /usr/local/bin/

              terraform version
            displayName: "Install Terraform"

          - script: |
              terraform -chdir=$(WORKING_DIR) init
            displayName: "Terraform Init"
            env
:              TF_TOKEN_app_terraform_io: $(TFC_TOKEN)
              AWS_ACCESS_KEY_ID: $(AWS_ACCESS_KEY_ID)
              AWS_SECRET_ACCESS_KEY: $(AWS_SECRET_ACCESS_KEY)
              AWS_REGION: $(AWS_REGION)
              AWS_DEFAULT_REGION: $(AWS_REGION)

          - script: |
              terraform -chdir=$(WORKING_DIR) fmt -check -recursive
            displayName: "Terraform Format Check"

          - script: |
              terraform -chdir=$(WORKING_DIR) validate
            displayName: "Terraform Validate"
            env
:              TF_TOKEN_app_terraform_io: $(TFC_TOKEN)

          - script: |
              terraform -chdir=$(WORKING_DIR) plan
            displayName: "Terraform Plan"
            env
:              TF_TOKEN_app_terraform_io: $(TFC_TOKEN)
              AWS_ACCESS_KEY_ID: $(AWS_ACCESS_KEY_ID)
              AWS_SECRET_ACCESS_KEY: $(AWS_SECRET_ACCESS_KEY)
              AWS_REGION: $(AWS_REGION)
              AWS_DEFAULT_REGION: $(AWS_REGION)

  - stage: Apply
    displayName: "Terraform Apply"
    dependsOn: Validate_And_Plan
    condition: and(succeeded(), eq(variables[\'Build.SourceBranch\'], \'refs/heads/main\'))

    jobs
:      - deployment: terraform_apply
        displayName: "Terraform Apply"
        environment: "terraform-dev"
        pool
:          vmImage: "ubuntu-latest"

        strategy
:          runOnce
:            deploy
:              steps
:                - checkout: self

                - script: |
                    echo "Installing Terraform version $(TERRAFORM_VERSION)"
                    sudo apt-get update
                    sudo apt-get install -y wget unzip

                    wget https://releases.hashicorp.com/terraform/$(TERRAFORM_VERSION)/terraform_$(TERRAFORM_VERSION)_linux_amd64.zip
                    unzip terraform_$(TERRAFORM_VERSION)_linux_amd64.zip
                    sudo mv terraform /usr/local/bin/

                    terraform version
                  displayName: "Install Terraform"

                - script: |
                    terraform -chdir=$(WORKING_DIR) init
                  displayName: "Terraform Init"
                  env
:                    TF_TOKEN_app_terraform_io: $(TFC_TOKEN)
                    AWS_ACCESS_KEY_ID: $(AWS_ACCESS_KEY_ID)
                    AWS_SECRET_ACCESS_KEY: $(AWS_SECRET_ACCESS_KEY)
                    AWS_REGION: $(AWS_REGION)
                    AWS_DEFAULT_REGION: $(AWS_REGION)

                - script: |
                    terraform -chdir=$(WORKING_DIR) apply -auto-approve
                  displayName: "Terraform Apply"
                  env
:                    TF_TOKEN_app_terraform_io: $(TFC_TOKEN)
                    AWS_ACCESS_KEY_ID: $(AWS_ACCESS_KEY_ID)
                    AWS_SECRET_ACCESS_KEY: $(AWS_SECRET_ACCESS_KEY)
                    AWS_REGION: $(AWS_REGION)
                    AWS_DEFAULT_REGION: $(AWS_REGION)
```

---

# 12. Manual Approval Before Apply

In Azure DevOps

:```text
Pipelines > Environments > New Environment
```

Create environment

:```text
terraform-dev
```

Then configure

:```text
Approvals and checks
```

Add approvers.

Now the pipeline will

:```text
1. Run terraform init
2. Run terraform fmt
3. Run terraform validate
4. Run terraform plan
5. Wait for approval
6. Run terraform apply
```

---

# 13. Important Terraform Cloud Configuration

Because Azure DevOps is running Terraform, make sure your Terraform Cloud workspace uses

:```text
Execution Mode: Local
```

If execution mode is

:```text
Remote
```

then Terraform Cloud will execute the plan/apply, not Azure DevOps.

For this roadmap, use

:```text
Local Execution
```

Terraform Cloud will only store

:```text
1. State file
2. State versions
3. State lock
```

---

# 14. Environment Expansion

You can later create separate environments

:```text
dev
stage
prod
```

Each environment should have

:```text
1. Separate Terraform Cloud workspace
2. Separate AWS account or AWS role
3. Separate tfvars
4. Separate Azure DevOps approval flow
```

Example Terraform Cloud workspaces

:```text
aws-dev
aws-stage
aws-prod
```

---

## Example Stage `versions.tf`

```hcl
terraform {
  required_version = ">= 1.6.0"

  cloud {
    organization = "my-company-org"

    workspaces {
      name = "aws-stage"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

---

## Example Prod `versions.tf`

```hcl
terraform {
  required_version = ">= 1.6.0"

  cloud {
    organization = "my-company-org"

    workspaces {
      name = "aws-prod"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

---

# 15. Terraform Commands You Should Know

## Initialize

```bash
terraform init
```

Downloads providers and configures backend/state.

---

## Format

```bash
terraform fmt
```

Formats Terraform files.

---

## Validate

```bash
terraform validate
```

Checks syntax and configuration.

---

## Plan

```bash
terraform plan
```

Shows what Terraform will create, change, or destroy.

---

## Apply

```bash
terraform apply
```

Creates or updates infrastructure.

---

## Destroy

```bash
terraform destroy
```

Deletes Terraform-managed infrastructure.

---

## Show State

```bash
terraform state list
```

Shows resources managed by Terraform.

---

## Show Specific Resource

```bash
terraform state show <resource_name>
```

Example

:```bash
terraform state show module.app_bucket.aws_s3_bucket.this
```

---

# 16. Recommended Git Workflow

Use this workflow

:```text
1. Developer creates feature branch
2. Developer writes Terraform code
3. Developer raises pull request
4. Pipeline runs terraform fmt, validate, and plan
5. Team reviews plan output
6. PR is approved
7. PR is merged to main
8. Pipeline runs plan again
9. Manual approval is required
10. Pipeline runs terraform apply
```

---

# 17. Branching Strategy

Recommended

:```text
main        -> production-ready code
feature/*   -> developer changes
hotfix/*    -> emergency fixes
```

Example

:```bash
git checkout -b feature/create-s3-module
```

---

# 18. Files You Should Not Commit

Create `.gitignore` in repo root

:```gitignore
# Terraform local files
**/.terraform/*
*.tfstate
*.tfstate.*
crash.log
crash.*.log

# Terraform variable files containing secrets
*.auto.tfvars
*.auto.tfvars.json

# Terraform plan files
*.tfplan
plan.out

# CLI config
.terraformrc
terraform.rc

# OS/editor files
.DS_Store
.vscode/
.idea/
```

Note

:You can commit `terraform.tfvars` only if it does not contain secrets.

Never commit

:```text
AWS access keys
Passwords
Private keys
Sensitive tfvars
Terraform state files
```

---

# 19. Security Best Practices

## Do Not Store AWS Keys in Code

Bad

:```hcl
provider "aws" {
  access_key = "AKIA..."
  secret_key = "abcd..."
}
```

Good

:```hcl
provider "aws" {
  region = var.aws_region
}
```

Pass credentials using environment variables.

---

## Use Least Privilege IAM

Avoid using this permanently

:```text
AdministratorAccess
```

Instead, create IAM policies based on what Terraform needs.

---

## Use Separate AWS Accounts

Recommended account structure

:```text
dev AWS account
stage AWS account
prod AWS account
```

---

## Protect Production

For production

:```text
1. Require manual approval
2. Restrict who can approve
3. Restrict who can merge to main
4. Enable branch policies
5. Enable Terraform plan review
```

---

## Rotate Secrets

Rotate periodically

:```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
Terraform Cloud token
```

---

# 20. Better Future Setup: AWS OIDC

Access keys are simple but not ideal.

Better long-term design

:```text
Azure DevOps Pipeline
   |
   | OIDC Federation
   v
AWS IAM Role
   |
   v
Temporary AWS Credentials
```

Benefits

:```text
1. No long-lived AWS keys
2. Better security
3. Easier rotation
4. Cloud-native authentication
```

Start with access keys if you are learning.

Move to OIDC when your base pipeline is stable.

---

# 21. Terraform Module Best Practices

## Keep Modules Reusable

Good module

:```text
modules/s3-bucket
modules/vpc
modules/ec2
modules/rds
modules/iam-role
```

Bad module

:```text
modules/dev-s3-bucket-only
```

---

## Module Should Not Know Environment

Bad

:```hcl
bucket = "dev-my-bucket"
```

Good

:```hcl
bucket = var.bucket_name
```

---

## Pass Environment-Specific Values From Environment Folder

Example

:```hcl
module "app_bucket" {
  source = "../../modules/s3-bucket"

  bucket_name = var.bucket_name
}
```

---

# 22. Terraform Naming Standards

Use consistent names.

Example

:```text
company-project-environment-resource
```

Example S3 bucket

:```text
mycompany-payments-dev-logs-001
```

Example tags

:```hcl
tags = {
  Environment = "dev"
  Project     = "payments"
  Owner       = "devops"
  ManagedBy   = "terraform"
}
```

---

# 23. Common Errors and Fixes

## Error: Terraform Cloud Authentication Failed

Example

:```text
Error: Required token could not be found
```

Fix

:Make sure Azure DevOps variable exists

:```text
TFC_TOKEN
```

And pipeline environment variable is

:```yaml
TF_TOKEN_app_terraform_io: $(TFC_TOKEN)
```

---

## Error: AWS Credentials Not Found

Example

:```text
Error: No valid credential sources found
```

Fix

:Make sure these variables exist in Azure DevOps

:```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
```

And are passed in the pipeline

:```yaml
env
:  AWS_ACCESS_KEY_ID: $(AWS_ACCESS_KEY_ID)
  AWS_SECRET_ACCESS_KEY: $(AWS_SECRET_ACCESS_KEY)
  AWS_REGION: $(AWS_REGION)
```

---

## Error: S3 Bucket Already Exists

Example

:```text
BucketAlreadyExists
```

Fix

:S3 bucket names are globally unique.

Change

:```hcl
bucket_name = "my-company-dev-demo-bucket-001"
```

to something unique

:```hcl
bucket_name = "my-company-dev-demo-bucket-20250101"
```

---

## Error: Workspace Not Found

Example

:```text
Terraform Cloud workspace aws-dev does not exist
```

Fix

:Create workspace in Terraform Cloud

:```text
aws-dev
```

Or update `versions.tf`

:```hcl
workspaces {
  name = "correct-workspace-name"
}
```

---

## Error: Remote Execution Issue

If Terraform Cloud tries to run the plan itself, check workspace execution mode.

Fix

:```text
Terraform Cloud Workspace > Settings > General > Execution Mode > Local
```

---

# 24. Day-1 Implementation Checklist

Use this checklist when implementing from scratch.

```text
[ ] Create AWS account/access
[ ] Create Terraform Cloud account
[ ] Create Terraform Cloud organization
[ ] Create Terraform Cloud workspace: aws-dev
[ ] Set workspace execution mode to Local
[ ] Create Terraform Cloud API token
[ ] Create AWS IAM user for Terraform
[ ] Generate AWS access key and secret key
[ ] Create Azure DevOps project
[ ] Create Git repository
[ ] Create Azure DevOps variable group: terraform-secrets
[ ] Add TFC_TOKEN as secret
[ ] Add AWS_ACCESS_KEY_ID as secret
[ ] Add AWS_SECRET_ACCESS_KEY as secret
[ ] Add AWS_REGION
[ ] Create repo folder structure
[ ] Add Terraform module code
[ ] Add dev environment Terraform code
[ ] Add azure-pipelines.yml
[ ] Push code to feature branch
[ ] Create pull request
[ ] Validate pipeline plan output
[ ] Merge to main
[ ] Approve apply stage
[ ] Verify resource in AWS
[ ] Verify state in Terraform Cloud
```

---

# 25. Recommended Learning Order

Since you are returning to Terraform after a gap, follow this order

:```text
1. Terraform basics
2. Providers
3. Variables
4. Outputs
5. State
6. Remote state
7. Modules
8. Workspaces
9. Azure DevOps pipeline basics
10. Terraform Cloud state
11. AWS IAM for Terraform
12. CI/CD approvals
13. Security and governance
```

---

# 26. Final Implementation Flow

```text
Step 1
:Create Terraform Cloud organization and workspace.

Step 2
:Create AWS IAM user or role for Terraform.

Step 3
:Create Azure DevOps variable group with secrets.

Step 4
:Create Terraform repo structure.

Step 5
:Write provider, backend, variables, module, and environment code.

Step 6
:Test locally using terraform init, validate, plan, apply.

Step 7
:Create Azure DevOps pipeline.

Step 8
:Run pipeline on pull request for validation and plan.

Step 9
:Merge to main.

Step 10
:Approve apply stage.

Step 11
:Verify infrastructure in AWS.

Step 12
:Verify state in Terraform Cloud.
```

---

# 27. Production Recommendations

Before using this in production, implement

:```text
1. Separate AWS accounts for dev/stage/prod
2. Separate Terraform Cloud workspaces
3. Azure DevOps branch policies
4. Manual approvals for prod
5. Least privilege IAM permissions
6. OIDC instead of long-lived AWS keys
7. Terraform code review process
8. Cost estimation
9. Security scanning
10. Drift detection
```

---

# 28. Useful Commands Summary

```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
terraform destroy
terraform state list
terraform output
```

---

# 29. Useful Links

```text
Terraform Documentation
:https://developer.hashicorp.com/terraform/docs

Terraform AWS Provider
:https://registry.terraform.io/providers/hashicorp/aws/latest/docs

Terraform Cloud
:https://developer.hashicorp.com/terraform/cloud-docs

Azure DevOps Pipelines
:https://learn.microsoft.com/en-us/azure/devops/pipelines/

AWS IAM
:https://docs.aws.amazon.com/iam/
```

---

# 30. Final Notes

Your first working version should be simple

:```text
Azure DevOps Pipeline
Terraform Cloud remote state
AWS provider
One AWS resource
One environment
Manual approval before apply
```

Once that works, gradually add

:```text
1. More modules
2. More environments
3. More AWS services
4. Better IAM security
5. OIDC authentication
6. Policy checks
7. Cost controls
```'
