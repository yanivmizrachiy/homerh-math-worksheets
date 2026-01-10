#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
סקריפט נוח ליצירת PDF מדפי עבודה
Convenient script for generating PDFs from worksheets
"""

import sys
from pathlib import Path
from core.pdf_engine import generate_pdf

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("שימוש: python generate_pdf.py <קובץ_markdown> [קובץ_pdf_פלט]")
        print("\nדוגמה:")
        print("  python generate_pdf.py worksheets/grade-8/kavba_a1_graph_reading.md")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        pdf_path = generate_pdf(input_file, output_file)
        sys.stdout.buffer.write(f"\n✅ PDF נוצר בהצלחה: {pdf_path}\n".encode('utf-8'))
    except Exception as e:
        sys.stderr.buffer.write(f"\n❌ שגיאה: {e}\n".encode('utf-8'))
        sys.exit(1)
