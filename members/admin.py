from django.contrib import admin
from .models import Member, SubscriptionPlan, Subscription


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_days', 'price']


class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 0
    readonly_fields = ['end_date', 'created_at']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'gender', 'is_active']
    search_fields = ['full_name', 'phone']
    inlines = [SubscriptionInline]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['member', 'plan', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'plan']
    search_fields = ['member__full_name']
