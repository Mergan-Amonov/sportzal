from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from .models import Member, SubscriptionPlan, Subscription
from .forms import MemberForm, SubscriptionForm, SubscriptionPlanForm


@login_required
def dashboard(request):
    today = timezone.now().date()
    total_members = Member.objects.count()
    active_members = Member.objects.filter(
        subscriptions__is_active=True,
        subscriptions__end_date__gte=today
    ).distinct().count()
    expiring_soon = Subscription.objects.filter(
        is_active=True,
        end_date__gte=today,
        end_date__lte=today + timezone.timedelta(days=3)
    ).select_related('member', 'plan')
    expired = Subscription.objects.filter(
        is_active=True,
        end_date__lt=today
    ).count()
    recent_subscriptions = Subscription.objects.select_related('member', 'plan').order_by('-created_at')[:5]
    context = {
        'total_members': total_members,
        'active_members': active_members,
        'expiring_soon': expiring_soon,
        'expired_count': expired,
        'recent_subscriptions': recent_subscriptions,
    }
    return render(request, 'members/dashboard.html', context)


@login_required
def member_list(request):
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    today = timezone.now().date()
    members = Member.objects.all()
    if q:
        members = members.filter(Q(full_name__icontains=q) | Q(phone__icontains=q))
    if status == 'active':
        members = members.filter(
            subscriptions__is_active=True,
            subscriptions__end_date__gte=today
        ).distinct()
    elif status == 'inactive':
        active_ids = Member.objects.filter(
            subscriptions__is_active=True,
            subscriptions__end_date__gte=today
        ).values_list('id', flat=True)
        members = members.exclude(id__in=active_ids)
    return render(request, 'members/member_list.html', {'members': members, 'q': q, 'status': status})


@login_required
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    subscriptions = member.subscriptions.select_related('plan').order_by('-created_at')
    return render(request, 'members/member_detail.html', {'member': member, 'subscriptions': subscriptions})


@login_required
def member_create(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save()
            messages.success(request, f"'{member.full_name}' muvaffaqiyatli qo'shildi.")
            return redirect('member_detail', pk=member.pk)
    else:
        form = MemberForm()
    return render(request, 'members/member_form.html', {'form': form, 'title': "Yangi a'zo"})


@login_required
def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Ma'lumotlar yangilandi.")
            return redirect('member_detail', pk=pk)
    else:
        form = MemberForm(instance=member)
    return render(request, 'members/member_form.html', {'form': form, 'title': "A'zoni tahrirlash"})


@login_required
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, f"'{member.full_name}' o'chirildi.")
        return redirect('member_list')
    return render(request, 'members/confirm_delete.html', {'object': member, 'type': "a'zo"})


@login_required
def subscription_create(request, member_pk):
    member = get_object_or_404(Member, pk=member_pk)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.member = member
            sub.save()
            messages.success(request, "Abonement qo'shildi.")
            return redirect('member_detail', pk=member_pk)
    else:
        form = SubscriptionForm(initial={'start_date': timezone.now().date()})
    return render(request, 'members/subscription_form.html', {'form': form, 'member': member})


@login_required
def subscription_delete(request, pk):
    sub = get_object_or_404(Subscription, pk=pk)
    member_pk = sub.member.pk
    if request.method == 'POST':
        sub.delete()
        messages.success(request, "Abonement o'chirildi.")
        return redirect('member_detail', pk=member_pk)
    return render(request, 'members/confirm_delete.html', {'object': sub, 'type': 'abonement'})


@login_required
def plan_list(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'members/plan_list.html', {'plans': plans})


@login_required
def plan_create(request):
    if request.method == 'POST':
        form = SubscriptionPlanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Yangi tur qo'shildi.")
            return redirect('plan_list')
    else:
        form = SubscriptionPlanForm()
    return render(request, 'members/plan_form.html', {'form': form, 'title': "Yangi tur"})


@login_required
def plan_edit(request, pk):
    plan = get_object_or_404(SubscriptionPlan, pk=pk)
    if request.method == 'POST':
        form = SubscriptionPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, "Tur yangilandi.")
            return redirect('plan_list')
    else:
        form = SubscriptionPlanForm(instance=plan)
    return render(request, 'members/plan_form.html', {'form': form, 'title': "Turni tahrirlash"})


@login_required
def plan_delete(request, pk):
    plan = get_object_or_404(SubscriptionPlan, pk=pk)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, "Tur o'chirildi.")
        return redirect('plan_list')
    return render(request, 'members/confirm_delete.html', {'object': plan, 'type': 'abonement turi'})
