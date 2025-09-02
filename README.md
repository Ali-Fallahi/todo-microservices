پروژه میکروسرویس To-Do: قدم اول یک جنگو دولوپر
این پروژه یک نقشه راه ساده و کاربردی برای توسعه‌دهندگان جنگو است که می‌خواهند اولین قدم را برای ساخت اپلیکیشن با معماری میکروسرویس بردارند.

ما یک اپلیکیشن ساده To-Do را به چند سرویس مستقل تقسیم کرده‌ایم که هر کدام وظیفه مشخصی دارند و با ابزارهای مدرن با یکدیگر صحبت می‌کنند.

🏗️ معماری کلی
سیستم ما از چند قطعه اصلی تشکیل شده که هر کدام در یک کانتینر داکر مجزا اجرا می‌شوند:

graph TD
    subgraph Browser
        F[Frontend - React]
    end

    subgraph Backend
        G[API Gateway - FastAPI]
        U[User Service - Django]
        T[Todo Service - Django]
    end

    subgraph Tools
        K[Kafka]
        E[ELK Stack]
    end

    F -- Request --> G
    G -- Routes to --> U & T
    U -- Event --> K
    T -- Listens to --> K
    G & U & T -- Logs --> E

جریان کار به زبان ساده:

کاربر از طریق رابط کاربری (React) یک درخواست ارسال می‌کند.

درخواست به API Gateway می‌رسد. این دروازه، نگهبان و راهنمای اصلی سیستم ماست.

Gateway تصمیم می‌گیرد که درخواست مربوط به کدام سرویس است (مثلاً درخواست لاگین به User Service و درخواست افزودن تسک به Todo Service می‌رود).

اگر سرویس‌ها نیاز به صحبت غیرمستقیم با هم داشته باشند (مثلاً وقتی یک کاربر حذف می‌شود)، از کافکا (Kafka) به عنوان یک پیام‌رسان استفاده می‌کنند.

تمام اتفاقات و لاگ‌ها در ELK Stack به صورت متمرکز ذخیره می‌شوند تا بتوانیم سیستم را رصد کنیم.

🛠️ تکنولوژی‌ها
بک‌اند: Django, FastAPI

فرانت‌اند: React

دیتابیس: PostgreSQL

زیرساخت: Docker, Docker Compose, Kafka, ELK Stack

احراز هویت: JWT

🚀 راهنمای راه‌اندازی
برای اجرای پروژه، فقط به Docker و Docker Compose نیاز دارید.

۱. کلون کردن پروژه
```
git clone Ali-Fallahi/todo-microservices-django
```
۲. ساخت فایل‌های .env (مهم‌ترین بخش!)
برای هر سرویس بک‌اند، یک فایل .env برای نگهداری اطلاعات حساس نیاز داریم.

۱. برای User Service: یک فایل در مسیر backend/user-service/.env بسازید:
```
SECRET_KEY=your-strong-secret-key-for-user-service
JWT_SIGNING_KEY=a-very-secret-key-that-must-be-the-same
POSTGRES_DB=user_db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=user_db_postgres
```
۲. برای Todo Service: یک فایل در مسیر backend/todo-service/.env بسازید:
```
SECRET_KEY=your-strong-secret-key-for-todo-service
POSTGRES_DB=todo_db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=todo_db_postgres
```
۳. برای API Gateway: یک فایل در مسیر backend/api-gateway/.env بسازید:
```
JWT_SIGNING_KEY=a-very-secret-key-that-must-be-the-same
```
⚠️ نکته بسیار مهم
مقدار JWT_SIGNING_KEY باید در user-service و api-gateway دقیقا یکسان باشد. چرا؟ چون user-service با این کلید توکن را امضا (Sign) می‌کند و api-gateway با همان کلید، امضا را بررسی (Verify) می‌کند تا از معتبر بودن توکن مطمئن شود.

۳. اجرا با Docker Compose
در ریشه اصلی پروژه، دستور زیر را اجرا کنید:
```
docker-compose up --build
```
پس از چند دقیقه، تمام سرویس‌ها آماده به کار هستند:

اپلیکیشن: http://localhost:3000
```
API Gateway: http://localhost:8000

Kafka UI (رابط کاربری کافکا): http://localhost:8080

Kibana (رابط کاربری لاگ‌ها): http://localhost:15601
```
🔬 نحوه استفاده از API
می‌توانید از طریق ابزارهایی مانند Postman یا cURL با API تعامل کنید.

۱. ثبت‌نام کاربر جدید
یک درخواست POST به API Gateway ارسال کنید تا کاربر جدیدی در user-service ساخته شود.
```
curl -X POST http://localhost:8000/auth/register/ \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "email": "test@example.com", "password": "strongpassword123"}'
```
۲. دریافت توکن (لاگین)
با نام کاربری و رمز عبور خود، یک توکن دسترسی (Access Token) دریافت کنید.
```
curl -X POST http://localhost:8000/auth/token/ \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "strongpassword123"}'
```
در پاسخ، یک access توکن دریافت خواهید کرد که برای مراحل بعدی نیاز است.

۳. حذف کاربر
برای تست کردن سناریوی کافکا، می‌توانید کاربری که ساختید را حذف کنید. توکن دریافتی از مرحله قبل را در هدر Authorization قرار دهید.
```
curl -X DELETE http://localhost:8000/auth/profile/ \
-H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```
پس از اجرای این دستور، user-service کاربر را حذف کرده و یک رویداد به کافکا ارسال می‌کند. todo-service این رویداد را دریافت کرده و تسک‌های مربوط به این کاربر را (اگر وجود داشته باشد) حذف می‌کند.

🧠 مفاهیم کلیدی در این پروژه
API Gateway
این سرویس دروازه اصلی ورود به سیستم ماست:

نقطه ورود واحد: فرانت‌اند فقط با Gateway صحبت می‌کند، نه با تک تک سرویس‌ها.

مسیریابی هوشمند: درخواست‌ها را بر اساس آدرس به سرویس مناسب هدایت می‌کند.

امنیت متمرکز: توکن‌های JWT را قبل از رسیدن درخواست به سرویس‌های داخلی، اعتبارسنجی می‌کند.

ارتباط رویداد-محور با Kafka
سرویس‌ها نباید مستقیماً با هم صحبت کنند. به جای آن، از یک پیام‌رسان استفاده می‌کنند:

مثال: وقتی کاربری حذف می‌شود، user-service یک پیام "کاربر X حذف شد" در کافکا منتشر می‌کند.

todo-service که به این نوع پیام‌ها گوش می‌دهد، آن را دریافت کرده و تمام تسک‌های کاربر X را حذف می‌کند.

لاگینگ متمرکز با ELK
به جای چک کردن لاگ‌ها در چندین ترمینال، همه چیز در یک جا جمع می‌شود:

هر سرویس لاگ‌های خود را به Logstash می‌فرستد.

Logstash آن‌ها را پردازش و در Elasticsearch ذخیره می‌کند.

ما با Kibana می‌توانیم به راحتی همه لاگ‌ها را جستجو و تحلیل کنیم.

🤝 مشارکت
این پروژه با هدف آموزش ساخته شده است. اگر پیشنهادی برای بهبود دارید، لطفاً یک Issue باز کنید یا یک Pull Request ارسال کنید.
