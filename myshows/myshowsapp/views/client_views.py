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
    form_class = RatingForm
    serial_change_id = None

    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        if not client.is_authenticated:
            return redirect('start_page')
        context = self.get_context_data(request, **kwargs)
        context['form_rating'] = self.form_class
        return self.render_to_response(context)

    def get_context_data(self, request, **kwargs):
        """Insert data into the context dict."""
        context = super().get_context_data(**kwargs)
        list_later_watch_page = self.paginate(
            serials=list_later_watch_show(),
            page=request.GET.get('page1')
        )
        list_full_watched_page = self.paginate(
            serials=list_full_watched_show(),
            page=request.GET.get('page2')
        )
        context['serials_later'] = list_later_watch_page
        context['serials_full'] = list_full_watched_page
        return context

    def paginate(self, serials, page):
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
        form_rating = self.form_class(request.POST)
        in_context = {}
        if 'del_later' in request.POST:
            id = request.POST['del_later']
            delete_show_later(id)
        if 'del_full' in request.POST:
            id = request.POST['del_full']
            delete_show_full(id)
        if 'change_rating' in request.POST:
            self.serial_change_id = int(request.POST['change_rating'])
            in_context['form_rating'] = form_rating
            in_context['serial_change_id'] = self.serial_change_id
        if 'set_rating' in request.POST:
            if form_rating.is_valid():
                id = request.POST['set_rating']
                rating = form_rating.cleaned_data.get('rating')
                set_rating(id, rating)
        if 'change_rating' in request.POST:
            self.serial_change_id = int(request.POST['change_rating'])
            in_context['serial_change_id'] = self.serial_change_id
        context = {**self.get_context_data(request, **kwargs), **in_context}
        return self.render_to_response(context)


class DetailView(TemplateView):
    """Detail page rendering."""
    template_name = 'myshowsapp/detail.html'
    id = None
    myshows_id = None
    title_eng = None
    year = None
    show_button_later = True
    show_button_full = True

    def get_context_data(self, **kwargs):
        """Insert data into the context dict."""
        self.myshows_id = kwargs['myshows_id']
        response = myshows_getbyid(self.myshows_id)
        if response == 'not found':
            context = super().get_context_data(**kwargs)
            context['not_found'] = 'Show was not found.'
        else:
            self.title_eng = response['result']['titleOriginal']
            self.year = response['result']['year']
            context = {**super().get_context_data(**kwargs), **response['result']}
            if client.is_authenticated:
                self.set_button_later(self.myshows_id)
                self.set_button_full(self.myshows_id)
                context['show_button_later'] = self.show_button_later
                context['show_button_full'] = self.show_button_full
        return context

    def post(self, request, *args, **kwargs):
        """Handle POST requests."""
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
        """Setting the flag of displaying the button "Going to watch"."""
        list_later_watch = list_later_watch_show()
        if isinstance(list_later_watch, list):
            for show in list_later_watch:
                if show["myshows_id"] == myshows_id:
                    self.show_button_later = False
                    self.id = show['id']

    def set_button_full(self, myshows_id):
        """Setting the flag of displaying the button "Watched all"."""
        list_full_watched = list_full_watched_show()
        if isinstance(list_full_watched, list):
            for show in list_full_watched:
                if show["myshows_id"] == myshows_id:
                    self.show_button_full = False
