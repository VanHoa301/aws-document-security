from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "AWS_Security_Incident_Response_Workshop.docx"


def r(text, bold=False, italic=False, size=22, color=None, font="Arial"):
    props = [f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}"/>', f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>']
    if bold:
        props.append("<w:b/>")
    if italic:
        props.append("<w:i/>")
    if color:
        props.append(f'<w:color w:val="{color}"/>')
    return f'<w:r><w:rPr>{"".join(props)}</w:rPr><w:t xml:space="preserve">{escape(str(text))}</w:t></w:r>'


def p(text="", style=None, align=None, bold=False, italic=False, size=22, color=None, before=0, after=120, keep=False):
    props = [f'<w:spacing w:before="{before}" w:after="{after}" w:line="276" w:lineRule="auto"/>']
    if style:
        props.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        props.append(f'<w:jc w:val="{align}"/>')
    if keep:
        props.append("<w:keepNext/>")
    return f'<w:p><w:pPr>{"".join(props)}</w:pPr>{r(text, bold, italic, size, color)}</w:p>'


def h(text, level=1):
    return p(text, style=f"Heading{level}", keep=True)


def bullet(text, level=0):
    left = 720 + level * 360
    return f'<w:p><w:pPr><w:spacing w:after="70"/><w:ind w:left="{left}" w:hanging="300"/></w:pPr>{r("•", True)}{r("  " + text)}</w:p>'


def numbered(items):
    return "".join(p(f"{i}. {text}", after=75) for i, text in enumerate(items, 1))


def code(text):
    out = []
    for line in str(text).splitlines() or [""]:
        out.append('<w:p><w:pPr><w:shd w:val="clear" w:fill="F3F4F6"/><w:spacing w:after="0"/><w:ind w:left="240" w:right="240"/></w:pPr>' + r(line, size=18, font="Consolas") + '</w:p>')
    return "".join(out) + p("", after=60)


def note(text, warning=False):
    fill = "FDE9D9" if warning else "EAF2F8"
    color = "9C0006" if warning else "1F4E78"
    return '<w:tbl><w:tblPr><w:tblW w:w="9000" w:type="dxa"/></w:tblPr><w:tblGrid><w:gridCol w:w="9000"/></w:tblGrid><w:tr><w:tc><w:tcPr><w:shd w:val="clear" w:fill="' + fill + '"/><w:tcMar><w:top w:w="120" w:type="dxa"/><w:left w:w="160" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:right w:w="160" w:type="dxa"/></w:tcMar></w:tcPr>' + p(("CẢNH BÁO: " if warning else "GHI CHÚ: ") + text, bold=True, color=color, after=0) + '</w:tc></w:tr></w:tbl>' + p("")


def table(headers, rows, widths=None):
    widths = widths or [int(9000 / len(headers))] * len(headers)
    grid = "".join(f'<w:gridCol w:w="{x}"/>' for x in widths)
    def cell(value, i, head=False):
        fill = '<w:shd w:val="clear" w:fill="1F4E78"/>' if head else ""
        return f'<w:tc><w:tcPr><w:tcW w:w="{widths[i]}" w:type="dxa"/>{fill}<w:tcMar><w:top w:w="75" w:type="dxa"/><w:left w:w="90" w:type="dxa"/><w:bottom w:w="75" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tcMar></w:tcPr>' + p(value, bold=head, color="FFFFFF" if head else None, after=0) + '</w:tc>'
    trs = ['<w:tr>' + ''.join(cell(v, i, True) for i, v in enumerate(headers)) + '</w:tr>']
    trs += ['<w:tr>' + ''.join(cell(v, i) for i, v in enumerate(row)) + '</w:tr>' for row in rows]
    borders = '<w:tblBorders><w:top w:val="single" w:sz="4" w:color="B7C9DB"/><w:left w:val="single" w:sz="4" w:color="B7C9DB"/><w:bottom w:val="single" w:sz="4" w:color="B7C9DB"/><w:right w:val="single" w:sz="4" w:color="B7C9DB"/><w:insideH w:val="single" w:sz="4" w:color="D9E2F3"/><w:insideV w:val="single" w:sz="4" w:color="D9E2F3"/></w:tblBorders>'
    return f'<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/>{borders}</w:tblPr><w:tblGrid>{grid}</w:tblGrid>{"".join(trs)}</w:tbl>' + p("")


