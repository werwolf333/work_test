from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.views.generic import View
from shortener.models import Link
import hashlib


class Registration(FormView):
    form_class = UserCreationForm
    template_name = "shortener/registration.html"
    success_url = "/login/?registration_completed"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@method_decorator(csrf_exempt, name='dispatch')
class Login(FormView):
    def get(self, request):
        args = {}

        if 'registration_completed' in request.GET:
            args['success_register'] = 'успешная регистрация'
        return render(request, 'shortener/login.html', args)

    def post(self, request):
        args = {}
        args.update(csrf(request))
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username == '' and password == '':
            args['login_error'] = "Не введён логин и пароль"
            return render(request, 'shortener/login.html', args)

        elif username == '':
            args['login_error'] = "Неввведён логин"
            return render(request, 'shortener/login.html', args)

        elif password == '':
            args['login_error'] = "Невведён пароль"
            return render(request, 'shortener/login.html', args)

        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/shortener/cut')
            else:
                args['login_error'] = "Неверен логин или пароль"
                return render(request, 'shortener/login.html', args)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class Logout(View):
    def get(self, request):
        auth.logout(request)
        return redirect('/shortener/login')


class ShortenLink(View):
    def get(self, request):
        args = {}
        args['new_link'] = ""
        return render(request, 'shortener/shortener.html', args)

    def post(self, request):
        args = {}
        old_link = request.POST.get('old_link', '')
        link = Link()
        link.old_link = old_link
        link.client = args['username'] = auth.get_user(request)
        link.save()
        new_link = hashlib.md5(str(link.id).encode()).hexdigest()[:10]
        args['new_link'] = new_link
        args['old_link'] = old_link
        link.new_link = new_link
        link.save()
        return render(request, 'shortener/shortener.html', args)


class ShowYourLinks(View):
    def get(self, request):
        args = {}
        user = auth.get_user(request)
        args['list'] = Link.objects.filter(client=user)
        return render(request, 'shortener/show.html', args)


class NewLink(View):
    def get(self, request, hash):
        link = Link.objects.get(new_link=hash)
        return HttpResponseRedirect(link.old_link)


class DeleteLink(View):
    def get(self, request, hash):
        link = Link.objects.get(new_link=hash)
        link.delete()
        return redirect("/shortener/show")
