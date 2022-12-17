from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [

    path('', login_view, name='login'),
    path('overview', overview_view, name='overview'),
    path('registration', registration_view, name='registration'),
    path('introduction', introduction_view, name='introduction'),
    path('change-password', change_password_view, name='change-password'),
    path('logout', logout_view, name='logout'),

] + static(settings.AVA_URL, document_root=settings.AVA_ROOT)
