# Black4Me Automation Bot

1. انسخ المستودع:
   git clone https://github.com/black4me/black4me-automation.git
   cd black4me-automation

2. أنشئ .env من .env.example واملأ المفاتيح.

3. شغّل محلياً:
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload

4. انشر على Railway مجاناً:
   - افتح https://railway.app
   - New Project → Deploy from GitHub repo
   - Variables → أضف المتغيرات من .env
   - بعد النجاح خذ الرابط: https://xxx.up.railway.app

5. في لوحة Fourthwall:
   Settings → Webhooks → Add:
   URL: https://xxx.up.railway.app/webhook/fourthwall
   Events: ORDER_PLACED (اختر فقط ما تحتاج)
   Secret: نفس FW_WEBHOOK_SECRET في .env

6. اختبر: اشتري منتجك بنفسك → تأكد من وصول البريد خلال دقيقة.
