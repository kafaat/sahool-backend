# سهول - نسخة موحّدة V2

هذا المشروع يجمع:
- الباك-اند (FastAPI + PostGIS + Celery + Sentinel + NDVI + Tiles + تنبيهات + طقس مجاني)
- تطبيق Flutter بنمط Farmonaut
- تطبيق ويب React بنفس النمط

## تشغيل الباك-اند
1) انسخ `.env.example` إلى `.env` واملأ بيانات CDSE.
2) شغّل:
   docker compose up --build -d
3) أنشئ الجداول:
   docker compose exec api alembic revision --autogenerate -m "init"
   docker compose exec api alembic upgrade head
4) Swagger:
   http://localhost:8000/docs

## ملاحظات UI
- Flutter: أضف الحزم المذكورة في `ui/flutter/pubspec_additions.txt`
  ثم استخدم صفحة `FieldDetailPage` لعرض NDVI وتقرير PDF.
- Web: أضف الحزم في `ui/web/package_additions.txt`
  وأضف Route لصفحة FieldDetail عندك حسب هيكل تطبيقك.

## مسارات API المستخدمة
- /fields/
- /satellite/images/fetch
- /satellite/ndvi/process
- /satellite/ndvi/tiles/{result_id}/{z}/{x}/{y}.png
- /satellite/ndvi/timeline?field_id=...
- /satellite/change/process
- /alerts/?field_id=...
- /weather/current?lat=...&lon=...
- /reports/weekly?field_id=...
