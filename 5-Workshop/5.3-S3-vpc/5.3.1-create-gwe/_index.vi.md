---
title: "Cấu hình S3 và DynamoDB"
date: 2026-07-14
weight: 1
chapter: false
pre: " <b> 5.3.1 </b> "
---

# Cấu hình S3 và DynamoDB

#### Kiểm tra S3 bucket

1. Mở **Amazon S3 Console** tại Region Singapore.
2. Chọn bucket `aws-s3-duanthuctap`.
3. Trong **Permissions**, xác nhận **Block all public access** đang bật.
4. Trong **Properties**, bật Versioning nếu cần giữ lịch sử object.

Có thể kiểm tra bằng AWS CLI:

```bash
aws s3api get-public-access-block --bucket aws-s3-duanthuctap
aws s3api get-bucket-versioning --bucket aws-s3-duanthuctap
```

{{% notice info %}}
File được lưu private. Người dùng tải xuống thông qua presigned URL có thời hạn do Flask backend phát hành.
{{% /notice %}}

#### Kiểm tra hai bảng DynamoDB

1. Mở **DynamoDB → Tables**.
2. Kiểm tra bảng `Documents` có partition key `document_id` kiểu String.
3. Kiểm tra bảng `SecurityIncidents` có partition key `incident_id` kiểu String.
4. Chọn chế độ **On-demand** để phù hợp workload demo có lưu lượng không ổn định.

```bash
aws dynamodb describe-table --table-name Documents --region ap-southeast-1
aws dynamodb describe-table --table-name SecurityIncidents --region ap-southeast-1
```

Trạng thái của cả hai bảng phải là `ACTIVE`.

#### Dữ liệu tài liệu

Mỗi bản ghi trong `Documents` gồm các trường chính: mã tài liệu, tên file gốc, S3 object key, người tải lên, kích thước, loại file và thời gian tạo. Nội dung file không được lưu trong DynamoDB.
