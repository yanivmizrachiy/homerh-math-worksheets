# הוראות פרסום לאתר חיצוני

## אפשרות 1: GitHub Pages (מומלץ - חינמי)

### שלב 1: העלאה ל-GitHub
```bash
# אם עדיין לא יצרת repository:
git init
git add .
git commit -m "Initial commit - Math worksheets"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/homerh.git
git push -u origin main
```

### שלב 2: הפעלת GitHub Pages
1. לך ל-GitHub repository שלך
2. לחץ על **Settings** → **Pages**
3. תחת **Source**, בחר **main branch** (או **master**)
4. לחץ **Save**
5. תוך דקות, האתר יהיה זמין ב: `https://YOUR_USERNAME.github.io/homerh/`

### שלב 3: עדכון קישורים (אם צריך)
אם ה-repository לא נקרא `homerh`, עדכן את הנתיבים ב-`index.html` ו-`preview.html`.

---

## אפשרות 2: Netlify Drop (הכי פשוט - ללא Git)

### שלב 1: הכנת קבצים
1. ודא שכל הקבצים בתיקייה:
   - `index.html`
   - `preview.html`
   - `preview_pages/` (כל הדפים)
   - `assets/graphs/` (הגרפים)

### שלב 2: העלאה ל-Netlify
1. לך ל: https://app.netlify.com/drop
2. גרור את כל התיקייה `homerh` לתוך החלון
3. תוך שניות, תקבל קישור: `https://random-name-123.netlify.app`

### שלב 3: שינוי שם (אופציונלי)
1. ב-Netlify, לחץ על **Site settings** → **Change site name**
2. בחר שם ייחודי (למשל: `math-worksheets-grade8`)

---

## אפשרות 3: Vercel (חינמי, מהיר)

### שלב 1: התקנת Vercel CLI
```bash
npm install -g vercel
```

### שלב 2: פרסום
```bash
cd c:\Users\yaniv\OneDrive\Desktop\homerh
vercel
```

עקוב אחר ההוראות - תוך דקות תקבל קישור!

---

## בדיקה לפני פרסום

ודא שהקבצים הבאים קיימים:
- ✅ `index.html` - דף ראשי
- ✅ `preview.html` - דף רשימה (גיבוי)
- ✅ `preview_pages/kavba_a1_graph_reading.html`
- ✅ `preview_pages/kavba_a1_slope_table.html`
- ✅ `preview_pages/kavba_a1_50_questions_coefficients.html`
- ✅ `assets/graphs/jerusalem_motion_graph.png`

---

## פתרון מהיר - Netlify Drop (5 דקות)

1. **לך ל**: https://app.netlify.com/drop
2. **גרור את התיקייה** `homerh` (כל התיקייה!)
3. **קבל קישור** - מוכן!

זה הכל! 🎉
