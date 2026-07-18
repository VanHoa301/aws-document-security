from __future__ import annotations

from datetime import datetime

from generate_word_docs import OUT, code, heading, make_docx, page_break, para, run, table


def bullet(text: str, level: int = 0) -> str:
    left = 720 + level * 360
    return (
        f'<w:p><w:pPr><w:spacing w:after="70"/><w:ind w:left="{left}" w:hanging="300"/>'
        f'</w:pPr>{run("•", bold=True)}{run("  " + text)}</w:p>'
    )


def figure(number: int, title: str, capture: str) -> str:
    return "".join([
        '<w:p><w:pPr><w:shd w:val="clear" w:color="auto" w:fill="FFF2CC"/>'
        '<w:spacing w:before="100" w:after="70"/><w:ind w:left="240" w:right="240"/></w:pPr>'
        + run(f"[CHÈN HÌNH {number}: {title}]", bold=True, color="C00000") + '</w:p>',
        '<w:p><w:pPr><w:shd w:val="clear" w:color="auto" w:fill="FFF9E6"/>'
        '<w:spacing w:after="70"/><w:ind w:left="240" w:right="240"/></w:pPr>'
        + run("Cần chụp: " + capture, italic=True, color="7F6000") + '</w:p>',
        para(f"Hình {number}. {title}", align="center", italic=True, after=170),
    ])


def cover() -> str:
    return "".join([
        para("BÁO CÁO WORKSHOP AWS", align="center", before=800, after=260,
             bold=True, size=26, color="4472C4"),
        para("TRIỂN KHAI GIÁM SÁT, KIỂM TOÁN\nVÀ ĐÁNH GIÁ TUÂN THỦ AN NINH", align="center",
             before=260, after=320, bold=True, size=40, color="1F4E78"),
        para("CloudTrail • VPC Flow Logs • S3 Server Access Logging • AWS Config",
             align="center", after=650, italic=True, size=24, color="595959"),
        table(["Thông tin", "Nội dung"], [
            ["Họ và tên", "[ĐIỀN HỌ VÀ TÊN]"],
            ["MSSV / Lớp", "[ĐIỀN MSSV VÀ LỚP]"],
            ["Giảng viên", "[ĐIỀN TÊN GIẢNG VIÊN]"],
            ["Tài khoản thực hành", "Admin-lab"],
            ["Region", "Asia Pacific (Singapore) – ap-southeast-1"],
            ["Dự án", "Document Management Application"],
        ], [2600, 6400]),
        para(f"Ngày hoàn thiện báo cáo: {datetime.now().strftime('%d/%m/%Y')}", align="center",
             before=650, size=21, color="666666"),
        page_break(),
    ])


