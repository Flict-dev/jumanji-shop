from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import MyLoginView, MyRegistrationView, ProfileView

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('registration/', MyRegistrationView.as_view(), name='reg'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

]