def page():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def build_body():
    b = []
    b += [p("AWS SECURITY WORKSHOP", align="center", before=1000, after=260, bold=True, size=26, color="4472C4"),
          p("XỬ LÝ SỰ CỐ GUARDDUTY\nVỚI PHÊ DUYỆT CON NGƯỜI", align="center", before=200, after=280, bold=True, size=42, color="1F4E78"),
          p("GuardDuty • EventBridge • Step Functions • Lambda • CloudWatch • Grafana • SNS • API Gateway • DynamoDB • EC2 • S3 • CloudFront", align="center", italic=True, size=20, color="595959", after=700),
          p("Tài liệu thực hành chi tiết – môi trường ap-southeast-1", align="center", size=22),
          p("Cập nhật: 17/07/2026", align="center", before=900, color="666666"), page()]

    b += [h("MỤC LỤC NỘI DUNG")]
    for x in ["1. Tổng quan và kết quả workshop", "2. Kiến trúc tổng thể và danh mục dịch vụ", "3. Chuẩn bị và nguyên tắc an toàn", "4. Lambda xử lý sự cố", "5. Kênh cảnh báo và phê duyệt", "6. Step Functions", "7. EventBridge, GuardDuty và Security Hub", "8. Frontend trên S3/CloudFront", "9. Backend EC2, mạng, IAM và Systems Manager", "10. CloudWatch, nhật ký kiểm toán và Grafana", "11. Kịch bản kiểm thử", "12. Xử lý lỗi", "13. Vận hành hằng ngày", "14. Bảo mật production", "15. Cleanup và checklist"]:
        b.append(bullet(x))
    b += [note("Các ARN, ID và tên tài nguyên trong tài liệu thuộc môi trường lab cụ thể. Khi tái sử dụng, hãy thay bằng thông tin tài khoản của bạn. Task token và địa chỉ email cá nhân không được ghi vào tài liệu."), page()]

    b += [h("1. TỔNG QUAN VÀ KẾT QUẢ WORKSHOP"), p("Workshop xây dựng một chuỗi phản ứng sự cố AWS có human-in-the-loop. GuardDuty phát hiện hành vi đáng ngờ; EventBridge khởi chạy Step Functions; Lambda ghi nhận incident vào DynamoDB và gửi cảnh báo; sự cố đủ nghiêm trọng phải chờ người vận hành chọn QUARANTINE, STOP hoặc REJECT. Frontend React được phân phối qua CloudFront và dùng cùng một domain để gọi backend EC2 qua đường dẫn /api/*.")]
    b += [h("1.1 Mục tiêu", 2)]
    for x in ["Tự động tiếp nhận finding từ GuardDuty.", "Lưu lịch sử incident và trạng thái phản ứng vào DynamoDB.", "Chỉ tự động cô lập hoặc dừng EC2 sau khi có xác nhận của con người.", "Gửi liên kết phê duyệt một lần qua SNS email.", "Duy trì website tĩnh qua CloudFront ngay cả khi backend EC2 ngừng chạy.", "Kiểm thử an toàn trước bằng Pass state, sau đó mới nối hành động EC2 thật."]:
        b.append(bullet(x))
    b += [h("1.2 Kết quả đã đạt", 2), table(["Hạng mục", "Kết quả"], [["API phê duyệt", "GET hiển thị xác nhận; POST hoàn tất task token một lần."], ["Workflow test", "Nhánh REJECT thành công, không tác động EC2."], ["Workflow đầy đủ", "Low severity đi nhánh không cần duyệt; high severity REJECT thành công."], ["EventBridge", "GuardDuty sample tự tạo execution UUID trong Step Functions."], ["Frontend", "React build được phục vụ từ S3 private qua CloudFront HTTPS."], ["SPA routing", "/login hoạt động nhờ fallback 403/404 về /index.html."], ["Backend proxy", "/api/* đi qua origin EC2; login hoạt động sau khi sửa origin/IP."], ["Ổn định IP", "Đã gắn Elastic IP để Stop/Start không làm đổi endpoint backend."]], [2600, 6400])]

    b += [h("2. KIẾN TRÚC TỔNG THỂ"), code("GuardDuty finding\n  → EventBridge rule\n  → Step Functions: SecurityIncidentApprovalWorkflow\n      → Lambda SecurityIncidentResponse (ghi DynamoDB + SNS)\n      → Choice: requires_approval?\n          ├─ false → RecordedWithoutApproval\n          └─ true  → Lambda SecurityApprovalNotifier (waitForTaskToken)\n                       → Email → API Gateway /approval\n                       → Lambda SecurityApprovalCallback\n                       → QUARANTINE | STOP | REJECT\n                       → Lambda SecurityIncidentResponse\n\nNgười dùng → CloudFront HTTPS\n  ├─ /*      → S3 private (React SPA)\n  └─ /api/*  → EC2/Nginx/Flask qua HTTP origin")]
    b += [table(["Lớp", "Dịch vụ", "Vai trò"], [["Mạng", "VPC, subnet, Internet Gateway, route table", "Mạng public cho EC2 và luồng ra/vào Internet."], ["Compute", "EC2, EBS, Elastic IP, ENI", "Chạy Nginx, Flask/Gunicorn, Grafana; giữ endpoint và network interface ổn định."], ["Danh tính", "IAM, STS, Systems Manager", "Role tối thiểu, credential tạm thời và Session Manager/port forwarding."], ["Lưu trữ", "S3", "Tài liệu private, frontend tĩnh, log CloudTrail/Config/S3 access nếu bật."], ["Dữ liệu", "DynamoDB", "Bảng Documents và SecurityIncidents."], ["Phân phối", "CloudFront, OAC, WAF", "HTTPS cho SPA, S3 private origin, /api/* tới EC2 và bảo vệ edge."], ["Phát hiện", "GuardDuty, Security Hub", "Sinh finding và tổng hợp trạng thái bảo mật."], ["Định tuyến", "EventBridge", "Khởi chạy Step Functions từ finding."], ["Điều phối", "Step Functions Standard", "Chờ callback và rẽ nhánh quyết định."], ["Xử lý", "Lambda", "Ghi incident, callback và tác động EC2."], ["Phê duyệt", "SNS, API Gateway", "Email và endpoint xác nhận quyết định."], ["Quan sát", "CloudWatch, CloudWatch Agent, Grafana", "Metric/log tập trung, truy vấn và dashboard."], ["Kiểm toán", "CloudTrail, VPC Flow Logs, S3 access logging, AWS Config", "Dấu vết API, network flow, truy cập object và compliance."]], [1700, 3000, 4300])]

    b += [h("3. CHUẨN BỊ VÀ NGUYÊN TẮC AN TOÀN"), h("3.1 Tài nguyên lab", 2), table(["Tài nguyên", "Giá trị lab"], [["Region", "ap-southeast-1"], ["Account", "674695457317"], ["EC2 allowlist", "i-0f86ac8ae3872226e"], ["DynamoDB", "SecurityIncidents"], ["SNS topic", "SecurityAlerts"], ["Quarantine SG", "sg-04978dcbac0c063ad"], ["API Gateway", "hrpsx9hfaa / ANY /approval"], ["S3 frontend", "security-approval-portal-674695457317"], ["CloudFront", "E26NQV7INBOPFP / d3rxc4d21dw065.cloudfront.net"]], [3000, 6000])]
    b += [h("3.2 Quy tắc an toàn", 2)]
    for x in ["Chỉ đưa instance thử nghiệm vào ALLOWED_INSTANCE_IDS.", "Thực hiện REJECT trước; chỉ thử QUARANTINE/STOP khi có kế hoạch khôi phục.", "Không chụp hoặc chia sẻ task token trong URL email.", "Không terminate EC2 và không release/disassociate Elastic IP nếu muốn giữ endpoint.", "Quarantine SG phải thuộc đúng VPC và có quy tắc tối thiểu cần thiết.", "Tách management plane khỏi workload trong môi trường production."]:
        b.append(bullet(x))
    b.append(note("STOP hoặc QUARANTINE chính EC2 đang chạy backend sẽ làm /api và đăng nhập tạm thời không hoạt động. Website tĩnh vẫn mở được từ CloudFront.", True))

    b += [h("4. LAMBDA SECURITYINCIDENTRESPONSE"), p("Mã nguồn tham chiếu: lambda/security_incident_response.py. Lambda hỗ trợ cả xử lý finding ban đầu và bốn hành động sau phê duyệt."), h("4.1 Biến môi trường", 2), table(["Key", "Giá trị / ý nghĩa"], [["ALLOWED_INSTANCE_IDS", "i-0f86ac8ae3872226e; có thể là danh sách phân cách dấu phẩy."], ["INCIDENTS_TABLE", "SecurityIncidents"], ["INCIDENT_PORTAL_URL", "https://d3rxc4d21dw065.cloudfront.net"], ["QUARANTINE_SG_ID", "sg-04978dcbac0c063ad"], ["SNS_TOPIC_ARN", "arn:aws:sns:ap-southeast-1:674695457317:SecurityAlerts"], ["TAG_MIN_SEVERITY", "7"]], [3000, 6000])]
    b += [h("4.2 Xử lý finding", 2), numbered(["Đọc detail, finding ID/type/severity/resource/region/account.", "Tạo item status OPEN và response_action RECORDED_AND_ALERTED.", "Nếu EC2, severity ≥ 7 và nằm trong allowlist: tag SecurityStatus=Suspected.", "Ghi item vào SecurityIncidents.", "Publish SNS với thông tin sự cố và link portal.", "Trả requires_approval để Step Functions rẽ nhánh."])]
    b += [h("4.3 Các hành động", 2), table(["Action", "Hành vi"], [["QUARANTINE_APPROVED", "Lưu SG gốc, thay SG của ENI chính bằng quarantine SG, tag EC2, cập nhật incident."], ["RESTORE_APPROVED", "Đọc SG gốc từ incident, gắn lại ENI, cập nhật RESOLVED."], ["STOP_APPROVED", "Gọi ec2:StopInstances, tag và cập nhật trạng thái."], ["REJECT_APPROVAL", "Không tác động EC2; ghi REJECTED_NO_AUTOMATED_ACTION."]], [2800, 6200])]
    b += [h("4.4 IAM tối thiểu", 2), p("Role Lambda cần quyền theo đúng tài nguyên: DynamoDB PutItem/UpdateItem/GetItem; SNS Publish; EC2 DescribeInstances/DescribeSecurityGroups/CreateTags/ModifyNetworkInterfaceAttribute/StopInstances; CloudWatch Logs. Hạn chế resource ARN khi API cho phép.")]

    b += [h("5. KÊNH CẢNH BÁO VÀ PHÊ DUYỆT"), h("5.1 SNS", 2), p("Topic SecurityAlerts gửi email thông báo. Subscription phải ở trạng thái Confirmed. Không đưa địa chỉ email cá nhân vào repository hoặc báo cáo công khai."), h("5.2 SecurityApprovalNotifier", 2), p("Lambda nhận task_token từ Step Functions, tạo ba URL đã URL-encode cho QUARANTINE, STOP và REJECT, rồi publish email. Biến APPROVAL_API_URL là https://hrpsx9hfaa.execute-api.ap-southeast-1.amazonaws.com/approval."), h("5.3 API Gateway", 2), table(["Thiết lập", "Giá trị"], [["API", "SecurityApprovalApi (hrpsx9hfaa)"], ["Loại", "HTTP API"], ["Route", "ANY /approval"], ["Integration", "SecurityApprovalCallback"], ["Stage", "$default"], ["Deployment", "Automatic deployment enabled"]], [3000, 6000])]
    b += [h("5.4 SecurityApprovalCallback", 2), numbered(["GET kiểm tra decision, incident_id, task_token rồi hiển thị trang xác nhận.", "Form POST lại cùng dữ liệu; quyết định chỉ được thực thi khi bấm Confirm.", "POST gọi states:SendTaskSuccess với output decision/incident_id/approved_by.", "Token hết hạn, sai hoặc đã dùng trả HTTP 409."])]
    b += [note("Mẫu GET → trang xác nhận → POST giúp tránh email security scanner tự động kích hoạt link. Trong production vẫn cần Cognito/SSO và kiểm tra danh tính approver.")]

    b += [h("6. STEP FUNCTIONS"), h("6.1 Workflow kiểm thử an toàn", 2), p("SecurityApprovalTestWorkflow dùng waitForTaskToken nhưng các nhánh chỉ là Pass state. Đây là bước bắt buộc trước khi cho workflow tác động EC2. File: lambda/security_approval_test_state_machine.json."), h("6.2 Workflow đầy đủ", 2), p("File: lambda/security_incident_approval_state_machine.json. State machine loại Standard, TimeoutSeconds=86400."), table(["State", "Ý nghĩa"], [["ProcessGuardDutyFinding", "Invoke SecurityIncidentResponse và parse Payload.body."], ["ApprovalRequired", "Choice theo processing.result.requires_approval."], ["RecordedWithoutApproval", "Kết thúc an toàn với finding không đủ điều kiện."], ["WaitForSecurityApproval", "Invoke notifier với callback token và chờ tối đa workflow timeout."], ["RouteDecision", "Choice QUARANTINE/STOP/REJECT."], ["QuarantineInstance", "Invoke QUARANTINE_APPROVED."], ["StopInstance", "Invoke STOP_APPROVED."], ["RecordRejection", "Invoke REJECT_APPROVAL."], ["InvalidDecision", "Fail nếu callback trả quyết định lạ."]], [3000, 6000])]
    b += [h("6.3 Quyền execution role", 2), p("Role Step Functions cần lambda:InvokeFunction cho SecurityIncidentResponse và SecurityApprovalNotifier. Lambda callback cần states:SendTaskSuccess (và SendTaskFailure nếu triển khai lỗi chủ động).")]

    b += [h("7. EVENTBRIDGE VÀ GUARDDUTY"), h("7.1 Rule", 2), p("Rule GuardDuty-To-SecurityIncidentResponse được sửa target từ Lambda trực tiếp sang Step Functions SecurityIncidentApprovalWorkflow. Input dùng Matched event; EventBridge dùng execution role có states:StartExecution."), h("7.2 Tạo sample finding", 2), code("DETECTOR_ID=$(aws guardduty list-detectors \\\n  --region ap-southeast-1 \\\n  --query 'DetectorIds[0]' \\\n  --output text)\n\naws guardduty create-sample-findings \\\n  --region ap-southeast-1 \\\n  --detector-id \"$DETECTOR_ID\" \\\n  --finding-types \"Recon:EC2/PortProbeUnprotectedPort\"")]
    b += [h("7.3 Xác minh", 2), numbered(["Mở Step Functions → SecurityIncidentApprovalWorkflow → Executions.", "Tìm execution tên UUID tạo tự động sau sample finding.", "Mở Graph view và kiểm tra nhánh xanh.", "Xem DynamoDB SecurityIncidents và email SNS.", "Nếu severity/instance không đủ điều kiện, execution kết thúc ở RecordedWithoutApproval."])]

    b += [page(), h("8. FRONTEND TRÊN S3 VÀ CLOUDFRONT"), h("8.1 Build và upload", 2), code("cd frontend\nnpm install\nnpm run build"), p("Upload toàn bộ nội dung frontend/dist vào gốc bucket security-approval-portal-674695457317: index.html, favicon.svg, icons.svg và thư mục assets/. Bucket giữ private và bật Block Public Access.")]
    b += [h("8.2 CloudFront distribution", 2), table(["Thiết lập", "Giá trị"], [["Name", "SecurityApprovalPortal"], ["Domain", "d3rxc4d21dw065.cloudfront.net"], ["S3 origin", "security-approval-portal-674695457317.s3.ap-southeast-1.amazonaws.com"], ["S3 access", "Private, CloudFront Origin Access Control"], ["Default root object", "index.html"], ["HTTPS", "CloudFront certificate"], ["WAF", "Security protections enabled; monitor mode trong giai đoạn quan sát"]], [3000, 6000])]
    b += [h("8.3 SPA fallback", 2), p("React Router yêu cầu mọi đường dẫn frontend như /login hoặc /incidents trả index.html. Tạo hai Custom error responses:"), table(["Origin error", "Response page", "Viewer code", "TTL"], [["403 Forbidden", "/index.html", "200 OK", "0"], ["404 Not Found", "/index.html", "200 OK", "0"]], [2200, 3000, 2200, 1600])]
    b += [h("8.4 Backend origin và behavior /api/*", 2), p("Tạo custom origin SecurityPortalBackend dùng Public DNS tương ứng với Elastic IP của EC2, protocol HTTP, port 80. Không nhập http:// và không nhập /api vào Origin domain."), table(["Behavior", "Giá trị"], [["Path pattern", "/api/*"], ["Origin", "SecurityPortalBackend"], ["Viewer protocol", "Redirect HTTP to HTTPS"], ["Methods", "GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE"], ["Cache policy", "CachingDisabled"], ["Origin request policy", "AllViewer"], ["Restrict viewer access", "No"], ["Compress", "Yes"]], [3000, 6000])]
    b += [note("Không cần custom error response cho 504. Lỗi 504 ở /api là lỗi kết nối backend, không phải lỗi SPA; phải sửa EC2, Security Group, Nginx hoặc origin.", True)]
    b += [h("8.5 Invalidation sau deploy", 2), code("aws cloudfront create-invalidation \\\n  --distribution-id E26NQV7INBOPFP \\\n  --paths '/*'"), p("Chờ distribution/changes ở trạng thái Deployed trước khi kiểm thử lại.")]

    b += [h("9. BACKEND EC2 VÀ ELASTIC IP"), p("Backend chạy trên instance i-0f86ac8ae3872226e (document-app-server), phía trước là Nginx port 80. Public IP động từng thay từ 18.143.145.0 sang 54.254.170.58, làm CloudFront origin cũ trả 504. Giải pháp bền vững là gắn Elastic IP và trỏ origin bằng Public DNS tương ứng."), h("9.1 Checklist mạng", 2)]
    for x in ["Instance ở trạng thái Running và Status checks 2/2.", "Elastic IP vẫn Associated với đúng instance/ENI.", "Security Group cho phép TCP 80 từ CloudFront hoặc 0.0.0.0/0 trong lab tạm thời.", "Nginx lắng nghe 0.0.0.0:80.", "Flask/Gunicorn service đang Active.", "CloudFront custom origin dùng DNS/IP hiện tại, không dùng địa chỉ cũ."]:
        b.append(bullet(x))
    b += [h("9.2 Health check", 2), code("curl -i http://<ELASTIC-IP>/api/health\ncurl -i https://d3rxc4d21dw065.cloudfront.net/api/health"), p("Phải kiểm tra direct EC2 trước. Nếu direct EC2 timeout thì CloudFront chắc chắn cũng 504.")]
    b += [h("9.3 Dịch vụ tự khởi động", 2), code("sudo systemctl enable nginx\nsudo systemctl restart nginx\nsudo systemctl status nginx\n\n# Thay tên service backend thực tế\nsudo systemctl enable <backend-service>\nsudo systemctl restart <backend-service>\nsudo systemctl status <backend-service>")]

    b += [page(), h("10. CLOUDWATCH, NHẬT KÝ KIỂM TOÁN VÀ GRAFANA"), p("CloudWatch là nguồn metric/log tập trung; Grafana đọc dữ liệu CloudWatch để trực quan hóa và không thay thế CloudWatch."), h("10.1 Nguồn dữ liệu", 2), table(["Nguồn", "Dữ liệu", "Cách thu thập"], [["EC2", "CPU, network, status check", "Metric AWS/EC2 tự động."], ["Nginx và hệ thống", "Access/error/system log", "CloudWatch Agent trên EC2."], ["Lambda", "Invocation, error, duration, throttle và log", "AWS/Lambda và /aws/lambda/SecurityIncidentResponse."], ["DynamoDB", "Read/write capacity, system error", "AWS/DynamoDB."], ["SNS và EventBridge", "Delivery/invocation/failure", "AWS/SNS và AWS/Events."], ["S3", "Bucket size và object count", "AWS/S3; storage metric cập nhật hằng ngày."], ["CloudTrail", "AWS API management events", "Trail ghi S3 và tùy chọn CloudWatch Logs."], ["VPC Flow Logs", "ACCEPT/REJECT theo ENI", "Flow log tới CloudWatch Logs."], ["S3 access logging", "Request tới bucket tài liệu", "Bucket log riêng và prefix s3-access-logs/."], ["AWS Config", "Lịch sử cấu hình và compliance", "Recorder, delivery channel và Config rules."]], [2100, 3300, 3600])]
    b += [h("10.2 CloudWatch Agent", 2), numbered(["Gắn CloudWatchAgentServerPolicy hoặc policy tối thiểu vào EC2 role.", "Cài amazon-cloudwatch-agent trên EC2.", "Thu thập /var/log/nginx/access.log, /var/log/nginx/error.log và system log vào đúng log group.", "Start/enable agent và kiểm tra log stream trong CloudWatch Logs.", "Đặt retention phù hợp, ví dụ 7 ngày cho lab."]), code("sudo systemctl enable amazon-cloudwatch-agent\nsudo systemctl restart amazon-cloudwatch-agent\nsudo systemctl status amazon-cloudwatch-agent")]
    b += [h("10.3 Truy cập Grafana an toàn", 2), p("Grafana chạy trên EC2 nhưng không mở public TCP 3000. Dùng Systems Manager port forwarding:"), code("aws ssm start-session \\\n  --target i-0f86ac8ae3872226e \\\n  --document-name AWS-StartPortForwardingSession \\\n  --parameters '{\"portNumber\":[\"3000\"],\"localPortNumber\":[\"3000\"]}'\n\n# Mở http://localhost:3000"), p("Tạo CloudWatch data source tại ap-southeast-1 và dùng IAM role của EC2; không lưu access key trong Grafana.")]
    b += [h("10.4 Import dashboard", 2), table(["File", "Nội dung"], [["grafana/aws-services-monitoring.json", "Lambda, DynamoDB Documents/SecurityIncidents, S3, SNS và EventBridge."], ["grafana/security-logs-monitoring.json", "HTTP 4xx/5xx, Lambda log, Nginx access/error và system log."]], [4200, 4800]), numbered(["Grafana → Dashboards → New → Import.", "Upload từng JSON và chọn CloudWatch data source.", "Với dashboard log, nhập AWS Account ID theo prompt.", "Chọn Last 1 hour/Last 24 hours và refresh 1m.", "Tạo upload/download và GuardDuty sample finding để sinh dữ liệu."])]
    b += [h("10.5 Xử lý No data", 2), table(["Triệu chứng", "Kiểm tra"], [["Tất cả panel No data", "Region, IAM GetMetricData/GetMetricStatistics và data source Save & test."], ["Chỉ log No data", "Tên log group, Account ID, CloudWatch Agent và time range."], ["S3 size/object trống", "Chờ metric storage cập nhật theo ngày; dùng Last 7 days."], ["EventBridge/Lambda trống", "Tạo sample finding và xác nhận rule/execution chạy."], ["Grafana không mở", "SSM managed instance, plugin, grafana-server và local port 3000."]], [2800, 6200])]

    b += [h("11. KỊCH BẢN KIỂM THỬ END-TO-END"), h("11.1 Kiểm thử low severity", 2), numbered(["Start execution với event GuardDuty severity dưới 7 hoặc resource không thuộc allowlist.", "Xác nhận ProcessGuardDutyFinding thành công.", "ApprovalRequired đi Default.", "Execution kết thúc Succeeded tại RecordedWithoutApproval.", "DynamoDB có incident, SNS có cảnh báo và Grafana hiển thị invocation."])]
    b += [h("11.2 High severity + REJECT", 2), numbered(["Start execution bằng finding EC2 severity ≥ 7 và đúng allowlist.", "Workflow dừng tại WaitForSecurityApproval.", "Mở email, chọn REJECT, kiểm tra trang xác nhận rồi bấm Confirm.", "Workflow đi RouteDecision → RecordRejection → Succeeded.", "DynamoDB ghi REJECTED_NO_AUTOMATED_ACTION; EC2 không bị thay đổi."])]
    b += [h("11.3 QUARANTINE", 2), numbered(["Chụp lại Security Groups gốc và xác nhận quarantine SG thuộc đúng VPC.", "Thực hiện approval QUARANTINE.", "Kiểm tra ENI chỉ còn quarantine SG và tag SecurityStatus=Quarantined.", "Kiểm tra incident có original_security_groups để phục hồi.", "Thực hiện RESTORE_APPROVED bằng quy trình quản trị khi điều tra xong."])]
    b += [h("11.4 STOP", 2), numbered(["Đảm bảo Elastic IP đã gắn và backend service auto-start.", "Thực hiện STOP trên instance lab.", "Xác nhận Step Functions Succeeded và EC2 chuyển Stopped.", "Start lại EC2, chờ 2/2 checks, kiểm tra direct health, CloudFront health và Grafana."])]

    b += [h("12. XỬ LÝ LỖI ĐÃ GẶP"), table(["Triệu chứng", "Nguyên nhân", "Cách xử lý"], [["/login trả XML AccessDenied", "S3 private trả 403 cho route không có object.", "Tạo 403 và 404 custom response về /index.html với code 200."], ["Nút Sign in quay mãi", "Request /api không nhận phản hồi.", "Mở DevTools Network và kiểm tra /api/health."], ["CloudFront /api/health trả 504", "CloudFront không kết nối được EC2 origin.", "Kiểm tra direct IP, SG port 80, Nginx và origin DNS."], ["Direct IP timeout", "IP đã đổi, SG chặn hoặc service dừng.", "Dùng IP hiện tại/EIP, mở port phù hợp và restart service."], ["Approval link 409", "Task token sai, hết hạn hoặc đã dùng.", "Tạo execution mới; mỗi token chỉ dùng một lần."], ["Không thấy execution mới", "EventBridge target/role/pattern sai.", "Kiểm tra target Step Functions, states:StartExecution và Monitoring."], ["Email không đến", "Subscription chưa Confirmed hoặc Lambda thiếu sns:Publish.", "Kiểm tra SNS subscription, Lambda logs và IAM."], ["QUARANTINE lỗi VPC", "Quarantine SG khác VPC.", "Tạo/chọn SG trong đúng VPC của instance."]], [2500, 2900, 3600])]

    b += [h("13. VẬN HÀNH HẰNG NGÀY"), h("13.1 Khi dừng EC2 để tiết kiệm", 2)]
    for x in ["Có thể Stop EC2; dữ liệu EBS và cấu hình không mất.", "Elastic IP không đổi khi Stop/Start nếu vẫn associated và không release.", "CloudFront/S3 vẫn phục vụ giao diện tĩnh; login/API không hoạt động khi EC2 dừng.", "Khi Start lại không phải cài lại ứng dụng nếu volume còn nguyên và service được enable.", "Elastic IP có thể phát sinh chi phí khi không được sử dụng/không gắn đúng tài nguyên; theo dõi AWS billing."]:
        b.append(bullet(x))
    b += [h("13.2 Quy trình Start lại", 2), numbered(["EC2 → Instances → chọn document-app-server → Start instance.", "Chờ Instance state Running và Status checks 2/2.", "Xác nhận Elastic IP association.", "Mở http://<ELASTIC-IP>/api/health.", "Mở https://d3rxc4d21dw065.cloudfront.net/api/health.", "Đăng nhập portal và thử danh sách incident.", "Nếu lỗi, kiểm tra systemctl status nginx và backend service."])]
    b += [h("13.3 Cập nhật frontend", 2), numbered(["Sửa mã và chạy npm run build.", "Upload nội dung dist, giữ đúng cấu trúc thư mục assets.", "Tạo CloudFront invalidation /*.", "Chờ Deployed và kiểm tra bằng cửa sổ ẩn danh."])]

    b += [h("14. BẢO MẬT CHO PRODUCTION"), p("Thiết kế hiện tại phù hợp workshop/demo. Trước production cần nâng cấp:" )]
    for x in ["Dùng Cognito/SSO cho portal và API phê duyệt; không tin chuỗi approved_by cố định.", "Rút ngắn thời hạn callback và ghi audit identity, IP, timestamp, decision.", "Ký hoặc mã hóa dữ liệu liên kết; tránh task token trong log, analytics và screenshot.", "Giới hạn API Gateway bằng authorizer/WAF/rate limit.", "Áp dụng least privilege cho Step Functions, Lambda và EventBridge roles.", "Chuyển backend management khỏi chính EC2 có thể bị stop/quarantine; ưu tiên API Gateway + Lambda hoặc một management VPC riêng.", "Bật CloudTrail, CloudWatch alarms, DLQ/retry hợp lý và log retention.", "Hạn chế SG origin chỉ nhận CloudFront managed prefix list hoặc dùng ALB/VPC origin.", "Sau thời gian quan sát, chuyển WAF monitor/count sang block có kiểm soát."]:
        b.append(bullet(x))

    b += [h("15. CLEANUP VÀ CHECKLIST HOÀN THÀNH"), h("15.1 Cleanup lab", 2), p("Chỉ cleanup khi workshop kết thúc và đã sao lưu dữ liệu cần thiết."), numbered(["Disable EventBridge rule để ngừng execution mới.", "Dừng hoặc xóa execution đang chờ callback.", "Xóa sample findings/incident test theo chính sách dữ liệu.", "Xóa CloudFront distribution sau khi Disable và chờ trạng thái cho phép.", "Xóa object rồi bucket S3 frontend nếu không dùng.", "Xóa API Gateway/Lambda/Step Functions/IAM roles được tạo riêng cho lab.", "Xóa SNS subscription/topic nếu không dùng.", "Release Elastic IP chỉ khi chắc chắn không còn cần endpoint."])]
    b += [h("15.2 Checklist bàn giao", 2)]
    for x in ["[ ] EventBridge target là SecurityIncidentApprovalWorkflow.", "[ ] Workflow low severity và REJECT đều Succeeded.", "[ ] DynamoDB ghi đúng trạng thái.", "[ ] Email approval không lộ token trong tài liệu.", "[ ] CloudFront /login tải SPA.", "[ ] CloudFront /api/health trả thành công.", "[ ] Elastic IP gắn đúng EC2.", "[ ] Nginx/backend và CloudWatch Agent tự khởi động.", "[ ] Grafana truy cập được qua SSM, không mở public port 3000.", "[ ] Hai dashboard JSON hiển thị metric/log sau khi tạo traffic.", "[ ] CloudTrail, Flow Logs, S3 access log và Config có retention/lifecycle phù hợp nếu đã bật.", "[ ] INCIDENT_PORTAL_URL dùng CloudFront HTTPS.", "[ ] Có kế hoạch restore sau quarantine/stop."]:
        b.append(bullet(x))
    b += [note("Workshop hoàn tất khi cả luồng tự động GuardDuty → EventBridge → Step Functions và luồng người dùng CloudFront → /api đều được kiểm thử sau một lần Stop/Start EC2."), h("PHỤ LỤC A — FILE NGUỒN LIÊN QUAN")]
    b += [table(["File", "Vai trò"], [["lambda/security_incident_response.py", "Xử lý finding và hành động EC2."], ["lambda/security_approval_notifier.py", "Tạo email link phê duyệt."], ["lambda/security_approval_callback.py", "GET xác nhận, POST callback Step Functions."], ["lambda/security_approval_test_state_machine.json", "Workflow an toàn."], ["lambda/security_incident_approval_state_machine.json", "Workflow đầy đủ."], ["frontend/", "React/Vite portal."], ["frontend/dist/", "Artefact upload S3 sau build."], ["grafana/aws-services-monitoring.json", "Dashboard metric dịch vụ AWS."], ["grafana/security-logs-monitoring.json", "Dashboard log ứng dụng và bảo mật."], ["5-Workshop/5.5-Policy/_index.vi.md", "Bài thực hành CloudWatch và Grafana."]], [4200, 4800])]
    b += [h("PHỤ LỤC B — ENDPOINT THAM CHIẾU"), table(["Endpoint", "Mục đích"], [["https://d3rxc4d21dw065.cloudfront.net", "Portal chính."], ["https://d3rxc4d21dw065.cloudfront.net/login", "Đăng nhập SPA."], ["https://d3rxc4d21dw065.cloudfront.net/api/health", "Health qua CloudFront."], ["https://hrpsx9hfaa.execute-api.ap-southeast-1.amazonaws.com/approval", "Callback phê duyệt; cần query từ email."]], [5000, 4000])]
    return "".join(b)


STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="300" w:after="140"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:color w:val="1F4E78"/><w:sz w:val="32"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="220" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:color w:val="2F5597"/><w:sz w:val="27"/></w:rPr></w:style></w:styles>'''


def write_docx():
    body = build_body()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><w:body>{body}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" w:header="500" w:footer="500"/><w:footerReference w:type="default" r:id="rId3"/></w:sectPr></w:body></w:document>'''
    parts = {
        "[Content_Types].xml": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/><Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>''',
        "_rels/.rels": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>''',
        "word/document.xml": document,
        "word/styles.xml": STYLES,
        "word/settings.xml": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:zoom w:percent="100"/><w:defaultTabStop w:val="720"/></w:settings>''',
        "word/footer1.xml": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:t>Trang </w:t></w:r><w:fldSimple w:instr="PAGE"><w:r><w:t>1</w:t></w:r></w:fldSimple></w:p></w:ftr>''',
        "word/_rels/document.xml.rels": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/></Relationships>''',
        "docProps/core.xml": f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>AWS Security Incident Response Workshop</dc:title><dc:creator>Workshop AWS</dc:creator><dc:subject>GuardDuty human approval workflow</dc:subject><dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified></cp:coreProperties>''',
        "docProps/app.xml": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Microsoft Office Word</Application><AppVersion>16.0000</AppVersion></Properties>''',
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as z:
        for name, data in parts.items():
            z.writestr(name, data)
    print(OUTPUT)


if __name__ == "__main__":
    write_docx()
