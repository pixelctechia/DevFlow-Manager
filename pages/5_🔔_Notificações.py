# pages/5_🔔_Notificações.py
import streamlit as st
import sys
import os

# Adicionar o diretório raiz ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_recent_notifications, mark_notification_as_read
from utils.ui import apply_custom_styles, render_sidebar

def main():
    apply_custom_styles()
    render_sidebar()
    st.title("🔔 Notificações")
    
    st.header("Notificações Recentes")
    
    notifications = get_recent_notifications(20)  # Pegar as 20 mais recentes
    
    if not notifications:
        st.info("Nenhuma notificação encontrada.")
        return
    
    for notification in notifications:
        # Determinar cor com base no tipo de notificação
        color_map = {
            'info': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'error': '#e74c3c'
        }
        color = color_map.get(notification['type'], '#7f8c8d')
        
        with st.container():
            col1, col2, col3 = st.columns([6, 2, 1])
            
            with col1:
                st.markdown(
                    f"""
                    <div style="
                        border-left: 4px solid {color};
                        padding-left: 15px;
                        margin-bottom: 10px;
                        background-color: #f8f9fa;
                        padding: 10px;
                        border-radius: 5px;
                    ">
                        <strong>{notification['title']}</strong><br>
                        <small style="color: #666;">{notification['message']}</small><br>
                        <small style="color: #999;">{notification['created_at']}</small>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            
            with col2:
                status_text = "Lida" if notification['is_read'] else "Não lida"
                status_color = "green" if notification['is_read'] else "red"
                st.markdown(f"<span style='color: {status_color};'>● {status_text}</span>", unsafe_allow_html=True)
            
            with col3:
                if not notification['is_read']:
                    if st.button("Marcar como lida", key=f"mark_read_{notification['id']}"):
                        mark_notification_as_read(notification['id'])
                        st.rerun()

if __name__ == "__main__":
    main()