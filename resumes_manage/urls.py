
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create_resume/', views.create_resume, name='create_resume'),
    path('save_resume/', views.save_resume, name='save_resume'),
    path('select_resume/', views.select_resume, name='select_resume'),
    path('view_resume/', views.show_resumes, name='show_resume'),
    path('resume/<int:id>/delete/', views.delete_resume, name='delete_resume'),
    path('resume/<int:id>/edit/', views.edit_resume, name='edit_resume'),
    path('resume/<int:resume_id>/pdf/', views.generate_pdf, name='generate_pdf'),
    path('resume/<int:id>/delete_uploaded/', views.delete_uploaded_resume, name='delete_uploaded_resume'),
    path('api/save_applied_page/', views.save_applied_page, name='save_applied_page'),
    path('api/get_user_email/', views.get_user_email, name='get_user_email'),
    path('api/check_user_role/', views.check_user_role, name='check_user_role'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    #path('resume/<int:id>/logout/', views.logout, name='logout'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)