def body() -> str:
    b: list[str] = [cover()]
    b += [heading("MỤC LỤC NỘI DUNG", 1)]
    for item in [
        "1. Tổng quan workshop", "2. Mục tiêu và phạm vi", "3. Kiến trúc hệ thống",
        "4. Hiện trạng và yêu cầu an ninh", "5. Triển khai AWS CloudTrail",
        "6. Triển khai VPC Flow Logs", "7. Triển khai S3 Server Access Logging",
        "8. Triển khai AWS Config", "9. Phát hiện và khắc phục Security Group",
        "10. Xác minh sau khắc phục", "11. Kết quả và đánh giá", "12. Chi phí và vận hành",
        "13. Danh mục ảnh minh chứng", "14. Kết luận", "Phụ lục A. Lệnh kiểm tra",
        "Phụ lục B. Checklist nghiệm thu",
    ]:
        b.append(bullet(item))

    b += [page_break(), heading("1. TỔNG QUAN WORKSHOP", 1)]
    b.append(para(
        "Workshop xây dựng một lớp giám sát và kiểm toán an ninh cho hệ thống quản lý tài liệu "
        "đang chạy trên AWS. Hệ thống ứng dụng gồm một EC2 Linux chạy Nginx và Flask/Gunicorn, "
        "Amazon S3 lưu tài liệu, Amazon DynamoDB lưu metadata và AWS Systems Manager phục vụ quản trị. "
        "Phần workshop không thay đổi mã nguồn ứng dụng; các cơ chế kiểm toán được cấu hình trực tiếp "
        "trên AWS Management Console."
    ))
    b.append(para(
        "Bốn năng lực được triển khai theo thứ tự CloudTrail → VPC Flow Logs → S3 Server Access Logging "
        "→ AWS Config. Chuỗi này bao phủ hoạt động quản trị, lưu lượng mạng, truy cập dữ liệu và thay đổi "
        "cấu hình. Kết quả AWS Config sau đó được dùng để phát hiện Security Group mở SSH công khai, "
        "khắc phục và xác minh hệ thống vẫn hoạt động qua Session Manager."
    ))
    b += [heading("1.1 Kết quả nổi bật", 2)]
    for x in [
        "CloudTrail multi-Region ghi management events và chuyển file log nén vào S3.",
        "VPC Flow Logs ghi toàn bộ ACCEPT/REJECT của Linux-vpc vào CloudWatch Logs theo chu kỳ 1 phút.",
        "S3 Server Access Logging được bật cho bucket tài liệu và chuyển log sang bucket riêng.",
        "AWS Config ghi liên tục EC2 Instance, EC2 Security Group và S3 Bucket.",
        "Hai managed rules được bật: restricted-ssh và s3-bucket-public-read-prohibited.",
        "AWS Config phát hiện hai Security Group vi phạm; sau khắc phục cả hai rules đều Compliant.",
        "Website, API health, DynamoDB, S3, Nginx và Session Manager vẫn hoạt động sau khi đóng SSH.",
    ]:
        b.append(bullet(x))

    b += [heading("2. MỤC TIÊU VÀ PHẠM VI", 1)]
    b.append(table(["Mục tiêu", "Tiêu chí hoàn thành"], [
        ["Kiểm toán hoạt động quản trị", "Tra cứu được sự kiện API và có file CloudTrail trong S3."],
        ["Giám sát lưu lượng mạng", "Flow Log Active, CloudWatch có log stream và bản ghi ACCEPT/REJECT."],
        ["Theo dõi truy cập tài liệu", "Server access logging Enabled, đúng bucket đích và prefix."],
        ["Đánh giá cấu hình", "AWS Config recorder hoạt động và hai managed rules có kết quả."],
        ["Khắc phục rủi ro", "Loại bỏ SSH/port nội bộ công khai và đưa restricted-ssh về Compliant."],
        ["Không gián đoạn", "Website, API và Session Manager vẫn sử dụng được sau thay đổi."],
    ], [3100, 5900]))
    b += [heading("2.1 Ngoài phạm vi", 2)]
    for x in [
        "Không triển khai tự động remediation vì có nguy cơ ngắt kết nối quản trị.",
        "Không bật toàn bộ AWS Config resource types/rules để hạn chế chi phí.",
        "Không bật CloudTrail data events trong giai đoạn này vì S3 access logging đã đáp ứng mục tiêu minh chứng truy cập.",
        "Không công khai CloudWatch Logs hoặc các bucket log.",
    ]:
        b.append(bullet(x))

    b += [heading("3. KIẾN TRÚC HỆ THỐNG", 1)]
    b.append(code(
        "Người dùng → Internet → Security Group → Nginx (80/443)\n"
        "Nginx → Flask/Gunicorn (127.0.0.1:5000)\n"
        "Flask → Amazon S3 + Amazon DynamoDB\n\n"
        "CloudTrail → S3 CloudTrail log bucket\n"
        "Linux-vpc Flow Logs → CloudWatch Logs\n"
        "S3 document bucket access logs → S3 access-log bucket\n"
        "AWS Config → Config S3 bucket + managed rule evaluations\n"
        "Quản trị viên → Systems Manager Session Manager → EC2"
    ))
    b.append(table(["Tài nguyên", "Giá trị sử dụng trong workshop", "Vai trò"], [
        ["EC2", "document-app-server", "Chạy Nginx, frontend và backend."],
        ["VPC", "Linux-vpc", "Mạng của EC2 ứng dụng."],
        ["S3 nguồn", "aws-s3-duanthuctap", "Lưu tài liệu ứng dụng."],
        ["S3 CloudTrail", "aws-cloudtrail-logs-…", "Lưu audit log CloudTrail."],
        ["S3 access log", "document-app-access-logs-…", "Lưu S3 server access log."],
        ["S3 Config", "config-bucket-…", "Lưu configuration snapshot/history."],
        ["CloudWatch", "/aws/vpc/flowlogs/linux-vpc", "Lưu VPC Flow Logs."],
        ["AWS Config rules", "restricted-ssh; s3-bucket-public-read-prohibited", "Đánh giá tuân thủ."],
    ], [2100, 3600, 3300]))
    b.append(figure(1, "Sơ đồ kiến trúc tổng thể sau workshop",
                    "Sơ đồ draw.io thể hiện EC2, VPC, S3, DynamoDB và bốn luồng log/đánh giá. Dùng mũi tên và ghi rõ Region ap-southeast-1."))
    b.append(figure(2, "EC2 document-app-server và thông tin mạng",
                    "EC2 Instance summary, tên instance, trạng thái Running, VPC Linux-vpc, subnet và IAM role. Che Account ID/Public IP nếu nộp công khai."))

    b += [heading("4. HIỆN TRẠNG VÀ YÊU CẦU AN NINH", 1)]
    b.append(para(
        "Trước workshop, ứng dụng đã hoạt động nhưng cần bổ sung bằng chứng kiểm toán và khả năng phát hiện "
        "sai cấu hình. Security Group ban đầu mở nhiều cổng đến 0.0.0.0/0, gồm SSH 22, backend 5000 và "
        "MySQL 3306. Trong khi đó, Nginx chỉ cần gọi backend qua loopback 127.0.0.1:5000 và backend dùng "
        "DynamoDB thay vì MySQL. Đây là cơ hội áp dụng nguyên tắc least privilege."
    ))
    b.append(table(["Rủi ro", "Tác động", "Kiểm soát áp dụng"], [
        ["Thiếu audit trail", "Khó truy vết ai đã thay đổi tài nguyên.", "CloudTrail + S3."],
        ["Thiếu network evidence", "Khó chứng minh kết nối được chấp nhận/từ chối.", "VPC Flow Logs + CloudWatch."],
        ["Thiếu object access log", "Khó truy vết request đến bucket tài liệu.", "S3 Server Access Logging."],
        ["Security Group mở rộng", "Tăng bề mặt tấn công và dò quét dịch vụ.", "AWS Config + hardening."],
        ["Phụ thuộc SSH public", "Rủi ro brute force và lộ cổng quản trị.", "Systems Manager Session Manager."],
    ], [2500, 3300, 3200]))

    b += [page_break(), heading("5. TRIỂN KHAI AWS CLOUDTRAIL", 1)]
    b += [heading("5.1 Mục đích", 2)]
    b.append(para(
        "AWS CloudTrail ghi nhận hoạt động API và sự kiện quản trị trong tài khoản. Event history hỗ trợ tra cứu "
        "90 ngày, trong khi trail chuyển log lâu dài đến S3 để phục vụ điều tra và lưu bằng chứng."
    ))
    b += [heading("5.2 Cấu hình", 2)]
    b.append(table(["Thuộc tính", "Giá trị"], [
        ["Trail name", "security-audit-trail"],
        ["Phạm vi", "Multi-Region trail"],
        ["Event type", "Management events – Read và Write"],
        ["Destination", "S3 bucket do CloudTrail tạo"],
        ["Log file", "JSON nén .json.gz"],
        ["Region kiểm tra", "ap-southeast-1"],
    ], [3200, 5800]))
    b.append(para(
        "Trail được tạo bằng Quick trail create. AWS tự tạo bucket có policy phù hợp, bật ghi management events "
        "và tổ chức object theo AWSLogs/<account-id>/CloudTrail/<region>/<yyyy>/<mm>/<dd>/."
    ))
    b.append(figure(3, "Trang Quick trail create",
                    "Tên security-audit-trail, thông báo multi-Region và tên bucket S3 sẽ được tạo."))
    b.append(figure(4, "CloudTrail trail đang ghi log",
                    "CloudTrail → Trails, hiển thị security-audit-trail, trạng thái Logging và S3 bucket đích."))
    b.append(figure(5, "CloudTrail Event history",
                    "Danh sách tối thiểu 5 sự kiện; nên có StartSession/CreateDataChannel hoặc sự kiện quản trị gần thời điểm workshop."))
    b.append(figure(6, "Chi tiết một sự kiện CloudTrail",
                    "Event name, event source, event time, user name, source IP và event record JSON; che dữ liệu nhạy cảm."))
    b.append(figure(7, "File CloudTrail trong S3",
                    "Đường dẫn AWSLogs/.../CloudTrail/ap-southeast-1/yyyy/mm/dd và ít nhất hai file .json.gz."))
    b += [heading("5.3 Kết quả", 2)]
    b.append(para(
        "CloudTrail đã chuyển thành công các file log nén vào S3. Event history ghi nhận hoạt động Systems Manager "
        "như StartSession, CreateDataChannel và OpenDataChannel. Điều này chứng minh cả hành động của quản trị viên "
        "và hoạt động dịch vụ đều có thể truy vết."
    ))

    b += [page_break(), heading("6. TRIỂN KHAI VPC FLOW LOGS", 1)]
    b += [heading("6.1 Xác định phạm vi", 2)]
    b.append(para(
        "Flow Log được tạo trên VPC chứa document-app-server thay vì chọn một VPC mặc định. EC2 sử dụng Linux-vpc "
        "tại ap-southeast-1; do đó toàn bộ network interface trong VPC có thể phát sinh bản ghi."
    ))
    b += [heading("6.2 Cấu hình", 2)]
    b.append(table(["Thuộc tính", "Giá trị"], [
        ["Name tag", "security-vpc-flow-log"],
        ["Traffic type", "All"],
        ["Aggregation interval", "1 minute"],
        ["Destination", "CloudWatch Logs"],
        ["Log group", "/aws/vpc/flowlogs/linux-vpc"],
        ["Service role", "VPCFlowLogs-Cloudwatch-…"],
        ["Record format", "AWS default format"],
    ], [3200, 5800]))
    b.append(para(
        "AWS default format gồm version, account-id, interface-id, srcaddr, dstaddr, srcport, dstport, protocol, "
        "packets, bytes, start, end, action và log-status. Trường action có giá trị ACCEPT hoặc REJECT."
    ))
    b.append(figure(8, "EC2 và VPC ID được chọn",
                    "Instance summary thể hiện document-app-server, VPC ID Linux-vpc và private IP."))
    b.append(figure(9, "Biểu mẫu tạo VPC Flow Log",
                    "Destination CloudWatch Logs, log group, service role và AWS default format."))
    b.append(figure(10, "Flow Log trạng thái Active",
                    "Tên security-vpc-flow-log, State Active, Traffic Type All, interval 1 minute và destination log group."))
    b.append(figure(11, "CloudWatch log group và các log streams",
                    "Log group /aws/vpc/flowlogs/linux-vpc, creation time, retention và danh sách log stream eni-...-all."))
    b.append(figure(12, "Bản ghi ACCEPT trong Flow Log",
                    "Mở log stream có Last event time mới nhất và chụp một hoặc nhiều record có action ACCEPT."))
    b.append(figure(13, "Bản ghi REJECT trong Flow Log",
                    "Nếu có, lọc hoặc tìm record REJECT; nếu không có thì ghi rõ chưa phát sinh traffic bị từ chối trong thời gian quan sát."))
    b.append(figure(14, "Retention của CloudWatch Logs",
                    "Log group details hoặc danh sách log groups thể hiện retention 7 days."))
    b += [heading("6.3 Ý nghĩa điều tra", 2)]
    b.append(para(
        "Flow Logs hỗ trợ xác định nguồn/đích, cổng, giao thức, lượng packet/byte và quyết định ACCEPT/REJECT. "
        "Dữ liệu này phù hợp để điều tra dò quét cổng, kết nối bất thường, lỗi Security Group và bằng chứng network monitoring."
    ))

    b += [page_break(), heading("7. TRIỂN KHAI S3 SERVER ACCESS LOGGING", 1)]
    b += [heading("7.1 Thiết kế bucket", 2)]
    b.append(table(["Vai trò", "Bucket", "Cấu hình chính"], [
        ["Nguồn", "aws-s3-duanthuctap", "Bucket tài liệu ứng dụng; server access logging Enabled."],
        ["Đích", "document-app-access-logs-…", "Private, Block Public Access, SSE-S3, cùng Region."],
        ["Prefix", "s3-access-logs/", "Phân tách access log khỏi các object khác."],
    ], [1800, 3400, 3800]))
    b.append(para(
        "Bucket đích được tạo riêng trong ap-southeast-1. Khi bật logging từ AWS Console, bucket policy được "
        "cập nhật để service principal logging.s3.amazonaws.com có quyền s3:PutObject vào đúng prefix. "
        "Không bật logging cho chính bucket đích để tránh vòng lặp log."
    ))
    b.append(figure(15, "Danh sách bucket trước khi tạo access-log bucket",
                    "Bucket tài liệu, CloudTrail bucket và các bucket hiện có; đánh dấu bucket nguồn."))
    b.append(figure(16, "Cấu hình tạo bucket access log",
                    "Tên bucket, Region Singapore, Bucket owner enforced, Block all public access và SSE-S3."))
    b.append(figure(17, "Cấu hình Server Access Logging",
                    "Enable, destination s3://document-app-access-logs-.../s3-access-logs/ và log object key format."))
    b.append(figure(18, "Server access logging đã Enabled",
                    "Properties của aws-s3-duanthuctap hiển thị Enabled, destination bucket và key format."))
    b.append(figure(19, "Bucket policy cho S3 log delivery",
                    "Permissions của bucket đích, statement có logging.s3.amazonaws.com và s3:PutObject. Che Account ID nếu cần."))
    b.append(figure(20, "Object access log trong bucket đích",
                    "Sau khi chờ AWS chuyển log, chụp object dưới prefix s3-access-logs/. Có thể cần vài giờ vì delivery là best-effort."))
    b += [heading("7.2 Lưu ý vận hành", 2)]
    for x in [
        "S3 Server Access Logging không giao log theo thời gian thực và có thể chậm vài giờ.",
        "Việc bucket đích trống ngay sau khi bật không đồng nghĩa cấu hình thất bại.",
        "Nên tạo request bằng cách mở/tải object ở bucket nguồn rồi kiểm tra lại sau.",
        "Không tải file thủ công vào bucket đích vì sẽ làm lẫn dữ liệu minh chứng.",
    ]:
        b.append(bullet(x))

    b += [page_break(), heading("8. TRIỂN KHAI AWS CONFIG", 1)]
    b += [heading("8.1 Chiến lược ghi nhận", 2)]
    b.append(para(
        "Để hạn chế số lượng configuration item và chi phí, recorder chỉ ghi ba resource types theo chế độ Continuous. "
        "AWS Config service-linked role được dùng thay vì cấp quyền cho một IAM role tùy ý. Configuration history "
        "được chuyển đến bucket config-bucket-…; SNS không được bật trong workshop."
    ))
    b.append(table(["Thành phần", "Cấu hình"], [
        ["Recording strategy", "Specific resource types"],
        ["AWS::EC2::Instance", "Continuous"],
        ["AWS::EC2::SecurityGroup", "Continuous"],
        ["AWS::S3::Bucket", "Continuous"],
        ["IAM role", "AWS Config service-linked role"],
        ["Delivery channel", "S3 config-bucket-…"],
        ["SNS", "Không bật"],
    ], [3300, 5700]))
    b += [heading("8.2 Managed rules", 2)]
    b.append(table(["Rule", "Mục tiêu", "Kết quả ban đầu"], [
        ["restricted-ssh", "Phát hiện Security Group cho phép TCP/22 từ 0.0.0.0/0 hoặc ::/0.", "2 Noncompliant resources"],
        ["s3-bucket-public-read-prohibited", "Kiểm tra bucket S3 không cho phép public read.", "Compliant"],
    ], [2900, 4400, 1700]))
    b.append(figure(21, "AWS Config Get started",
                    "Trang khởi tạo AWS Config tại Region Singapore, nút Get started."))
    b.append(figure(22, "Specific resource types và tần suất Continuous",
                    "Ba dòng EC2 Instance, EC2 SecurityGroup và S3 Bucket; mỗi dòng có Frequency Continuous."))
    b.append(figure(23, "IAM role và delivery channel của AWS Config",
                    "Service-linked role, Create a bucket/config-bucket-... và SNS không được chọn."))
    b.append(figure(24, "Review AWS Config trước Confirm",
                    "Recorded resource types (3), delivery bucket và hai Config rules."))
    b.append(figure(25, "Kết quả đánh giá AWS Config ban đầu",
                    "Rules page thể hiện restricted-ssh có 2 Noncompliant resources và S3 rule Compliant."))

    b += [page_break(), heading("9. PHÁT HIỆN VÀ KHẮC PHỤC SECURITY GROUP", 1)]
    b += [heading("9.1 Phát hiện", 2)]
    b.append(para(
        "Rule restricted-ssh phát hiện hai Security Group: Linux-SG thuộc VPC ứng dụng và Windows-SG thuộc một VPC khác. "
        "Linux-SG mở SSH 22 cho toàn Internet, đồng thời còn mở backend 5000 và MySQL 3306. Windows-SG là tài nguyên cũ "
        "không thuộc Linux-vpc nhưng vẫn bị AWS Config đánh giá do recorder ghi mọi EC2 Security Group thuộc loại đã chọn."
    ))
    b.append(figure(26, "Chi tiết restricted-ssh trước khắc phục",
                    "Last evaluation Successful, Detective compliance Noncompliant và hai Security Group ID trong Resources in scope."))
    b.append(figure(27, "Inbound rules ban đầu của Linux-SG",
                    "Hiển thị HTTP 80, HTTPS 443, SSH 22, Custom TCP 5000, MySQL 3306 và ICMP cùng source 0.0.0.0/0."))
    b.append(figure(28, "Inbound rules ban đầu của Windows-SG",
                    "Hiển thị SSH 22, RDP 3389, MySQL 3306, port 5000, HTTP/HTTPS và ICMP mở 0.0.0.0/0."))
    b += [heading("9.2 Phân tích và quyết định", 2)]
    b.append(table(["Rule/cổng", "Phân tích", "Quyết định"], [
        ["SSH 22", "Session Manager đã sẵn sàng; không cần SSH public.", "Xóa 0.0.0.0/0."],
        ["Custom TCP 5000", "Nginx proxy đến 127.0.0.1:5000.", "Xóa public ingress."],
        ["MySQL 3306", "Backend dùng DynamoDB, không có dependency MySQL.", "Xóa public ingress."],
        ["ICMP", "Không phải yêu cầu nghiệp vụ của web app.", "Xóa để giảm bề mặt."],
        ["HTTP 80 / HTTPS 443", "Cổng phục vụ website.", "Giữ công khai."],
        ["Windows-SG", "Thuộc VPC khác, không còn tài nguyên dự án sử dụng.", "Xác minh liên kết rồi xóa SG."],
    ], [1900, 4100, 3000]))
    b += [heading("9.3 Các thay đổi đã thực hiện", 2)]
    for x in [
        "Xóa ingress SSH 22 từ 0.0.0.0/0 trên Linux-SG.",
        "Xóa public ingress đến backend port 5000.",
        "Xóa MySQL/Aurora 3306 do ứng dụng sử dụng DynamoDB.",
        "Xóa các ICMP rules không cần thiết.",
        "Giữ HTTP 80 và HTTPS 443 để website tiếp tục hoạt động.",
        "Xác định Windows-SG thuộc VPC khác và xóa tài nguyên không còn sử dụng.",
    ]:
        b.append(bullet(x))
    b.append(figure(29, "Preview changes của Linux-SG",
                    "Màn hình Edit inbound rules/Preview changes, chỉ còn các cổng thực sự cần trước khi Save rules."))
    b.append(figure(30, "Linux-SG sau hardening",
                    "Inbound rules sau lưu, ưu tiên thể hiện chỉ HTTP 80 và HTTPS 443; chụp thêm Related resources nếu cần."))
    b.append(figure(31, "Xác minh Windows-SG không còn được sử dụng",
                    "Related resources trống hoặc bằng chứng VPC khác; nếu đã xóa thì chụp CloudTrail DeleteSecurityGroup hoặc Config resource timeline."))

    b += [page_break(), heading("10. XÁC MINH SAU KHẮC PHỤC", 1)]
    b += [heading("10.1 Kiểm tra AWS Config", 2)]
    b.append(para(
        "Sau khi Security Group thay đổi và tài nguyên cũ được xóa, AWS Config tự đánh giá lại. Hai managed rules đều "
        "chuyển thành Compliant. Kết quả này chứng minh vòng đời Detect → Investigate → Remediate → Verify đã hoàn tất."
    ))
    b.append(figure(32, "AWS Config sau khắc phục",
                    "Rules page hiển thị restricted-ssh và s3-bucket-public-read-prohibited đều có dấu xanh Compliant."))
    b += [heading("10.2 Kiểm tra website", 2)]
    b.append(figure(33, "Trang đăng nhập vẫn hoạt động",
                    "Website sau hardening, trang Login tải thành công qua HTTP/HTTPS."))
    b.append(figure(34, "Dashboard tài liệu sau đăng nhập",
                    "Danh sách tài liệu, trạng thái AWS/health và thông tin người dùng; tránh hiển thị token hoặc dữ liệu nhạy cảm."))
    b.append(figure(35, "Kiểm thử upload/download tài liệu",
                    "Thông báo upload thành công hoặc file xuất hiện trong danh sách; có thể chụp thêm object tương ứng trong S3."))
    b += [heading("10.3 Kiểm tra Session Manager", 2)]
    b.append(code(
        "whoami\n"
        "hostname\n"
        "curl http://127.0.0.1:5000/api/health\n"
        "sudo systemctl status nginx --no-pager"
    ))
    b.append(para(
        "Kết quả thực tế: phiên chạy dưới ssm-user; hostname đúng EC2; health API trả status=ok với documents_table, "
        "incidents_table và s3 đều ok=true; Nginx active (running). Điều này xác nhận đóng SSH không làm mất khả năng quản trị."
    ))
    b.append(figure(36, "Session Manager và kết quả health check",
                    "Terminal thể hiện whoami=ssm-user, hostname, JSON health status ok và nginx active (running). Che Session ID/Instance ID nếu công khai."))
    b.append(figure(37, "CloudTrail ghi nhận phiên Session Manager",
                    "Event history hoặc event detail cho StartSession/CreateDataChannel sau khi hardening."))

    b += [heading("11. KẾT QUẢ VÀ ĐÁNH GIÁ", 1)]
    b.append(table(["Hạng mục", "Trước workshop", "Sau workshop"], [
        ["Management audit", "Chỉ có Event history ngắn hạn.", "Multi-Region trail và log lâu dài trong S3."],
        ["Network monitoring", "Không có bằng chứng flow tập trung.", "CloudWatch có Flow Log stream theo ENI."],
        ["S3 access", "Không có bucket log truy cập riêng.", "Server Access Logging Enabled."],
        ["Configuration compliance", "Không có rule đánh giá tự động.", "Hai AWS managed rules hoạt động."],
        ["SSH exposure", "Hai Security Group Noncompliant.", "restricted-ssh Compliant."],
        ["Ứng dụng", "Hoạt động.", "Vẫn hoạt động sau hardening."],
        ["Quản trị EC2", "Có SSH public.", "Session Manager; không cần port 22."],
    ], [2200, 3300, 3500]))
    b += [heading("11.1 Giá trị an ninh", 2)]
    for x in [
        "Tăng khả năng truy vết và trách nhiệm giải trình đối với hoạt động quản trị.",
        "Có dữ liệu mạng phục vụ điều tra kết nối bất thường và lỗi kiểm soát truy cập.",
        "Có bằng chứng truy cập bucket tài liệu tách biệt với dữ liệu nghiệp vụ.",
        "Tự động phát hiện cấu hình không tuân thủ thay vì chỉ kiểm tra thủ công.",
        "Giảm bề mặt tấn công bằng cách loại bỏ cổng quản trị và dịch vụ nội bộ khỏi Internet.",
        "Chứng minh thay đổi bảo mật không gây gián đoạn bằng kiểm thử sau khắc phục.",
    ]:
        b.append(bullet(x))

    b += [heading("12. CHI PHÍ VÀ VẬN HÀNH", 1)]
    b.append(table(["Dịch vụ", "Nguồn chi phí", "Biện pháp kiểm soát"], [
        ["CloudTrail", "S3 storage/request; event copy bổ sung nếu cấu hình thêm.", "Chỉ management events cần thiết; lifecycle cho log."],
        ["VPC Flow Logs", "CloudWatch Logs ingestion và storage.", "Một VPC, retention 7 ngày, xóa khi kết thúc lab."],
        ["S3 access logging", "Object log và request ghi vào S3.", "Bucket riêng, lifecycle phù hợp."],
        ["AWS Config", "Configuration item và rule evaluation.", "Chỉ 3 resource types và 2 rules."],
        ["S3 Config bucket", "Configuration history/snapshot.", "Lifecycle và dừng recorder sau demo nếu được phép."],
    ], [2200, 3500, 3300]))
    b += [heading("12.1 Khuyến nghị sau khi nộp bài", 2)]
    for x in [
        "Giữ nguyên tài nguyên cho đến khi chụp đủ ảnh và được chấm/demo xong.",
        "Đặt CloudWatch log retention 7 ngày cho VPC Flow Logs.",
        "Thiết lập S3 Lifecycle theo chính sách môn học, ví dụ 30–90 ngày cho log lab.",
        "Nếu môi trường chỉ dùng thực hành: dừng AWS Config recorder, xóa Config rules và Flow Log sau khi được phép.",
        "Không xóa CloudTrail hoặc log khi vẫn cần bằng chứng kiểm toán.",
    ]:
        b.append(bullet(x))

    b += [page_break(), heading("13. DANH MỤC ẢNH MINH CHỨNG", 1)]
    evidence_rows = [
        ["01–02", "Kiến trúc và EC2/VPC", "Bắt buộc", "Che Account ID, Public IP"],
        ["03–07", "CloudTrail", "Bắt buộc", "Trail, event, event detail, S3 objects"],
        ["08–14", "VPC Flow Logs", "Bắt buộc", "Active, log streams, ACCEPT/REJECT, retention"],
        ["15–20", "S3 Server Access Logging", "Bắt buộc", "Bucket, Enabled, policy, object log"],
        ["21–25", "AWS Config setup", "Bắt buộc", "Recorder, delivery, rules, initial finding"],
        ["26–31", "Điều tra và hardening", "Bắt buộc", "Before/after SG, Windows-SG evidence"],
        ["32", "AWS Config Compliant", "Bắt buộc", "Hai dấu xanh"],
        ["33–35", "Website functional test", "Nên có", "Login, dashboard, upload/download"],
        ["36–37", "Session Manager và audit", "Bắt buộc", "Health, Nginx, StartSession"],
    ]
    b.append(table(["Số hình", "Nhóm minh chứng", "Mức độ", "Lưu ý"], evidence_rows,
                   [1300, 3100, 1500, 3100]))
    b += [heading("13.1 Quy tắc chụp ảnh", 2)]
    for x in [
        "Ảnh phải thấy tên dịch vụ, Region, tên tài nguyên và trạng thái quan trọng.",
        "Không cắt mất breadcrumb hoặc tiêu đề trang; tránh chụp quá nhiều khoảng trắng.",
        "Che Account ID, Session ID, Public IP, email, token, secret và URL ký tạm thời nếu báo cáo được công khai.",
        "Mỗi ảnh có số hình, chú thích và một đoạn giải thích kết quả ngay bên dưới.",
        "Ưu tiên cặp ảnh trước/sau để chứng minh tác động của biện pháp khắc phục.",
        "Không dùng ảnh chỉ có thông báo thành công; nên chụp cả trạng thái tài nguyên sau thao tác.",
    ]:
        b.append(bullet(x))

    b += [heading("14. KẾT LUẬN", 1)]
    b.append(para(
        "Workshop đã hoàn thiện một chu trình giám sát và kiểm toán an ninh có thể kiểm chứng trên AWS. "
        "CloudTrail cung cấp dấu vết quản trị; VPC Flow Logs cung cấp bằng chứng mạng; S3 Server Access Logging "
        "ghi nhận truy cập dữ liệu; AWS Config theo dõi cấu hình và đánh giá tuân thủ. Từ phát hiện hai Security Group "
        "không tuân thủ, nhóm đã điều tra, loại bỏ cổng không cần thiết và xóa tài nguyên cũ. Kết quả cuối cùng cho thấy "
        "hai Config rules đều Compliant, trong khi website, backend, DynamoDB, S3, Nginx và Session Manager vẫn hoạt động."
    ))
    b.append(para(
        "Kết quả không chỉ dừng ở việc bật dịch vụ mà còn chứng minh hiệu quả kiểm soát theo chuỗi Thu thập log → "
        "Giám sát → Phát hiện → Điều tra → Khắc phục → Xác minh. Đây là nền tảng phù hợp để mở rộng GuardDuty, "
        "Security Hub, CloudWatch alarms hoặc tự động remediation trong giai đoạn sau."
    ))

    b += [page_break(), heading("PHỤ LỤC A. LỆNH KIỂM TRA", 1)]
    b += [heading("A.1 Kiểm tra ứng dụng trong Session Manager", 2)]
    b.append(code(
        "whoami\n"
        "hostname\n"
        "curl http://127.0.0.1:5000/api/health\n"
        "sudo systemctl status nginx --no-pager"
    ))
    b += [heading("A.2 Diễn giải Flow Log mặc định", 2)]
    b.append(code(
        "version account-id interface-id srcaddr dstaddr srcport dstport "
        "protocol packets bytes start end action log-status"
    ))
    b += [heading("A.3 Đường dẫn log tham chiếu", 2)]
    b.append(code(
        "CloudTrail: s3://aws-cloudtrail-logs-.../AWSLogs/<account-id>/CloudTrail/ap-southeast-1/\n"
        "VPC Flow Logs: CloudWatch Logs /aws/vpc/flowlogs/linux-vpc\n"
        "S3 Access Logs: s3://document-app-access-logs-.../s3-access-logs/\n"
        "AWS Config: s3://config-bucket-.../AWSLogs/<account-id>/Config/ap-southeast-1/"
    ))

    b += [heading("PHỤ LỤC B. CHECKLIST NGHIỆM THU", 1)]
    checks = [
        "CloudTrail security-audit-trail đang Logging.",
        "CloudTrail là multi-Region trail.",
        "S3 CloudTrail bucket có file .json.gz.",
        "Event history có sự kiện quản trị gần thời điểm demo.",
        "VPC Flow Log security-vpc-flow-log đang Active.",
        "CloudWatch log group có log streams theo ENI.",
        "Có ảnh record ACCEPT và/hoặc REJECT.",
        "CloudWatch retention đã đặt 7 ngày.",
        "S3 Server Access Logging của bucket nguồn đang Enabled.",
        "Bucket đích access log private và có policy log delivery.",
        "AWS Config ghi đúng 3 resource types theo Continuous.",
        "Chỉ bật 2 managed rules theo phạm vi workshop.",
        "Có ảnh restricted-ssh trước khắc phục.",
        "Linux-SG không còn SSH 22 và port 5000 public.",
        "Windows-SG cũ đã được xác minh và xóa.",
        "restricted-ssh sau khắc phục là Compliant.",
        "s3-bucket-public-read-prohibited là Compliant.",
        "Website đăng nhập và thao tác tài liệu bình thường.",
        "Session Manager kết nối được khi port 22 đã đóng.",
        "Health API và Nginx đều OK.",
        "Ảnh đã che thông tin nhạy cảm trước khi nộp công khai.",
    ]
    for x in checks:
        b.append(bullet("☐ " + x))
    return "".join(b)


def main() -> None:
    path = OUT / "Bao_cao_Workshop_Giam_sat_Kiem_toan_An_ninh_AWS.docx"
    make_docx(path, body(), "Báo cáo Workshop giám sát và kiểm toán an ninh AWS")
    print(path)


if __name__ == "__main__":
    main()
