from django import template
import markdown

register = template.Library()


@register.filter
def markdown_to_html(value):
    return markdown.markdown(value)
