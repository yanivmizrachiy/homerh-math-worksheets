#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
יצירת גרף פונקציה קווית - דוגמה לנושא השיפוע
Create linear function graph - example for slope topic
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.graph_engine import GraphEngine
import numpy as np
import matplotlib.pyplot as plt

def create_linear_function_graph():
    """יצירת גרף פונקציה קווית עם שיפוע 3 ונקודת חיתוך 3"""
    engine = GraphEngine()
    
    # פרמטרים: y = 3x + 3
    slope = 3
    intercept = 3
    x_values = np.linspace(0, 4, 100)
    y_values = slope * x_values + intercept
    
    # יצירת הגרף
    fig, ax = plt.subplots(figsize=(18, 12))
    
    # קו הגרף
    ax.plot(x_values, y_values, color='#0066CC', linewidth=4, label=f'$y = {slope}x + {intercept}$', zorder=2)
    
    # סימון נקודות חשובות
    important_points = [
        (0, 3, 'A', 'חיתוך עם ציר y'),
        (1, 6, 'B', ''),
        (2, 9, 'C', ''),
        (3, 12, 'D', ''),
        (4, 15, 'E', '')
    ]
    
    from matplotlib.patches import Circle
    colors = ['#FF4444', '#0066FF', '#00AA00', '#FF8800', '#AA00AA']
    
    for i, ((x, y, label, desc), color) in enumerate(zip(important_points, colors)):
        circle = Circle((x, y), 0.3, facecolor=color, fill=True, zorder=4, 
                       edgecolor='black', linewidth=3, alpha=0.9)
        ax.add_patch(circle)
        ax.text(x, y + 1.5, label, fontsize=40, fontweight='900', ha='center', va='bottom',
               color='#000000', zorder=5, bbox=dict(boxstyle='round,pad=0.8', facecolor='white',
               edgecolor='#000000', linewidth=5, alpha=1.0))
        ax.text(x, y - 1.5, f'({x},{y})', fontsize=22, fontweight='900', ha='center', va='top',
               color='#000000', zorder=5, bbox=dict(boxstyle='round,pad=0.6', facecolor='#FFFF00',
               alpha=0.95, edgecolor='#000000', linewidth=4), family='monospace')
    
    # הגדרת הצירים
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-1, 16)
    ax.set_xlabel('$x$', fontsize=28, fontweight='900', labelpad=25, color='#000000')
    ax.set_ylabel('$y$', fontsize=28, fontweight='900', labelpad=30, color='#000000')
    ax.set_title(f'גרף פונקציה קווית: $y = {slope}x + {intercept}$', fontsize=30, fontweight='900', 
                pad=35, color='#000000')
    
    # סרגלי הגרף
    ax.set_xticks(range(0, 5))
    ax.set_xticklabels(['0', '1', '2', '3', '4'], fontsize=24, fontweight='900', color='#000000')
    ax.set_yticks(range(0, 16, 3))
    ax.set_yticklabels(['0', '3', '6', '9', '12', '15'], fontsize=24, fontweight='900', color='#000000')
    
    # רשת
    ax.grid(True, alpha=0.4, linestyle='--', linewidth=1.5, color='gray')
    ax.grid(True, which='major', alpha=0.6, linestyle='-', linewidth=2, color='darkgray')
    ax.axhline(y=0, color='black', linewidth=3)
    ax.axvline(x=0, color='black', linewidth=3)
    
    # הסרת מסגרות מיותרות
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('black')
    ax.spines['left'].set_linewidth(3)
    ax.spines['bottom'].set_color('black')
    ax.spines['bottom'].set_linewidth(3)
    
    plt.tight_layout()
    
    # שמירה
    output_path = Path('assets/graphs')
    output_path.mkdir(parents=True, exist_ok=True)
    filepath = output_path / 'linear_function_graph.png'
    fig.savefig(filepath, dpi=400, format='png', bbox_inches='tight', 
               facecolor='white', edgecolor='none', pad_inches=0.2)
    
    print(f"✅ גרף נשמר: {filepath}")
    return filepath

if __name__ == '__main__':
    create_linear_function_graph()
