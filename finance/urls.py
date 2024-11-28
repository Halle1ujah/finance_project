from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),  
    path('signup/', views.signup, name='signup'),  
    path('login/', auth_views.LoginView.as_view(template_name='finance/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add_transaction/', views.add_transaction, name='add_transaction'), 
    path('delete_transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('contact/', views.contact, name='contact'),
]
