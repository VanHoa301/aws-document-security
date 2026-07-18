---
title: "Tạo EventBridge rule"
date: 2026-07-14
weight: 3
chapter: false
pre: " <b> 5.4.3 </b> "
---

# Tạo EventBridge rule

#### Kiểm tra rule

1. Mở **Amazon EventBridge → Rules**.
2. Chọn event bus `default`.
3. Mở rule `GuardDutyToSecurityIncident`.
4. Xác nhận rule ở trạng thái **Enabled** và target là Lambda `SecurityIncidentResponse`.

Event pattern sử dụng cho workshop:

```json
{
  "source": ["aws.guardduty"],
  "detail-type": ["GuardDuty Finding"]
}
```

Pattern trên tiếp nhận mọi finding của GuardDuty. Trong production có thể lọc thêm `detail.severity` hoặc `detail.type` để chỉ kích hoạt tự động đối với nhóm sự cố phù hợp.

#### Cho phép EventBridge gọi Lambda

Lambda cần resource-based policy cho principal `events.amazonaws.com`. Trong trang target của rule, trạng thái phải hiển thị bình thường, không có lỗi quyền gọi hàm.

```bash
aws events describe-rule \
  --name GuardDutyToSecurityIncident \
  --region ap-southeast-1

aws events list-targets-by-rule \
  --rule GuardDutyToSecurityIncident \
  --region ap-southeast-1
```

Kết quả phải trả về ARN của `SecurityIncidentResponse`.
