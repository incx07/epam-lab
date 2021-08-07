from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from ..forms import RatingForm, Loginform
from ..service.services import *
from ..service.auth import client


def search(request):
    all_found = []
    response = myshows_search(request.GET.get("search", ""))
    for result in response["result"]:
        found = {'id': result["id"], 'title_eng': result["titleOriginal"]}
        all_found.append(found)
    context = {'all_found': all_found}
    return render(request, 'myshowsapp/search.html', context)


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
    '''
    if 'set_rating' in request.POST:
         form_rating = RatingForm(request.POST)
         if form_rating.is_valid():
             myshows_id = request.POST['set_rating']
             rating = request.POST['rating']
             set_rating(myshows_id, user.id, rating)
    if 'change_rating' in request.POST:
        serial_change_id = int(request.POST['change_rating'])
    serials_later_page = pagination(
        serials=set_all_seriallater(user),
        page=request.GET.get('page1'))
    serials_complete_page = pagination(
        serials=set_all_serialcomplete(user),
        page=request.GET.get('page2'))
    '''
    list_later_watch = list_later_watch_show()
    list_full_watched = list_full_watched_show()
    context = {
        'serials_later': list_later_watch,
        'serials_complete': list_full_watched,
        'form_rating': form_rating,
        'serial_change_id': serial_change_id
        }
    return render(request, 'myshowsapp/index.html', context)


def detail(request, myshows_id):
    show = Show(myshows_id)
    response = show.myshows_getbyid(myshows_id)
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
class MyRegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/accounts/login/"
    template_name = "registration/register.html"
    def form_valid(self, form):
        form.save()
        return super(MyRegisterFormView, self).form_valid(form)
    def form_invalid(self, form):
        return super(MyRegisterFormView, self).form_invalid(form)
'''

def start(request):
    return render(request, 'myshowsapp/start.html')


def loginpage(request):
    form = Loginform(request.POST or None)
    if form.is_valid():
        usernamevalue = form.cleaned_data.get("username")
        passwordvalue = form.cleaned_data.get("password")
        client.login(usernamevalue = usernamevalue, passwordvalue = passwordvalue)
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


def logoutpage(request):
    response = redirect('login')
    response.delete_cookie('refresh_token')
    return response
