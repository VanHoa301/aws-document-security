---
title: "Giới thiệu và kiến trúc"
date: 2026-07-14
weight: 1
chapter: false
pre: " <b> 5.1. </b> "
---

# Giới thiệu và kiến trúc

#### Bài toán

Doanh nghiệp cần lưu trữ và chia sẻ tài liệu nội bộ trên AWS nhưng vẫn phải kiểm soát truy cập, phát hiện hành vi bất thường và rút ngắn thời gian phản ứng khi có sự cố. Hệ thống được xây dựng để giải quyết đồng thời hai yêu cầu:

- Cung cấp ứng dụng web cho phép đăng nhập, tải lên, tìm kiếm và tải xuống tài liệu.
- Tự động tiếp nhận finding bảo mật, lưu incident, gửi cảnh báo và cung cấp dashboard giám sát.

#### Thành phần kiến trúc

| Thành phần | Vai trò trong hệ thống |
|---|---|
| Amazon EC2 | Chạy Nginx, React, Flask/Gunicorn, Grafana và CloudWatch Agent |
| Amazon S3 | Bucket `aws-s3-duanthuctap` lưu file tài liệu ở chế độ private |
| Amazon DynamoDB | Bảng `Documents` lưu metadata; `SecurityIncidents` lưu sự cố |
| GuardDuty và Security Hub | Phát hiện, tổng hợp và chuẩn hóa finding bảo mật |
| EventBridge | Rule `GuardDutyToSecurityIncident` chuyển finding đến Lambda |
| AWS Lambda | Hàm `SecurityIncidentResponse` xử lý sự cố |
| Amazon SNS | Topic `SecurityAlerts` gửi thông báo cho quản trị viên |
| CloudWatch | Thu thập metric, log ứng dụng, Nginx, hệ thống và Lambda |
| Grafana | Trực quan hóa tình trạng EC2, dịch vụ AWS và log bảo mật |
| Systems Manager | Truy cập EC2 và chuyển tiếp cổng Grafana mà không mở SSH công khai |
| VPC, Subnet, Internet Gateway, Route Table | Cung cấp mạng cho EC2 và luồng Internet |
| Security Group, ENI, Elastic IP | Kiểm soát mạng, cách ly instance và giữ endpoint backend cố định |
| IAM và STS | Role tối thiểu và credential tạm thời cho EC2, Lambda, Step Functions |
| Amazon CloudFront, OAC và WAF | Phân phối React qua HTTPS, giữ S3 private và chuyển `/api/*` tới backend |
| Amazon API Gateway | Endpoint callback phê duyệt cho Step Functions |
| AWS Step Functions | Điều phối phê duyệt QUARANTINE, STOP hoặc REJECT |
| AWS CloudTrail | Ghi dấu vết management API để kiểm toán |
| VPC Flow Logs | Ghi nhận network flow ACCEPT/REJECT |
| S3 Server Access Logging | Lưu request truy cập bucket tài liệu |
| AWS Config | Theo dõi thay đổi cấu hình và compliance |

#### Luồng quản lý tài liệu

1. Người dùng đăng nhập và nhận JWT có thời hạn.
2. React gửi file đến Flask API qua Nginx.
3. Backend kiểm tra loại file, kích thước và quyền truy cập.
4. File được đổi tên bằng UUID rồi tải lên S3.
5. Metadata được ghi vào bảng DynamoDB `Documents`.
6. Khi tải xuống, backend tạo presigned URL có thời hạn thay vì công khai object.

#### Luồng phản ứng sự cố

1. GuardDuty phân tích các nguồn telemetry và tạo finding.
2. EventBridge bắt sự kiện `GuardDuty Finding`.
3. Lambda phân tích loại, mức độ nghiêm trọng và tài nguyên bị ảnh hưởng.
4. Incident được ghi vào `SecurityIncidents`, log được ghi vào CloudWatch và cảnh báo được gửi đến SNS.
5. Quản trị viên theo dõi trên website hoặc Grafana và cập nhật trạng thái `OPEN`, `INVESTIGATING`, `RESOLVED`.

{{% notice note %}}
GuardDuty sample finding được dùng để kiểm thử an toàn. Đây là dữ liệu mô phỏng, không phải một cuộc tấn công thật vào hệ thống.
{{% /notice %}}
