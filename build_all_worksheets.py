#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
בניית דף HTML אחד עם כל דפי העבודה מחולקים ל-A4
Build single HTML file with all worksheets divided into A4 pages
"""

import sys
from pathlib import Path
import markdown
import re

# Ensure UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def process_markdown_to_html(md_content: str) -> str:
    """המרת Markdown ל-HTML"""
    # הסרת front matter
    if md_content.startswith('---'):
        parts = md_content.split('---', 2)
        if len(parts) >= 3:
            md_content = parts[2].strip()
    
    # המרת Markdown ל-HTML
    html = markdown.markdown(md_content, extensions=['fenced_code', 'tables', 'nl2br'])
    
    # עיבוד תמונות - תיקון נתיבים
    html = re.sub(
        r'<img src="([^"]+)"',
        r'<img src="../\1"',
        html
    )
    
    return html


def split_into_a4_pages(html_content: str, title: str) -> list:
    """חלוקת תוכן לדפי A4 - כל דף A4 נפרד"""
    # חלוקה לפי h2 או h3 - כל חלק גדול לדף A4 נפרד
    # נחלק לפי h2 (כותרות גדולות) - כל h2 מתחיל דף חדש
    parts = re.split(r'(<h2[^>]*>.*?</h2>)', html_content, flags=re.DOTALL)
    
    pages = []
    current_page = f'<div class="worksheet-content"><h1 class="worksheet-title">{title}</h1>'
    page_num = 1
    
    for i, part in enumerate(parts):
        if not part.strip():
            continue
        
        # אם זה h2, זה תחילת חלק חדש - בדוק אם צריך דף חדש
        if part.startswith('<h2'):
            # אם הדף הנוכחי כבר ארוך, סיים אותו
            if len(current_page) > 3000 and page_num > 1:
                current_page += '</div>'
                pages.append(current_page)
                current_page = f'<div class="worksheet-content"><h1 class="worksheet-title">{title} (המשך - דף {page_num})</h1>'
                page_num += 1
        
        current_page += part
        
        # אם הדף ארוך מדי, חתוך אותו
        if len(current_page) > 8000:
            # מצא את הסעיף האחרון לפני 8000 תווים
            last_h3 = current_page.rfind('<h3', 0, 8000)
            if last_h3 > 0:
                page_content = current_page[:last_h3]
                current_page = f'<div class="worksheet-content"><h1 class="worksheet-title">{title} (המשך - דף {page_num})</h1>' + current_page[last_h3:]
                page_content += '</div>'
                pages.append(page_content)
                page_num += 1
    
    # הוסף את הדף האחרון
    if current_page:
        current_page += '</div>'
        pages.append(current_page)
    
    return pages if pages else [f'<div class="worksheet-content"><h1 class="worksheet-title">{title}</h1>{html_content}</div>']


def build_all_worksheets():
    """בניית דף HTML אחד עם כל דפי העבודה"""
    
    # קריאת כל דפי העבודה
    worksheets = [
        {
            'file': Path('worksheets/grade-8/kavba_a1_graph_reading.md'),
            'title': 'קריאת גרף תנועה - מרחק וזמן'
        },
        {
            'file': Path('worksheets/grade-8/kavba_a1_slope_table.md'),
            'title': 'משמעות השיפוע באמצעות טבלת ערכים'
        },
        {
            'file': Path('worksheets/grade-8/kavba_a1_50_questions_coefficients.md'),
            'title': '50 שאלות על מקדמים בפונקציה קווית'
        }
    ]
    
    # קריאת תבנית HTML
    html_template_start = '''<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>כל דפי העבודה - כיתה ח' - מוכן להדפסה A4</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        window.MathJax = {tex: {inlineMath: [['$', '$']], displayMath: [['$$', '$$']]}};
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700&family=Assistant:wght@400;600;700&display=swap');
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        @page {
            size: A4;
            margin: 0;
        }
        
        body {
            font-family: 'Heebo', 'Assistant', 'Arial Hebrew', sans-serif;
            direction: rtl;
            background: #f0f0f0;
            padding: 0;
            margin: 0;
        }
        
        .a4-page {
            width: 210mm;
            min-height: 297mm;
            max-height: 297mm;
            margin: 0 auto 10mm auto;
            background: white;
            padding: 25mm 20mm;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            page-break-after: always;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .a4-page {
                margin: 0;
                box-shadow: none;
                page-break-after: always;
                page-break-inside: avoid;
            }
            
            .no-print {
                display: none;
            }
        }
        
        .worksheet-content {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        
        .worksheet-title {
            text-align: center;
            font-size: 20pt;
            font-weight: bold;
            color: #003366;
            margin-bottom: 1em;
            padding-bottom: 0.5em;
            border-bottom: 3px solid #003366;
        }
        
        h1 {
            font-size: 18pt;
            border-bottom: 2px solid #333;
            padding-bottom: 0.5em;
            margin-bottom: 1em;
            margin-top: 0;
            color: #003366;
        }
        
        h2 {
            font-size: 16pt;
            border-bottom: 1px solid #ddd;
            margin-top: 1.5em;
            margin-bottom: 0.8em;
            color: #003366;
        }
        
        h3 {
            font-size: 15pt;
            margin-top: 1.5em;
            margin-bottom: 0.7em;
            color: #003366;
            background-color: #e0f7fa;
            border-right: 5px solid #007bff;
            padding: 5px 10px;
            margin-right: -10px;
            page-break-after: avoid;
        }
        
        p {
            text-align: justify;
            margin: 0.8em 0;
            line-height: 1.8;
        }
        
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 1em auto;
            border: 3px solid #003366;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
            page-break-inside: avoid;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1em 0;
            page-break-inside: avoid;
        }
        
        table th, table td {
            border: 1px solid #333;
            padding: 0.5em;
            text-align: right;
        }
        
        table th {
            background-color: #f0f0f0;
            font-weight: bold;
        }
        
        ul, ol {
            margin: 0.8em 0;
            padding-right: 2em;
        }
        
        li {
            margin: 0.3em 0;
        }
        
        code {
            font-family: 'Courier New', monospace;
            background-color: #f5f5f5;
            padding: 0.2em 0.4em;
            border-radius: 3px;
        }
        
        pre {
            background-color: #f5f5f5;
            padding: 1em;
            border-radius: 5px;
            overflow-x: auto;
            page-break-inside: avoid;
        }
        
        .math-display {
            direction: ltr;
            text-align: center;
            margin: 1em 0;
            font-size: 1.1em;
        }
        
        .math-inline {
            direction: ltr;
            font-size: 1em;
        }
        
        hr {
            border: none;
            border-top: 1px solid #ddd;
            margin: 1.5em 0;
        }
        
        strong {
            font-weight: bold;
        }
        
        .print-button {
            position: fixed;
            top: 20px;
            left: 20px;
            background: #007bff;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            font-size: 16pt;
            cursor: pointer;
            z-index: 1000;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        
        .print-button:hover {
            background: #0056b3;
        }
    </style>
</head>
<body>
    <button class="print-button no-print" onclick="window.print()">🖨️ הדפס את כל הדפים</button>
'''
    
    html_content = html_template_start
    
    # עיבוד כל דף עבודה
    for ws in worksheets:
        if not ws['file'].exists():
            print(f"Warning: {ws['file']} not found, skipping...")
            continue
        
        print(f"Processing: {ws['title']}")
        content = ws['file'].read_text(encoding='utf-8')
        html_body = process_markdown_to_html(content)
        
        # חלוקה לדפי A4
        pages = split_into_a4_pages(html_body, ws['title'])
        
        # הוספת כל הדפים
        for page_html in pages:
            html_content += f'<div class="a4-page">{page_html}</div>\n'
    
    # סיום HTML
    html_content += '''
</body>
</html>'''
    
    # שמירה
    output_file = Path('all_worksheets.html')
    output_file.write_text(html_content, encoding='utf-8')
    print(f"\n✅ Created: {output_file}")
    print(f"📄 Total pages: {html_content.count('a4-page')}")


if __name__ == '__main__':
    build_all_worksheets()
