"""
DMBook — script gửi email nhắc nhở hằng ngày.
Chạy bởi GitHub Actions theo lịch (xem .github/workflows/daily-email.yml).

Biến môi trường cần có (đặt trong GitHub repo Settings -> Secrets and variables -> Actions):
  GMAIL_USER          địa chỉ Gmail dùng để gửi (vd: dmbook.sender@gmail.com)
  GMAIL_APP_PASSWORD  Mật khẩu ứng dụng Gmail (App Password) - KHÔNG phải mật khẩu đăng nhập thường
  TO_EMAIL            địa chỉ nhận (đặt sẵn mặc định: manhdd.cv@gmail.com)
  DMBOOK_URL          liên kết mở DMBook (artifact link hoặc link trang bạn tự host)

Lưu ý quan trọng: email này CHỈ LÀ LỜI NHẮC CHUNG, không kèm số liệu thật của bạn,
vì dữ liệu DMBook hiện chỉ lưu trong trình duyệt (localStorage) của từng thiết bị -
script chạy trên máy chủ GitHub không đọc được dữ liệu đó.
"""
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from datetime import datetime, timezone, timedelta

GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
TO_EMAIL = os.environ.get("TO_EMAIL", "manhdd.cv@gmail.com")
DMBOOK_URL = os.environ.get("DMBOOK_URL", "(chưa cấu hình DMBOOK_URL trong Secrets)")

# Giờ Việt Nam (ICT, UTC+7) cho đúng ngày hiển thị trong email
ict_now = datetime.now(timezone.utc) + timedelta(hours=7)
today_str = ict_now.strftime("%d/%m/%Y")

BODY = f"""Chào buổi sáng,

Đã 5:00 sáng ngày {today_str} - đây là lời nhắc hằng ngày từ DMBook.

Dành vài phút để:
  1. Review lại hôm qua - nhiệm vụ đã hoàn thành, mục tiêu còn dang dở.
  2. Nhập dữ liệu sức khỏe, bữa ăn, vận động, tâm trạng, tài chính của hôm qua nếu chưa kịp ghi.
  3. Đặt ra ba việc quan trọng nhất cho hôm nay.

Mở DMBook tại đây:
{DMBOOK_URL}

---
Đây là email nhắc nhở tự động, nội dung chung (chưa kèm số liệu thật của bạn).
— DMBook Daily Reminder
"""

msg = MIMEText(BODY, "plain", "utf-8")
msg["Subject"] = f"[DMBook] Nhắc nhập liệu & review ngày {today_str}"
msg["From"] = GMAIL_USER
msg["To"] = TO_EMAIL

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    server.sendmail(GMAIL_USER, [TO_EMAIL], msg.as_string())

print(f"Đã gửi email nhắc nhở tới {TO_EMAIL} lúc {ict_now.isoformat()} (giờ VN)")
