from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'info/index.html'


class AboutView(TemplateView):
    template_name = 'info/about.html'
