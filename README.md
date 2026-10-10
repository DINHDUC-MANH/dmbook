# DMBook — bản Online + nhắc nhở email hằng ngày

Gói này gồm:
- `index.html` — toàn bộ ứng dụng DMBook (1 file, chạy offline, dữ liệu lưu trong trình duyệt).
- `.github/workflows/daily-email.yml` — lịch chạy tự động mỗi ngày 5:00 sáng (giờ Việt Nam).
- `scripts/send_reminder.py` — script gửi email nhắc nhở qua Gmail.

**Đọc trước:** email nhắc nhở là nội dung CHUNG, không kèm số liệu thật trong app của bạn
(task gì, ăn gì hôm qua...) vì dữ liệu DMBook chỉ nằm trong trình duyệt của bạn, máy chủ
gửi mail không đọc được. Để có email cá nhân hóa theo đúng dữ liệu thật, cần nâng cấp lên
backend riêng (xem mục "Bước tiếp theo" cuối file).

---

## Phần 1 — Đưa DMBook lên mạng (hosting tĩnh, miễn phí)

Cách đơn giản nhất: **GitHub Pages** (dùng chung tài khoản GitHub với phần email ở Phần 2).

1. Tạo tài khoản GitHub (nếu chưa có): https://github.com/signup
2. Tạo repository mới, đặt tên `dmbook` (chọn Public hoặc Private đều được).
3. Giải nén file zip — các file nằm ngay ở thư mục gốc (`index.html`, `README.md`,
   `scripts/`, `.github/`), **không có thư mục bọc ngoài nào cả**, nên kéo-thả toàn bộ
   nội dung đã giải nén thẳng vào trang "Add file → Upload files" của repo là xong,
   không cần tạo hay di chuyển gì thêm.
   ⚠️ Lưu ý riêng cho thư mục `.github`: đây là thư mục **ẩn** theo quy ước của hệ điều
   hành (tên bắt đầu bằng dấu chấm). Nếu dùng Finder (Mac) hoặc File Explorer (Windows)
   để kéo-thả, hãy bật hiển thị file/thư mục ẩn trước (Mac: `Cmd+Shift+.` ; Windows: tab
   "View" → tích "Hidden items") để chắc chắn `.github` cũng được kéo theo — thiếu thư
   mục này thì lịch gửi email sẽ không chạy.
4. Vào **Settings → Pages** của repo → mục "Build and deployment" → Source chọn
   **"Deploy from a branch"** → Branch chọn `main` / thư mục `/ (root)` → Save.
5. Sau khoảng 1 phút, GitHub cho bạn một đường link dạng:
   `https://<tên-tài-khoản>.github.io/dmbook/`
   Đó chính là bản DMBook "Online" của bạn — mở được từ bất kỳ máy tính/điện thoại nào,
   cài "Thêm vào màn hình chính" để dùng như app thật.

Lưu ý: dữ liệu vẫn lưu riêng theo từng trình duyệt/thiết bị (localStorage) như bản trước —
đưa lên mạng chỉ giúp có **một địa chỉ cố định** để mở từ mọi nơi, chưa phải đồng bộ dữ liệu
tự động giữa các thiết bị. Vẫn dùng **Sao lưu / Khôi phục (gộp)** để đồng bộ tay như đã làm.

---

## Phần 2 — Bật email nhắc nhở 5h sáng hằng ngày

### Bước 1: Tạo Gmail App Password (không dùng mật khẩu Gmail chính)
1. Vào https://myaccount.google.com/security
2. Bật **Xác minh 2 bước** nếu chưa bật (bắt buộc để tạo App Password).
3. Vào https://myaccount.google.com/apppasswords → tạo mật khẩu ứng dụng mới, đặt tên
   "DMBook" → Google cho ra một chuỗi 16 ký tự — **copy lại**, đây là `GMAIL_APP_PASSWORD`.
   (Bạn có thể dùng chính Gmail `manhdd.cv@gmail.com` để vừa gửi vừa nhận, hoặc tạo một
   Gmail phụ riêng để gửi cho gọn.)

### Bước 2: Khai báo Secrets trong repo GitHub
Vào repo `dmbook` → **Settings → Secrets and variables → Actions → New repository secret**,
tạo lần lượt 3 secret:

| Tên secret            | Giá trị                                                   |
|------------------------|------------------------------------------------------------|
| `GMAIL_USER`           | Địa chỉ Gmail dùng để **gửi** (vd: manhdd.cv@gmail.com)    |
| `GMAIL_APP_PASSWORD`   | Chuỗi 16 ký tự lấy ở Bước 1                                |
| `DMBOOK_URL`           | Link DMBook của bạn (link GitHub Pages ở Phần 1, hoặc link artifact hiện tại) |

### Bước 3: Xong — lịch đã tự chạy
File `.github/workflows/daily-email.yml` đã cấu hình sẵn chạy lúc **22:00 UTC = 5:00 sáng
giờ Việt Nam** mỗi ngày, không cần làm gì thêm.

Muốn **test ngay** không cần chờ đến 5h sáng: vào tab **Actions** của repo → chọn workflow
"DMBook Daily Reminder Email" → bấm **"Run workflow"** → chạy thủ công, kiểm tra hộp mail.

---

## Giới hạn cần biết
- GitHub Actions free cho repo public là miễn phí không giới hạn cho việc này; repo private
  có một lượng phút miễn phí/tháng, một email/ngày dùng không đáng kể.
- Giờ chạy cron của GitHub Actions có thể trễ vài phút so với giờ hẹn (do lịch chạy theo
  hàng đợi chung của GitHub) — không đảm bảo đúng tuyệt đối 5:00:00.
- Email là lời nhắc chung, không đọc được dữ liệu thật trong DMBook.

## Bước tiếp theo (nếu muốn email có số liệu thật)
Cần xây một backend riêng (đúng kiến trúc trong bản đặc tả gốc: FastAPI + SQLite) để:
- Lưu dữ liệu tập trung thay vì chỉ trong trình duyệt.
- Script gửi email có thể truy vấn dữ liệu thật (task hôm qua, kcal đã ăn, mục tiêu...) 
  rồi đưa vào nội dung email, giống mục "Daily Briefing / Daily Review" trong đặc tả.
Đây là một dự án riêng, lớn hơn nhiều so với gói này — báo lại khi bạn muốn làm bước đó.
