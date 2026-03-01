#!/usr/bin/env python3
"""Build lab1_instruction.pdf using fpdf2 with Unicode Vietnamese support."""

from fpdf import FPDF

# ── Constants ──
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
OUTPUT = "lab1_instruction.pdf"

class LabPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        # Register DejaVu fonts for Vietnamese
        self.add_font("DejaVu", "", FONT_DIR + "DejaVuSerif.ttf")
        self.add_font("DejaVu", "B", FONT_DIR + "DejaVuSerif-Bold.ttf")
        self.add_font("DejaVuSans", "", FONT_DIR + "DejaVuSans.ttf")
        self.add_font("DejaVuSans", "B", FONT_DIR + "DejaVuSans-Bold.ttf")
        self.add_font("DejaVuMono", "", FONT_DIR + "DejaVuSansMono.ttf")
        self.add_font("DejaVuMono", "B", FONT_DIR + "DejaVuSansMono-Bold.ttf")
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DejaVu", "", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, "NT531 — Đánh giá hiệu năng Mạng máy tính", 0, 0, "L")
        self.cell(0, 5, "Lab 1", 0, 1, "R")
        self.line(10, 12, 200, 12)
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, str(self.page_no()), 0, 0, "C")

    def section_title(self, title):
        self.ln(3)
        self.set_font("DejaVuSans", "B", 14)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, title, 0, 1)
        self.ln(1)

    def subsection_title(self, title):
        self.ln(2)
        self.set_font("DejaVuSans", "B", 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 7, title, 0, 1)
        self.ln(1)

    def body_text(self, text):
        self.set_font("DejaVu", "", 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def bullet_list(self, items):
        self.set_font("DejaVu", "", 11)
        self.set_text_color(0, 0, 0)
        for item in items:
            self.cell(5)
            self.cell(5, 6, "•")
            self.multi_cell(0, 6, item)
            self.ln(0.5)
        self.ln(1)

    def numbered_list(self, items, bold_prefix=True):
        self.set_font("DejaVu", "", 11)
        self.set_text_color(0, 0, 0)
        for i, item in enumerate(items, 1):
            x = self.get_x()
            self.cell(8)
            if bold_prefix and ":" in item:
                prefix, rest = item.split(":", 1)
                self.set_font("DejaVu", "B", 11)
                self.cell(0, 6, f"{i}. {prefix}:")
                self.set_font("DejaVu", "", 11)
                self.ln()
                self.cell(8)
                self.multi_cell(0, 6, rest.strip())
            else:
                self.multi_cell(0, 6, f"{i}. {item}")
            self.ln(0.5)
        self.ln(1)

    def code_block(self, code):
        self.set_font("DejaVuMono", "", 9)
        self.set_fill_color(245, 245, 245)
        self.set_draw_color(180, 180, 180)
        x = self.get_x() + 5
        y = self.get_y()
        lines = code.split("\n")
        h = len(lines) * 5 + 4
        self.rect(x, y, 180, h, "D")
        self.rect(x, y, 180, h, "F")
        self.ln(2)
        for line in lines:
            self.cell(7)
            self.cell(0, 5, line)
            self.ln()
        self.ln(3)

    def formula(self, text):
        self.set_font("DejaVuMono", "", 10)
        self.set_text_color(0, 0, 100)
        self.cell(10)
        self.cell(0, 6, text)
        self.ln(7)
        self.set_text_color(0, 0, 0)

    def table(self, headers, rows, col_widths=None):
        if col_widths is None:
            col_widths = [190 // len(headers)] * len(headers)
        # Header
        self.set_font("DejaVuSans", "B", 10)
        self.set_fill_color(230, 230, 230)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, 1, 0, "C", fill=True)
        self.ln()
        # Rows
        self.set_font("DejaVu", "", 10)
        for row in rows:
            max_h = 7
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, cell, 1, 0, "C")
            self.ln()
        self.ln(2)


