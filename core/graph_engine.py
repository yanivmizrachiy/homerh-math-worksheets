#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מנוע גרפים חכם - יצירת גרפים באיכות גבוהה מאוד להדפסה מקצועית
Graph Engine - High-quality graph generation for professional printing
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from pathlib import Path
from typing import List, Tuple, Optional
from PIL import Image

# Ensure UTF-8 encoding for stdout
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


class GraphEngine:
    """מנוע יצירת גרפים מקצועיים עם בדיקות איכות מחמירות"""

    # הגדרות קיצוניות לאיכות הדפסה מקסימלית
    DPI = 400
    FIGSIZE_WIDTH = 18  # אינץ'
    FIGSIZE_HEIGHT = 12  # אינץ'
    MIN_LABEL_FONTSIZE = 40  # פונט מינימלי לתוויות נקודות
    MIN_AXIS_LABEL_FONTSIZE = 28  # פונט מינימלי לצירי הגרף
    MIN_TICK_FONTSIZE = 24  # פונט מינימלי לסרגלי הגרף
    MIN_LINEWIDTH = 4  # עובי קו מינימלי
    POINT_RADIUS = 0.25  # רדיוס נקודה מינימלי

    def __init__(self, output_dir: str = "assets/graphs"):
        """
        אתחול מנוע הגרפים

        Args:
            output_dir: תיקיית היעד לשמירת גרפים
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._setup_hebrew_font()

    def _setup_hebrew_font(self):
        """הגדרת פונט עברי עם גיבויים"""
        # הגדרת גודלי פונט גלובליים - גדולים מאוד
        plt.rcParams['font.size'] = 16
        plt.rcParams['axes.titlesize'] = 30
        plt.rcParams['axes.labelsize'] = 28
        plt.rcParams['xtick.labelsize'] = 24
        plt.rcParams['ytick.labelsize'] = 24
        plt.rcParams['legend.fontsize'] = 18
        plt.rcParams['figure.titlesize'] = 30

        # רשימת פונטים עבריים לפי עדיפות
        hebrew_fonts = [
            'Arial Unicode MS',
            'Tahoma',
            'Lucida Sans Unicode',
            'David',
            'DejaVu Sans'
        ]

        font_found = False
        for font_name in hebrew_fonts:
            try:
                plt.rcParams['font.family'] = font_name
                font_found = True
                break
            except:
                continue

        if not font_found:
            plt.rcParams['font.family'] = 'sans-serif'

        # Disable LaTeX for general text to avoid font issues
        plt.rcParams['text.usetex'] = False
        plt.rcParams['svg.fonttype'] = 'none'  # Embed fonts as text

    def create_motion_graph(
        self,
        points: List[Tuple[float, float]],
        labels: List[str],
        x_label: str,
        y_label: str,
        title: str,
        x_range: Tuple[float, float],
        y_range: Tuple[float, float],
        x_ticks: Optional[List[float]] = None,
        y_ticks: Optional[List[float]] = None,
        filename: str = "motion_graph.png"
    ) -> Path:
        """
        יצירת גרף תנועה מקצועי עם נקודות מסומנות

        Args:
            points: רשימת נקודות (זמן, מרחק)
            labels: תוויות לנקודות (A, B, C, ...)
            x_label: תווית ציר X
            y_label: תווית ציר Y
            title: כותרת הגרף
            x_range: טווח ציר X (min, max)
            y_range: טווח ציר Y (min, max)
            x_ticks: סרגלי ציר X (אופציונלי)
            y_ticks: סרגלי ציר Y (אופציונלי)
            filename: שם קובץ הגרף

        Returns:
            Path לקובץ הגרף שנוצר
        """
        # יצירת figure גדול מאוד
        fig, ax = plt.subplots(figsize=(self.FIGSIZE_WIDTH, self.FIGSIZE_HEIGHT))

        # חילוץ קואורדינטות
        times = [p[0] for p in points]
        distances = [p[1] for p in points]

        # ציור קו הגרף - עבה וברור
        ax.plot(times, distances, color='#0066CC', linewidth=self.MIN_LINEWIDTH,
                label='מסלול התנועה', zorder=1, alpha=0.9)

        # צבעים לנקודות - מגוון ברור
        point_colors = ['#FF4444', '#0066FF', '#00AA00', '#FF8800', '#AA00AA', '#8B4513', '#FF4444']

        # סימון כל נקודה בעיגול ובתווית - גדול ובולט מאוד
        for i, ((t, d), label) in enumerate(zip(points, labels)):
            color = point_colors[i % len(point_colors)]

            # עיגול מלא - גדול ובולט
            circle = Circle((t, d), self.POINT_RADIUS, facecolor=color, fill=True,
                           zorder=3, edgecolor='black', linewidth=3, alpha=0.9)
            ax.add_patch(circle)

            # תווית אות - גדולה מאוד ובולטת לחלוטין
            ax.text(t, d + 1.2, label, fontsize=self.MIN_LABEL_FONTSIZE,
                   fontweight='bold', ha='center', va='bottom', color='black',
                   zorder=4, bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                      edgecolor='black', linewidth=2))

            # זוג מסודר - גדול וברור
            y_offset = -0.8 if i % 2 == 0 else -1.1
            ax.text(t, d + y_offset, f'({int(t)},{int(d)})',
                   fontsize=22, fontweight='bold', ha='center', va='top',
                   color='black', zorder=4,
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow',
                            alpha=0.7, edgecolor='black', linewidth=1))

        # הגדרת הצירים
        ax.set_xlim(x_range[0] - 0.5, x_range[1] + 0.5)
        ax.set_ylim(y_range[0] - 1, y_range[1] + 1)

        # תוויות צירים - גדולות וברורות
        ax.set_xlabel(x_label, fontsize=self.MIN_AXIS_LABEL_FONTSIZE,
                     fontweight='bold', labelpad=15, color='#000000')
        ax.set_ylabel(y_label, fontsize=self.MIN_AXIS_LABEL_FONTSIZE,
                     fontweight='bold', labelpad=20, color='#000000')

        # סרגלים - ברורים וגדולים
        if x_ticks:
            ax.set_xticks(x_ticks)
            ax.set_xticklabels([str(int(t)) for t in x_ticks],
                              fontsize=self.MIN_TICK_FONTSIZE, fontweight='bold')
            ax.tick_params(axis='x', which='major', length=10, width=3,
                          labelsize=self.MIN_TICK_FONTSIZE)

        if y_ticks:
            ax.set_yticks(y_ticks)
            ax.set_yticklabels([str(int(t)) for t in y_ticks],
                              fontsize=self.MIN_TICK_FONTSIZE, fontweight='bold')
            ax.tick_params(axis='y', which='major', length=10, width=3,
                          labelsize=self.MIN_TICK_FONTSIZE)

        # רשת רקע - ברורה ונוחה לקריאה
        ax.grid(True, alpha=0.4, linestyle='--', linewidth=1.5, color='gray')
        ax.grid(True, which='major', alpha=0.6, linestyle='-', linewidth=2, color='darkgray')

        # קווי עזר על הצירים - עבה וברור
        ax.axhline(y=0, color='black', linewidth=3)
        ax.axvline(x=0, color='black', linewidth=3)

        # כותרת - גדולה ובולטת
        ax.set_title(title, fontsize=30, fontweight='bold', pad=25, color='#003366')

        # הסרת קווי המסגרת העליונים והימניים
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('black')
        ax.spines['left'].set_linewidth(3)
        ax.spines['bottom'].set_color('black')
        ax.spines['bottom'].set_linewidth(3)

        plt.tight_layout()

        # שמירה ברזולוציה גבוהה מאוד
        filepath = self.output_dir / filename
        fig.savefig(filepath, dpi=self.DPI, format='png', bbox_inches='tight',
                   facecolor='white', edgecolor='none', pad_inches=0.2)
        plt.close(fig)

        # בדיקת איכות מחמירה
        errors = self._verify_graph(filepath)
        if errors:
            raise RuntimeError(f"Graph verification failed: {', '.join(errors)}")

        sys.stdout.buffer.write(f"✅ גרף נוצר בהצלחה: {filepath}\n".encode('utf-8'))
        return filepath

    def _verify_graph(self, graph_path: Path) -> List[str]:
        """
        בדיקת איכות מחמירה של הגרף

        Returns:
            רשימת שגיאות (ריקה אם הכל תקין)
        """
        errors = []

        if not graph_path.exists():
            errors.append(f"קובץ הגרף לא נמצא: {graph_path}")
            return errors

        # בדיקת גודל קובץ
        file_size = graph_path.stat().st_size
        if file_size == 0:
            errors.append(f"קובץ הגרף ריק: {graph_path}")
            return errors

        if file_size < 10000:  # פחות מ-10KB זה חשוד
            errors.append(f"קובץ הגרף קטן מדי: {file_size} bytes")

        try:
            with Image.open(graph_path) as img:
                width, height = img.size

                # בדיקת מימדים
                expected_min_width = self.FIGSIZE_WIDTH * self.DPI * 0.9
                expected_min_height = self.FIGSIZE_HEIGHT * self.DPI * 0.9

                if width < expected_min_width:
                    errors.append(f"רוחב הגרף קטן מהצפוי: {width} < {expected_min_width}")

                if height < expected_min_height:
                    errors.append(f"גובה הגרף קטן מהצפוי: {height} < {expected_min_height}")

                # בדיקת יחס גובה-רוחב
                expected_aspect = self.FIGSIZE_WIDTH / self.FIGSIZE_HEIGHT
                actual_aspect = width / height
                if abs(actual_aspect - expected_aspect) > 0.1:
                    errors.append(f"יחס גובה-רוחב חורג: {actual_aspect:.2f} != {expected_aspect:.2f}")

                # בדיקת פורמט
                if img.format != 'PNG':
                    errors.append(f"פורמט הגרף אינו PNG: {img.format}")

        except Exception as e:
            errors.append(f"שגיאה בעת בדיקת הגרף: {e}")

        return errors


def create_jerusalem_motion_graph() -> Path:
    """
    יצירת גרף תנועה ספציפי: מרחק מהבית בירושלים לאורך זמן

    Returns:
        Path לקובץ הגרף שנוצר
    """
    engine = GraphEngine()

    # הגדרת נקודות הגרף (זמן, מרחק)
    # סיפור: יוצא מהבית, נוסע, עוצר, ממשיך, חוזר
    points = [
        (0, 0),   # A - התחלה בבית
        (1, 4),   # B - התרחק 4 ק"מ
        (2, 4),   # C - עצר (מרחק קבוע)
        (3, 8),   # D - התרחק עוד ל-8 ק"מ
        (4, 6),   # E - התקרב קצת ל-6 ק"מ
        (5, 6),   # F - עצר שוב
        (6, 0)    # G - חזר הביתה
    ]

    labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    return engine.create_motion_graph(
        points=points,
        labels=labels,
        x_label='זמן (שעות)',
        y_label='מרחק מהבית בירושלים (ק"מ)',
        title='גרף תנועה: מרחק מהבית בירושלים לאורך זמן',
        x_range=(0, 6),
        y_range=(0, 12),
        x_ticks=list(range(0, 7)),
        y_ticks=list(range(0, 11, 2)),
        filename='jerusalem_motion_graph.png'
    )


if __name__ == '__main__':
    create_jerusalem_motion_graph()
