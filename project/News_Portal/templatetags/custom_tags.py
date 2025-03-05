from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()  # Копируем текущие параметры запроса
    for k, v in kwargs.items():  # Устанавливаем новые значения для указанных параметров
        d[k] = v
    return d.urlencode()  # Кодируем параметры в строку
