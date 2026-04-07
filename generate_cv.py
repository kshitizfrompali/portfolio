from pathlib import Path
from weasyprint import HTML

base = Path(__file__).parent
html_path = base / "cv.html"
pdf_path = base / "cv.pdf"

HTML(filename=str(html_path)).write_pdf(str(pdf_path))
print(f"CV saved to {pdf_path}")
