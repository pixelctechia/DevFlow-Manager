# app.py
import streamlit as st
from dotenv import load_dotenv
import os
import sys

# Adicionar o diretório raiz ao path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.connection import init_db, get_project_statistics, get_all_projects, get_unread_notifications
from utils.helpers import format_status
from utils.ui import apply_custom_styles, render_sidebar

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar o banco de dados na inicialização
try:
    init_db()
except Exception as e:
    st.error(f"Erro ao inicializar o banco de dados: {e}")

# Configuração da página
st.set_page_config(
    page_title="DevFlow Manager",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS para aplicar cores roxo, branco e rosa claro
apply_custom_styles()

# Título da aplicação
st.title("📋 DevFlow Manager")
st.subheader("Controle de Projetos de Desenvolvimento")

# Introdução
st.markdown("""
Este sistema permite o controle e acompanhamento de projetos de desenvolvimento de aplicações,
com especial foco em programação e inteligência artificial. O sistema permite registrar:
- Informações básicas do projeto
- Histórico de plataformas utilizadas
- Tipos de projetos controlados
""")

# Estatísticas principais
stats = get_project_statistics()
projects = get_all_projects()

if stats:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Projetos", stats['total_projects'])
    
    with col2:
        active_projects = len([p for p in projects if p.status not in ['Concluído', 'Cancelado']])
        st.metric("Projetos Ativos", active_projects)
    
    with col3:
        completed_projects = len([p for p in projects if p.status == 'Concluído'])
        st.metric("Projetos Concluídos", completed_projects)
    
    with col4:
        if stats['status_counts']:
            status_counts = stats['status_counts']
            # Pegar o status com maior número de projetos
            most_common_status = max(status_counts, key=status_counts.get)
            st.metric("Status Mais Comum", format_status(most_common_status))

# Menu lateral
render_sidebar()