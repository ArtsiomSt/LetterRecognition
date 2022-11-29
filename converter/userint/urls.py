from django.urls import path
from .views import *


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('signin/', LoginView.as_view(), name='signin'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('logout/', logout_user, name='logout')
]