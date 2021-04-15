from account import views
from django.urls import path

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view()),
    path('', views.UserLoginView.as_view()),
    path('password/reset/', views.CustomPasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/', views.CustomPasswordResetConfirmView.as_view(),
         name='rest_password_reset_confirm'),

]
