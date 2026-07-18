---
title: "Cấu hình Lambda và SNS"
date: 2026-07-14
weight: 2
chapter: false
pre: " <b> 5.4.2 </b> "
---

# Cấu hình Lambda và SNS

#### Kiểm tra SNS topic

1. Mở **Amazon SNS → Topics**.
2. Chọn topic `SecurityAlerts`.
3. Tạo subscription kiểu **Email** nếu chưa có.
4. Mở email và chọn liên kết **Confirm subscription**.

Chỉ subscription có trạng thái `Confirmed` mới nhận được cảnh báo.

#### Kiểm tra Lambda

1. Mở **AWS Lambda → Functions → SecurityIncidentResponse**.
2. Chọn runtime Python và kiểm tra IAM execution role.
3. Trong **Configuration → Environment variables**, khai báo tên bảng incident và ARN của SNS topic nếu code đọc từ biến môi trường.
4. Trong **Monitor**, xác nhận CloudWatch log group `/aws/lambda/SecurityIncidentResponse` đã được tạo.

Lambda thực hiện các bước:

```text
Nhận EventBridge event
  → đọc finding ID, type, severity, resource và thời gian
  → ghi incident vào DynamoDB SecurityIncidents
  → publish thông báo đến SNS SecurityAlerts
  → ghi kết quả xử lý vào CloudWatch Logs
```

#### Quyền tối thiểu của Lambda

- `dynamodb:PutItem` trên bảng `SecurityIncidents`.
- `sns:Publish` trên topic `SecurityAlerts`.
- Quyền ghi CloudWatch Logs.
- Chỉ bổ sung quyền EC2/S3 khi thực sự triển khai hành động cô lập tự động.

{{% notice warning %}}
Không tự động cô lập hoặc thay đổi tài nguyên production chỉ dựa trên sample finding. Hành động có ảnh hưởng lớn cần điều kiện chặt chẽ, nhật ký kiểm toán và cơ chế phê duyệt phù hợp.
{{% /notice %}}
