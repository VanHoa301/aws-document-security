# Hướng dẫn sử dụng — Phần Member #4 (Web Application & EC2)

> **Phụ trách:** Member #4 — Công nghệ phần mềm  
> **Nội dung:** React 18 + Flask REST API + Deploy EC2  
> **EC2 Public IP:** `http://47.128.68.77` (xem lưu ý bên dưới)

---

## Mục lục

1. [Cấu trúc thư mục](#1-cấu-trúc-thư-mục)
2. [Yêu cầu môi trường](#2-yêu-cầu-môi-trường)
3. [Chạy local (phát triển)](#3-chạy-local-phát-triển)
4. [Biến môi trường](#4-biến-môi-trường)
5. [API Endpoints](#5-api-endpoints)
6. [Quản lý EC2](#6-quản-lý-ec2)
7. [Re-deploy lên EC2](#7-re-deploy-lên-ec2)
8. [Tài khoản demo](#8-tài-khoản-demo)

---

## 1. Cấu trúc thư mục

```
DA_AWS/
├── backend/
│   ├── app.py                  # Flask entry point
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Mẫu biến môi trường (copy → .env)
│   ├── middleware/
│   │   └── auth_middleware.py  # Kiểm tra JWT token
│   ├── routes/
│   │   ├── auth.py             # POST /api/login
│   │   └── documents.py        # CRUD tài liệu
│   └── services/
│       ├── s3_service.py       # Upload/Download/Delete S3
│       └── dynamodb_service.py # Ghi/Đọc metadata DynamoDB
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Router chính
│   │   ├── services/api.js     # Axios + JWT interceptor
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   └── PrivateRoute.jsx
│   │   └── pages/
│   │       ├── Login.jsx
│   │       ├── Dashboard.jsx
│   │       └── Upload.jsx
│   ├── vite.config.js          # Proxy /api → Flask (dev)
│   └── package.json
└── WorkFlow/
    └── Member4_Guide.md        # File này
```

---

## 2. Yêu cầu môi trường

| Công cụ | Phiên bản tối thiểu | Kiểm tra |
|---------|---------------------|----------|
| Python | 3.10+ | `python3 --version` |
| Node.js | 20.19+ | `node --version` |
| npm | 10+ | `npm --version` |
| AWS CLI | 2.x | `aws --version` |

**AWS CLI cần được cấu hình** với access key có quyền S3 + DynamoDB:
```bash
aws configure
# AWS Access Key ID: <key của nhóm>
# AWS Secret Access Key: <secret của nhóm>
# Default region name: ap-southeast-1
# Default output format: json
```

---

## 3. Chạy local (phát triển)

### Backend (Flask)

```bash
cd backend

# Tạo virtualenv và cài dependencies
python3 -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt

# Tạo file .env từ mẫu
copy .env.example .env      # Windows
cp .env.example .env        # Linux/Mac
# Sau đó sửa .env với đúng giá trị bucket/table/secret

# Chạy Flask
python app.py
# → Flask chạy tại http://127.0.0.1:5000
```

### Frontend (React)

```bash
cd frontend
npm install
npm run dev
# → React chạy tại http://localhost:5173
```

> **Lưu ý:** Vite đã được cấu hình proxy `/api` → `http://127.0.0.1:5000`.  
> Không cần đổi baseURL, frontend tự động gọi đúng Flask khi dev.

### Kiểm tra nhanh

Mở trình duyệt → `http://localhost:5173` → đăng nhập → upload file → xem danh sách.

---

## 4. Biến môi trường

File `backend/.env` (KHÔNG commit file này lên git):

```env
AWS_REGION=ap-southeast-1
S3_BUCKET_NAME=da-aws-documents-nhom5
DYNAMODB_DOCUMENTS_TABLE=Documents
DYNAMODB_INCIDENTS_TABLE=SecurityIncidents
JWT_SECRET_KEY=<chuỗi bí mật tối thiểu 32 ký tự>
```

> **Member #5 (Infrastructure):** Cung cấp tên S3 bucket và DynamoDB table chính xác.

---

## 5. API Endpoints

Base URL (local): `http://127.0.0.1:5000/api`  
Base URL (EC2): `http://47.128.68.77/api`

| Method | Endpoint | Auth | Mô tả |
|--------|----------|------|-------|
| POST | `/api/login` | Không | Đăng nhập, trả JWT token |
| GET | `/api/documents` | JWT | Danh sách tài liệu |
| POST | `/api/documents/upload` | JWT | Upload file lên S3 |
| GET | `/api/documents/download/<id>` | JWT | Lấy presigned URL download |
| DELETE | `/api/documents/<id>` | JWT | Xóa file khỏi S3 + DynamoDB |

**Header xác thực:**
```
Authorization: Bearer <jwt_token>
```

**Test nhanh bằng curl (Git Bash):**
```bash
# Đăng nhập
curl -X POST http://127.0.0.1:5000/api/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"admin123"}'

# Lấy danh sách (thay TOKEN bằng token vừa nhận)
curl http://127.0.0.1:5000/api/documents \
  -H 'Authorization: Bearer TOKEN'
```

---

## 6. Quản lý EC2

### EC2 có tốn tiền khi đang chạy không?

**Có.** t3.micro tốn ~$0.0104/giờ (~$7.5/tháng khi chạy liên tục).

### Dừng EC2 để tiết kiệm credit

1. Vào **AWS Console → EC2 → Instances**
2. Chọn instance `DA-AWS-WebApp` (ID: `i-0a1f224b7a1485455`)
3. **Instance state → Stop instance**
4. Xác nhận Stop

> ✅ **Stop** (dừng): Giữ nguyên data, chỉ tốn phí lưu trữ EBS (~$0.10/GB/tháng)  
> ❌ **Terminate** (xóa): Mất toàn bộ — KHÔNG bấm cái này

### Khởi động lại EC2

1. Vào EC2 Console → chọn instance → **Start instance**
2. Chờ ~1 phút để instance Running
3. **Lấy IP mới** (IP có thể thay đổi sau mỗi lần Start)
4. Kết nối qua **Session Manager** → chạy lại backend:

```bash
cd /tmp/backend && venv/bin/gunicorn -w 2 -b 127.0.0.1:5000 app:app --daemon --log-file /tmp/gunicorn.log
```

5. Kiểm tra nginx đang chạy:
```bash
sudo systemctl status nginx
# Nếu không chạy: sudo systemctl start nginx
```

---

## 7. Re-deploy lên EC2

Khi có thay đổi code cần đẩy lên EC2:

### Bước 1 — Nén và upload lên S3 (máy local, PowerShell)

```powershell
# Nén thư mục (bỏ node_modules và venv)
Compress-Archive -Path "C:\Users\admin\OneDrive\Desktop\DA_AWS\backend","C:\Users\admin\OneDrive\Desktop\DA_AWS\frontend\src","C:\Users\admin\OneDrive\Desktop\DA_AWS\frontend\package.json","C:\Users\admin\OneDrive\Desktop\DA_AWS\frontend\vite.config.js","C:\Users\admin\OneDrive\Desktop\DA_AWS\frontend\index.html" -DestinationPath "C:\Users\admin\OneDrive\Desktop\app.zip" -Force

# Upload lên S3
aws s3 cp "C:\Users\admin\OneDrive\Desktop\app.zip" s3://da-aws-documents-nhom5/app.zip
```

### Bước 2 — Tải và giải nén trên EC2 (Session Manager)

```bash
# Dừng gunicorn cũ
pkill -f gunicorn

# Tải code mới
aws s3 cp s3://da-aws-documents-nhom5/app.zip /tmp/app.zip

# Xóa và giải nén
rm -rf /tmp/backend /tmp/frontend
cd /tmp && unzip -o app.zip

# Cài dependencies backend
cd /tmp/backend && venv/bin/pip install -r requirements.txt

# Build frontend
cd /tmp/frontend && npm install && npm run build
sudo cp -r /tmp/frontend/dist/* /var/www/html/

# Khởi động lại backend
cd /tmp/backend && venv/bin/gunicorn -w 2 -b 127.0.0.1:5000 app:app --daemon --log-file /tmp/gunicorn.log

sudo systemctl restart nginx
```

---

## 8. Tài khoản demo

| Username | Password | Vai trò |
|----------|----------|---------|
| `admin` | `admin123` | Quản trị viên |
| `user1` | `password1` | Người dùng thường |

> **Lưu ý bảo mật:** Đây là tài khoản hardcoded trong `routes/auth.py` phục vụ demo.  
> Trong production thực tế cần thay bằng xác thực từ database.

---

## Liên hệ

Câu hỏi về phần Web App → liên hệ **Member #4**


