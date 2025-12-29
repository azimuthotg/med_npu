# 🏥 เว็บไซต์คณะแพทยศาสตร์ มหาวิทยาลัยนครพนม

Django Project Starter สำหรับพัฒนาเว็บไซต์คณะแพทยศาสตร์

## 🎨 Color Palette

สีหลัก: **#229799** (Teal)

```
Primary 500: #229799 (สีหลัก)
Primary 600: #1B7A7C
Primary 700: #155D5E
Primary 800: #0E4041
Primary 900: #082323
```

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/azimuthotg/med_npu.git
cd med_npu
```

### 2. สร้าง Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# หรือ
venv\Scripts\activate  # Windows
```

### 3. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 4. ตั้งค่า Environment Variables

**สร้างไฟล์ `.env` จาก `.env.example`:**

```bash
cp .env.example .env
```

**แก้ไขไฟล์ `.env` และกรอกข้อมูลของคุณ:**

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=3306
```

**⚠️ สำคัญ:** ไฟล์ `.env` จะไม่ถูก commit ขึ้น Git เพราะมีข้อมูลสำคัญ

### 5. ตั้งค่า Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. รัน Development Server

```bash
python manage.py runserver
```

เปิด http://127.0.0.1:8000

---

## 📁 โครงสร้างโปรเจค

```
med_npu/
├── config/                 # Django configuration
│   ├── settings.py        # Settings หลัก
│   ├── urls.py            # URL routing หลัก
│   └── wsgi.py
├── apps/                   # Django apps
│   ├── core/              # หน้าหลัก, base functions
│   ├── about/             # เกี่ยวกับคณะ
│   ├── education/         # การศึกษา, หลักสูตร
│   └── news/              # ข่าวประชาสัมพันธ์
├── templates/              # HTML templates
│   ├── base.html          # Layout หลัก
│   ├── components/        # Reusable components
│   │   ├── navbar.html
│   │   ├── footer.html
│   │   ├── hero.html
│   │   └── card_news.html
│   └── pages/             # Page templates
├── static/                 # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── media/                  # User uploads
├── requirements.txt
└── manage.py
```

---

## 🛠️ สำหรับ Claude Code

### คำสั่งที่ใช้บ่อย

```bash
# สร้าง app ใหม่
python manage.py startapp appname
mv appname apps/

# สร้าง migrations
python manage.py makemigrations
python manage.py migrate

# รัน server
python manage.py runserver

# เข้า shell
python manage.py shell

# สร้าง superuser
python manage.py createsuperuser
```

### การเพิ่มหน้าใหม่

1. **สร้าง View** ใน `apps/[app]/views.py`
2. **สร้าง URL** ใน `apps/[app]/urls.py`
3. **สร้าง Template** ใน `templates/[app]/`

### ตัวอย่างการเพิ่มหน้า

```python
# apps/about/views.py
from django.views.generic import TemplateView

class HistoryView(TemplateView):
    template_name = 'about/history.html'
```

```python
# apps/about/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.HistoryView.as_view(), name='history'),
]
```

---

## 📝 Tasks สำหรับ Claude Code

### Phase 1: พื้นฐาน
- [x] โครงสร้าง Django project
- [x] Base template + Tailwind CSS
- [x] Navbar, Footer components
- [x] Homepage
- [ ] เพิ่มรูปภาพจริง (logo, hero images)
- [ ] ปรับ responsive สำหรับ mobile

### Phase 2: เนื้อหา
- [ ] หน้าเกี่ยวกับคณะ (ประวัติ, วิสัยทัศน์, ผู้บริหาร)
- [ ] หน้าหลักสูตร
- [ ] หน้าการรับสมัคร
- [ ] หน้าข่าวสาร + Admin จัดการข่าว
- [ ] หน้าติดต่อ + Google Maps

### Phase 3: Features
- [ ] ระบบค้นหา
- [ ] Multi-language (TH/EN)
- [ ] SEO optimization
- [ ] Sitemap
- [ ] RSS Feed

---

## 🎯 Prompts สำหรับ Claude Code

### เพิ่มหน้าใหม่
```
สร้างหน้า "ประวัติคณะ" ใน apps/about/ 
- URL: /about/history/
- Template: templates/about/history.html
- มี breadcrumb, sidebar menu
- ใช้ component จาก base.html
```

### เพิ่ม Model
```
สร้าง Model สำหรับ "บุคลากร" ใน apps/about/
- ชื่อ, ตำแหน่ง, รูปภาพ, email, เบอร์โทร
- มี Admin interface
- แสดงในหน้า /about/staff/
```

### เพิ่ม Feature
```
เพิ่มระบบค้นหาข่าว
- Search box ใน navbar
- ค้นหาจาก title, content
- แสดงผลที่ /search/?q=keyword
```

---

## 📚 เอกสารอ้างอิง

- [Django Documentation](https://docs.djangoproject.com/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [HTMX](https://htmx.org/docs/)
- [Alpine.js](https://alpinejs.dev/)

---

## 👨‍💻 ผู้พัฒนา

สำนักวิทยบริการ มหาวิทยาลัยนครพนม

---

*สร้างโดย Claude AI - ธันวาคม 2567*