def build():
    pdf = LabPDF()
    pdf.add_page()

    # ── Title ──
    pdf.set_font("DejaVuSans", "B", 18)
    pdf.multi_cell(0, 9, "Lab 1 — Quá trình Poisson và\nMô phỏng Hàng đợi M/M/1, M/M/n", align="C")
    pdf.ln(2)
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 6, "Môn: NT531 — Đánh giá hiệu năng Mạng máy tính", 0, 1, "C")
    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 6, "Giảng viên: Chuong Dang — chuongdlb@uit.edu.vn", 0, 1, "C")
    pdf.cell(0, 6, "Học kỳ 2, 2025–2026", 0, 1, "C")
    pdf.ln(3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # ══════════════════════════════════════════════════════════
    # Section 1
    # ══════════════════════════════════════════════════════════
    pdf.section_title("1. Mục tiêu")
    pdf.body_text("Sau khi hoàn thành bài lab này, sinh viên sẽ:")
    pdf.bullet_list([
        "Hiểu quá trình đến (arrival process) Poisson và cách sinh thời gian giữa các lần đến.",
        "Hiểu ký hiệu Kendall (A/S/n) và ý nghĩa của M/M/1, M/M/n.",
        "Mô phỏng hàng đợi M/M/1 bằng Python thuần (array-based) và bằng thư viện SimPy.",
        "So sánh kết quả mô phỏng với công thức lý thuyết (closed-form).",
    ])

    # ══════════════════════════════════════════════════════════
    # Section 2
    # ══════════════════════════════════════════════════════════
    pdf.section_title("2. Kiến thức nền tảng")

    # 2.1
    pdf.subsection_title("2.1 Phân phối Poisson và thời gian giữa các lần đến")
    pdf.body_text(
        "Nếu số sự kiện (ví dụ: số gói tin đến) trong một khoảng thời gian Ts "
        "tuân theo phân phối Poisson với tốc độ (rate) λ, thì:"
    )
    pdf.formula("P(X = k) = (λ·Ts)^k / k! · e^(-λ·Ts),   k = 0, 1, 2, ...")
    pdf.body_text(
        "Thời gian giữa hai lần đến liên tiếp (inter-arrival time) tuân theo phân phối mũ "
        "(exponential). Ta có thể sinh mẫu bằng phương pháp nghịch đảo hàm phân phối "
        "(inverse transform):"
    )
    pdf.formula("t_inter = (-1/λ) · ln(1 - U),   U ~ Uniform(0,1)")

    # 2.2
    pdf.subsection_title("2.2 Ký hiệu Kendall (Kendall's Notation)")
    pdf.body_text("Hệ thống hàng đợi được mô tả bằng ký hiệu A/S/n:")
    pdf.bullet_list([
        "A — Phân phối thời gian đến (Arrival distribution)",
        "S — Phân phối thời gian phục vụ (Service distribution)",
        "n — Số server (bộ phục vụ)",
    ])
    pdf.body_text(
        "Trong đó M = Markovian (memoryless) = phân phối mũ.\n"
        "• M/M/1: Đến Poisson, phục vụ exponential, 1 server.\n"
        "• M/M/n: Đến Poisson, phục vụ exponential, n server."
    )

    # 2.3
    pdf.subsection_title("2.3 Các công thức M/M/1")
    pdf.body_text(
        "Gọi λ là tốc độ đến, μ là tốc độ phục vụ. "
        "Hệ thống ổn định khi ρ = λ/μ < 1."
    )
    pdf.table(
        ["Ký hiệu", "Công thức", "Ý nghĩa"],
        [
            ["ρ",  "λ / μ",          "Hệ số sử dụng (utilization)"],
            ["L",  "ρ / (1 - ρ)",    "Số trung bình trong hệ thống"],
            ["Lq", "ρ² / (1 - ρ)",   "Số trung bình trong hàng đợi"],
            ["W",  "1 / (μ - λ)",    "Thời gian TB trong hệ thống"],
            ["Wq", "ρ / (μ - λ)",    "Thời gian chờ TB trong hàng đợi"],
        ],
        col_widths=[25, 45, 120],
    )

    # 2.4
    pdf.subsection_title("2.4 Các công thức M/M/n (tham khảo)")
    pdf.body_text(
        "Với hệ thống M/M/n (n server), hệ số sử dụng mỗi server là: ρ = λ/(n·μ)"
    )
    pdf.body_text(
        "Xác suất một gói tin phải chờ trong hàng đợi được tính bằng công thức Erlang-C:"
    )
    pdf.formula("C(n,a) = [a^n/n! · 1/(1-ρ)] / [Σ(k=0..n-1) a^k/k! + a^n/n! · 1/(1-ρ)]")
    pdf.formula("với a = λ/μ")
    pdf.body_text("Từ đó:")
    pdf.formula("Wq = C(n,a) / (n·μ - λ),    Lq = λ · Wq")
    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 5,
        "Ghi chú: Sinh viên không cần tự suy dẫn công thức Erlang-C; "
        "chỉ cần hiểu ý nghĩa và sử dụng hàm đã cung cấp trong notebook."
    )
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    # ══════════════════════════════════════════════════════════
    # Section 3
    # ══════════════════════════════════════════════════════════
    pdf.section_title("3. Kịch bản thực hành")
    pdf.set_font("DejaVu", "", 11)
    pdf.set_fill_color(245, 248, 255)
    pdf.set_draw_color(100, 100, 200)
    x, y = pdf.get_x() + 5, pdf.get_y()

    scenario = (
        "Một bộ định tuyến mạng (network router) có cổng đầu ra xử lý gói tin. "
        "Gói tin đến theo quá trình Poisson với tốc độ λ = 5 gói/giây. "
        "Thời gian xử lý mỗi gói tuân theo phân phối mũ với tốc độ μ = 8 gói/giây. "
        "Mô phỏng 10.000 gói tin."
    )
    pdf.cell(5)
    w = 180
    pdf.multi_cell(w, 6, scenario, border=1, fill=True)
    pdf.ln(3)

    pdf.body_text("Các tham số:")
    pdf.bullet_list([
        "λ = 5 gói/giây (tốc độ đến)",
        "μ = 8 gói/giây (tốc độ phục vụ)",
        "ρ = λ/μ = 0,625 (hệ thống ổn định)",
        "Số gói mô phỏng: N = 10.000",
    ])

    # ══════════════════════════════════════════════════════════
    # Section 4
    # ══════════════════════════════════════════════════════════
    pdf.section_title("4. Hướng dẫn thực hành")
    pdf.body_text(
        "Bài lab gồm 3 phần, tương ứng với 3 phần trong notebook lab1_notebook.ipynb. "
        "Tổng cộng có 20 TODO sinh viên cần hoàn thành."
    )

    # Part 1
    pdf.subsection_title("Phần 1: Quá trình đến Poisson (TODO 1–7)")
    pdf.body_text(
        "Phần này giữ lại nội dung cốt lõi của bài lab gốc (Excel), nhưng chuyển sang Python."
    )
    pdf.numbered_list([
        "TODO 1: Sinh N=200 thời gian giữa các lần đến bằng phương pháp inverse transform.",
        "TODO 2: Tính thời gian đến tích lũy (cumulative arrival times).",
        "TODO 3: Chia trục thời gian thành các khe (time slot), đếm số gói đến mỗi khe.",
        "TODO 4: Tính PMF thực nghiệm — tần suất f(x) và %real.",
        "TODO 5: Tính PMF lý thuyết Poisson — %theory.",
        "TODO 6: Vẽ biểu đồ cột so sánh PMF thực nghiệm vs lý thuyết.",
        "TODO 7: In trung bình và phương sai của số gói đến mỗi khe. Xác minh rằng với Poisson, mean ≈ variance ≈ λ·Ts.",
    ])

    # Part 2
    pdf.subsection_title("Phần 2: Mô phỏng hàng đợi M/M/1 bằng Python thuần (TODO 8–16)")
    pdf.body_text("Sinh viên sẽ xây dựng vòng lặp mô phỏng array-based:")
    pdf.code_block(
        "arrival_time[i]   = arrival_time[i-1] + inter_arrival[i]\n"
        "service_start[i]  = max(arrival_time[i], departure_time[i-1])\n"
        "departure_time[i] = service_start[i] + service_time[i]\n"
        "wait_time[i]      = service_start[i] - arrival_time[i]"
    )
    pdf.numbered_list([
        "TODO 8: Sinh thời gian giữa các lần đến (exponential, rate λ).",
        "TODO 9: Sinh thời gian phục vụ (exponential, rate μ).",
        "TODO 10: Hoàn thành vòng lặp mô phỏng (event-driven loop).",
        "TODO 11: Tính các chỉ số mô phỏng: L, Lq, W, Wq, ρ.",
        "TODO 12: Tính các chỉ số lý thuyết M/M/1.",
        "TODO 13: In bảng so sánh mô phỏng vs lý thuyết.",
        "TODO 14: Vẽ biểu đồ — Số gói trong hàng đợi theo thời gian (step plot).",
        "TODO 15: Vẽ biểu đồ — Histogram thời gian chờ.",
        "TODO 16: Vẽ biểu đồ — Hệ số sử dụng server theo thời gian (rolling average).",
    ])

    # Part 3
    pdf.subsection_title("Phần 3: Mô phỏng bằng SimPy + M/M/n (TODO 17–20)")
    pdf.body_text(
        "SimPy là thư viện mô phỏng sự kiện rời rạc (discrete-event simulation) cho Python. "
        "Sinh viên sử dụng simpy.Resource(capacity=n) để mô phỏng hệ thống với n server."
    )
    pdf.numbered_list([
        "TODO 17: Viết mô phỏng M/M/1 bằng SimPy (packet generator + server resource).",
        "TODO 18: So sánh kết quả SimPy M/M/1 với kết quả Phần 2.",
        "TODO 19: Mở rộng sang M/M/n — chạy với n = 1, 2, 3, 4 và thu thập Wq.",
        "TODO 20: Vẽ biểu đồ — Wq theo số server n.",
    ])

    # ══════════════════════════════════════════════════════════
    # Section 5
    # ══════════════════════════════════════════════════════════
    pdf.section_title("5. Yêu cầu nộp bài")
    pdf.body_text("Upload file .zip chứa:")
    pdf.bullet_list([
        "Notebook đã hoàn thành (.ipynb)",
        "Báo cáo (.docx) — sử dụng template đã cung cấp",
    ])
    pdf.body_text("Tên file: <HoTen>_<MSSV>_lab1.zip")
    pdf.body_text("Ví dụ: NguyenVanA_22520001_lab1.zip")

    # ══════════════════════════════════════════════════════════
    # Section 6
    # ══════════════════════════════════════════════════════════
    pdf.section_title("6. Câu hỏi thảo luận")
    pdf.body_text("Sinh viên trả lời các câu hỏi sau trong báo cáo:")
    pdf.ln(1)

    pdf.set_font("DejaVu", "", 11)
    pdf.multi_cell(0, 6,
        "Q1: Khi ρ → 1, điều gì xảy ra với thời gian chờ Wq? "
        "Giải thích bằng công thức và bằng kết quả mô phỏng."
    )
    pdf.ln(2)

    pdf.multi_cell(0, 6,
        "Q2: So sánh kết quả mô phỏng M/M/1 giữa Python thuần (Phần 2) và SimPy (Phần 3). "
        "Có khác biệt đáng kể không? Giải thích tại sao."
    )
    pdf.ln(2)

    pdf.multi_cell(0, 6,
        "Q3: Với M/M/n, cho λ = 5 gói/giây và μ = 3 gói/giây, cần bao nhiêu server để "
        "Wq < 0,1 giây? Trả lời bằng cách chạy mô phỏng với các giá trị n khác nhau."
    )
    pdf.ln(5)

    # ── End ──
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 6, "— Hết —", 0, 1, "C")

    pdf.output(OUTPUT)
    print(f"PDF generated: {OUTPUT}")


if __name__ == "__main__":
    build()
