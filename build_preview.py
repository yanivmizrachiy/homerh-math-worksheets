#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
בניית דפי תצוגה סטטיים מראש - יוצר HTML מעובד מקבצי Markdown
Build static preview pages from Markdown files
"""

import sys
from pathlib import Path
import markdown

# Ensure UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def build_preview_pages():
    """בניית דפי תצוגה לכל דפי העבודה"""
    worksheets_dir = Path('worksheets/grade-8')
    output_dir = Path('preview_pages')
    output_dir.mkdir(exist_ok=True)

    # קריאת תבנית HTML
    template = Path('view.html').read_text(encoding='utf-8')

    # עיבוד כל דף עבודה
    for md_file in sorted(worksheets_dir.glob('*.md')):
        print(f"Processing: {md_file.name}")

        # קריאת תוכן Markdown
        content = md_file.read_text(encoding='utf-8')

        # הסרת front matter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2].strip()

        # המרת Markdown ל-HTML
        html_body = markdown.markdown(content, extensions=['fenced_code', 'tables', 'nl2br'])

        # עיבוד LaTeX math
        html_body = html_body.replace('$$', '$$$$')  # Escape for template

        # תיקון נתיב תמונות עבור GitHub Pages - מ-preview_pages צריך לעלות 2 תיקיות
        html_body = html_body.replace('src="assets/', 'src="../../assets/')

        # יצירת HTML מלא
        html_output = template.replace(
            '<div class="page" id="content">\n        <div class="loading">⏳ טוען...</div>\n    </div>',
            f'<div class="page" id="content">{html_body}</div>'
        ).replace(
            'const params = new URLSearchParams(window.location.search);\n        const file = params.get(\'file\') || \'worksheets/grade-8/kavba_a1_graph_reading.md\';',
            f'// Static page for {md_file.name}'
        ).replace(
            'fetch(filePath)',
            'Promise.resolve("")'  # Skip fetch for static page
        )

        # שמירה
        output_file = output_dir / f"{md_file.stem}.html"
        output_file.write_text(html_output, encoding='utf-8')
        print(f"  Created: {output_file}")

    print(f"\n✅ All preview pages created in {output_dir}/")


if __name__ == '__main__':
    build_preview_pages()
