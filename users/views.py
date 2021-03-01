from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.base import View

from .forms import MyRegistrationForm


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
