# Member #4 — Web Application & EC2
### To-Do List | Phân công công việc

> **Chuyên ngành:** Công nghệ phần mềm
> **Phụ trách:** Xây dựng giao diện người dùng (React 18 + Bootstrap 5) và REST API backend (Python Flask), deploy toàn bộ ứng dụng lên EC2.

---

## Tiến độ tổng quan

| Giai đoạn | Nội dung | Trạng thái |
|-----------|----------|------------|
| Giai đoạn 1 | Chuẩn bị môi trường | ✅ Hoàn thành |
| Giai đoạn 2 | Backend Flask API | ✅ Hoàn thành |
| Giai đoạn 3 | Frontend React | ✅ Hoàn thành |
| Giai đoạn 4 | Deploy lên EC2 | ✅ Hoàn thành |
| Giai đoạn 5 | Kiểm thử & Tích hợp | 🔄 Đang làm |

> Cập nhật trạng thái: ⬜ Chưa bắt đầu → 🔄 Đang làm → ✅ Hoàn thành

---

## Giai đoạn 1 — Chuẩn bị môi trường (Local)

- [ ] Cài **Node.js 18+** và npm trên máy local
- [ ] Cài **Python 3.10+**, pip, virtualenv trên máy local
- [ ] Cài **Git** và **AWS CLI**, cấu hình `aws configure` (access key, region `ap-southeast-1`)
- [ ] Tạo cấu trúc thư mục project: `DA_AWS/frontend/` và `DA_AWS/backend/`
- [ ] Khởi tạo React project bằng Vite:
  ```bash
  npm create vite@latest frontend -- --template react
  ```
- [ ] Khởi tạo Flask project: tạo `backend/app.py` và `backend/requirements.txt`
- [ ] Tạo file `.gitignore` (loại trừ `node_modules/`, `venv/`, `.env`)

---

## Giai đoạn 2 — Backend Flask API

- [ ] Cài dependencies:
  ```bash
  pip install flask flask-cors pyjwt boto3 python-dotenv gunicorn
  ```
- [ ] Tạo file `backend/.env` với các biến môi trường:
  ```
  AWS_REGION=ap-southeast-1
  S3_BUCKET_NAME=<tên bucket do Member #5 tạo>
  DYNAMODB_DOCUMENTS_TABLE=Documents
  DYNAMODB_INCIDENTS_TABLE=SecurityIncidents
  JWT_SECRET_KEY=<chuỗi ngẫu nhiên bí mật>
  ```
- [ ] Viết `backend/services/s3_service.py`:
  - Hàm `upload_file(file, filename)` → upload lên S3
  - Hàm `generate_download_url(filename)` → tạo presigned URL (hết hạn sau 1 giờ)
- [ ] Viết `backend/services/dynamodb_service.py`:
  - Hàm `save_document_metadata(doc_id, filename, uploader, size)` → ghi vào DynamoDB
  - Hàm `list_documents()` → đọc danh sách tài liệu
- [ ] Viết `backend/middleware/auth_middleware.py`:
  - Decorator `@require_auth` kiểm tra JWT token trong header `Authorization: Bearer <token>`
- [ ] Viết `backend/routes/auth.py`:
  - `POST /api/login` → nhận username/password, trả JWT token
- [ ] Viết `backend/routes/documents.py`:
  - `GET /api/documents` → trả danh sách tài liệu từ DynamoDB
  - `POST /api/documents/upload` → nhận file, upload S3, ghi metadata DynamoDB
  - `GET /api/documents/download/<doc_id>` → trả presigned URL download
- [ ] Viết `backend/app.py`: đăng ký tất cả routes, cấu hình CORS
- [ ] Test toàn bộ API bằng **Postman** hoặc `curl` trên localhost

---

## Giai đoạn 3 — Frontend React

- [ ] Cài dependencies:
  ```bash
  npm install axios react-router-dom bootstrap
  ```
- [ ] Viết `frontend/src/services/api.js`:
  - Cấu hình Axios với `baseURL` trỏ đến Flask API
  - Interceptor tự động đính JWT token vào header mỗi request
- [ ] Viết `frontend/src/components/PrivateRoute.jsx`:
  - Kiểm tra token trong localStorage, redirect về `/login` nếu chưa đăng nhập
