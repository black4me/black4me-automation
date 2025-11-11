import os, sendgrid
from sendgrid.helpers.mail import Mail
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Lead, Message, engine

sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_NAME  = os.getenv("FROM_NAME")
UPSELL_URL = f"https://black4me.com/products/{os.getenv('UPSELL_PRODUCT_ID')}?coupon={os.getenv('UPSELL_COUPON')}&order_id={{order_id}}"

def add_lead(data: dict):
    with Session(engine) as db:
        lead = Lead(
            fw_order_id = data["order"]["id"],
            email = data["order"]["customer"]["email"],
            name  = data["order"]["customer"]["first_name"],
            product = data["order"]["line_items"][0]["product_name"],
            amount  = float(data["order"]["total"]),
        )
        # تحديد VIP
        if lead.amount >= float(os.getenv("VIP_THRESHOLD")):
            lead.tags += ",vip"
            lead.status = "vip"
        db.add(lead); db.commit(); db.refresh(lead)
        return lead

def send_email(to, subject, html):
    mail = Mail(
        from_email=(FROM_EMAIL, FROM_NAME),
        to_emails=to,
        subject=subject,
        html_content=html
    )
    sg.send(mail)

def welcome_and_upsell(lead: Lead, download_url: str):
    subject = f"{lead.name}، طلبك جاهز… وهل تريد النسخة الكاملة بخصم 40٪؟"
    body = f"""
مرحباً {lead.name},<br><br>
شكراً لشرائك «{lead.product}».<br>
رابط التنزيل (ينتهي خلال 72 ساعة):<br>
<a href=\"{download_url}\">اضغط هنا</a><br><br>
🎁 عرض الترقية الحصري خلال 24 ساعة فقط:<br>
«باقة المحترفين» (قيمتها 99$) الآن بـ 59$ فقط.<br>
<a href=\"{UPSELL_URL.format(order_id=lead.fw_order_id)}\">احصل عليها الآن</a><br>
أسئلة؟ فقط اضغط «رد» على هذا البريد.<br>
فريق Black4Me
"""
    send_email(lead.email, subject, body)
    with Session(engine) as db:
        lead.tags += ",upsell_sent"
        db.add(Message(lead_id=lead.id, channel="email", subject=subject, body=body,
                       scheduled_at=datetime.utcnow(), sent_at=datetime.utcnow()))
        db.commit()

def handle_vip(lead: Lead):
    subject = "مرحباً بك في نادي Black4Me Pro"
    body = f"""
أهلاً {lead.name},<br>
لأنك اخترت منتجنا الأعلى قيمة، ندعوك لحجز استشارة 20 دقيقة مجانية مع فريقنا.<br>
<a href=\"https://calendly.com/black4me/vip\">احجز موعدك المجاني</a><br>
أيضاً تلقيت كوبون خصم 50٪ على أي منتج مستقبلاً: كود <b>VIP50</b><br>
نحن في خدمتك دائماً.
"""
    send_email(lead.email, subject, body)
