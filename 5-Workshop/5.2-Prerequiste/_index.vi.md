---
title: "Các bước chuẩn bị"
date: 2026-07-14
weight: 2
chapter: false
pre: " <b> 5.2. </b> "
---

# Các bước chuẩn bị

#### Tài khoản và Region

- Một tài khoản AWS có quyền tạo VPC/EC2/EIP/Security Group, IAM/SSM, S3, DynamoDB, CloudFront/WAF, GuardDuty, Security Hub, EventBridge, Step Functions, Lambda, API Gateway, SNS, CloudWatch, CloudTrail và AWS Config.
- Chọn Region **Asia Pacific (Singapore) – `ap-southeast-1`** cho toàn bộ workshop.
- Máy cá nhân có Git, AWS CLI, Python 3.10+ và Node.js 18+.

{{% notice warning %}}
Không lưu AWS access key trong source code hoặc đưa file `.env` lên Git. Khi chạy trên EC2, hãy gắn IAM instance profile và sử dụng credential tạm thời.
{{% /notice %}}

#### Tài nguyên sử dụng

| Loại | Tên/cấu hình |
|---|---|
| S3 bucket | `aws-s3-duanthuctap`, Block Public Access bật |
| DynamoDB | `Documents` – partition key `document_id` (String) |
| DynamoDB | `SecurityIncidents` – partition key `incident_id` (String) |
| Lambda | `SecurityIncidentResponse` |
| EventBridge rule | `GuardDutyToSecurityIncident` |
| SNS topic | `SecurityAlerts` |
| EC2 | Ubuntu, gắn IAM role và được quản lý bởi Systems Manager |
| Step Functions | `SecurityIncidentApprovalWorkflow` – Standard workflow |
| API Gateway | HTTP API route `ANY /approval` |
| CloudFront | S3 private origin cho SPA và EC2 origin cho `/api/*` |
| Elastic IP | Gắn cố định vào EC2 backend |
| CloudWatch | Metric, log group và CloudWatch Agent |
| Grafana | Chạy private trên EC2, truy cập bằng SSM port forwarding |
| CloudTrail / Flow Logs / S3 access log | Nguồn dữ liệu kiểm toán |
| AWS Config | Recorder, delivery channel và compliance rules |

#### Chuẩn bị mã nguồn

```bash
git clone <repository-url>
cd aws
```

Tạo `backend/.env` từ file mẫu và điền đúng tài nguyên:

```env
AWS_REGION=ap-southeast-1
S3_BUCKET_NAME=aws-s3-duanthuctap
DYNAMODB_DOCUMENTS_TABLE=Documents
DYNAMODB_INCIDENTS_TABLE=SecurityIncidents
JWT_SECRET_KEY=<chuoi-ngau-nhien-it-nhat-32-ky-tu>
```

#### Nguyên tắc IAM

EC2 chỉ cần quyền thao tác object trong đúng bucket, đọc/ghi hai bảng DynamoDB, gửi log/metric CloudWatch và kết nối Systems Manager. Lambda chỉ cần đọc thông tin finding, ghi bảng `SecurityIncidents`, publish đến topic `SecurityAlerts` và ghi CloudWatch Logs.

{{% notice tip %}}
Trong môi trường báo cáo có thể dùng managed policy để triển khai nhanh. Khi đưa vào production, nên thay bằng policy giới hạn theo ARN tài nguyên và đúng các action cần thiết.
{{% /notice %}}

#### Kiểm tra danh tính AWS

```bash
aws sts get-caller-identity
aws configure get region
```

Kết quả mong đợi là đúng AWS Account đang làm workshop và Region `ap-southeast-1`.
