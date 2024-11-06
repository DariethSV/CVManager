
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create_resume/', views.create_resume, name='create_resume'),
    path('save_resume/', views.save_resume, name='save_resume'),
    path('select_resume/', views.select_resume, name='select_resume'),
    path('view_resume/', views.resume_list, name='show_resume'),
    path('resume/<int:id>/delete/', views.delete_resume, name='delete_resume'),
    path('resume/<int:id>/edit/', views.edit_resume, name='edit_resume'),
    path('resume/<int:resume_id>/pdf/', views.generate_pdf, name='generate_pdf'),
    #path('resume/<int:id>/logout/', views.logout, name='logout'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)