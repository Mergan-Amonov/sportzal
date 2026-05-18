from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from members import auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('login/', auth_views.login_page, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('auth/telegram/', auth_views.telegram_callback, name='telegram_callback'),
    path('', include('members.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
