from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home/index.html"
    extra_context = {
        "page_title": "The Spark Playhouse",
    }
