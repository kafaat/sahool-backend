# تشغيل مشروع سهول (النسخة النهائية Static)

## 1) تشغيل الباك-اند
```bash
cp .env.example .env
# عبّي CDSE_USER و CDSE_PASS
docker compose up --build -d
docker compose exec api alembic revision --autogenerate -m "init"
docker compose exec api alembic upgrade head
```
افتح:
http://localhost:8000/docs

ملفات NDVI/PNG/Tiles سوف تظهر تحت:
http://localhost:8000/storage/...

## 2) Flutter
اتبع ui/flutter/README.md ثم أضف الحزم من pubspec_additions.txt.

## 3) Web
اتبع ui/web/README.md ثم أضف الحزم من package_additions.txt.
