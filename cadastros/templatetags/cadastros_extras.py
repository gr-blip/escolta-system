from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def iso_to_date(value):
    """Converte string ISO (2025-11-24T00:00:00.000Z) para dd/mm/yyyy."""
    if not value or not isinstance(value, str):
        return value
    try:
        data_str = value.split('T')[0]  # 2025-11-24
        partes = data_str.split('-')
        if len(partes) == 3:
            return f'{partes[2]}/{partes[1]}/{partes[0]}'
    except (ValueError, IndexError):
        pass
    return value