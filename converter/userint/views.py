from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .mixins import LoginRequiredRedirectMixin
from .forms import LoginForm, RegisterForm


class HomePageView(LoginRequiredRedirectMixin, View):
    def get(self, request):
        return render(request, 'userint/homepage.html', context={'title': 'Home'})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'userint/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
            try:
                login(request, user)
                return redirect('home')
            except:
                pass
        return redirect('/signin/?message=InvalidData')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        context = {
            'form': form,
        }
        return render(request, 'userint/registration.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/signin/?message=Success')
        return redirect('/signup/?message=Invaliddata')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('signin')
