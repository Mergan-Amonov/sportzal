from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('members/', views.member_list, name='member_list'),
    path('members/new/', views.member_create, name='member_create'),
    path('members/<int:pk>/', views.member_detail, name='member_detail'),
    path('members/<int:pk>/edit/', views.member_edit, name='member_edit'),
    path('members/<int:pk>/delete/', views.member_delete, name='member_delete'),
    path('members/<int:member_pk>/subscribe/', views.subscription_create, name='subscription_create'),
    path('subscriptions/<int:pk>/delete/', views.subscription_delete, name='subscription_delete'),
    path('plans/', views.plan_list, name='plan_list'),
    path('plans/new/', views.plan_create, name='plan_create'),
    path('plans/<int:pk>/edit/', views.plan_edit, name='plan_edit'),
    path('plans/<int:pk>/delete/', views.plan_delete, name='plan_delete'),
]
