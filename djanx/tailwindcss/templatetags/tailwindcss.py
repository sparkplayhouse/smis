from django import template
from django.templatetags.static import static
from django.utils.safestring import SafeString, mark_safe

register = template.Library()


@register.simple_tag
def tailwindcss() -> SafeString:
    """
    Generate a <link> tag for TailwindCSS.

    Returns:
        SafeString containing the HTML <link> tag for TailwindCSS

    Usage:
        {% tailwindcss %}
    """
    path = static("tailwindcss/min.css")
    return mark_safe(f'<link rel="stylesheet" href="{path}">')
