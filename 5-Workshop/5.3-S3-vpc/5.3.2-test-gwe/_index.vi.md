---
title: "Triển khai và kiểm tra ứng dụng trên EC2"
date: 2026-07-14
weight: 2
chapter: false
pre: " <b> 5.3.2 </b> "
---

# Triển khai và kiểm tra ứng dụng trên EC2

#### Kết nối bằng Session Manager

1. Mở **AWS Systems Manager → Session Manager**.
2. Chọn **Start session** và chọn EC2 của ứng dụng.
3. Không cần mở inbound port 22 hoặc quản lý SSH key.

#### Cài backend

```bash
cd /app/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn --bind 127.0.0.1:5000 app:app
```

Trong triển khai thực tế, Gunicorn nên chạy bằng `systemd` để tự khởi động lại khi EC2 reboot.

#### Build frontend

```bash
cd /app/frontend
npm ci
npm run build
```

Cấu hình Nginx phục vụ thư mục `dist` và chuyển các request `/api` đến `http://127.0.0.1:5000`.

#### Kiểm tra chức năng

1. Truy cập địa chỉ website của EC2 và đăng nhập bằng tài khoản demo.
2. Tải lên một file hợp lệ nhỏ hơn 20 MB.
3. Mở trang danh sách và tìm tài liệu vừa tải lên.
4. Chọn **Download** và xác nhận presigned URL hoạt động.
5. Với tài khoản admin, kiểm tra chức năng xóa tài liệu.

Kiểm tra API trực tiếp trên EC2:

```bash
curl http://127.0.0.1:5000/api/health
sudo systemctl status nginx
```

#### Xác minh dữ liệu AWS

- Trong S3, object mới xuất hiện trong bucket `aws-s3-duanthuctap` và không public.
- Trong DynamoDB `Documents`, một bản ghi metadata tương ứng được tạo.
- Xóa bằng tài khoản admin phải loại bỏ cả S3 object và metadata.

{{% notice note %}}
Tài khoản demo đang được hard-code để phục vụ workshop. Môi trường production nên dùng Amazon Cognito hoặc một nhà cung cấp danh tính, HTTPS và cookie HttpOnly.
{{% /notice %}}
