from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView, View
from ..forms import LoginForm, RegisterForm, PasswordResetForm, PasswordResetConfirmForm
from ..service.auth_api_service import (
    client, Registration, password_reset_by_email, password_reset_confirm
)


class LoginView(FormView):
    """Login page rendering."""
    form_class = LoginForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        '''Is called when valid form data has been POSTed.'''
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        client.login(username, password)
        if client.is_authenticated:
            response = redirect('index')
            response.set_cookie('refresh_token', client.refresh_token, httponly=True)
            return response
        else:
            context = {'form': form, 'msg': client.error}
            return self.render_to_response(context)


class LogoutView(View):
    """Logout page rendering."""

    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        response = redirect('login')
        response.delete_cookie('refresh_token')
        return response


class RegisterView(FormView):
    """Register page rendering."""
    form_class = RegisterForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        '''Is called when valid form data has been POSTed.'''
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        re_password = form.cleaned_data.get('re_password')
        registration = Registration()
        registration.register(username, email, password, re_password)
        if registration.is_registered:
            context = {'form': form, 'usernamevalue': registration.username}
            return self.render_to_response(context)
        else:
            context = {'form': form, 'errors': registration.errors}
            return self.render_to_response(context)


class PasswordResetView(FormView):
    """PasswordReset page rendering."""
    form_class = PasswordResetForm
    template_name = 'registration/password_reset.html'

    def form_valid(self, form):
        '''Is called when valid form data has been POSTed.'''
        email = form.cleaned_data.get('email')
        password_reset_by_email(email)
        return redirect('password_reset_done')


class PasswordResetDoneView(TemplateView):
    """PasswordResetDone page rendering."""
    template_name = 'registration/password_reset_done.html'


class PasswordResetConfirmView(FormView):
    """PasswordResetConfirm page rendering."""
    form_class = PasswordResetConfirmForm
    template_name = 'registration/password_reset_confirm.html'

    def form_valid(self, form):
        '''Is called when valid form data has been POSTed.'''
        uidb64, token = self.kwargs['uidb64'], self.kwargs['token']
        password = form.cleaned_data.get('password')
        re_password = form.cleaned_data.get('re_password')
        errors = password_reset_confirm(uidb64, token, password, re_password)
        if errors:
            context = {'form': form, 'errors': res}
            return self.render_to_response(context)
        else:
            return redirect('password_reset_complete')


class PasswordResetCompleteView(TemplateView):
    """PasswordResetComplete page rendering."""
    template_name = 'registration/password_reset_complete.html'
