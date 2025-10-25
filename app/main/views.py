from django.views.generic import TemplateView


class Page(TemplateView):
    template_name = "main/page.html"


class Home(Page):
    extra_context = {
        "page_title": "The Spark Playhouse",
    }
