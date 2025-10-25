from django.views.generic import TemplateView


class Page(TemplateView):
    template_name = "pages/index.html"


class Home(Page):
    extra_context = {
        "page_title": "The Spark Playhouse",
    }
