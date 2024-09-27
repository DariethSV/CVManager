
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create_resume/', views.create_resume, name='create_resume'),
    path('save_resume/', views.save_resume, name='save_resume'),
    

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)