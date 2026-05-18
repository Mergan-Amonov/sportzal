from django.db import models
from django.utils import timezone
from datetime import timedelta


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    duration_days = models.PositiveIntegerField(verbose_name="Muddat (kun)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi (so'm)")
    description = models.TextField(blank=True, verbose_name="Tavsif")

    class Meta:
        verbose_name = "Abonement turi"
        verbose_name_plural = "Abonement turlari"

    def __str__(self):
        return f"{self.name} ({self.duration_days} kun)"


class Member(models.Model):
    GENDER_CHOICES = [
        ('M', 'Erkak'),
        ('F', 'Ayol'),
    ]
    full_name = models.CharField(max_length=200, verbose_name="To'liq ism")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Jins")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan sana")
    photo = models.ImageField(upload_to='members/', null=True, blank=True, verbose_name="Rasm")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "A'zo"
        verbose_name_plural = "A'zolar"
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

    @property
    def active_subscription(self):
        return self.subscriptions.filter(
            is_active=True,
            end_date__gte=timezone.now().date()
        ).first()

    @property
    def is_active(self):
        return self.active_subscription is not None


class Subscription(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='subscriptions', verbose_name="A'zo")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, verbose_name="Abonement turi")
    start_date = models.DateField(verbose_name="Boshlanish sanasi")
    end_date = models.DateField(verbose_name="Tugash sanasi")
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="To'langan summa")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    notes = models.TextField(blank=True, verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Abonement"
        verbose_name_plural = "Abonementlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.member.full_name} - {self.plan.name} ({self.end_date})"

    def save(self, *args, **kwargs):
        if not self.pk and self.start_date and self.plan_id:
            plan = SubscriptionPlan.objects.get(pk=self.plan_id)
            self.end_date = self.start_date + timedelta(days=plan.duration_days)
        super().save(*args, **kwargs)

    @property
    def days_left(self):
        today = timezone.now().date()
        if self.end_date >= today:
            return (self.end_date - today).days
        return 0

    @property
    def is_expired(self):
        return self.end_date < timezone.now().date()

    @property
    def status_class(self):
        days = self.days_left
        if self.is_expired:
            return 'danger'
        elif days <= 3:
            return 'warning'
        return 'success'
