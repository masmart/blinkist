<div align="center">
  <img src="static/images/logo.png" alt="Blinkist logo" width="180">

  # Blinkist فارسی

  **خلاصه‌ی کتاب‌های ارزشمند؛ کوتاه، خواندنی و همیشه در دسترس.**

  یک وب‌اپلیکیشن فارسی برای کشف، مطالعه و ذخیره‌ی خلاصه‌ی کتاب‌ها؛ ساخته‌شده با Flask و PostgreSQL.

  ![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
  ![Flask](https://img.shields.io/badge/Flask-2.2-000000?logo=flask&logoColor=white)
  ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-4169E1?logo=postgresql&logoColor=white)
  ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3-06B6D4?logo=tailwindcss&logoColor=white)
</div>

---

## درباره‌ی پروژه

Blinkist فارسی تجربه‌ای ساده و راست‌به‌چپ برای مرور ایده‌های مهم کتاب‌ها فراهم می‌کند. کاربران می‌توانند کتاب‌ها را بر اساس دسته‌بندی و نویسنده پیدا کنند، خلاصه‌ها را بخوانند و کتاب‌های موردعلاقه‌شان را در کتابخانه شخصی ذخیره کنند. پروژه همچنین یک پنل مدیریت محافظت‌شده برای مدیریت محتوا دارد.

## امکانات

- 📚 نمایش تازه‌ترین کتاب‌ها، دسته‌بندی‌ها و پیشنهادهای روز
- 🔎 جست‌وجوی کتاب و نویسنده
- 💡 مطالعه‌ی ایده‌ها و خلاصه‌ی هر کتاب در نمای Reader
- 🔖 نشان‌کردن کتاب‌ها و نگهداری آن‌ها در کتابخانه‌ی شخصی
- 👤 ثبت‌نام، ورود و داشبورد کاربری
- ✍️ مدیریت کتاب‌ها، نویسندگان، دسته‌بندی‌ها، ایده‌ها و فایل‌های صوتی
- 🗂️ ذخیره‌سازی اختیاری فایل‌ها روی MinIO
- 🛡️ محافظت CSRF، کنترل دسترسی ادمین و اعتبارسنجی آپلودها
- 🇮🇷 رابط فارسی و راست‌به‌چپ

## فناوری‌ها

| بخش | ابزارها |
| --- | --- |
| Backend | Python، Flask، SQLAlchemy |
| Database | PostgreSQL، Alembic / Flask-Migrate |
| Frontend | Jinja2، Tailwind CSS، JavaScript |
| Authentication | Flask-Login |
| Object storage | MinIO (اختیاری) |
| Tests | Pytest |

## راه‌اندازی سریع در Windows

### پیش‌نیازها

- Python 3.11
- PostgreSQL 15 یا جدیدتر
- Node.js 18 یا جدیدتر؛ فقط برای بازسازی فایل‌های CSS

### ۱. ساخت محیط مجازی

```powershell
py -3.11 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### ۲. نصب وابستگی‌ها

```powershell
python -m pip install -r requirements.txt
npm install
```

### ۳. تنظیم متغیرهای محیطی

فایل نمونه را کپی کنید و مقادیر آن را با اطلاعات محیط خودتان جایگزین کنید:

```powershell
Copy-Item .env.example .env
```

برای اجرای سریع در همان پنجره‌ی PowerShell، حداقل این مقادیر را تنظیم کنید:

```powershell
$env:SECRET_KEY = "یک-رشته-تصادفی-و-طولانی"
$env:DATABASE_URL = "postgresql://USER:PASSWORD@127.0.0.1:5432/blinkist"
$env:ADMIN_EMAILS = "admin@example.com"
```

> اگر رمز دیتابیس دارای `@`، `#`، `%` یا `:` است، آن را URL-encode کنید. هیچ رمز یا کلید واقعی را در Git ثبت نکنید.

### ۴. آماده‌سازی دیتابیس

ابتدا دیتابیس خالی `blinkist` را بسازید. ساختار دیتابیس فقط از migrationها ایجاد می‌شود و دادهٔ نمونه اختیاری است:

```powershell
python -m flask --app app db upgrade
python -m seeds.seed
```

فایل `public.sql` صرفاً snapshot قدیمی محتواست و دیگر برای ساخت یا ارتقای schema استفاده نمی‌شود.

### ۵. اجرای برنامه

```powershell
python app.py
```

حالا مرورگر را روی [http://127.0.0.1:5000](http://127.0.0.1:5000) باز کنید. 🎉

## توسعه و تست

برای بازسازی خودکار Tailwind هنگام ویرایش قالب‌ها:

```powershell
npm run watch-css
```

برای اجرای تست‌ها:

```powershell
python -m pytest -v
```

خروجی مورد انتظار نسخه‌ی فعلی:

```text
3 passed
```

## ساختار پروژه

```text
blinkist/
├── app.py              # نقطه‌ی ورود برنامه
├── config.py           # تنظیمات و اتصال سرویس‌ها
├── controllers/        # منطق درخواست‌ها
├── models/             # مدل‌های دیتابیس
├── routes/             # مسیرها و Blueprintها
├── templates/          # رابط کاربری Jinja2
├── static/             # CSS، JavaScript، فونت و تصاویر
├── migrations/         # نسخه‌بندی ساختار دیتابیس
└── tests/              # تست‌های خودکار
```

## نکات امنیتی

- فایل `.env`، رمز دیتابیس و کلیدهای MinIO را commit نکنید.
- دسترسی پنل مدیریت فقط برای ایمیل‌های موجود در `ADMIN_EMAILS` فعال است.
- برای محیط production از یک WSGI server مناسب استفاده کنید؛ سرور داخلی Flask فقط برای توسعه است.
- هر کلیدی که قبلاً وارد تاریخچه‌ی Git شده باید تعویض شود؛ حذف آن از فایل فعلی کافی نیست.

## مشارکت

پیشنهادها و بهبودها خوش‌آمدند. برای تغییرات بزرگ، ابتدا یک Issue باز کنید و هدف تغییر را توضیح دهید؛ سپس یک branch مجزا بسازید و Pull Request بفرستید.

---

<div align="center">
  ساخته‌شده برای دوست‌داران کتاب و یادگیری 📖
</div>
