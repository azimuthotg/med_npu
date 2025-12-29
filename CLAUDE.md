# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django-based website for Faculty of Medicine, Nakhon Phanom University. The site uses a Thai-language CMS with Django admin for content management, Tailwind CSS for styling, and Alpine.js for interactivity.

## Common Commands

### Development Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py migrate
python manage.py createsuperuser
```

### Development Workflow
```bash
# Run development server
python manage.py runserver

# After modifying models
python manage.py makemigrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Collect static files (production)
python manage.py collectstatic
```

### Creating New Django Apps
```bash
# Create app and move to apps directory
python manage.py startapp appname
mv appname apps/

# Remember to:
# 1. Add 'apps.appname' to INSTALLED_APPS in config/settings.py
# 2. Create apps/appname/urls.py
# 3. Include URLs in config/urls.py
```

## Architecture Overview

### App Structure and Responsibilities

The project follows Django's app-based architecture with four main apps:

**apps/core** - Foundation layer
- Base models (`TimeStampedModel`, `SiteSettings`)
- Site-wide context processor (`site_settings`)
- Homepage and contact views
- Provides shared functionality for other apps

**apps/about** - Organization information
- Executive leadership (`Executive` model with position hierarchy)
- Departments (`Department` model linked to executives)
- Views for about pages, leadership directory

**apps/education** - Academic programs
- Program catalog (`Program` model with levels: bachelor/master/doctoral)
- Admissions (`Admission` model with date-based `is_open` property)
- Curriculum file handling

**apps/news** - Content management
- News articles (`News` model with slugs, view tracking)
- Categories (`Category` model with color coding)
- File attachments (`NewsAttachment` model)
- Featured news and publishing workflow

### Model Inheritance Pattern

All timestamped models inherit from `apps.core.models.TimeStampedModel`, which provides:
- `created_at` - Auto-set on creation
- `updated_at` - Auto-updated on save

This ensures consistent timestamp handling across the application.

### URL Structure

```
/                       # Homepage (apps.core)
/about/                 # About faculty (apps.about)
/education/             # Programs and admissions (apps.education)
/news/                  # News listing (apps.news)
/news/<slug>/           # News detail
/admin/                 # Django admin
```

Root URL configuration is in `config/urls.py`, each app has its own `urls.py`.

### Template Organization

```
templates/
├── base.html                    # Main layout with Tailwind config
├── components/                  # Reusable UI components
│   ├── navbar.html             # Main navigation
│   ├── footer.html             # Site footer
│   ├── topbar.html             # Top information bar
│   └── card_news.html          # News card component
├── pages/                       # Standalone pages
│   └── home.html               # Homepage
└── [app]/                       # App-specific templates
    └── [app]_*.html
```

Templates extend `base.html` and use components via `{% include 'components/...' %}`.

### Context Processor

`apps.core.context_processors.site_settings` makes these variables available in all templates:
- `SITE_NAME`, `SITE_NAME_EN`, `SITE_SHORT_NAME`
- `SITE_DESCRIPTION`
- `CONTACT_EMAIL`, `CONTACT_PHONE`, `CONTACT_ADDRESS`
- `SOCIAL_FACEBOOK`, `SOCIAL_YOUTUBE`, `SOCIAL_LINE`
- `PRIMARY_COLOR` (#229799)

These are defined in `config/settings.py` and accessible in any template without passing through view context.

### Static Files and Styling

- **CSS Framework**: Tailwind CSS (CDN in development, configured in `base.html`)
- **JavaScript**: Alpine.js for reactive components
- **Font**: IBM Plex Sans Thai (Google Fonts)
- **Primary Color**: #229799 (teal) with full palette in Tailwind config

Custom CSS classes defined in `base.html`:
- `.gradient-hero` - Teal gradient background
- `.card-hover` - Card lift effect on hover
- `.glass-effect` - Glassmorphism style

### Database Configuration

- **Development**: SQLite (`db.sqlite3`)
- **Production**: MySQL (commented configuration in `settings.py`)

When switching to MySQL for production, uncomment the MySQL `DATABASES` configuration and install `mysqlclient` or `PyMySQL`.

### Slug Generation

Models with slugs (`News`, `Program`) auto-generate slugs from Thai text using `django.utils.text.slugify` with `allow_unicode=True`. The `News` model handles slug conflicts by appending numeric suffixes.

### Key Model Properties and Methods

**News model**:
- `increment_view()` - Atomic view count increment
- `get_absolute_url()` - Returns detail page URL using slug
- Auto-slug generation with conflict resolution

**Admission model**:
- `is_open` property - Checks if admission is currently accepting applications based on dates

**Executive/Department**:
- `order` field controls display sequence
- `is_active` filters visible items

### Site Settings Singleton

`SiteSettings` model in `apps/core` implements singleton pattern:
- Always uses `pk=1`
- `save()` method enforces single instance
- `load()` classmethod for easy retrieval
- Stores site-wide configuration editable via admin

## Development Guidelines

### Adding New Pages

1. Create view in `apps/[app]/views.py` (typically `TemplateView` or class-based view)
2. Add URL pattern in `apps/[app]/urls.py`
3. Create template in `templates/[app]/`
4. Use `{% extends 'base.html' %}` and override `{% block content %}`

### Adding New Models

1. Define model in `apps/[app]/models.py`
2. Inherit from `TimeStampedModel` if timestamps needed
3. Add verbose names in Thai (both singular and plural)
4. Run `python manage.py makemigrations` and `python manage.py migrate`
5. Register in `apps/[app]/admin.py` for admin interface

### Working with Images

- News images: Upload to `media/news/YYYY/MM/`
- Attachments: Upload to `media/news/attachments/YYYY/MM/`
- Executive photos: Upload to `media/executives/`
- Program images: Upload to `media/education/programs/`

Files are organized by date using `upload_to` patterns like `'news/%Y/%m/'`.

### Language and i18n

- Primary language: Thai (`LANGUAGE_CODE = 'th'`)
- Timezone: `Asia/Bangkok`
- Multi-language support configured (Thai/English) via `LANGUAGES` setting
- `LocaleMiddleware` enabled for future i18n expansion
- Locale files should go in `locale/` directory (create as needed)

## Color Palette

Primary color: **#229799** (Teal)

Full palette configured in Tailwind:
- `primary-50`: #E8F7F7
- `primary-100`: #D1EFEF
- `primary-200`: #A3DFDF
- `primary-300`: #75CFCF
- `primary-400`: #47BFBF
- `primary-500`: #229799 (base)
- `primary-600`: #1B7A7C
- `primary-700`: #155D5E
- `primary-800`: #0E4041
- `primary-900`: #082323

Use in templates: `bg-primary-500`, `text-primary-700`, etc.

## Important Notes

- **Security**: Change `SECRET_KEY` before production deployment
- **Debug**: Set `DEBUG = False` in production
- **Static Files**: Uncomment WhiteNoise middleware and storage for production
- **Database**: Switch from SQLite to MySQL for production
- **Media Files**: Configure web server to serve `MEDIA_ROOT` in production
- **Third-party Apps**: Several apps in `requirements.txt` are commented out in `INSTALLED_APPS` (django-ckeditor, django-taggit, etc.) - uncomment as needed
