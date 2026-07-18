---
title: "Giám sát bằng CloudWatch và Grafana"
date: 2026-07-14
weight: 5
chapter: false
pre: " <b> 5.5. </b> "
---

# Giám sát hệ thống bằng CloudWatch và Grafana

#### Vai trò trong kiến trúc

**Amazon CloudWatch** là nơi lưu metric và log tập trung. **Grafana** kết nối tới CloudWatch bằng IAM role để truy vấn và trực quan hóa dữ liệu; Grafana không thay thế CloudWatch và không cần quyền thay đổi tài nguyên AWS.

Luồng dữ liệu:

```text
EC2 metrics ───────────────────────────────┐
CloudWatch Agent → Nginx/system logs ─────┤
Lambda/DynamoDB/S3/SNS/EventBridge metrics ├→ CloudWatch → Grafana
Lambda logs ──────────────────────────────┘
```

#### Chuẩn bị CloudWatch Agent

1. Gắn `CloudWatchAgentServerPolicy` hoặc policy tối thiểu tương đương vào IAM role của EC2.
2. Cài `amazon-cloudwatch-agent` trên EC2.
3. Cấu hình các log group:

```text
/document-app/nginx/access
/document-app/nginx/error
/document-app/system
/aws/lambda/SecurityIncidentResponse
```

4. Khởi động và bật tự chạy:

```bash
sudo systemctl enable amazon-cloudwatch-agent
sudo systemctl restart amazon-cloudwatch-agent
sudo systemctl status amazon-cloudwatch-agent
```

5. Mở CloudWatch Logs để xác nhận mỗi log group có log stream mới. Đặt retention 7 ngày cho môi trường lab.

#### Nguồn dữ liệu

Grafana sử dụng CloudWatch data source tại Region `ap-southeast-1`. IAM role của EC2/Grafana chỉ cần quyền đọc metric và log; không cần quyền thay đổi tài nguyên nghiệp vụ.

#### Dashboard dịch vụ AWS

Import file `grafana/aws-services-monitoring.json`. Dashboard theo dõi:

- Lambda `SecurityIncidentResponse`: Invocations, Errors, Duration, Throttles.
- DynamoDB `Documents`: read/write capacity đã tiêu thụ.
- DynamoDB `SecurityIncidents`: write capacity và SystemErrors.
- S3 `aws-s3-duanthuctap`: dung lượng bucket và số object.
- SNS `SecurityAlerts`: số thông báo gửi thành công/thất bại.
- EventBridge `GuardDutyToSecurityIncident`: Invocations và FailedInvocations.

{{% notice note %}}
Metric `BucketSizeBytes` và `NumberOfObjects` của S3 được cập nhật theo ngày nên có thể chưa hiển thị ngay sau khi upload.
{{% /notice %}}

#### Dashboard log bảo mật

Import file `grafana/security-logs-monitoring.json`, nhập AWS Account ID khi dashboard yêu cầu. Dashboard đọc các log group:

```text
/document-app/nginx/access
/document-app/nginx/error
/document-app/system
/aws/lambda/SecurityIncidentResponse
```

Các panel giúp theo dõi tổng HTTP request, phản hồi 4xx/5xx, Nginx access/error, system log và quá trình xử lý incident của Lambda.

#### Truy cập Grafana an toàn

Không mở public port 3000. EC2 phải là Systems Manager managed instance và máy cá nhân phải có Session Manager plugin. Chạy:

```bash
aws ssm start-session \
  --target i-0f86ac8ae3872226e \
  --document-name AWS-StartPortForwardingSession \
  --parameters '{"portNumber":["3000"],"localPortNumber":["3000"]}'
```

Giữ terminal hoạt động rồi mở `http://localhost:3000`. Trong Grafana, tạo CloudWatch data source tại `ap-southeast-1`, dùng IAM role của EC2 và bấm **Save & test**.

#### Import dashboard

1. Chọn **Dashboards → New → Import**.
2. Upload `grafana/aws-services-monitoring.json`, chọn CloudWatch data source.
3. Upload `grafana/security-logs-monitoring.json`, chọn data source và nhập AWS Account ID khi được hỏi.
4. Chọn **Last 1 hour** hoặc **Last 24 hours**, refresh `1m`.

#### Kiểm tra dashboard

1. Upload và download một tài liệu để tạo access log và metric DynamoDB/S3.
2. Sinh GuardDuty sample finding để tạo EventBridge, Lambda, SNS và incident metric.
3. Chọn time range phù hợp, ví dụ **Last 1 hour**, rồi refresh dashboard.
4. Xác nhận Lambda Errors, DynamoDB SystemErrors, EventBridge FailedInvocations và SNS Delivery Failures đều bằng 0.

#### Nhật ký kiểm toán liên quan

Workshop tổng thể còn sử dụng các nguồn bằng chứng sau; có thể điều tra trong CloudWatch/S3 và mở rộng thành panel Grafana:

| Dịch vụ | Bằng chứng |
|---|---|
| AWS CloudTrail | Management API events, trail lưu trong S3 |
| VPC Flow Logs | Network ACCEPT/REJECT theo ENI trong CloudWatch Logs |
| S3 Server Access Logging | Request truy cập bucket tài liệu trong bucket log riêng |
| AWS Config | Lịch sử cấu hình và compliance của EC2, Security Group, S3 |

#### Xử lý lỗi

| Triệu chứng | Cách kiểm tra |
|---|---|
| Tất cả panel `No data` | Region, quyền `cloudwatch:GetMetricData`, data source **Save & test** |
| Chỉ panel log không có dữ liệu | Account ID, tên log group, CloudWatch Agent và time range |
| S3 size/object trống | Storage metric cập nhật theo ngày; chọn **Last 7 days** |
| Lambda/EventBridge trống | Tạo GuardDuty sample finding và kiểm tra rule/workflow |
| Không mở được Grafana | `grafana-server`, trạng thái SSM và local port 3000 |

#### Đánh giá kết quả

Dashboard cung cấp một góc nhìn thống nhất từ hạ tầng, dịch vụ AWS đến log ứng dụng. Khi phát hiện lỗi, quản trị viên có thể đi từ panel Grafana đến CloudWatch log stream tương ứng để điều tra chi tiết.
