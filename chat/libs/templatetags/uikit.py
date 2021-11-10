from django import template

register = template.Library()


@register.filter(name="tags_parser")
def tags_parser(tag: str):
    tag_map = {
        "debug": "primary",
        "info": "primary",
        "success": "success",
        "warning": "warning",
        "error": "danger",
    }
    return tag_map[tag] if tag in tag_map else "primary"
