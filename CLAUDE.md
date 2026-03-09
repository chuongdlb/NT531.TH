# NT531.TH — Đánh giá hiệu năng Mạng máy tính (Network Performance Evaluation)

## Project Overview
University course lab materials for NT531 at UIT. Vietnamese-language content.
- **Instructor:** Chuong Dang (chuongdlb@uit.edu.vn)
- **Repo:** https://github.com/chuongdlb/NT531.TH
- **Semester:** HK2, 2025–2026

## Project Structure
```
NT531.TH/
├── CLAUDE.md
├── .gitignore
└── lab1/                          # Lab 1: Poisson Process & M/M/1, M/M/n Queue Simulation
    ├── lab1_instruction.tex       # LaTeX source (Vietnamese)
    ├── lab1_instruction.pdf       # Generated PDF (built via build_pdf.py, NOT lualatex)
    ├── build_pdf.py               # PDF generator using fpdf2 + DejaVu fonts
    ├── lab1_notebook.ipynb        # Jupyter notebook — 20 TODOs, 3 parts, currently has solutions filled in
    ├── requirements.txt           # numpy, matplotlib, scipy, simpy
    └── report-template-2023.docx  # Student report template (unchanged)
```

## Key Technical Decisions

### PDF Generation
- **lualatex does NOT work** on this WSL environment — luaotfload font database is missing and cannot be installed (no sudo, tlmgr version mismatch)
- Use `build_pdf.py` (fpdf2 library) instead: `cd lab1 && python3 build_pdf.py`
- Fonts: DejaVu Serif/Sans/Mono from `/usr/share/fonts/truetype/dejavu/` for Vietnamese Unicode

### Lab 1 Design
- **Scenario:** Network router, λ=5 pkt/s, μ=8 pkt/s, ρ=0.625
- **3 Parts:** (1) Poisson arrival process, (2) M/M/1 pure Python, (3) SimPy M/M/n
- **20 TODOs** total across the notebook
- **Notebook currently contains solutions** — the TODOs have been filled in and executed. To create a student skeleton, replace solution code with `... # TODO` placeholders.
- Simulation verified: all metrics within ~5-10% of M/M/1 closed-form theory

### Git Config (repo-local)
- user.name: chuongdlb
- user.email: chuongdlb@users.noreply.github.com

## Conventions
- All instruction documents are in **Vietnamese**
- Lab naming: `lab<N>/` directories
- Student submission format: `<HoTen>_<MSSV>_lab<N>.zip`
- Each lab has: instruction PDF, Jupyter notebook, requirements.txt
