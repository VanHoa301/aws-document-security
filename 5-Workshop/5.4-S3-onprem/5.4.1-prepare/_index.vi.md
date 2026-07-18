---
title: "Bật GuardDuty và Security Hub"
date: 2026-07-14
weight: 1
chapter: false
pre: " <b> 5.4.1 </b> "
---

# Bật GuardDuty và Security Hub

#### Amazon GuardDuty

1. Chuyển AWS Console sang Region `ap-southeast-1`.
2. Mở **Amazon GuardDuty**.
3. Chọn **Get started → Enable GuardDuty** nếu detector chưa được bật.
4. Kiểm tra trang **Findings** và trạng thái bảo vệ của các nguồn dữ liệu.

GuardDuty liên tục phân tích các nguồn telemetry được hỗ trợ để phát hiện hành vi như dò cổng, brute force, truy cập bất thường hoặc hoạt động đáng ngờ liên quan đến S3 và IAM.

#### AWS Security Hub

1. Mở **AWS Security Hub → Summary**.
2. Chọn **Go to Security Hub/Enable** nếu dịch vụ chưa hoạt động.
3. Kiểm tra mục **Findings** để xem finding đã được chuẩn hóa.

{{% notice note %}}
Security Hub giúp tổng hợp và ưu tiên finding. Trong luồng tự động của workshop, EventBridge bắt trực tiếp sự kiện GuardDuty để giảm độ trễ xử lý.
{{% /notice %}}

#### Kiểm tra bằng CLI

```bash
aws guardduty list-detectors --region ap-southeast-1
aws securityhub describe-hub --region ap-southeast-1
```
