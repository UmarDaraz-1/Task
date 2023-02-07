from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_project/', views.create_project, name='create_project'),
    path('dashboard/', views.dashboard, name='dashboard'),
    #path('update/<int:pk>/', views.update_project, name='update_project'),
    path('update_project/<int:pk>/', views.update_project, name='update_project'),
    path('delete_project/<int:pk>/', views.delete_project, name='delete_project'),
    path('view_profile/', views.view_profile, name='view_profile'),
    #path('show_profile/<profile_id>', views.show_profile, name='show_profile'),
    #path('show_profile/', views.show_profile, name='show_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),




    #User Auth
    path('registerUser/', views.registerUser, name='registerUser'),
    path('loginUser/', views.loginUser, name='loginUser'),
    path('success/', views.success, name='success'),
    path('token_send/', views.token_send, name='token_send'),
    path('verify/<auth_token>' , views.verify , name="verify"),
    path('error' , views.error_page , name="error")
    
]
