import streamlit as st
import os
from database.connection import get_unread_notifications

def apply_custom_styles():
    """Aplica estilos personalizados CSS"""
    st.markdown("""
    <style>
        :root {
            --primary-color: #6B46C1;  /* Roxo */
            --base-color: #FFFFFF;     /* Branco */
            --accent-color: #F8BBD9;   /* Rosa claro */
        }
        
        .stApp {
            background-color: var(--base-color);
        }
        
        [data-testid="stSidebar"] {
            background-color: var(--primary-color);
        }
        
        [data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }
        
        [data-testid="stSidebar"] a {
            color: #FFFFFF !important;
        }
        
        [data-testid="stSidebar"] span, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] div,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
             color: #FFFFFF !important;
        }
        
        [data-testid="stSidebar"] svg {
            fill: #FFFFFF !important;
        }

        .stButton>button {
            background-color: var(--primary-color);
            color: white;
        }
        
        .stButton>button:hover {
            background-color: #553C9A;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: var(--primary-color);
        }
        
        .stSelectbox, .stTextInput, .stTextArea, .stDateInput {
            color: var(--primary-color);
        }
        
        .timeline-event {
            border-left: 3px solid var(--primary-color);
            padding-left: 15px;
            margin-bottom: 15px;
            position: relative;
        }
        
        .timeline-event:before {
            content: '';
            position: absolute;
            left: -8px;
            top: 5px;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: var(--accent-color);
            border: 2px solid var(--primary-color);
        }
        
        .notification-badge {
            background-color: #e74c3c;
            color: white;
            border-radius: 50%;
            padding: 2px 6px;
            font-size: 0.8em;
            margin-left: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Renderiza a barra lateral personalizada"""
    with st.sidebar:
        st.header("Menu")
        st.page_link("app.py", label="Dashboard", icon="🏠")
        st.page_link("pages/1_📋_Projetos.py", label="Gerenciar Projetos", icon="📋")
        st.page_link("pages/2_🔧_Configurações.py", label="Configurações", icon="🔧")
        st.page_link("pages/3_📊_Relatórios.py", label="Relatórios", icon="📊")
        st.page_link("pages/4_📤_Exportação.py", label="Exportação", icon="📤")
        st.page_link("pages/5_🔔_Notificações.py", label="Notificações", icon="🔔")
        
        # Contador de notificações não lidas
        try:
            unread_notifications = get_unread_notifications()
            if unread_notifications:
                notification_badge = f'<span class="notification-badge">{len(unread_notifications)}</span>'
                st.markdown(f"🔔 Notificações {notification_badge}", unsafe_allow_html=True)
        except:
            pass
        
        st.divider()
        st.markdown("**DevFlow Manager**")
        st.markdown("Gestão de Soluções Web")
        
        # Informações do banco de dados
        st.divider()
        st.markdown("**Status do Banco de Dados**")
        
        # Caminho absoluto para o banco
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(root_dir, 'devflow_manager.db')
        
        if os.path.exists(db_path):
            db_size = os.path.getsize(db_path)
            st.success(f"✅ Banco de dados pronto ({db_size} bytes)")
        else:
            st.warning("⚠ Banco de dados não encontrado")
