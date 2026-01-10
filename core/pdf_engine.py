#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מנוע PDF מקצועי - יצירת PDF מוכן להדפסה ב-A4 עם תמיכה מלאה בעברית ו-RTL
PDF Engine - Professional PDF generation for A4 printing with full Hebrew and RTL support
"""

import sys
import re
import base64
from pathlib import Path
from typing import Optional, List
from PIL import Image

# Ensure UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# PDF generation engines - try multiple options
try:
    import pypandoc
    PYPANDOC_AVAILABLE = True
except ImportError:
    PYPANDOC_AVAILABLE = False

try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except ImportError:
    PDFKIT_AVAILABLE = False

try:
    import weasyprint
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):
    WEASYPRINT_AVAILABLE = False

try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False


class PDFEngine:
    """מחלקה ליצירת PDF מקצועי עבור דפי עבודה במתמטיקה"""

    # הגדרות A4 מדויקות - EXTREME PROMPT SPECS
    A4_WIDTH_CM = 21.0
    A4_HEIGHT_CM = 29.7
    MARGIN_TOP_CM = 2.5  # 25mm
    MARGIN_BOTTOM_CM = 2.5  # 25mm
    MARGIN_SIDE_CM = 2.0  # 20mm
    CONTENT_WIDTH_CM = A4_WIDTH_CM - (2 * MARGIN_SIDE_CM)  # 17cm

    def __init__(self):
        """אתחול מנוע PDF"""
        self.hebrew_fonts = [
            'David Libre',
            'Frank Ruhl Libre',
            'Assistant',
            'Heebo',
            'Alef',
            'Noto Sans Hebrew',
            'Arial Hebrew'
        ]

    def generate(self, markdown_file: str, output_file: Optional[str] = None) -> Path:
        """
        יצירת PDF מקובץ Markdown

        Args:
            markdown_file: נתיב לקובץ Markdown
            output_file: נתיב לקובץ PDF פלט (אופציונלי)

        Returns:
            Path לקובץ PDF שנוצר
        """
        input_path = Path(markdown_file)
        if not input_path.exists():
            raise FileNotFoundError(f"קובץ לא נמצא: {markdown_file}")

        if output_file:
            output_path = Path(output_file)
        else:
            output_path = input_path.with_suffix('.pdf')

        # קריאת תוכן Markdown
        content = input_path.read_text(encoding='utf-8')

        # עיבוד Markdown ל-HTML
        html = self._markdown_to_html(content, input_path.parent)

        # יצירת PDF - נסה מנועים שונים לפי זמינות
        tried_engines = []

        if WEASYPRINT_AVAILABLE:
            try:
                self._generate_with_weasyprint(html, output_path)
                return output_path
            except Exception as e:
                tried_engines.append(f"weasyprint (שגיאה: {e})")

        if PDFKIT_AVAILABLE:
            try:
                self._generate_with_pdfkit(html, output_path, input_path.parent)
                return output_path
            except Exception as e:
                tried_engines.append(f"pdfkit (שגיאה: {e})")

        if PYPANDOC_AVAILABLE:
            try:
                self._generate_with_pypandoc(content, output_path)
                return output_path
            except Exception as e:
                tried_engines.append(f"pypandoc (שגיאה: {e})")

        # אם אף מנוע לא עבד
        error_msg = "לא נמצא מנוע PDF זמין או תקין.\n"
        if tried_engines:
            error_msg += "ניסיתי:\n"
            for engine in tried_engines:
                error_msg += f"- {engine}\n"
        error_msg += "\nאנא התקן אחד מהחבילות:\n"
        error_msg += "- weasyprint (מומלץ): pip install weasyprint\n"
        error_msg += "- pdfkit (דורש wkhtmltopdf): pip install pdfkit\n"
        error_msg += "- pypandoc-binary: pip install pypandoc-binary"

        raise RuntimeError(error_msg)

        sys.stdout.buffer.write(f"✅ PDF נוצר בהצלחה: {output_path}\n".encode('utf-8'))
        return output_path

    def _markdown_to_html(self, markdown_content: str, base_dir: Path) -> str:
        """המרת Markdown ל-HTML עם עיבוד תמונות ו-LaTeX"""
        # הפרדת front matter אם קיים
        front_matter = {}
        if markdown_content.startswith('---'):
            parts = markdown_content.split('---', 2)
            if len(parts) >= 3:
                front_matter_text = parts[1].strip()
                markdown_content = parts[2].strip()
                # פשוט התעלם מה-front matter כרגע

        # עיבוד תמונות - המרת נתיבים יחסיים לנתיבים מלאים
        def process_images(match):
            img_path = match.group(1)
            if not Path(img_path).is_absolute():
                full_path = base_dir / img_path
                if full_path.exists():
                    return f'![{match.group(2) or ""}]({full_path})'
            return match.group(0)

        markdown_content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', process_images, markdown_content)

        # המרת Markdown ל-HTML
        if MARKDOWN_AVAILABLE:
            html_body = markdown.markdown(
                markdown_content,
                extensions=['fenced_code', 'tables', 'nl2br']
            )
        else:
            # Fallback פשוט אם markdown לא מותקן
            html_body = markdown_content.replace('\n', '<br>\n')

        # עיבוד LaTeX math
        html_body = self._process_latex_math(html_body)

        # יצירת HTML מלא עם CSS
        html = self._wrap_with_html(html_body)

        return html

    def _process_latex_math(self, html: str) -> str:
        """עיבוד LaTeX math - המרה ל-HTML עם MathJax"""
        # $$...$$ - block equations
        def process_block(match):
            math_content = match.group(1).strip()
            return f'<div class="math-display">$${math_content}$$</div>'

        html = re.sub(r'\$\$([^$]+)\$\$', process_block, html)

        # $...$ - inline equations
        def process_inline(match):
            math_content = match.group(1).strip()
            return f'<span class="math-inline">${math_content}$</span>'

        html = re.sub(r'\$([^$]+)\$', process_inline, html)

        return html

    def _wrap_with_html(self, html_body: str) -> str:
        """עטיפת HTML body ב-HTML מלא עם CSS"""
        fonts_css = ','.join([f"'{f}'" for f in self.hebrew_fonts])

        css = f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=David+Libre:wght@400;700&family=Assistant:wght@400;600;700&family=Heebo:wght@400;500;700&display=swap');

            @page {{
                size: A4;
                margin-top: {self.MARGIN_TOP_CM}cm;
                margin-bottom: {self.MARGIN_BOTTOM_CM}cm;
                margin-left: {self.MARGIN_SIDE_CM}cm;
                margin-right: {self.MARGIN_SIDE_CM}cm;
            }}

            * {{
                box-sizing: border-box;
            }}

            body {{
                direction: rtl;
                text-align: right;
                font-family: {fonts_css}, sans-serif;
                font-size: 12pt;
                line-height: 1.8;
                margin: 0;
                padding: 0;
                color: #000000;
                background: #ffffff;
            }}

            h1 {{
                font-size: 18pt;
                font-weight: bold;
                border-bottom: 2px solid #333;
                padding-bottom: 0.5em;
                margin-bottom: 1em;
                margin-top: 0;
            }}

            h2 {{
                font-size: 16pt;
                font-weight: bold;
                border-bottom: 1px solid #ddd;
                margin-top: 1.5em;
                margin-bottom: 0.8em;
            }}

            h3 {{
                font-size: 14pt;
                font-weight: bold;
                margin-top: 1.5em;
                margin-bottom: 0.7em;
                color: #003366;
            }}

            p {{
                text-align: justify;
                margin: 0.8em 0;
                line-height: 1.8;
            }}

            img {{
                max-width: {self.CONTENT_WIDTH_CM}cm;
                height: auto;
                display: block;
                margin: 1em auto;
                page-break-inside: avoid;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 1em 0;
                page-break-inside: avoid;
            }}

            table th, table td {{
                border: 1px solid #333;
                padding: 0.5em;
                text-align: right;
            }}

            table th {{
                background-color: #f0f0f0;
                font-weight: bold;
            }}

            ul, ol {{
                margin: 0.8em 0;
                padding-right: 2em;
            }}

            li {{
                margin: 0.3em 0;
            }}

            code {{
                font-family: 'Courier New', monospace;
                background-color: #f5f5f5;
                padding: 0.2em 0.4em;
                border-radius: 3px;
                font-size: 0.9em;
            }}

            pre {{
                background-color: #f5f5f5;
                padding: 1em;
                border-radius: 5px;
                overflow-x: auto;
                page-break-inside: avoid;
            }}

            .math-display {{
                direction: ltr;
                text-align: center;
                margin: 1em 0;
                font-size: 1.1em;
            }}

            .math-inline {{
                direction: ltr;
                font-size: 1em;
            }}

            hr {{
                border: none;
                border-top: 1px solid #ddd;
                margin: 1.5em 0;
            }}

            strong {{
                font-weight: bold;
            }}

            em {{
                font-style: italic;
            }}
        </style>
        """

        html_full = f"""<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <title>דף עבודה במתמטיקה</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        window.MathJax = {{tex: {{inlineMath: [['$', '$']], displayMath: [['$$', '$$']]}}}};
    </script>
    {css}
</head>
<body>
    {html_body}
</body>
</html>"""

        return html_full

    def _generate_with_weasyprint(self, html: str, output_path: Path):
        """יצירת PDF עם WeasyPrint"""
        html_doc = weasyprint.HTML(string=html)
        html_doc.write_pdf(output_path)

    def _generate_with_pdfkit(self, html: str, output_path: Path, base_dir: Path):
        """יצירת PDF עם pdfkit"""
        # עיבוד תמונות - המרה ל-base64
        html = self._embed_images_base64(html, base_dir)

        options = {
            'page-size': 'A4',
            'margin-top': f'{self.MARGIN_TOP_CM}cm',
            'margin-bottom': f'{self.MARGIN_BOTTOM_CM}cm',
            'margin-left': f'{self.MARGIN_SIDE_CM}cm',
            'margin-right': f'{self.MARGIN_SIDE_CM}cm',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }

        pdfkit.from_string(html, str(output_path), options=options)

    def _generate_with_pypandoc(self, markdown_content: str, output_path: Path):
        """יצירת PDF עם pypandoc"""
        pypandoc.convert_text(
            markdown_content,
            'pdf',
            format='md',
            outputfile=str(output_path),
            extra_args=[
                f'--pdf-engine=xelatex',
                f'--variable=geometry:margin={self.MARGIN_TOP_CM}cm',
                f'--variable=mainfont:{"David Libre"}',
                '--variable=dir:rtl'
            ]
        )

    def _embed_images_base64(self, html: str, base_dir: Path) -> str:
        """המרת תמונות ל-base64"""
        def embed_image(match):
            img_path_str = match.group(1)
            alt_text = match.group(2) or ""

            img_path = Path(img_path_str)
            if not img_path.is_absolute():
                img_path = base_dir / img_path

            if img_path.exists():
                try:
                    with Image.open(img_path) as img:
                        # אופטימיזציה לתמונה - התאמה ל-A4
                        max_width_px = int(self.CONTENT_WIDTH_CM * 37.8)  # 1cm ≈ 37.8px at 96 DPI
                        if img.width > max_width_px:
                            ratio = max_width_px / img.width
                            new_size = (max_width_px, int(img.height * ratio))
                            img = img.resize(new_size, Image.Resampling.LANCZOS)

                        # המרה ל-base64
                        import io
                        buffer = io.BytesIO()
                        img.save(buffer, format='PNG')
                        img_base64 = base64.b64encode(buffer.getvalue()).decode()

                        return f'<img src="data:image/png;base64,{img_base64}" alt="{alt_text}" style="max-width: {self.CONTENT_WIDTH_CM}cm; height: auto;">'
                except Exception as e:
                    sys.stderr.buffer.write(f"שגיאה בעיבוד תמונה {img_path}: {e}\n".encode('utf-8'))
                    return match.group(0)

            return match.group(0)

        html = re.sub(r'<img src="([^"]+)"[^>]*alt="([^"]*)"[^>]*>', embed_image, html)
        return html


def generate_pdf(markdown_file: str, output_file: Optional[str] = None) -> Path:
    """
    פונקציה נוחה ליצירת PDF

    Args:
        markdown_file: נתיב לקובץ Markdown
        output_file: נתיב לקובץ PDF פלט (אופציונלי)

    Returns:
        Path לקובץ PDF שנוצר
    """
    engine = PDFEngine()
    return engine.generate(markdown_file, output_file)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("שימוש: python pdf_engine.py <קובץ_markdown> [קובץ_pdf_פלט]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    generate_pdf(input_file, output_file)
