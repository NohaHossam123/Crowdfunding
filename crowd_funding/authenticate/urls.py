from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('home/', views.home_page, name="home")

]