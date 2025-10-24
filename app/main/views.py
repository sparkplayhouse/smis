from django.views.generic import TemplateView


class View(TemplateView):
    template_name = "main/index.html"


class HomeView(View):
    extra_context = {
        "page_title": "The Spark Playhouse",
    }
