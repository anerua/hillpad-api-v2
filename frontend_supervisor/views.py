from django.views.generic import TemplateView


class HomeView(TemplateView):

    template_name = "frontend_supervisor/index.html"