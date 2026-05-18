import hashlib
import hmac
import time
from django.conf import settings
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

User = get_user_model()


def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'account/login.html', {
        'telegram_bot_name': settings.TELEGRAM_BOT_NAME,
    })


def logout_view(request):
    logout(request)
    return redirect('login')


def telegram_callback(request):
    """
    Verifies Telegram Login Widget data using HMAC-SHA256.
    Telegram sends: id, first_name, last_name, username, photo_url, auth_date, hash
    """
    data = request.GET.dict()
    received_hash = data.pop('hash', None)

    if not received_hash:
        return redirect('login')

    # Build check string: sorted key=value pairs joined by \n
    check_string = '\n'.join(f'{k}={v}' for k, v in sorted(data.items()))

    # Key = SHA256 of bot token
    secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()
    computed = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(computed, received_hash):
        return render(request, 'account/login.html', {
            'error': "Telegram ma'lumotlari tasdiqlanmadi.",
            'telegram_bot_name': settings.TELEGRAM_BOT_NAME,
        })

    # Auth date must be within 24 hours
    auth_age = time.time() - int(data.get('auth_date', 0))
    if auth_age > 86400:
        return render(request, 'account/login.html', {
            'error': "Telegram sessiyasi muddati o'tgan. Qayta urinib ko'ring.",
            'telegram_bot_name': settings.TELEGRAM_BOT_NAME,
        })

    tg_id    = data['id']
    username = data.get('username', f'tg_{tg_id}')
    first    = data.get('first_name', '')
    last     = data.get('last_name', '')

    # Find or create user by Telegram ID stored in username field
    tg_username = f'tg_{tg_id}'
    user, created = User.objects.get_or_create(
        username=tg_username,
        defaults={'first_name': first, 'last_name': last},
    )
    if not created:
        user.first_name = first
        user.last_name  = last
        user.save(update_fields=['first_name', 'last_name'])

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('dashboard')
