# 🧪 AWS Local Demo

A **100% free, offline AWS playground** built on your Mac using LocalStack + Docker.  
Practice real AWS CLI commands — no account, no credit card, no cost.

## 🏗️ Architecture

```
LocalStack (localhost:4566)
├── S3           → File storage (buckets, upload, download)
├── Lambda       → Python serverless functions
├── DynamoDB     → NoSQL database (full CRUD)
├── API Gateway  → HTTP REST API → triggers Lambda
└── S3 Trigger   → Upload file → Lambda auto-fires
```

## 🚀 Quick Start

### Prerequisites
- [Docker](https://docker.com)
- [AWS CLI v2](https://aws.amazon.com/cli/)
- Python 3.x

### 1. Start LocalStack
```bash
docker run -d \
  --name localstack \
  -p 4566:4566 \
  -e SERVICES=s3,lambda,dynamodb,apigateway \
  -v /var/run/docker.sock:/var/run/docker.sock \
  localstack/localstack:3.0.0
```

### 2. Configure fake credentials
```bash
aws configure set aws_access_key_id     "test"
aws configure set aws_secret_access_key "test"
aws configure set default.region        "us-east-1"
aws configure set default.s3.request_checksum_calculation when_required
```

### 3. Set shortcut alias
```bash
echo 'alias awslocal="aws --endpoint-url http://localhost:4566"' >> ~/.zshrc
source ~/.zshrc
```

## 📦 S3 Commands
```bash
# Create bucket
aws --endpoint-url http://localhost:4566 s3 mb s3://my-bucket

# Upload file
aws --endpoint-url http://localhost:4566 s3 cp file.txt s3://my-bucket/

# List contents
aws --endpoint-url http://localhost:4566 s3 ls s3://my-bucket/
```

## ⚡ Lambda Commands
```bash
# Deploy function
aws --endpoint-url http://localhost:4566 lambda create-function \
  --function-name hello-lambda \
  --runtime python3.11 \
  --role arn:aws:iam::000000000000:role/fake-role \
  --handler handler.lambda_handler \
  --zip-file fileb://function.zip

# Invoke function
aws --endpoint-url http://localhost:4566 lambda invoke \
  --function-name hello-lambda \
  --payload '{"name": "Saiyash"}' \
  --cli-binary-format raw-in-base64-out \
  response.json && cat response.json
```

## 🗃️ DynamoDB Commands
```bash
# Create table
aws --endpoint-url http://localhost:4566 dynamodb create-table \
  --table-name Users \
  --attribute-definitions AttributeName=UserId,AttributeType=S \
  --key-schema AttributeName=UserId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# Put item
aws --endpoint-url http://localhost:4566 dynamodb put-item \
  --table-name Users \
  --item '{"UserId":{"S":"u001"},"Name":{"S":"Saiyash"},"Role":{"S":"Admin"}}'

# Get item
aws --endpoint-url http://localhost:4566 dynamodb get-item \
  --table-name Users \
  --key '{"UserId":{"S":"u001"}}'

# Scan all
aws --endpoint-url http://localhost:4566 dynamodb scan --table-name Users

# Update item
aws --endpoint-url http://localhost:4566 dynamodb update-item \
  --table-name Users \
  --key '{"UserId":{"S":"u001"}}' \
  --update-expression "SET #r = :val" \
  --expression-attribute-names '{"#r":"Role"}' \
  --expression-attribute-values '{":val":{"S":"Architect"}}' \
  --return-values ALL_NEW

# Delete item
aws --endpoint-url http://localhost:4566 dynamodb delete-item \
  --table-name Users \
  --key '{"UserId":{"S":"u001"}}'
```

## 🌐 API Gateway — REST API → Lambda
```bash
# Create API
API_ID=$(aws --endpoint-url http://localhost:4566 apigateway create-rest-api \
  --name "HelloAPI" --query 'id' --output text)

# Call your API
curl http://localhost:4566/restapis/$API_ID/test/_user_request_/hello
```

## 🛑 Stop LocalStack
```bash
docker stop localstack
```

## 📋 Cheat Sheet

| Service | Command Prefix |
|---------|---------------|
| S3 | `aws --endpoint-url http://localhost:4566 s3 ...` |
| Lambda | `aws --endpoint-url http://localhost:4566 lambda ...` |
| DynamoDB | `aws --endpoint-url http://localhost:4566 dynamodb ...` |
| API Gateway | `aws --endpoint-url http://localhost:4566 apigateway ...` |

## 🛠️ Tech Stack
- **LocalStack 3.0.0** — AWS cloud emulator
- **Docker** — Container runtime
- **AWS CLI v2** — Command line interface
- **Python 3.11** — Lambda runtime

---
> Built for learning AWS without spending a rupee 💰❌
