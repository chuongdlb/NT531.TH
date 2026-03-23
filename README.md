# NT531.TH

Tài liệu và bài thực hành cho môn **NT531 — Đánh giá hiệu năng Mạng máy tính** tại UIT.

Repo hiện chứa:
- `lab1`: notebook và tài liệu về quá trình Poisson, mô phỏng hàng đợi `M/M/1`, `M/M/n`
- `lab2`: notebook, file Excel và tài liệu về mô hình `M/M/n/K/N`
- `lecture_02_arrival processes and queuing systems (1).pdf`: bài giảng lý thuyết chính đã dùng để đối chiếu công thức
- `lecture_07_notes-loadtest.md`: ghi chú về load testing

## Cấu trúc thư mục

```text
NT531.TH/
├── README.md
├── CLAUDE.md
├── lab1/
│   ├── lab1_instruction.pdf
│   ├── lab1_instruction.tex
│   ├── lab1_notebook.ipynb
│   ├── build_pdf.py
│   ├── requirements.txt
│   └── report-template-2023.docx
├── lab2/
│   ├── lab2_instruction.pdf
│   ├── lab2_notebook.ipynb
│   ├── lab2_Student.xlsx
│   ├── build_notebook.py
│   ├── render_notebook_outputs.py
│   ├── fill_excel_formulas.py
│   └── requirements.txt
└── lecture_02_arrival processes and queuing systems (1).pdf
```

## Lab 1

Nội dung chính:
- mô hình mũ và Poisson cho quá trình đến
- mô phỏng `M/M/1` bằng Python thuần
- mô phỏng `M/M/n` bằng SimPy

File chính:
- `lab1/lab1_notebook.ipynb`
- `lab1/lab1_instruction.pdf`

## Lab 2

Nội dung chính:
- mô hình hàng đợi `M/M/n/K/N`
- bảng trạng thái `x, q, λ_x, μ_x, T_x, P_x`
- các chỉ số `P{immediate service}`, `P{delay}`, `P{loss}`, `E{q}`, `E{x}`, `t_w`
- notebook đã có biểu đồ nhúng và ghi chú đối chiếu với bài giảng

File chính:
- `lab2/lab2_notebook.ipynb`
- `lab2/lab2_Student.xlsx`
- `lab2/lab2_instruction.pdf`

## Cách tái tạo file trong lab2

Sinh lại notebook:

```bash
python3 lab2/build_notebook.py
uv run --python python3 python lab2/render_notebook_outputs.py
```

Điền công thức vào file Excel:

```bash
python3 lab2/fill_excel_formulas.py
```

## Ghi chú

- Công thức trong `lab1` và `lab2` đã được rà lại theo `lecture_02_arrival processes and queuing systems (1).pdf`.
- `lab2` dùng mô hình birth-death để tính xác suất trạng thái và các xác suất theo phía arrival.
- File Excel của `lab2` đã được điền công thức để khi mở trong Excel có thể tự recalculate.
