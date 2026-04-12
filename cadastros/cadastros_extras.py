from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Acessa um dicionário por chave dentro de templates Django.
    Uso: {{ meu_dict|get_item:chave }}
    """
    return dictionary.get(key)
