from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # authentication
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('', views.home_page, name="home"),
    path('show_projects/<id>', views.projects_view, name="show_projects"),
    path('search/', views.search, name="search"),
    path('profile/', views.account_view, name="profile"),
    path('delete/', views.delete_profile, name="delete"),
    # password reset
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name="password_reset_done"),
    path('reset_password/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
         name="password_reset_complete"),
    # login with facebook
    path('oauth/', include('social_django.urls', namespace='social')),
    # activation email
    path('<str:token>', views.activate, name="auth.activate"),

]