"""Demo ma'lumotlar yaratish skripti"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from members.models import SubscriptionPlan, Member, Subscription
from datetime import date, timedelta

plans = [
    SubscriptionPlan(name="1 oylik", duration_days=30, price=150000, description="Standart oylik abonement"),
    SubscriptionPlan(name="3 oylik", duration_days=90, price=400000, description="3 oylik tejamli taklif"),
    SubscriptionPlan(name="6 oylik", duration_days=180, price=700000, description="Yarim yillik abonement"),
    SubscriptionPlan(name="1 yillik", duration_days=365, price=1200000, description="Yillik abonement"),
]
SubscriptionPlan.objects.all().delete()
for p in plans:
    p.save()

print("Abonement turlari yaratildi.")

members_data = [
    ("Alisher Karimov", "+998901234567", "M"),
    ("Malika Yusupova", "+998901234568", "F"),
    ("Bobur Toshmatov", "+998901234569", "M"),
    ("Nilufar Hasanova", "+998901234570", "F"),
    ("Jasur Mirzayev", "+998901234571", "M"),
]

Member.objects.all().delete()
today = date.today()
plan1 = SubscriptionPlan.objects.get(name="1 oylik")
plan3 = SubscriptionPlan.objects.get(name="3 oylik")

for i, (name, phone, gender) in enumerate(members_data):
    m = Member.objects.create(full_name=name, phone=phone, gender=gender)
    plan = plan1 if i % 2 == 0 else plan3
    start = today - timedelta(days=i * 5)
    sub = Subscription(member=m, plan=plan, start_date=start,
                       end_date=start + timedelta(days=plan.duration_days),
                       paid_amount=plan.price)
    sub.save()

print("Demo a'zolar yaratildi.")
print("\nAdmin yaratish uchun: python manage.py createsuperuser")
print("Serverni ishga tushurish: python manage.py runserver")
