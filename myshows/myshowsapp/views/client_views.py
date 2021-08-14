from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from ..forms import *
from ..service.drf_api_service import *
from ..service.myshows_api_service import myshows_search, myshows_getbyid
from ..service.auth_api_service import client, Registration, password_reset_by_email, password_reset_confirmation


class SearchView(TemplateView):

    template_name = "myshowsapp/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_found = []
        response = myshows_search(self.request.GET.get("search", ""))
        for result in response["result"]:
            found = {'id': result["id"], 'title_eng': result["titleOriginal"]}
            all_found.append(found)
        context['all_found'] = all_found
        return context


def index(request):
    if not client.is_authenticated:
        return redirect('start_page')
    form_rating = RatingForm()
    serial_change_id = None
    if 'del_later' in request.POST:
        id = request.POST['del_later']
        delete_show_later(id)
    if 'del_full' in request.POST:
        id = request.POST['del_full']
        delete_show_full(id)
    if 'set_rating' in request.POST:
         form_rating = RatingForm(request.POST)
         if form_rating.is_valid():
             id = request.POST['set_rating']
             rating = form_rating.cleaned_data.get('rating')
             set_rating(id, rating)
    if 'change_rating' in request.POST:
        serial_change_id = int(request.POST['change_rating'])
    list_later_watch_page = pagination(
        serials=list_later_watch_show(),
        page=request.GET.get('page1'))
    list_full_watched_page = pagination(
        serials=list_full_watched_show(),
        page=request.GET.get('page2'))    
    context = {
        'serials_later': list_later_watch_page,
        'serials_complete': list_full_watched_page,
        'form_rating': form_rating,
        'serial_change_id': serial_change_id
        }
    return render(request, 'myshowsapp/index.html', context)


class DetailView(TemplateView):

    template_name = 'myshowsapp/detail.html'
    id = None
    myshows_id = None
    title_eng = None
    year = None
    show_button_later = True
    show_button_full = True

     
    def get_context_data(self, **kwargs):
        self.myshows_id = kwargs['myshows_id']
        response = myshows_getbyid(self.myshows_id)
        self.title_eng = response['result']['titleOriginal']
        self.year = response['result']['year']
        context = {**super().get_context_data(**kwargs), **response['result']}
        self.set_button_later(self.myshows_id)
        self.set_button_full(self.myshows_id)
        context['show_button_later'] = self.show_button_later
        context['show_button_full'] = self.show_button_full
        return context


    def post(self, request, *args, **kwargs):
        self.get_context_data(**kwargs)
        if 'add_later' in request.POST:
            create_show_later(self.myshows_id, self.title_eng, self.year)
            return redirect('detail', myshows_id=self.myshows_id)
        if 'add_full' in request.POST:
            create_show_full(self.myshows_id, self.title_eng, self.year)
            if not self.show_button_later:
                delete_show_later(self.id)
            return redirect('detail', myshows_id=self.myshows_id)


    def set_button_later(self, myshows_id):
        """ Установка флага отображения кнопки "Хочу посмотреть" """
        list_later_watch = list_later_watch_show()
        if isinstance(list_later_watch, list):
            for show in list_later_watch:
                if show["myshows_id"] == myshows_id:
                    self.show_button_later = False
                    self.id = show['id']


    def set_button_full(self, myshows_id):
        """ Установка флага отображения кнопки "Полностью посмотрел" """
        list_full_watched = list_full_watched_show()
        if isinstance(list_full_watched, list):
            for show in list_full_watched:
                if show["myshows_id"] == myshows_id:
                    self.show_button_full = False

'''
def detail(request, myshows_id):
    show = Show(myshows_id)
    response = show.get_by_id(myshows_id)
    context = response['result']
    context['show_button_later'] = show.show_button_later
    context['show_button_full'] = show.show_button_full
    if 'add_later' in request.POST:
        show.create_show_later()
        return redirect('detail', myshows_id=myshows_id)
    if 'add_full' in request.POST:
        show.create_show_full()
        return redirect('detail', myshows_id=myshows_id)
    return render(request, 'myshowsapp/detail.html', context)
'''

class StartView(TemplateView):

    template_name = "myshowsapp/start.html"


def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        client.login(username, password)
        if client.is_authenticated:
            response = redirect('index')
            response.set_cookie('refresh_token', client.refresh_token, httponly=True)
            return response
        else:
            context= {'form': form, 'msg': client.error}
            return render(request, 'registration/login.html', context)
    else:
        context= {'form': form}
        return render(request, 'registration/login.html', context)


def logout(request):
    response = redirect('login')
    response.delete_cookie('refresh_token')
    return response


def register(request):
    registration = Registration()
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        re_password = form.cleaned_data.get('re_password')
        registration.register(username, email, password, re_password) 
        if registration.is_registered:
            context= {'form': form, 'usernamevalue': registration.username}
            return render(request, 'registration/register.html', context)
        else:
            context= {'form': form, 'errors': registration.errors}
            return render(request, 'registration/register.html', context)
    else:
        context= {'form': form}
        return render(request, 'registration/register.html', context)


def password_reset(request):
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password_reset_by_email(email)
        return redirect('password_reset_done')
    else:
        context= {'form': form}
        return render(request, 'registration/password_reset.html', context)


def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')


def password_reset_confirm(request, uidb64, token):
    form = PasswordResetConfirmForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data.get('password')
        re_password = form.cleaned_data.get('re_password')
        res = password_reset_confirmation(uidb64, token, password, re_password)
        if res:
            context= {'form': form, 'errors': res}
            return render(request, 'registration/password_reset_confirm.html', context)
        else:
            return redirect('password_reset_complete')
    else:
        context= {'form': form}
        return render(request, 'registration/password_reset_confirm.html', context)


def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html')
