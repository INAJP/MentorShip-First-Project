# OpenLibrary Book Fetcher 📚

اسکریپت پایتونی ساده برای دریافت اطلاعات کتاب از API عمومی [OpenLibrary](https://openlibrary.org/dev/docs/api/subjects)، فیلتر کردن کتاب‌های منتشرشده بعد از سال ۲۰۰۰ میلادی و ذخیره‌ی خروجی مرتب‌شده در یک فایل CSV.

## قابلیت‌ها

- دریافت اطلاعات کتاب‌ها از طریق [Subjects API](https://openlibrary.org/dev/docs/api/subjects) خود OpenLibrary.
- فیلتر کردن و نگه‌داشتن فقط کتاب‌هایی که سال انتشار اول (`first_publish_year`) آن‌ها بعد از سال ۲۰۰۰ است.
- ذخیره‌ی نتیجه در فایل `books_after_2000.csv`، مرتب‌شده بر اساس سال انتشار.
- استفاده از کتابخانه‌ی `requests`.

## پیش‌نیازها

- پایتون نسخه‌ی ۳.۸ یا بالاتر
- کتابخانه‌ی `requests`

## نصب و اجرا

۱. کلون کردن ریپازیتوری:
```bash
git clone <REPO_URL>
cd openlibrary-books

```

۲. ساخت محیط مجازی (اختیاری):

```bash
python -m venv venv
venv\Scripts\activate

```

۳. نصب وابستگی‌ها:

```bash
pip install -r requirements.txt

```

۴. اجرای اسکریپت:

```bash
python book_fetcher.py

```

پس از اجرا، فایل `books_after_2000.csv` در همان پوشه ساخته می‌شود.

## نمونه خروجی فایل (Sample Output)

> نکته: برای رعایت استانداردهای کنترل نسخه، فایل خروجی `CSV` در `.gitignore` قرار گرفته و آپلود نمی‌شود. در جدول زیر، ۳ سطر اول از دیتای استخراج‌شده به عنوان نمونه قرار داده شده است:

| title | author | first_publish_year | edition_count | openlibrary_key |
| --- | --- | --- | --- | --- |
| Altered Carbon | Richard K. Morgan | 2002 | 28 | /works/OL29914687W |
| Broken Angels | Richard K. Morgan | 2003 | 16 | /works/OL5730139W |
| Market Forces | Richard K. Morgan | 2004 | 11 | /works/OL5730140W |

## تغییر تنظیمات

در ابتدای فایل `book_fetcher.py` چند متغیر برای شخصی‌سازی وجود دارد:

| متغیر | توضیح |
| --- | --- |
| `SUBJECT` | موضوع کتاب‌ها (مثلاً `cyberpunk`, `science`, `history`) |
| `BOOK_LIMIT` | تعداد کتاب‌هایی که از API درخواست می‌شود |
| `MIN_PUBLISH_YEAR` | سال مبنا برای فیلتر کردن |
| `OUTPUT_CSV_PATH` | مسیر فایل خروجی CSV |
| `REQUEST_TIMEOUT_SECONDS` | حداکثر زمان انتظار برای دریافت پاسخ از API |

## ساختار خروجی CSV

| ستون | توضیح |
| --- | --- |
| `title` | عنوان کتاب |
| `author` | نام نویسنده(ها) |
| `first_publish_year` | سال اولین انتشار |
| `edition_count` | تعداد نسخه‌های ثبت‌شده در OpenLibrary |
| `openlibrary_key` | شناسه‌ی یکتای کتاب در OpenLibrary |

## ساختار پروژه

```text
openlibrary-books/
├── book_fetcher.py
├── requirements.txt
└── README.md

```

## منبع داده

تمام اطلاعات از API عمومی و رایگان OpenLibrary دریافت می‌شود و نیازی به کلید API ندارد:
https://openlibrary.org/dev/docs/api/subjects

```
