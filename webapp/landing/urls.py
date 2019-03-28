from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('big-picture', views.big_picture, name='big_picture'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
