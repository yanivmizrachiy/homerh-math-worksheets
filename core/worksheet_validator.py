#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
בודק איכות אוטומטי לדפי עבודה - בדיקת מבנה, מקום לכתיבה, RTL ועברית
Worksheet Validator - Automatic quality checks for worksheets
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Ensure UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


class WorksheetValidator:
    """בודק איכות אוטומטי לדפי עבודה"""

    def __init__(self):
        """אתחול בודק"""
        self.errors = []
        self.warnings = []

    def validate(self, markdown_file: Path) -> Tuple[List[str], List[str]]:
        """
        בדיקת איכות מקיפה של דף עבודה

        Returns:
            (רשימת שגיאות, רשימת אזהרות)
        """
        self.errors = []
        self.warnings = []

        if not markdown_file.exists():
            self.errors.append(f"קובץ לא נמצא: {markdown_file}")
            return self.errors, self.warnings

        content = markdown_file.read_text(encoding='utf-8')

        # בדיקות מבנה
        self._check_structure(content)

        # בדיקת מקום לכתיבה
        self._check_writing_space(content)

        # בדיקת RTL ועברית
        self._check_rtl_hebrew(content)

        # בדיקת עקביות עיצוב
        self._check_design_consistency(content)

        # בדיקת תוכן פדגוגי
        self._check_pedagogical_content(content)

        return self.errors, self.warnings

    def _check_structure(self, content: str):
        """בדיקת מבנה דף העבודה"""
        # חובה: כותרת
        if not re.search(r'^#\s+', content, re.MULTILINE):
            self.warnings.append("לא נמצאה כותרת ראשית (# ...)")

        # חובה: הוראות
        if '## הוראות' not in content and 'הוראות' not in content:
            self.warnings.append("לא נמצאו הוראות לתלמידים")

        # בדיקת מספיק שאלות
        question_count = len(re.findall(r'^###\s*\([א-ת]\)', content, re.MULTILINE))
        if question_count == 0:
            question_count = len(re.findall(r'^\d+\.', content, re.MULTILINE))

        if question_count < 3:
            self.warnings.append(f"מספר שאלות נמוך: {question_count}")

    def _check_writing_space(self, content: str):
        """בדיקת מקום מספיק לכתיבה"""
        # חיפוש "דרך פתרון" או "הסבר"
        solution_blocks = re.findall(r'(דרך פתרון|הסבר|נימוק)[^\n]*\n([_ ]+)', content, re.MULTILINE)

        for match_type, space in solution_blocks:
            lines = space.count('\n')
            underscores = space.count('_')

            # בדיקה: לפחות 3 שורות או 50 תווים
            if lines < 2 and underscores < 40:
                self.warnings.append(f"מקום לכתיבה קטן מדי בסעיף '{match_type}': {lines} שורות, {underscores} תווים")

        # בדיקה: מספיק שורות ריקות אחרי שאלות
        question_sections = re.split(r'###\s*\([א-ת]\)', content)
        for i, section in enumerate(question_sections[1:], 1):  # התעלם מהחלק הראשון
            trailing_lines = len(section.rstrip().split('\n')[-1]) if section.rstrip() else 0
            if trailing_lines < 3:
                self.warnings.append(f"סעיף ({chr(0x05D0 + i - 1)}): מקום לכתיבה קטן מדי אחרי השאלה")

    def _check_rtl_hebrew(self, content: str):
        """בדיקת RTL ועברית"""
        # בדיקת תווים עבריים
        hebrew_chars = len(re.findall(r'[\u0590-\u05FF]', content))
        if hebrew_chars < 100:
            self.warnings.append(f"תוכן עברי מועט: {hebrew_chars} תווים עבריים")

        # בדיקת LTR לא תקין (אנגלית במקום לא נכון)
        # לא נבדוק יותר מדי כדי לא להתלונן על נוסחאות LaTeX

    def _check_design_consistency(self, content: str):
        """בדיקת עקביות עיצוב"""
        # בדיקת שימוש עקבי בכותרות
        h1_count = len(re.findall(r'^#\s+', content, re.MULTILINE))
        h2_count = len(re.findall(r'^##\s+', content, re.MULTILINE))
        h3_count = len(re.findall(r'^###\s+', content, re.MULTILINE))

        # חובה: כותרת ראשית אחת
        if h1_count != 1:
            self.warnings.append(f"מספר כותרות ראשיות שונה מ-1: {h1_count}")

    def _check_pedagogical_content(self, content: str):
        """בדיקת תוכן פדגוגי"""
        # אסור: פתרונות
        if re.search(r'(תשובה:|פתרון:|דוגמה פתורה)', content, re.IGNORECASE):
            self.errors.append("נמצאו פתרונות או תשובות - זה אסור לפי EXTREME PROMPT")

        # אסור: רמזים מובהקים
        if 'רמז:' in content or 'hint:' in content.lower():
            self.warnings.append("נמצאו רמזים - זה אסור לפי EXTREME PROMPT")

        # בדיקה: שאלות מתאימות לכיתה ח'
        # לא נבדוק כאן בפירוט, אבל נבדוק שלא נמצא חומר מתקדם מדי
        advanced_topics = ['נגזרת', 'אינטגרל', 'לוגריתם', 'מטריצה']
        for topic in advanced_topics:
            if topic in content:
                self.warnings.append(f"נמצא נושא מתקדם: {topic} - יתכן שלא מתאים לכיתה ח'")

    def print_report(self, markdown_file: Path):
        """הדפסת דוח בדיקה"""
        errors, warnings = self.validate(markdown_file)

        sys.stdout.buffer.write(f"\n{'='*60}\n".encode('utf-8'))
        sys.stdout.buffer.write(f"דוח בדיקת איכות: {markdown_file.name}\n".encode('utf-8'))
        sys.stdout.buffer.write(f"{'='*60}\n".encode('utf-8'))

        if errors:
            sys.stdout.buffer.write(f"❌ שגיאות ({len(errors)}):\n".encode('utf-8'))
            for error in errors:
                sys.stdout.buffer.write(f"  - {error}\n".encode('utf-8'))
        else:
            sys.stdout.buffer.write(f"✅ אין שגיאות\n".encode('utf-8'))

        if warnings:
            sys.stdout.buffer.write(f"⚠️ אזהרות ({len(warnings)}):\n".encode('utf-8'))
            for warning in warnings:
                sys.stdout.buffer.write(f"  - {warning}\n".encode('utf-8'))
        else:
            sys.stdout.buffer.write(f"✅ אין אזהרות\n".encode('utf-8'))

        sys.stdout.buffer.write(f"{'='*60}\n\n".encode('utf-8'))

        return len(errors) == 0


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("שימוש: python worksheet_validator.py <קובץ_markdown>")
        sys.exit(1)

    validator = WorksheetValidator()
    markdown_file = Path(sys.argv[1])
    is_valid = validator.print_report(markdown_file)
    sys.exit(0 if is_valid else 1)
