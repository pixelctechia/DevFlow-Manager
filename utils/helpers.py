# utils/helpers.py
"""
Funções auxiliares para o DevFlow Manager
"""
from datetime import datetime

def format_date(date_str):
    """Formata data para exibição"""
    if not date_str:
        return "Não definido"
    try:
        date_obj = datetime.strptime(str(date_str), "%Y-%m-%d")
        return date_obj.strftime("%d/%m/%Y")
    except:
        return date_str

def validate_date(date_str):
    """Valida formato de data"""
    try:
        datetime.strptime(str(date_str), "%Y-%m-%d")
        return True
    except ValueError:
        return False

def format_status(status):
    """Formata status para exibição"""
    status_map = {
        'Planejamento': '📋 Planejamento',
        'Em Desenvolvimento': '⚙️ Em Desenvolvimento',
        'Testes': '🧪 Testes',
        'Implantação': '🚀 Implantação',
        'Concluído': '✅ Concluído',
        'Cancelado': '❌ Cancelado'
    }
    return status_map.get(status, status)

def truncate_text(text, max_length=100):
    """Trunca texto se for muito longo"""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def format_currency(value):
    """Formata valor monetário"""
    try:
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return value