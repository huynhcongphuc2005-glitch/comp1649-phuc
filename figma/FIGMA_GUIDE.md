# Hướng dẫn import vào Figma Design (html.to.design)

Mỗi file `NN-*.html` trong thư mục này là **một frame 430 × 932**, không có khung iPhone, không JavaScript.
`index.html` chỉ để xem nhanh, **không import file này**.

## 1. Mở các màn trên một URL công khai

html.to.design import từ URL, nên các file cần được phục vụ qua web:

- Cách nhanh nhất: dùng **Live Server** trong VS Code (đã cấu hình port 5501), chuột phải `figma/01-today.html` → *Open with Live Server*.
  Plugin chạy trên máy bạn nên `http://127.0.0.1:5501/figma/01-today.html` thường dùng được. Nếu không được, dùng cách dưới.
- Hoặc đẩy repo lên GitHub Pages / Netlify Drop rồi dùng URL công khai.

## 2. Import

1. Figma Design → *Plugins* → **html.to.design** → tab *URL*.
2. Viewport: **Custom 430 × 932** (hoặc chọn iPhone 14 Pro Max / 15 Plus, cùng kích thước).
3. Import lần lượt 12 file theo thứ tự dưới đây. Đổi tên frame đúng như cột "Frame".
4. Bật *Auto layout* trong tùy chọn của plugin nếu có: các màn được dựng bằng flexbox nên sẽ ra Auto layout sạch.

| Frame | File |
|---|---|
| 01 Today | `01-today.html` |
| 02 Plan | `02-plan.html` |
| 03 Step | `03-step.html` |
| 04 Focus | `04-focus.html` |
| 04b Focus paused | `04b-focus-paused.html` |
| 05 Rest | `05-rest.html` |
| 06 Calm | `06-calm.html` |
| 06b Calm quiet mode | `06b-calm-muted.html` |
| 07 Settings | `07-settings.html` |
| 07b Settings applied | `07b-settings-applied.html` |
| 08 Progress | `08-progress.html` |
| 00 Today (control) | `00-today-dashboard.html` — chỉ dùng cho nghiên cứu (mục 5) |

Font: Inter và Atkinson Hyperlegible đều là Google Fonts, Figma có sẵn.

## 3. Tạo component (khuyến nghị, thể hiện tính nhất quán)

Chọn trên frame 01 rồi *Create component* (⌥⌘K): **Tab bar**, **Calm pill**, **Button / Primary**, **Button / Secondary**, **Segmented control**, **Toggle**.
Thay các bản sao ở các frame khác bằng instance của component.

## 4. Nối interaction (tab *Prototype*)

Mặc định: **On tap → Navigate to**, *Smart animate*, 200 ms, *Ease out*. Starting frame: **01 Today**. Thiết bị: iPhone 14 Pro Max.

| From frame | Phần tử | To frame |
|---|---|---|
| 01 Today | Start focus | 04 Focus |
| 01 Today | Details | 03 Step |
| 01 Today | 2 more steps today | 02 Plan |
| 02 Plan | nút ▶ ở bước hiện tại | 03 Step |
| 03 Step | Start 15-minute focus | 04 Focus |
| 03 Step / 04 Focus | nút ‹ Back | 02 Plan / 03 Step |
| 04 Focus | Pause | 04b Focus paused |
| 04b Focus paused | Resume | 04 Focus |
| 04 / 04b | I finished early, end this step | 05 Rest |
| 05 Rest | Start rest, Stop here for today | 01 Today |
| Mọi frame | Calm (góc phải trên) | 06 Calm |
| 06 Calm | Start breathing | 06b Calm quiet mode |
| 06b | Stop breathing guide | 06 Calm |
| 06 / 06b | ‹ Back, I'm okay, back to Today | 01 Today |
| 06 / 06b | Talk to someone | 08 Progress |
| 07 Settings | segment Night (Colour) | 07b Settings applied (dùng *Instant*) |
| Tab bar (mọi frame) | Today / Plan / Progress / Settings | 01 / 02 / 08 / 07 |

Mẹo: nối Tab bar và Calm pill **trong component** một lần, mọi instance sẽ tự có link.

Cho nghiên cứu A/B: tạo flow thứ hai bắt đầu từ **00 Today (control)**, nối mỗi ô bước tới 03 Step.

## 5. Nộp bài

*File → Save local copy…* → `.fig`. Kiểm tra bằng *Present* (▶) rằng đi được cả 3 journey.

## Sửa màn hình

Không sửa HTML bằng tay: sửa `scripts/build_screens.py` rồi chạy

```bash
python3 scripts/build_screens.py   # tạo lại figma/*.html
bash scripts/capture.sh            # chụp lại figma/png/*.png (860 × 1864, @2x)
```
