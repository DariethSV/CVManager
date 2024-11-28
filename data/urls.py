
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('get_data/',views.get_data, name="get_data"),
    path('check_customer_resume/',views.check_customer_resume, name="check_customer_resume"),
    path('upload/',views.upload_resume, name="upload_resume"),
    path('match_inputs_info_resume/',views.match_inputs_info_resume, name="match_inputs_info_resume"), 
    path('strategy_function/',views.strategy_function, name="strategy_function"), 
    path('match_inputs_info_resume_uploaded/',views.match_inputs_info_resume_uploaded, name="match_inputs_info_resume_uploaded"), 
    path('get_company_name/',views.get_company_name, name="get_company_name"), 


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)