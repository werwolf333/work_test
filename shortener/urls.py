from django.urls import path, re_path
from . import views

app_name = 'shortener'

urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('registration', views.Registration.as_view(), name='reg'),
    path('cut', views.ShortenLink.as_view(), name='short'),
    path('show', views.ShowYourLinks.as_view(), name='show'),
    path('logout', views.Logout.as_view(), name='Logout'),
    re_path(r'^(?P<hash>.{10})$', views.NewLink.as_view(), name='hash'),
    re_path(r'^(?P<hash>.{10})/delete$', views.DeleteLink.as_view(), name='delete'),
]