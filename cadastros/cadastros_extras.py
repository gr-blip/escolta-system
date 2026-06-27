from django import template
import re

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Acessa um dicionário por chave dentro de templates Django.
    Uso: {{ meu_dict|get_item:chave }}
    """
    return dictionary.get(key)


@register.filter
def fmt_cpf(value):
    """Formata CPF: 12345678900 → 123.456.789-00"""
    if not value:
        return value
    digits = re.sub(r'\D', '', str(value))
    if len(digits) == 11:
        return f'{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}'
    return value  # retorna original se não tiver 11 dígitos


@register.filter
def fmt_tel(value):
    """Formata telefone: 11 dígitos → (00) 0 0000-0000 | 10 → (00) 0000-0000"""
    if not value:
        return value
    digits = re.sub(r'\D', '', str(value))
    if len(digits) == 11:
        return f'({digits[:2]}) {digits[2]} {digits[3:7]}-{digits[7:]}'
    if len(digits) == 10:
        return f'({digits[:2]}) {digits[2:6]}-{digits[6:]}'
    return value
