from allauth.account.adapter import get_adapter
from allauth.account import app_settings
from allauth.account.utils import perform_login, url_str_to_user_pk
from allauth.compat import is_anonymous
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib import messages
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC



class ConfirmEmailView(TemplateResponseMixin, View):

    template_name = "account/email_confirm." + app_settings.TEMPLATE_EXTENSION

    def get(self, *args, **kwargs):
        try:
            self.object = self.get_object()
            if app_settings.CONFIRM_EMAIL_ON_GET:
                return self.post(*args, **kwargs)
        except Http404:
            self.object = None
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def post(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        return HttpResponse("You're email has been confirmed")


    def get_object(self, queryset=None):
        key = self.kwargs['key']
        emailconfirmation = EmailConfirmationHMAC.from_key(key)
        if not emailconfirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                emailconfirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                raise Http404()
        return emailconfirmation

    def get_context_data(self, **kwargs):
        ctx = kwargs
        ctx["confirmation"] = self.object
        return ctx


confirm_email = ConfirmEmailView.as_view()