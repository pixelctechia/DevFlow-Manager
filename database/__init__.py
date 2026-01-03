# database/__init__.py
"""
Módulo de banco de dados para o DevFlow Manager
"""
from .connection import get_db_connection, init_db

__all__ = ['get_db_connection', 'init_db']