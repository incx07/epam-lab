"""Module contains rendering logics for client pages."""

from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..forms import RatingForm
from ..service.drf_api_service import (
    list_later_watch_show, list_full_watched_show, delete_show_later,
    delete_show_full, set_rating, create_show_later, create_show_full
)
from ..service.myshows_api_service import myshows_search, myshows_getbyid
from ..service.auth_api_service import client


class StartView(TemplateView):
    """Start page rendering."""
    template_name = "myshowsapp/start.html"

    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        if client.is_authenticated:
            return redirect('index')
        return super().get(request, *args, **kwargs)


class SearchView(TemplateView):
    """Search page rendering."""
    template_name = "myshowsapp/search.html"

    def get_context_data(self, **kwargs):
        """Insert data into the context dict."""
        context = super().get_context_data(**kwargs)
        searching_results = []
        response = myshows_search(self.request.GET.get("search", ""))
        for result in response["result"]:
            found = {'id': result["id"], 'title_eng': result["titleOriginal"]}
            searching_results.append(found)
        context['searching_results'] = searching_results
        return context


class IndexView(TemplateView):
    """Index page rendering."""
    template_name = 'myshowsapp/index.html'

    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        if not client.is_authenticated:
            return redirect('start_page')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """Insert data into the context dict."""
        context = super().get_context_data(**kwargs)
        list_later_watch_page = self.paginate(
            serials=list_later_watch_show(),
            page=self.request.GET.get('page1')
        )
        list_full_watched_page = self.paginate(
            serials=list_full_watched_show(),
            page=self.request.GET.get('page2')
        )
        context['list_going_to_watch'] = list_later_watch_page
        context['list_watched_all'] = list_full_watched_page
        return context

    @staticmethod
    def paginate(serials, page):
        """Django standard pagination."""
        paginator = Paginator(serials, 5)
        try:
            serials_page = paginator.page(page)
        except PageNotAnInteger:
            serials_page = paginator.page(1)
        except EmptyPage:
            serials_page = paginator.page(paginator.num_pages)
        return serials_page

    def post(self, request, *args, **kwargs):
        """Handle POST requests."""
        form_rating = RatingForm(request.POST)
        in_context = {}
        if 'del_later' in request.POST:
            id = int(request.POST['del_later'])
            delete_show_later(id)
        if 'del_full' in request.POST:
            id = int(request.POST['del_full'])
            delete_show_full(id)
        if 'change_rating' in request.POST:
            serial_change_id = int(request.POST['change_rating'])
            in_context['form_rating'] = form_rating
            in_context['serial_change_id'] = serial_change_id
        if 'set_rating' in request.POST:
            if form_rating.is_valid():
                id = int(request.POST['set_rating'])
                rating = form_rating.cleaned_data.get('rating')
                set_rating(id, rating)
        context = {**self.get_context_data(**kwargs), **in_context}
        return self.render_to_response(context)


class DetailView(TemplateView):
    """Detail page rendering."""
    template_name = 'myshowsapp/detail.html'

    def get_context_data(self, **kwargs):
        """Insert data into the context dict."""
        myshows_id = kwargs['myshows_id']
        response = myshows_getbyid(myshows_id)
        context = super().get_context_data(**kwargs)
        if 'error' in response:
            context['not_found'] = response['error']
        else:
            context['result'] = response['result']
            if client.is_authenticated:
                context['show_button_later'] = self.show_button_later(myshows_id)
                context['show_button_full'] = self.show_button_full(myshows_id)
        return context

    def post(self, request, *args, **kwargs):
        """Handle POST requests."""
        if 'add_later' in request.POST:
            myshows_id = int(request.POST['add_later'])
            create_show_later(myshows_id)
            return redirect('detail', myshows_id)
        if 'add_full' in request.POST:
            myshows_id = int(request.POST['add_full'])
            create_show_full(myshows_id)
            for show in list_later_watch_show():
                if show["myshows_id"] == myshows_id:
                    delete_show_later(show['id'])
            return redirect('detail', myshows_id)

    @staticmethod
    def show_button_later(myshows_id):
        """Setting the flag of displaying the button "Going to watch"."""
        for show in list_later_watch_show():
            if show["myshows_id"] == myshows_id:
                return False
        return True

    @staticmethod
    def show_button_full(myshows_id):
        """Setting the flag of displaying the button "Watched all"."""
        for show in list_full_watched_show():
            if show["myshows_id"] == myshows_id:
                return False
        return True
