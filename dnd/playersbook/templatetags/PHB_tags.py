from django import template
from playersbook.models import *
from django.db.models import QuerySet

register = template.Library()


@register.inclusion_tag('playersbook/sources_drop_list.html')
def get_sources_drops(list_type: str) -> dict:
    elements: QuerySet = Sources.objects.all()
    if list_type == 'spells':
        elements = Sources.objects.all()
    elif list_type == 'classes':
        elements = Classes.objects.filter(source__name='PHB')

    return {'elements': elements,
            'list_type': list_type}
