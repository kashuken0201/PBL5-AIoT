from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [

    path('', student_list_view, name='student-list'),
    path('create', create_view, name='create'),
    path('<int:id>/update', update_view, name='update'),
    path('<int:id>/delete', delete_view, name='delete'),

] + static(settings.AVA_URL, document_root=settings.AVA_ROOT)
