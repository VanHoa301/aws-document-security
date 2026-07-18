---
title: "Sinh finding và kiểm tra phản ứng"
date: 2026-07-14
weight: 4
chapter: false
pre: " <b> 5.4.4 </b> "
---

# Sinh finding và kiểm tra phản ứng

#### Tạo sample finding

1. Mở **GuardDuty → Settings**.
2. Chọn **Generate sample findings**.
3. Quay lại trang **Findings** và chọn một finding mẫu để xem type, severity và resource.

Có thể tạo một số loại mẫu bằng CLI sau khi lấy detector ID:

```bash
aws guardduty create-sample-findings \
  --detector-id <detector-id> \
  --finding-types \
    UnauthorizedAccess:EC2/SSHBruteForce \
    Recon:EC2/PortProbeUnprotectedPort \
  --region ap-southeast-1
```

#### Xác minh chuỗi tự động

Chờ khoảng một phút rồi lần lượt kiểm tra:

1. **EventBridge Monitoring:** metric `Invocations` của rule tăng và `FailedInvocations` bằng 0.
2. **Lambda Monitor:** `Invocations` tăng, `Errors` và `Throttles` bằng 0.
3. **CloudWatch Logs:** log stream mới ghi rõ finding ID, type và kết quả xử lý.
4. **DynamoDB:** bảng `SecurityIncidents` có item mới với trạng thái ban đầu `OPEN`.
5. **SNS:** email đã xác nhận subscription nhận được cảnh báo.
6. **Web application:** trang Incidents hiển thị bản ghi và admin có thể cập nhật trạng thái.

#### Kết quả mong đợi

Một finding chỉ được ghi thành một incident hợp lệ; nội dung cảnh báo đủ để xác định loại, mức độ nghiêm trọng, tài nguyên và thời gian. Không có Lambda error, EventBridge failed invocation hoặc SNS delivery failure.

{{% notice info %}}
Sample finding có tiền tố hoặc trường dữ liệu cho biết đây là dữ liệu kiểm thử. Hãy nêu rõ điều này khi chụp hình và trình bày kết quả workshop.
{{% /notice %}}
