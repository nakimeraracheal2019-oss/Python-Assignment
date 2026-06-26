from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('home/', views.home, name='home'),
    path('threats/', views.cyber_threats, name='threats'),
    path('forensics/', views.forensics, name='forensics'),
    path('contact/', views.contact, name='contact'),
    path('create/', views.create_post, name='create'),
    path('edit/<int:pk>/', views.edit_post, name='edit_post'),  # ✅ added
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
