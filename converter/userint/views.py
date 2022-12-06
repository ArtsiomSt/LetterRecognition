import cv2
import io
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .mixins import LoginRequiredRedirectMixin
from .forms import LoginForm, RegisterForm, ChangeUserProfileDataForm, SetNewPassword, AddPictureForRecogintionForm
from .models import UserProfile, PictureForRecongition
from .serializers import PictureSerializer, ImageSerializer
import requests
from PIL import Image
import os
from converter.settings import MEDIA_ROOT, BASE_DIR


class HomePageView(LoginRequiredRedirectMixin, View):
    def get(self, request):
        form = AddPictureForRecogintionForm()
        context = {
            'form': form,
            'title': 'Homepage'
        }
        return render(request, 'userint/homepage.html', context=context)

    def post(self, request):
        form = AddPictureForRecogintionForm(request.POST, request.FILES)
        if form.is_valid():
            current_picture = PictureForRecongition.objects.create(
                made_by_user=UserProfile.objects.get(user=request.user),
                picture_file=form.cleaned_data['picture_file'])
            serializer = ImageSerializer({'image': form.cleaned_data['picture_file']})
            media = str(BASE_DIR) + current_picture.picture_file.url.replace('/', '\\')
            url = "http://127.0.0.1:8000/recpicture/api/v1/recognise/"
            payload = {}
            files = [('image', ('77-10.png', open(media, 'rb'), 'image/png'))]
            headers = {}
            resp = requests.request("POST", url, headers=headers, data=payload, files=files)
            print(resp.json())
            context = {
                'title': 'Homepage',
                'current_picture': current_picture,
            }
            return render(request, 'userint/homepage.html', context=context)
        return redirect('/?Error')


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
            user = form.save()
            UserProfile.objects.create(user=user)
            return redirect('/signin/?message=Success')
        return redirect('/signup/?message=Invaliddata')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('signin')


class ProfileView(LoginRequiredRedirectMixin, View):
    def get(self, request):
        import random
        cur_user = UserProfile.objects.select_related().get(user=request.user)
        form = SetNewPassword(cur_user.user)
        user_data = {
            'Username': cur_user.user.username,
            'First name': cur_user.user.first_name if cur_user.user.first_name else 'Empty',
            'Last name': cur_user.user.last_name if cur_user.user.first_name else 'Empty',
            'Email': cur_user.user.email if cur_user.user.first_name else 'Empty',
            'Password': ''.join(['*' for x in range(0, random.randrange(5, 10))])
        }
        context = {
            'user_data': user_data,
            'title': 'Profile',
        }
        if request.GET.get('chps') == 'true':
            context['form'] = form
        return render(request, 'userint/profile.html', context)

    def post(self, request):
        cur_user = UserProfile.objects.select_related().get(user=request.user)
        form = SetNewPassword(user=cur_user.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return redirect('profile')


class ChangeProfileDataView(LoginRequiredRedirectMixin, View):
    def get(self, request):
        cur_user = UserProfile.objects.select_related().get(user=request.user)
        user_data = {
            'username': cur_user.user.username,
            'first_name': cur_user.user.first_name if cur_user.user.first_name else 'Empty',
            'last_name': cur_user.user.last_name if cur_user.user.first_name else 'Empty',
            'email': cur_user.user.email if cur_user.user.first_name else 'Empty',
        }
        user_data_change_form = ChangeUserProfileDataForm(initial=user_data)
        context = {
            'change_form': user_data_change_form,
            'title': 'ChangeProfile',
        }
        return render(request, 'userint/changeprofile.html', context)

    def post(self, request):
        cur_user = UserProfile.objects.select_related().get(user=request.user)
        user_data_change_form = ChangeUserProfileDataForm(request.POST)
        if user_data_change_form.is_valid():
            cur_user.user.first_name = user_data_change_form.cleaned_data.get('first_name')
            cur_user.user.last_name = user_data_change_form.cleaned_data.get('last_name')
            cur_user.user.email = user_data_change_form.cleaned_data.get('email')
            cur_user.user.username = user_data_change_form.cleaned_data.get('username')
            cur_user.user.save()
            cur_user.save()
        return redirect('profile')
