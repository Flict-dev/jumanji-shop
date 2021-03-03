from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from .forms import MyRegistrationForm, ProfileForm


class MyLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class MyRegistrationView(View):
    def get(self, request):
        return render(request, 'users/registration.html', context={'form': MyRegistrationForm})

    def post(self, request, *args, **kwargs):
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        return render(request, 'users/registration.html', context={'form': form})


@method_decorator(login_required, name='post')
class ProfileView(View):
    def get(self, request):
        user = request.user
        return render(request, 'users/profile.html', context={'form': ProfileForm(instance=user)})

    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            messages.info(request, 'Профиль обнолвен!')
            return redirect('/profile/')
        return render(request, 'users/profile.html', context={'form': form})