- [ ] Viết `frontend/src/components/Navbar.jsx`:
  - Thanh điều hướng: logo, link Dashboard, link Upload, nút Logout
- [ ] Viết `frontend/src/pages/Login.jsx`:
  - Form nhập username / password
  - Gọi `POST /api/login`, lưu token vào localStorage, chuyển sang Dashboard
- [ ] Viết `frontend/src/pages/Dashboard.jsx`:
  - Gọi `GET /api/documents`, hiển thị bảng danh sách tài liệu (tên, người upload, ngày, kích thước)
  - Nút **Download** cho từng tài liệu → gọi API lấy presigned URL rồi tự động tải xuống
- [ ] Viết `frontend/src/pages/Upload.jsx`:
  - Form chọn file (input type file)
  - Gọi `POST /api/documents/upload`, hiển thị thông báo thành công / lỗi
- [ ] Cấu hình React Router trong `frontend/src/App.jsx`:
  - Route `/login` → Login page (public)
  - Route `/` → Dashboard (bảo vệ bởi PrivateRoute)
  - Route `/upload` → Upload (bảo vệ bởi PrivateRoute)
- [ ] Import Bootstrap trong `frontend/src/main.jsx`:
  ```js
  import 'bootstrap/dist/css/bootstrap.min.css'
  ```
- [ ] Test toàn bộ giao diện trên **localhost** (React port 5173 ↔ Flask port 5000)

---

## Giai đoạn 4 — Deploy lên EC2

- [ ] Launch EC2 instance (Ubuntu 22.04 LTS, t3.micro) trên AWS Console
- [ ] Gắn **IAM Role** cho EC2 với quyền: `AmazonS3FullAccess`, `AmazonDynamoDBFullAccess`
- [ ] Tạo Security Group: mở port **80** (HTTP) — **không mở port 22** (dùng Session Manager)
- [ ] Kết nối EC2 qua **AWS Console → Systems Manager → Session Manager → Start Session**
- [ ] Cài đặt môi trường trên EC2:
  ```bash
  sudo apt update
  sudo apt install -y python3 python3-pip python3-venv nginx
  curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
  sudo apt install -y nodejs
  ```
- [ ] Clone code lên EC2: `git clone <repository-url> /app`
- [ ] Cài dependencies backend:
  ```bash
  cd /app/backend
  python3 -m venv venv && source venv/bin/activate
  pip install -r requirements.txt
  ```
- [ ] Tạo file `/app/backend/.env` trên EC2 với đúng giá trị bucket, table
- [ ] Chạy Flask bằng gunicorn (daemon):
  ```bash
  gunicorn -w 4 -b 127.0.0.1:5000 app:app --daemon
  ```
- [ ] Build React và copy vào nginx:
  ```bash
  cd /app/frontend && npm install && npm run build
  sudo cp -r dist/* /var/www/html/
  ```
- [ ] Cấu hình nginx: serve React tĩnh + proxy `/api/` → Flask port 5000
- [ ] Restart nginx: `sudo systemctl restart nginx`
- [ ] Mở trình duyệt, truy cập `http://<ec2-public-ip>` → kiểm tra ứng dụng chạy đúng

---

## Giai đoạn 5 — Kiểm thử & Tích hợp với nhóm

- [ ] Test luồng đầy đủ: **Đăng nhập → Upload file → Xem danh sách → Download file**
- [ ] Vào **AWS Console → S3** xác nhận file đã lưu đúng trong bucket
- [ ] Vào **AWS Console → DynamoDB → Table Documents** xác nhận metadata đã ghi đúng
- [ ] Phối hợp **Member #3** (Grafana): đảm bảo web app tạo đủ traffic để GuardDuty có dữ liệu
- [ ] Phối hợp **Member #5** (Infrastructure): xác nhận S3 bucket name và DynamoDB table name khớp với `.env`
- [ ] Chụp **screenshot** các trang Login, Dashboard, Upload để đưa vào phần demo
- [ ] Cập nhật ảnh vào `docs/screenshots/web-app-ui.png`

---

*Member #4 — Cập nhật tiến độ vào bảng tổng quan khi hoàn thành từng giai đoạn*
