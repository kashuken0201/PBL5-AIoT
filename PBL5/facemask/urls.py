from django.urls import path 
from .views import *

urlpatterns = [
    
    path('', face_view, name='face'),
    path('stream', stream_view, name='stream'),
    path('capture', capture_view, name='capture'),
    path('detect', detect_view, name='detect'),
    path('log', log_view, name='log'),

]