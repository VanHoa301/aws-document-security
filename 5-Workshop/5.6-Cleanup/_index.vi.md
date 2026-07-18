---
title: "Dọn dẹp tài nguyên"
date: 2026-07-14
weight: 6
chapter: false
pre: " <b> 5.6. </b> "
---

# Dọn dẹp tài nguyên

Chúc mừng bạn đã hoàn thành workshop quản lý tài liệu và phản ứng sự cố tự động trên AWS.

{{% notice danger %}}
Chỉ thực hiện phần này khi không còn sử dụng hệ thống. Xuất dữ liệu hoặc chụp hình báo cáo trước khi xóa; thao tác xóa S3 object, DynamoDB table và log có thể không khôi phục được.
{{% /notice %}}

#### Thứ tự dọn dẹp đề xuất

1. Dừng ứng dụng và Grafana trên EC2.
2. Disable rồi xóa EventBridge rule `GuardDutyToSecurityIncident`.
3. Xóa Lambda `SecurityIncidentResponse`.
4. Xóa subscription và SNS topic `SecurityAlerts`.
5. Xuất dữ liệu cần thiết, sau đó xóa bảng `SecurityIncidents` và `Documents`.
6. Empty toàn bộ version của bucket `aws-s3-duanthuctap`, sau đó xóa bucket.
7. Xóa CloudWatch log groups, metric filter và alarm không còn sử dụng.
8. Terminate EC2, xóa volume/EIP không cần thiết, IAM instance profile và policy riêng của workshop.
9. Tắt Security Hub và GuardDuty nếu tài khoản không còn dùng các dịch vụ này.

#### Kiểm tra chi phí còn lại

Mở **AWS Billing and Cost Management → Cost Explorer** và kiểm tra theo Region `ap-southeast-1`. Đặc biệt rà soát EC2, EBS, Elastic IP, CloudWatch Logs, GuardDuty và Security Hub.

#### Tổng kết

Workshop đã hoàn thiện đầy đủ luồng nghiệp vụ và bảo mật:

- Lưu file private trên S3 và metadata trong DynamoDB.
- Triển khai React/Flask trên EC2, quản trị qua Systems Manager.
- Phát hiện finding bằng GuardDuty/Security Hub.
- Định tuyến và xử lý bằng EventBridge/Lambda.
- Lưu incident, gửi SNS và giám sát bằng CloudWatch/Grafana.
