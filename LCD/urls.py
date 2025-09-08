from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.home, name='home'),
    path('customer/create/', views.create_customer, name='create_customer'),
    path('customer/create/ajax/', views.create_customer_ajax, name='create_customer_ajax'),
    path('pictures/upload/', views.upload_picture, name='upload_picture'),
    path('pictures/delete/<int:pic_id>/', views.delete_picture, name='delete_picture'),

]
