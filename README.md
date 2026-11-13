# COMP1649 HCI Coursework: NeuroPulse HE (Option A)

Hướng dẫn sử dụng bộ tài liệu dành cho Phúc. Đọc hết một lượt trước khi sửa.

## 1. Bộ tài liệu gồm những gì

| Đường dẫn | Là gì |
|---|---|
| `report/COMP1649_Coursework_Report.docx` | Report chính (khoảng 3.000 từ, 12 references Harvard, Appendix A–F) |
| `report/figures/sketches/` | Hình phác thảo tay dùng trong report (bản mẫu, **cần vẽ lại**) |
| `report/figures/` | Ảnh màn hình (`screen-*.png`), hình Norman (`norman-*.png`), sơ đồ flow (`flow-*.png`) |
| `figma/` | 12 màn hình HTML để import vào Figma bằng html.to.design |
| `figma/png/` | Ảnh chụp từng màn hình |
| `figma/FIGMA_GUIDE.md` | Hướng dẫn import và nối tương tác trong Figma |
| `scripts/` | Script tạo lại màn hình, hình và report |

Brief yêu cầu nộp **2 file**: report dạng **PDF** và prototype dạng **.fig** (Figma Design).

## 2. Việc cần làm trước khi nộp (theo thứ tự)

### Bước 1. Điền tên, MSSV, tutor

Có hai cách, chọn **một**:

- **Sửa trực tiếp trong Word** (đơn giản nhất): mở `report/COMP1649_Coursework_Report.docx`, sửa trang bìa:
  `[Student name]`, `[Student ID]`, `[Tutor name]`.
- **Sửa trong script** (nếu sẽ build lại report): mở `scripts/build_report.py`, sửa dòng
  `STUDENT = {"name": "[Student name]", "id": "[Student ID]", "tutor": "[Tutor name]", ...}`
  rồi chạy lại script (xem mục 4).

> Lưu ý: nếu đã sửa tay trong Word rồi chạy lại script, mọi chỉnh tay trong Word sẽ **bị ghi đè**. Đã sửa tay thì không chạy script nữa.

Cũng điền thông tin liên hệ ở **Appendix B1** (`[Researcher name and university email]`, `[Supervisor name and email]`).

### Bước 2. Figma (chưa cần link)

- Report hiện **không có link Figma**, chưa cần thêm.
- Làm prototype theo `figma/FIGMA_GUIDE.md`: import 12 màn, nối tương tác theo bảng ở Appendix F, kiểm tra bằng Present (▶) đi được cả 3 journey.
- Nộp file `.fig` (File → Save local copy).

### Bước 3. Vẽ lại sketch bằng tay (quan trọng)

Report viết rằng các sketch được vẽ bằng bút chì trên giấy. Các ảnh hiện tại là **bản mẫu do máy vẽ**. Phải vẽ lại thật, nếu không là khai sai quá trình làm bài.

Cách làm:
1. Vẽ trên giấy trắng: **bút chì hoặc bút đen** cho khung màn hình, **bút đỏ** cho ghi chú, giống bản mẫu. Không cần đẹp, cần rõ.
2. Chụp thẳng từ trên xuống, đủ sáng, cắt bỏ phần thừa.
3. Lưu đè lên file **cùng tên** trong `report/figures/sketches/` (định dạng PNG; nếu chụp ra JPG thì đổi sang PNG).
4. Giữ tỉ lệ khung gần giống bản mẫu để bố cục trang không bị xô.
5. Sau khi thay hết: build lại report (mục 4), hoặc trong Word bấm chuột phải vào từng hình → Change Picture.

| File | Hình trong report |
|---|---|
| `idea_flow.png` | Figure 1: sơ đồ ý tưởng |
| `focus_v1.png` | Figure 2: bản đầu màn Focus |
| `settings_v1.png` | Figure 3: bản đầu Reading + Sensory |
| `storyboard.png` | Figure 4: storyboard 6 cảnh |
| `cards.png` | Figure 5: card-based prototype |
| `today.png`, `plan.png`, `step.png`, `focus.png`, `rest.png`, `calm.png`, `settings.png`, `progress.png` | Figure D1–D8 (Appendix D) |

Gợi ý: với `cards.png`, có thể vẽ mỗi màn trên một tấm giấy nhỏ, xếp lên bàn theo 3 hàng rồi chụp một tấm. Đó đúng là card-based prototype.

### Bước 4. Kiểm tra kỹ từ trang bìa đến appendix

