from django.urls import path
from . import views

app_name = 'gifts'

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('gift/<int:gift_id>/like/', views.toggle_like, name='toggle_like'),
    path('gift/<int:gift_id>/save/', views.toggle_save, name='toggle_save'),
    path('gift/<int:gift_id>/', views.gift_detail, name='gift_detail'),
    path('gift/<int:gift_id>/comment/', views.add_comment, name='add_comment'),
]
