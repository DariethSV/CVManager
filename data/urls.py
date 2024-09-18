
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('save_data/', views.save_data, name='save_data'),
    path('get_data/',views.get_data, name="get_data"),
    path('check_customer_resume/',views.check_customer_resume, name="check_customer_resume"),
    path('upload/',views.upload_resume, name="upload_resume")

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)