from django.views.generic import TemplateView


class IndexPage(TemplateView):
    template_name = 'index.html'


class TestLoginPage(TemplateView):
    template_name = 'test.html'


class TestLogoutPage(TemplateView):
    template_name = 'thanks.html'