Mở file Word và đi từng mục:

- [ ] **Trang bìa**: tên, MSSV, tutor, ngày đúng; số từ ghi trên bìa khớp.
- [ ] **Contents / List of figures and tables**: số trang khớp thực tế. Trong Word số trang có thể lệch 1 trang so với lúc tạo, nên sửa tay nếu lệch.
- [ ] **1 Introduction**: có ghi rõ "Option A".
- [ ] **2 Annotated bibliography**: 8 nguồn, mỗi đoạn bắt đầu bằng tên tác giả (năm).
- [ ] **3 Product design**: Table 1, mục 3.1.4 Design assumptions, Figure 1–10 hiển thị đúng; sketch là bản vẽ tay của bạn.
- [ ] **4 Prototype**: 3 sơ đồ flow; bấm thử vài link "Figure E…" xem có nhảy xuống Appendix E không.
- [ ] **5 Research study**: đủ 5.1–5.7.
- [ ] **6 Conclusion**: **viết lại bằng trải nghiệm thật của bạn**, vì phần này chấm insight cá nhân.
- [ ] **References**: 12 nguồn, xếp A–Z; bấm thử link DOI xem có mở được không.
- [ ] **Appendix A**: sửa database và thời gian tìm cho **đúng với cách bạn thật sự tìm** tài liệu.
- [ ] **Appendix B**: đã điền contact ở B1.
- [ ] **Appendix C**: điền form khai báo AI của trường (link trong appendix), ghi rõ AI đã hỗ trợ việc gì.
- [ ] **Appendix D**: là ảnh sketch vẽ tay thật.
- [ ] **Appendix E, F**: ảnh màn hình đủ 12; bảng nối tương tác khớp với file Figma.
- [ ] **Số từ** từ Introduction đến hết Conclusion không quá 3.000 (cho phép tối đa 3.300). Nếu sửa nhiều thì đếm lại: bôi đen từ chữ đầu Introduction đến chữ cuối Conclusion, xem số từ ở thanh dưới cùng của Word.

### Bước 5. Chuyển sang PDF để nộp

Brief yêu cầu nộp **một file PDF, chữ phải chọn được** (không phải ảnh scan).

1. Mở file `.docx` bằng **Microsoft Word** (không dùng Google Docs vì có thể làm mất link nội bộ và lệch hình).
2. File → Save As (hoặc Export) → chọn **PDF**.
3. Trong Options: bật **Create bookmarks using: Headings** và giữ nguyên hyperlink.
4. Mở file PDF kiểm tra: bôi đen được chữ, bấm được link DOI và link "Figure …", hình không bị vỡ.
5. Đặt tên file gọn, ví dụ `COMP1649_<MSSV>_Report.pdf`.

## 3. Tóm tắt nội dung report

- **Chủ đề:** Option A, app cho sinh viên neurodivergent (ADHD, autism, dyslexia) ở đại học.
- **Ý chính:** chỉ hiện một bước tiếp theo; nghỉ là một bước chính thức; màn Calm mở được từ mọi màn; chỉnh giao diện không cần khai chẩn đoán; không streak hay điểm số.
- **3 journey:** planning (Today → Step → Focus → Rest), overload (Calm → talk to someone), personalise (Plan → Settings).
- **Nghiên cứu đề xuất:** so sánh màn một bước với màn dashboard (within-subjects, 12 sinh viên), đo thời gian bắt đầu, SUS, phỏng vấn.

## 4. Build lại (chỉ khi cần)

Cần: Python 3, Google Chrome, LibreOffice.

```bash
pip install python-docx pillow pypdf
brew install --cask libreoffice      # nếu chưa có

python3 scripts/build_screens.py     # tạo figma/*.html
bash scripts/capture.sh              # chụp figma/png/*.png
python3 scripts/build_figures.py     # report/figures/*.png
bash scripts/build_sketches.sh       # bản mẫu sketch (GHI ĐÈ sketch vẽ tay, cẩn thận)
python3 scripts/build_report.py      # tạo report .docx, in số từ và kiểm tra trích dẫn
```

> **Cẩn thận:** `build_sketches.sh` sẽ **ghi đè** ảnh sketch vẽ tay bằng bản mẫu. Sau khi đã thay ảnh vẽ tay thì **không chạy lại** lệnh này.

Chỉ cần sửa chữ trong report thì chỉ chạy dòng cuối (`build_report.py`).
