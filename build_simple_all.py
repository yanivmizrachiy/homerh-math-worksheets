#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
בניית דף HTML פשוט עם כל דפי העבודה - כל דף A4 נפרד
"""

import sys
from pathlib import Path
import markdown

sys.stdout.reconfigure(encoding='utf-8')

def build_simple_all():
    worksheets = [
        ('worksheets/grade-8/kavba_a1_graph_reading.md', 'קריאת גרף תנועה - מרחק וזמן'),
        ('worksheets/grade-8/kavba_a1_slope_table.md', 'משמעות השיפוע באמצעות טבלת ערכים'),
        ('worksheets/grade-8/kavba_a1_50_questions_coefficients.md', '50 שאלות על מקדמים בפונקציה קווית')
    ]

    html = '''<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <title>כל דפי העבודה - כיתה ח' - מוכן להדפסה A4</title>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>window.MathJax = {tex: {inlineMath: [['$', '$']], displayMath: [['$$', '$$']]}};</script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700&display=swap');
        * {box-sizing: border-box; margin: 0; padding: 0;}
        @page {size: A4; margin: 0;}
        body {font-family: 'Heebo', sans-serif; direction: rtl; background: #f0f0f0; padding: 0;}
        .a4-page {width: 210mm; min-height: 297mm; margin: 0 auto 10mm; background: white; padding: 25mm 20mm; box-shadow: 0 0 10px rgba(0,0,0,0.1); page-break-after: always;}
        @media print {body {background: white;} .a4-page {margin: 0; box-shadow: none; page-break-after: always;}}
        h1 {font-size: 18pt; border-bottom: 2px solid #333; padding-bottom: 0.5em; margin-bottom: 1em; color: #003366;}
        h2 {font-size: 16pt; border-bottom: 1px solid #ddd; margin-top: 1.5em; margin-bottom: 0.8em; color: #003366;}
        h3 {font-size: 15pt; margin-top: 1.5em; margin-bottom: 0.7em; color: #003366; background: #e0f7fa; border-right: 5px solid #007bff; padding: 5px 10px; margin-right: -10px;}
        p {text-align: justify; margin: 0.8em 0; line-height: 1.8;}
        img {max-width: 100%; height: auto; display: block; margin: 1em auto; border: 3px solid #003366;}
        table {width: 100%; border-collapse: collapse; margin: 1em 0;}
        table th, table td {border: 1px solid #333; padding: 0.5em; text-align: right;}
        table th {background: #f0f0f0; font-weight: bold;}
        hr {border: none; border-top: 1px solid #ddd; margin: 1.5em 0;}
        .print-btn {position: fixed; top: 20px; left: 20px; background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-size: 16pt; cursor: pointer; z-index: 1000;}
        @media print {.print-btn {display: none;}}
    </style>
</head>
<body>
    <button class="print-btn" onclick="window.print()">🖨️ הדפס את כל הדפים</button>
'''

    for md_file, title in worksheets:
        content = Path(md_file).read_text(encoding='utf-8')
        if content.startswith('---'):
            content = content.split('---', 2)[2].strip()

        html_body = markdown.markdown(content, extensions=['fenced_code', 'tables', 'nl2br'])
        html_body = html_body.replace('src="assets/', 'src="../assets/')

        # הסרת כותרת כפולה - אם יש <h1> בתחילת html_body, נסיר אותו
        if html_body.strip().startswith('<h1>'):
            # מוצאים את סוף ה-h1 הראשון
            h1_end = html_body.find('</h1>')
            if h1_end != -1:
                html_body = html_body[h1_end + 5:].strip()

        html += f'<div class="a4-page"><h1 style="text-align: center; font-size: 20pt; margin-bottom: 1em;">{title}</h1>{html_body}</div>\n'

    html += '</body></html>'

    Path('all_worksheets.html').write_text(html, encoding='utf-8')
    print('✅ Created all_worksheets.html')

if __name__ == '__main__':
    build_simple_all()
