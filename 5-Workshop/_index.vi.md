---
title: "Workshop"
date: 2026-07-14
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# Xây dựng hệ thống quản lý tài liệu và phản ứng sự cố bảo mật tự động trên AWS

#### Tổng quan

Workshop này trình bày quá trình xây dựng một hệ thống quản lý tài liệu chạy trên **Amazon EC2**. Người dùng đăng nhập vào ứng dụng React, tải tài liệu qua Flask API; nội dung file được lưu trong bucket S3 private và metadata được lưu tại DynamoDB.

Song song với luồng nghiệp vụ, hệ thống sử dụng **Amazon GuardDuty**, **AWS Security Hub**, **Amazon EventBridge** và **AWS Lambda** để tiếp nhận, xử lý và lưu sự cố bảo mật. Cảnh báo được gửi qua **Amazon SNS**, log và metric được tập trung tại **Amazon CloudWatch**, sau đó trực quan hóa trên **Grafana**.

```text
Người dùng → Nginx/React → Flask API → S3 + DynamoDB Documents
                                      
GuardDuty → Security Hub/EventBridge → Lambda SecurityIncidentResponse
                                      ├─ DynamoDB SecurityIncidents
                                      ├─ SNS SecurityAlerts
                                      └─ CloudWatch Logs/Metrics → Grafana
```

{{% notice info %}}
Các tài nguyên trong workshop đã được triển khai tại Region **ap-southeast-1 (Singapore)**. Nội dung dưới đây vừa là hướng dẫn tái tạo, vừa là quy trình kiểm tra kết quả triển khai thực tế.
{{% /notice %}}

#### Nội dung

1. [Giới thiệu và kiến trúc](5.1-Workshop-overview/)
2. [Các bước chuẩn bị](5.2-Prerequiste/)
3. [Triển khai ứng dụng quản lý tài liệu](5.3-S3-vpc/)
4. [Xây dựng phản ứng sự cố bảo mật tự động](5.4-S3-onprem/)
5. [Giám sát hệ thống bằng CloudWatch và Grafana](5.5-Policy/)
6. [Dọn dẹp tài nguyên](5.6-Cleanup/)
