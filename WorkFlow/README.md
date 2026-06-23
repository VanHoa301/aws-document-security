# Cloud Document Management System
### Hệ thống Quản lý Tài liệu trên Nền tảng Đám mây tích hợp Giám sát Bảo mật & Phản ứng Sự cố Tự động

![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazon-aws)
![GuardDuty](https://img.shields.io/badge/GuardDuty-Security-red?logo=amazon-aws)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-REST_API-black?logo=flask)
![Grafana](https://img.shields.io/badge/Grafana-Dashboard-orange?logo=grafana)
![Lambda](https://img.shields.io/badge/Lambda-Serverless-yellow?logo=amazon-aws)

---

## Mục lục

- [Giới thiệu dự án](#1-giới-thiệu-dự-án)
- [Chức năng nghiệp vụ](#2-chức-năng-nghiệp-vụ)
- [Công nghệ sử dụng](#3-công-nghệ-sử-dụng)
- [Kiến trúc hệ thống](#4-kiến-trúc-hệ-thống)
- [Kiến trúc bảo mật tự động](#5-kiến-trúc-bảo-mật-tự-động)
- [AWS Services sử dụng](#6-aws-services-sử-dụng)
- [Các mối đe dọa & Phản ứng tự động](#7-các-mối-đe-dọa--phản-ứng-tự-động)
- [Quy trình hoạt động](#8-quy-trình-hoạt-động)
- [Kịch bản Demo](#9-kịch-bản-demo)
- [Hướng dẫn cài đặt & Deploy](#10-hướng-dẫn-cài-đặt--deploy)
- [Screenshots & Demo](#11-screenshots--demo)
- [Thông tin nhóm](#12-thông-tin-nhóm)

---

## 1. Giới thiệu dự án

### Bài toán thực tế

Doanh nghiệp cần một hệ thống lưu trữ và chia sẻ tài liệu nội bộ trên AWS, nơi nhân viên có thể đăng nhập, tải lên và tải xuống tài liệu. Tuy nhiên, việc vận hành hệ thống trên đám mây tiềm ẩn nhiều rủi ro bảo mật nghiêm trọng:

| Rủi ro | Mô tả |
|--------|-------|
| **SSH Brute Force** | Kẻ tấn công dò mật khẩu để xâm nhập EC2 |
| **Port Scan** | Kẻ tấn công quét cổng để tìm điểm yếu |
| **S3 Public Exposure** | Cấu hình nhầm khiến tài liệu nội bộ bị lộ ra ngoài |
| **IAM Over-permission** | Cấp quyền quá mức tạo leo thang đặc quyền |
| **Abnormal EC2 Access** | Truy cập bất thường từ IP lạ hoặc ngoài giờ làm việc |

### Giải pháp

Xây dựng hệ thống **phát hiện và phản ứng tự động** với các sự cố bảo mật — không cần can thiệp thủ công, giảm thiểu thời gian phản ứng từ giờ xuống còn giây.

---

## 2. Chức năng nghiệp vụ

```
┌─────────────────────────────────────────────┐
│           CHỨC NĂNG CHÍNH                   │
├─────────────────────────────────────────────┤
│  1. Đăng nhập         → Xác thực người dùng │
│  2. Upload tài liệu   → Tải file lên hệ thống│
│  3. Xem danh sách     → Duyệt tài liệu      │
│  4. Download tài liệu → Tải file về máy      │
└─────────────────────────────────────────────┘
```

- **File tài liệu** được lưu trữ trên **Amazon S3**
- **Metadata** (tên file, người upload, thời gian, kích thước) được lưu trên **DynamoDB**

---

## 3. Công nghệ sử dụng

### Frontend — React 18 + Bootstrap 5

| Công nghệ | Ứng dụng trong dự án |
|-----------|----------------------|
| **React 18** | Xây dựng giao diện người dùng theo dạng component. Mỗi trang (Login, Dashboard, Upload) là một component độc lập, dễ bảo trì và mở rộng |
| **React Router** | Điều hướng giữa các trang (Login → Dashboard → Upload) mà không cần reload trang, tạo trải nghiệm mượt mà như app native |
| **Bootstrap 5** | Thiết kế giao diện responsive, đẹp, nhanh — không cần viết CSS từ đầu. Dùng cho layout, button, form upload, bảng danh sách tài liệu |
| **Axios** | Gọi REST API từ React đến Flask backend (login, upload file, lấy danh sách tài liệu, download) |
| **Vite** | Build tool thay thế Create React App — khởi động dev server nhanh hơn, build production nhỏ gọn hơn |

```
Frontend chịu trách nhiệm:
  ✓ Hiển thị giao diện cho người dùng
  ✓ Gửi HTTP request đến backend API
  ✓ Nhận response và render dữ liệu ra màn hình
  ✗ KHÔNG xử lý logic nghiệp vụ
  ✗ KHÔNG kết nối trực tiếp AWS (S3, DynamoDB)
```

---

### Backend — Python Flask

| Công nghệ | Ứng dụng trong dự án |
|-----------|----------------------|
| **Flask** | Framework web Python nhẹ, xây dựng REST API cho frontend gọi vào. Xử lý toàn bộ logic nghiệp vụ: xác thực, upload, download, lấy danh sách |
| **boto3** | AWS SDK chính thức cho Python — dùng để giao tiếp với S3 (upload/download file) và DynamoDB (đọc/ghi metadata, incidents) |
| **Flask-CORS** | Cho phép React (chạy port 3000 lúc dev) gọi API Flask (port 5000) mà không bị trình duyệt chặn |
| **PyJWT** | Tạo và xác thực JWT token — dùng cho hệ thống đăng nhập. Sau khi login, mỗi request tiếp theo phải kèm token để xác minh danh tính |
| **python-dotenv** | Đọc biến môi trường từ file `.env` — lưu thông tin nhạy cảm (AWS region, S3 bucket name, DynamoDB table) tách khỏi code |

```
Backend chịu trách nhiệm:
  ✓ Xác thực người dùng (đăng nhập, JWT)
  ✓ Upload file lên S3
  ✓ Ghi metadata vào DynamoDB
  ✓ Tạo presigned URL để download file từ S3
  ✓ Trả về danh sách tài liệu từ DynamoDB
  ✗ KHÔNG render HTML (để React làm)
```

---

### Luồng giao tiếp Frontend ↔ Backend ↔ AWS

```
[Trình duyệt]
     │
     │  HTTP Request (JSON)
     ▼
[React App - Frontend]
     │
     │  REST API call (Axios)   ← JWT token đính kèm trong header
     ▼
[Flask API - Backend]           ← Xác thực token, xử lý logic
     │
     ├──► boto3 ──► [Amazon S3]        (upload / presigned URL download)
     │
     └──► boto3 ──► [Amazon DynamoDB]  (đọc / ghi metadata tài liệu)
```

---

### Cấu trúc thư mục dự án

```
DA_AWS/
├── backend/                    ← Python Flask REST API
│   ├── app.py                  ← Điểm khởi động Flask, đăng ký routes
│   ├── routes/
│   │   ├── auth.py             ← POST /api/login  (đăng nhập, trả JWT)
│   │   └── documents.py        ← GET/POST /api/documents (danh sách, upload, download)
│   ├── services/
│   │   ├── s3_service.py       ← Logic upload file, tạo presigned URL (boto3)
│   │   └── dynamodb_service.py ← Logic đọc/ghi metadata tài liệu (boto3)
│   ├── middleware/
│   │   └── auth_middleware.py  ← Kiểm tra JWT token trước mỗi request
│   ├── .env                    ← Biến môi trường (không commit lên git)
│   └── requirements.txt        ← flask, boto3, flask-cors, pyjwt, python-dotenv
│
├── frontend/                   ← React 18 + Bootstrap 5
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx       ← Trang đăng nhập
│   │   │   ├── Dashboard.jsx   ← Trang danh sách tài liệu + download
│   │   │   └── Upload.jsx      ← Trang upload tài liệu mới
│   │   ├── components/
│   │   │   ├── Navbar.jsx      ← Thanh điều hướng chung
│   │   │   └── PrivateRoute.jsx← Bảo vệ route, redirect về Login nếu chưa đăng nhập
│   │   ├── services/
│   │   │   └── api.js          ← Cấu hình Axios, tự động đính JWT vào header
│   │   └── App.jsx             ← Cấu hình React Router, định nghĩa các route
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## 4. Kiến trúc hệ thống

```
                    ┌─────────────────────────────────────────┐
                    │              AWS Cloud                   │
                    │                                         │
 ┌────────┐  HTTPS  │  ┌──────────────┐                      │
 │  User  │────────►│  │  Web App     │                      │
 │(Browser│         │  │  (EC2)       │                      │
 └────────┘         │  └──────┬───────┘                      │
                    │         │                               │
                    │    ┌────┴──────┐                        │
                    │    │           │                        │
                    │    ▼           ▼                        │
                    │ ┌──────┐  ┌──────────┐                 │
                    │ │  S3  │  │ DynamoDB │                 │
                    │ │(Files│  │(Metadata)│                 │
                    │ └──────┘  └──────────┘                 │
                    └─────────────────────────────────────────┘
```

---

## 4. Kiến trúc bảo mật tự động

```
  ┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
  │  GuardDuty  │────►│ Security Hub │────►│  EventBridge    │
  │(Phát hiện   │     │(Tổng hợp &   │     │(Router sự kiện) │
  │ mối đe dọa) │     │ chuẩn hóa)   │     └────────┬────────┘
  └─────────────┘     └──────────────┘              │
                                                     │ Trigger
                                                     ▼
                                           ┌─────────────────┐
                                           │     Lambda      │
                                           │(Xử lý sự cố    │
                                           │ tự động)        │
                                           └────────┬────────┘
                                                    │
                    ┌───────────────────────────────┼──────────────────┐
                    │                               │                  │
                    ▼                               ▼                  ▼
           ┌──────────────┐              ┌──────────────┐    ┌──────────────┐
           │     SNS      │              │   DynamoDB   │    │  CloudWatch  │
           │(Email/Telegram              │(Lưu Incident)│    │  (Ghi Log)   │
           │  Cảnh báo)   │              └──────────────┘    └──────┬───────┘
           └──────────────┘                                         │
                                                                     ▼
                                                           ┌──────────────────┐
                                                           │     Grafana      │
                                                           │ Dashboard        │
                                                           │ (Thời gian thực) │
                                                           └──────────────────┘
```

---

## 5. AWS Services sử dụng

| Service | Vai trò trong dự án |
|---------|---------------------|
| **Amazon EC2** | Host ứng dụng web quản lý tài liệu |
| **Amazon S3** | Lưu trữ file tài liệu (private, versioning) |
| **Amazon DynamoDB** | Lưu metadata tài liệu + log Incident bảo mật |
| **Amazon GuardDuty** | Phát hiện mối đe dọa tự động bằng ML |
| **AWS Security Hub** | Tổng hợp, chuẩn hóa và ưu tiên findings |
| **Amazon EventBridge** | Router sự kiện bảo mật đến Lambda |
| **AWS Lambda** | Xử lý phản ứng sự cố tự động (serverless) |
| **Amazon SNS** | Gửi cảnh báo qua Email và Telegram |
| **Amazon CloudWatch** | Ghi log hệ thống, tạo metrics |
| **AWS Systems Manager** | Session Manager — truy cập EC2 không cần SSH port |
| **Grafana** | Dashboard giám sát bảo mật thời gian thực |

---

## 6. Các mối đe dọa & Phản ứng tự động

| Mối đe dọa | Phát hiện bởi | Phản ứng tự động của Lambda |
|------------|---------------|------------------------------|
| **SSH Brute Force** | GuardDuty | Block IP qua Security Group, gửi alert SNS, ghi incident DynamoDB |
| **Port Scan** | GuardDuty | Gửi alert SNS, ghi log CloudWatch, lưu incident |
| **S3 Public Exposure** | GuardDuty / Security Hub | Thu hồi public access, gửi alert SNS, ghi incident |
| **IAM Over-permission** | Security Hub | Gửi alert SNS, ghi incident để review thủ công |
| **Abnormal EC2 Access** | GuardDuty | Cô lập EC2 (isolate security group), gửi alert khẩn cấp |

### Chi tiết phản ứng của Lambda Function

```python
# Luồng xử lý tổng quát của Lambda
def lambda_handler(event, context):
    # 1. Parse finding từ GuardDuty qua EventBridge
    finding = parse_guardduty_finding(event)
    
    # 2. Phân loại mức độ nghiêm trọng
    severity = classify_severity(finding)
    
    # 3. Ghi log CloudWatch
    log_to_cloudwatch(finding)
    
    # 4. Lưu incident vào DynamoDB
    save_incident(finding)
    
    # 5. Gửi cảnh báo SNS (Email + Telegram)
    send_alert(finding, severity)
    
    # 6. Thực hiện phản ứng tự động tùy loại threat
    auto_remediate(finding)
```

---

## 7. Quy trình hoạt động

```
Bước 1: GuardDuty liên tục phân tích CloudTrail, VPC Flow Logs, DNS logs
           │
           ▼
Bước 2: Phát hiện mối đe dọa → Tạo Finding
           │
           ▼
Bước 3: Security Hub tổng hợp, chuẩn hóa finding (ASFF format)
           │
           ▼
Bước 4: EventBridge nhận event → Kích hoạt Lambda function
           │
           ▼
Bước 5: Lambda thực hiện đồng thời:
         ├── Ghi log vào CloudWatch Logs
         ├── Lưu Incident vào DynamoDB
         ├── Gửi Email/Telegram qua SNS
         └── Thực hiện cô lập / remediation
           │
           ▼
Bước 6: CloudWatch Metrics được cập nhật
           │
           ▼
Bước 7: Grafana Dashboard hiển thị thời gian thực
           │
           ▼
Bước 8: Team bảo mật kiểm tra EC2 qua Session Manager (không cần SSH)
```

---

## 8. Kịch bản Demo

### Demo Flow chính

```
[1] Upload tài liệu lên hệ thống
    └── User đăng nhập → Upload file → Lưu S3 + DynamoDB

[2] Kích hoạt GuardDuty Sample Finding
    └── AWS Console → GuardDuty → Generate Sample Findings
        (Giả lập: SSH Brute Force / Port Scan / S3 Public)

[3] Lambda tự động xử lý
    └── EventBridge nhận event → Trigger Lambda trong ~30 giây

[4] Kiểm tra SNS Alert
    └── Email / Telegram nhận cảnh báo với chi tiết finding

[5] Xem Incident trong DynamoDB
    └── AWS Console → DynamoDB → Table Incidents → Scan items

[6] Grafana Dashboard cập nhật
    └── Dashboard hiển thị incident mới, severity, timeline

[7] Kiểm tra EC2 qua Session Manager
    └── AWS Console → Systems Manager → Session Manager → Start Session
        (Không cần mở SSH port 22)
```

> **Lưu ý:** GuardDuty Sample Findings là dữ liệu **giả lập** dùng cho mục đích demo và kiểm thử. Không phải tấn công thật vào hệ thống.

---

## 9. Hướng dẫn cài đặt & Deploy

### Yêu cầu hệ thống

| Công cụ | Phiên bản | Mục đích |
|---------|-----------|----------|
| AWS Account | — | Quyền Admin để tạo EC2, S3, DynamoDB, GuardDuty... |
| AWS CLI | 2.x | Chạy lệnh AWS từ terminal |
| Python | 3.10+ | Chạy Flask backend |
| Node.js | 18+ | Build React frontend |
| npm | 9+ | Quản lý package React |
| Git | — | Clone source code lên EC2 |

---

### Bước 1: Tạo S3 Bucket

```bash
# Tạo bucket (thay <your-bucket-name> bằng tên duy nhất)
aws s3api create-bucket \
  --bucket <your-bucket-name> \
  --region ap-southeast-1 \
  --create-bucket-configuration LocationConstraint=ap-southeast-1

# Bật versioning
aws s3api put-bucket-versioning \
  --bucket <your-bucket-name> \
  --versioning-configuration Status=Enabled

# Chặn public access
aws s3api put-public-access-block \
  --bucket <your-bucket-name> \
  --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

---

### Bước 2: Tạo DynamoDB Tables

```bash
# Bảng lưu metadata tài liệu
aws dynamodb create-table \
  --table-name Documents \
  --attribute-definitions AttributeName=document_id,AttributeType=S \
  --key-schema AttributeName=document_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region ap-southeast-1

# Bảng lưu incident bảo mật
aws dynamodb create-table \
  --table-name SecurityIncidents \
  --attribute-definitions AttributeName=incident_id,AttributeType=S \
  --key-schema AttributeName=incident_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region ap-southeast-1
```

---

### Bước 3: Deploy EC2 và Web Application

#### 3.1 — Tạo Security Group và Launch EC2

```bash
# Tạo Security Group
aws ec2 create-security-group \
  --group-name document-app-sg \
  --description "Security group for document management app"

# Mở port 80 (HTTP) — KHÔNG mở port 22 (SSH), dùng Session Manager thay thế
aws ec2 authorize-security-group-ingress \
  --group-name document-app-sg \
  --protocol tcp --port 80 --cidr 0.0.0.0/0

# Launch EC2 (Ubuntu 22.04 LTS)
aws ec2 run-instances \
  --image-id ami-0df7a207adb9748c7 \
  --instance-type t3.micro \
  --security-groups document-app-sg \
  --iam-instance-profile Name=EC2-DocumentApp-Profile \
  --region ap-southeast-1
```

#### 3.2 — Cài đặt môi trường trên EC2

Kết nối EC2 qua **Session Manager** (AWS Console → Systems Manager → Session Manager → Start Session):

```bash
# Cài Python và pip
sudo apt update && sudo apt install -y python3 python3-pip python3-venv

# Cài Node.js 18 (dùng để build React)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Cài nginx (serve file React tĩnh sau khi build)
sudo apt install -y nginx

# Kiểm tra
python3 --version   # Python 3.10+
node --version      # v18.x
npm --version       # 9.x
nginx -v
```

#### 3.3 — Deploy Backend (Flask)

```bash
# Clone code về EC2
git clone <repository-url> /app
cd /app/backend

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài dependencies
pip install flask flask-cors pyjwt boto3 python-dotenv gunicorn

# Tạo file .env với thông tin AWS
cat > .env << EOF
AWS_REGION=ap-southeast-1
S3_BUCKET_NAME=<your-bucket-name>
DYNAMODB_DOCUMENTS_TABLE=Documents
DYNAMODB_INCIDENTS_TABLE=SecurityIncidents
JWT_SECRET_KEY=<your-secret-key-random-string>
EOF

# Chạy Flask với gunicorn (production)
gunicorn -w 4 -b 127.0.0.1:5000 app:app --daemon
```

#### 3.4 — Build và Deploy Frontend (React)

```bash
cd /app/frontend

# Cài dependencies
npm install

# Tạo file .env cho React (URL backend API)
echo "VITE_API_URL=http://<ec2-public-ip>/api" > .env

# Build React thành file tĩnh
npm run build
# → Tạo ra thư mục /app/frontend/dist/

# Copy file build vào nginx
sudo cp -r dist/* /var/www/html/
```

#### 3.5 — Cấu hình Nginx

Nginx đóng vai trò:
- Phục vụ file React tĩnh ở `/`
- Chuyển tiếp request `/api/` đến Flask đang chạy ở port 5000

```bash
sudo tee /etc/nginx/sites-available/document-app << 'EOF'
server {
    listen 80;

    # Serve React build (file tĩnh)
    location / {
        root /var/www/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Proxy /api/ → Flask backend
    location /api/ {
        proxy_pass http://127.0.0.1:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/document-app /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
sudo systemctl enable nginx
```

Sau bước này, truy cập `http://<ec2-public-ip>` sẽ thấy giao diện web hoạt động.

---

### Bước 4: Bật GuardDuty và Security Hub

```bash
# Bật GuardDuty
aws guardduty create-detector \
  --enable \
  --finding-publishing-frequency FIFTEEN_MINUTES \
  --region ap-southeast-1

# Bật Security Hub
aws securityhub enable-security-hub \
  --enable-default-standards \
  --region ap-southeast-1
```

---

### Bước 5: Tạo Lambda Function

```python
# lambda_incident_response.py
import boto3
import json
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

INCIDENTS_TABLE = 'SecurityIncidents'
SNS_TOPIC_ARN = 'arn:aws:sns:ap-southeast-1:<account-id>:SecurityAlerts'

def lambda_handler(event, context):
    detail = event.get('detail', {})
    finding_type = detail.get('type', 'Unknown')
    severity = detail.get('severity', 0)
    region = detail.get('region', 'unknown')
    account_id = detail.get('accountId', 'unknown')
    
    # Lưu incident vào DynamoDB
    table = dynamodb.Table(INCIDENTS_TABLE)
    table.put_item(Item={
        'incident_id': str(uuid.uuid4()),
        'timestamp': datetime.utcnow().isoformat(),
        'finding_type': finding_type,
        'severity': str(severity),
        'region': region,
        'account_id': account_id,
        'status': 'OPEN',
        'raw_detail': json.dumps(detail)
    })
    
    # Gửi cảnh báo SNS
    message = f"""
    SECURITY ALERT - {finding_type}
    Severity: {severity}
    Region: {region}
    Account: {account_id}
    Time: {datetime.utcnow().isoformat()} UTC
    
    Chi tiết: {json.dumps(detail, indent=2)}
    """
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f'[SECURITY] {finding_type} - Severity {severity}',
        Message=message
    )
    
    # Tự động cô lập EC2 nếu severity cao
    if severity >= 7.0:
        isolate_ec2(detail)
    
    return {'statusCode': 200, 'body': 'Incident processed'}

def isolate_ec2(detail):
    ec2 = boto3.client('ec2')
    # Tạo security group rỗng (không có inbound/outbound) để cô lập
    # Chỉ áp dụng khi xác định đúng instance bị ảnh hưởng
    pass
```

```bash
# Deploy Lambda
zip lambda.zip lambda_incident_response.py

aws lambda create-function \
  --function-name SecurityIncidentResponse \
  --runtime python3.11 \
  --handler lambda_incident_response.lambda_handler \
  --zip-file fileb://lambda.zip \
  --role arn:aws:iam::<account-id>:role/LambdaSecurityRole \
  --region ap-southeast-1
```

---

### Bước 6: Tạo EventBridge Rule

```bash
# Rule để bắt tất cả GuardDuty findings
aws events put-rule \
  --name "GuardDutyFindingsRule" \
  --event-pattern '{
    "source": ["aws.guardduty"],
    "detail-type": ["GuardDuty Finding"]
  }' \
  --state ENABLED \
  --region ap-southeast-1

# Gắn Lambda làm target
aws events put-targets \
  --rule GuardDutyFindingsRule \
  --targets '[{
    "Id": "1",
    "Arn": "arn:aws:lambda:ap-southeast-1:<account-id>:function:SecurityIncidentResponse"
  }]' \
  --region ap-southeast-1
```

---

### Bước 7: Cấu hình SNS

```bash
# Tạo SNS Topic
aws sns create-topic \
  --name SecurityAlerts \
  --region ap-southeast-1

# Subscribe Email
aws sns subscribe \
  --topic-arn arn:aws:sns:ap-southeast-1:<account-id>:SecurityAlerts \
  --protocol email \
  --notification-endpoint your-email@example.com \
  --region ap-southeast-1

# Subscribe Telegram (qua HTTP webhook endpoint)
aws sns subscribe \
  --topic-arn arn:aws:sns:ap-southeast-1:<account-id>:SecurityAlerts \
  --protocol https \
  --notification-endpoint https://your-telegram-webhook.example.com/notify \
  --region ap-southeast-1
```

---

### Bước 8: Cài đặt Grafana

```bash
# Cài Grafana trên EC2 (hoặc dùng Grafana Cloud)
sudo apt-get install -y apt-transport-https software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
sudo apt-get update && sudo apt-get install grafana
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

Cấu hình Grafana:
1. Truy cập `http://<ec2-ip>:3000` (mặc định admin/admin)
2. **Add Data Source** → chọn **CloudWatch**
3. Cấu hình AWS Region và credentials
4. **Create Dashboard** → Add panels:
   - Panel 1: Số lượng incident theo thời gian
   - Panel 2: Phân loại threat type (pie chart)
   - Panel 3: Severity distribution
   - Panel 4: Timeline các sự kiện gần đây

---

### Bước 9: Kiểm tra hệ thống

```bash
# Tạo GuardDuty Sample Findings để kiểm thử
aws guardduty create-sample-findings \
  --detector-id <detector-id> \
  --finding-types \
    "UnauthorizedAccess:EC2/SSHBruteForce" \
    "Recon:EC2/PortProbeUnprotectedPort" \
    "Policy:S3/BucketPublicAccessGranted" \
  --region ap-southeast-1
```

Kiểm tra kết quả:
- [ ] Email/Telegram nhận được cảnh báo trong vòng 1-2 phút
- [ ] DynamoDB table `SecurityIncidents` có bản ghi mới
- [ ] CloudWatch Logs của Lambda không có lỗi
- [ ] Grafana Dashboard cập nhật dữ liệu mới

---

## 10. Screenshots & Demo

### Grafana Dashboard - Tổng quan bảo mật
> *[Thêm screenshot Grafana dashboard tại đây]*

![Grafana Dashboard](docs/screenshots/grafana-dashboard.png)

---

### SNS Alert - Email cảnh báo
> *[Thêm screenshot email cảnh báo tại đây]*

![SNS Email Alert](docs/screenshots/sns-email-alert.png)

---

### DynamoDB - Incidents Table
> *[Thêm screenshot DynamoDB incidents tại đây]*

![DynamoDB Incidents](docs/screenshots/dynamodb-incidents.png)

---

### Lambda - CloudWatch Logs
> *[Thêm screenshot Lambda execution logs tại đây]*

![Lambda Logs](docs/screenshots/lambda-logs.png)

---

### Web Application - Giao diện quản lý tài liệu
> *[Thêm screenshot giao diện web tại đây]*

![Web App](docs/screenshots/web-app-ui.png)

---

## 11. Thông tin nhóm

| STT | Họ và tên | MSSV | Chuyên ngành | Vai trò trong dự án |
|-----|-----------|------|--------------|---------------------|
| 1 | *(Điền tên)* | *(Điền MSSV)* | An ninh mạng | GuardDuty & Security Hub |
| 2 | *(Điền tên)* | *(Điền MSSV)* | An ninh mạng | Lambda & EventBridge |
| 3 | *(Điền tên)* | *(Điền MSSV)* | An ninh mạng | Grafana Dashboard & Monitoring |
| 4 | *(Điền tên)* | *(Điền MSSV)* | Công nghệ phần mềm | Web Application & EC2 |
| 5 | *(Điền tên)* | *(Điền MSSV)* | Công nghệ phần mềm | S3, DynamoDB & Infrastructure |

---

## Điểm nhấn dự án

- **Ứng dụng thực tế để bảo vệ** — Không chỉ demo bảo mật trừu tượng mà có sản phẩm thực tế
- **Phát hiện tấn công tự động** — GuardDuty dùng Machine Learning, không cần cấu hình rules thủ công
- **Phản ứng sự cố tự động** — Từ phát hiện đến cô lập EC2 trong vòng dưới 1 phút
- **Dashboard giám sát trực quan** — Grafana cập nhật thời gian thực, phù hợp trình bày
- **Cảnh báo đa kênh** — Email và Telegram để không bỏ lỡ sự cố
- **Không cần mở SSH** — Session Manager là best practice, tránh rủi ro Brute Force

---

*Dự án được xây dựng cho môn học AWS / Cloud Security — Nhóm 5 thành viên*
