from pathlib import Path
import re

from generate_word_docs import bullet, code, cover, heading, make_docx, page_break, para, table


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "Workshop_AWS_Quan_ly_tai_lieu_va_phan_ung_su_co.docx"

FILES = [
    ROOT / "5-Workshop/_index.vi.md",
    ROOT / "5-Workshop/5.1-Workshop-overview/_index.vi.md",
    ROOT / "5-Workshop/5.2-Prerequiste/_index.vi.md",
    ROOT / "5-Workshop/5.3-S3-vpc/_index.vi.md",
    ROOT / "5-Workshop/5.3-S3-vpc/5.3.1-create-gwe/_index.vi.md",
    ROOT / "5-Workshop/5.3-S3-vpc/5.3.2-test-gwe/_index.vi.md",
    ROOT / "5-Workshop/5.4-S3-onprem/_index.vi.md",
    ROOT / "5-Workshop/5.4-S3-onprem/5.4.1-prepare/_index.vi.md",
    ROOT / "5-Workshop/5.4-S3-onprem/5.4.2-create-interface-enpoint/_index.vi.md",
    ROOT / "5-Workshop/5.4-S3-onprem/5.4.3-test-endpoint/_index.vi.md",
    ROOT / "5-Workshop/5.4-S3-onprem/5.4.4-dns-simulation/_index.vi.md",
    ROOT / "5-Workshop/5.5-Policy/_index.vi.md",
    ROOT / "5-Workshop/5.6-Cleanup/_index.vi.md",
]


def clean_inline(text):
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("**", "").replace("`", "")
    return text.strip()


def parse_markdown(path):
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"^---\s*.*?\s*---\s*", "", raw, count=1, flags=re.S)
    lines = raw.splitlines()
    result = []
    i = 0
    in_notice = False
    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()
        if stripped.startswith("{{% notice"):
            in_notice = True
            i += 1
            continue
        if stripped == "{{% /notice %}}":
            in_notice = False
            i += 1
            continue
        if stripped.startswith("```"):
            language = stripped[3:]
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            result.append(code("\n".join(block)))
            i += 1
            continue
        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-+", lines[i + 1]):
            headers = [clean_inline(x) for x in stripped.strip("|").split("|")]
            rows = []
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = [clean_inline(x) for x in lines[i].strip().strip("|").split("|")]
                if len(row) == len(headers):
                    rows.append(row)
                i += 1
            result.append(table(headers, rows))
            continue
        match = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if match:
            level = min(len(match.group(1)), 3)
            result.append(heading(clean_inline(match.group(2)), level))
        elif re.match(r"^[-*]\s+", stripped):
            result.append(bullet(clean_inline(re.sub(r"^[-*]\s+", "", stripped))))
        elif re.match(r"^\d+\.\s+", stripped):
            result.append(bullet(clean_inline(stripped), 0))
        elif stripped:
            result.append(para(clean_inline(stripped), italic=in_notice, color="9C5700" if in_notice else None))
        i += 1
    return "".join(result)


def main():
    body = [cover(
        "PHẦN 5 – WORKSHOP",
        "Xây dựng hệ thống quản lý tài liệu và phản ứng sự cố bảo mật tự động trên AWS",
    )]
    body.append(heading("NỘI DUNG WORKSHOP", 1))
    for item in [
        "5.1. Giới thiệu và kiến trúc",
        "5.2. Các bước chuẩn bị",
        "5.3. Triển khai ứng dụng quản lý tài liệu",
        "5.4. Phản ứng sự cố bảo mật tự động",
        "5.5. Giám sát bằng CloudWatch và Grafana",
        "5.6. Dọn dẹp tài nguyên",
    ]:
        body.append(bullet(item))
    body.append(page_break())
    for index, path in enumerate(FILES):
        body.append(parse_markdown(path))
        if index in (0, 1, 2, 5, 10, 11):
            body.append(page_break())
    make_docx(OUT, "".join(body), "Phần 5 – Workshop AWS")
    print(OUT)


if __name__ == "__main__":
    main()
