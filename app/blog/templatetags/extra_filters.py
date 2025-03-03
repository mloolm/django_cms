from django import template

register = template.Library()

@register.filter
def get(dictionary, key):
    """
    Возвращает значение из словаря по ключу, или None, если ключ не найден.
    """
    try:
        return dictionary.get(key)
    except (AttributeError, TypeError):  # если dictionary не словарь или key не хешируемый
        return None