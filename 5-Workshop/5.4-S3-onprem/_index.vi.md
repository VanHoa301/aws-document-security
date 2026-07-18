---
title: "Phản ứng sự cố bảo mật tự động"
date: 2026-07-14
weight: 4
chapter: false
pre: " <b> 5.4. </b> "
---

# Xây dựng phản ứng sự cố bảo mật tự động

Phần này hoàn thiện chuỗi phát hiện và phản ứng: **GuardDuty → EventBridge → Lambda → DynamoDB/SNS/CloudWatch**. Security Hub được dùng để tổng hợp và theo dõi findings bảo mật trên tài khoản.

#### Nội dung

- [5.4.1. Bật GuardDuty và Security Hub](5.4.1-prepare/)
- [5.4.2. Cấu hình Lambda và SNS](5.4.2-create-interface-enpoint/)
- [5.4.3. Tạo EventBridge rule](5.4.3-test-endpoint/)
- [5.4.4. Sinh finding và kiểm tra phản ứng](5.4.4-dns-simulation/)
