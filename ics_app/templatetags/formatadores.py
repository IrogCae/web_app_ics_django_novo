from django import template
from datetime import date

register = template.Library()

@register.filter
def moeda_brasileira(valor):
    try:
        valor = float(valor)
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return valor


@register.filter
def remover_decimal(valor):
    """Remove .0 se for número decimal terminando com .0"""
    try:
        if float(valor).is_integer():
            return str(int(float(valor)))
        return valor
    except (ValueError, TypeError):
        return valor

@register.filter
def data_por_extenso(valor):
    """
    Converte date em '3 de Julho de 2025'.
    Se não for date, retorna o valor original.
    """
    if isinstance(valor, date):
        meses = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }
        return f"{valor.day} de {meses[valor.month]} de {valor.year}"
    return valor

@register.filter
def get_item(obj, key):
    # Se for dicionário
    if isinstance(obj, dict):
        return obj.get(key)
    # Se for um objeto Django (model instance)
    return getattr(obj, key, '')