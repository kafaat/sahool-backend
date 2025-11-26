# سهول - نظام المراقبة الزراعية المتكامل

## نظرة عامة

**سهول** هو نظام متكامل لمراقبة وتحليل الأراضي الزراعية باستخدام صور الأقمار الصناعية Sentinel-2، مع تحليل مؤشر الغطاء النباتي (NDVI) وكشف التغيرات ونظام تنبيهات ذكي.

## المكونات الرئيسية

### 1. Backend API (FastAPI)
- **التقنيات:** FastAPI, PostgreSQL + PostGIS, Celery, Redis
- **الميزات:**
  - إدارة المزارع والحقول
  - جلب ومعالجة صور Sentinel-2
  - حساب NDVI بتقنية Windowed Processing
  - توليد XYZ Tiles للخرائط
  - كشف التغيرات (Change Detection)
  - نظام تنبيهات ذكي
  - بيانات طقس مجانية (Open-Meteo)
  - تقارير أسبوعية

### 2. Flutter Application
- **التقنيات:** Flutter 3.0+, Provider, Dio
- **الميزات:**
  - واجهة مستخدم عربية كاملة
  - إدارة المزارع والحقول
  - رسم الحقول على الخريطة
  - عرض تحليل NDVI
  - رسوم بيانية للتغيرات الزمنية
  - مقارنة الصور قبل وبعد
  - توليد تقارير PDF

### 3. Web Application (قيد التطوير)
- **التقنيات:** React 19, Tailwind CSS 4
- **الميزات:** واجهة ويب تفاعلية مع خرائط Google Maps

## التثبيت والتشغيل

### المتطلبات الأساسية
- Docker و Docker Compose
- حساب في Copernicus Data Space Ecosystem (CDSE)

### خطوات التشغيل السريع

1. **إعداد البيئة:**
```bash
cp .env.example .env
# قم بتعديل .env وإضافة بيانات اعتماد CDSE
```

2. **تشغيل المشروع:**
```bash
chmod +x setup.sh
./setup.sh
```

3. **الوصول إلى التطبيق:**
- API Documentation: http://localhost:8000/docs
- Storage Files: http://localhost:8000/storage/

### التشغيل اليدوي

```bash
# تشغيل الحاويات
docker compose up -d

# تطبيق migrations
docker compose exec api alembic upgrade head

# عرض السجلات
docker compose logs -f
```

## بنية المشروع

```
sahool_project/
├── app/                      # Backend FastAPI
│   ├── core/                 # إعدادات أساسية
│   ├── modules/              # وحدات النظام
│   │   ├── farms/            # إدارة المزارع
│   │   ├── fields/           # إدارة الحقول
│   │   ├── satellite/        # معالجة الأقمار الصناعية
│   │   ├── alerts/           # نظام التنبيهات
│   │   ├── weather/          # بيانات الطقس
│   │   └── reports/          # التقارير
│   └── workers/              # Celery workers
├── migrations/               # Database migrations
├── ui/                       # واجهات المستخدم
│   ├── flutter/              # تطبيق Flutter
│   └── web/                  # تطبيق الويب
├── docker-compose.yml        # إعدادات Docker
├── setup.sh                  # سكريبت التشغيل السريع
└── README.md                 # هذا الملف
```

## API Endpoints

### المزارع (Farms)
- `POST /farms/` - إنشاء مزرعة جديدة
- `GET /farms/` - قائمة المزارع
- `GET /farms/{id}` - تفاصيل مزرعة

### الحقول (Fields)
- `POST /fields/` - إنشاء حقل جديد
- `GET /fields/` - قائمة الحقول
- `GET /fields/{id}` - تفاصيل حقل

### صور الأقمار الصناعية
- `POST /satellite/images/fetch` - جلب صور جديدة
- `GET /satellite/images/` - قائمة الصور

### تحليل NDVI
- `POST /satellite/ndvi/process` - معالجة NDVI
- `GET /satellite/ndvi/` - قائمة النتائج
- `GET /satellite/ndvi/{result_id}` - تفاصيل نتيجة
- `GET /satellite/ndvi/tiles/{result_id}/{z}/{x}/{y}.png` - XYZ Tiles
- `GET /satellite/ndvi/legend.png` - مفتاح الألوان
- `GET /satellite/ndvi/timeline` - الجدول الزمني

### كشف التغيرات
- `POST /satellite/change/process` - معالجة التغيرات
- `GET /satellite/change/` - قائمة النتائج

### التنبيهات
- `GET /alerts/` - قائمة التنبيهات

### الطقس
- `GET /weather/current` - الطقس الحالي
- `GET /weather/daily` - توقعات يومية
- `GET /weather/history` - بيانات تاريخية

### التقارير
- `GET /reports/weekly` - تقرير أسبوعي

## قاعدة البيانات

### الجداول الرئيسية
- `farms` - المزارع
- `fields` - الحقول (مع دعم PostGIS)
- `satellite_images` - صور الأقمار الصناعية
- `ndvi_results` - نتائج تحليل NDVI
- `change_detection_results` - نتائج كشف التغيرات
- `alerts` - التنبيهات

## تطبيق Flutter

### التثبيت
```bash
cd ui/flutter
flutter pub get
```

### التشغيل
```bash
flutter run
```

### الإعدادات
قم بتعديل عنوان API في `lib/main.dart`:
```dart
ApiService(baseUrl: 'http://YOUR_SERVER_IP:8000')
```

## المساهمة

هذا المشروع مفتوح للتطوير والتحسين. يمكنك المساهمة من خلال:
- إضافة ميزات جديدة
- إصلاح الأخطاء
- تحسين الأداء
- تطوير واجهة الويب

## الترخيص

هذا المشروع مطور لأغراض تعليمية وبحثية.

## الدعم

للحصول على الدعم أو الإبلاغ عن مشاكل، يرجى فتح issue في المستودع.

---

**ملاحظة:** تم تطوير هذا المشروع بواسطة Manus AI
