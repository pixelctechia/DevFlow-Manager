# components/project_timeline.py
"""
Componente para exibir a linha do tempo de plataformas de um projeto
"""
import streamlit as st

def render_project_timeline(platform_history):
    """
    Renderiza a linha do tempo de plataformas de um projeto
    
    Args:
        platform_history: Lista de dicionários com informações de plataforma
    """
    if not platform_history:
        st.info("Nenhuma plataforma registrada para este projeto.")
        return
    
    # Ordenar por data de atribuição
    sorted_history = sorted(platform_history, key=lambda x: x['assigned_date'])
    
    # Container para a linha do tempo
    with st.container():
        for i, platform in enumerate(sorted_history):
            # Card para cada plataforma
            with st.container():
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    # Indicador de posição na linha do tempo
                    st.markdown(
                        f"""
                        <div style="
                            width: 30px;
                            height: 30px;
                            border-radius: 50%;
                            background-color: #6B46C1;
                            color: white;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-weight: bold;
                            margin: 10px 0;
                        ">
                            {i+1}
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                
                with col2:
                    st.markdown(
                        f"""
                        <div style="
                            border-left: 3px solid #6B46C1;
                            padding-left: 20px;
                            margin-left: 15px;
                            padding-bottom: 15px;
                        ">
                            <h5 style="color: #6B46C1; margin-bottom: 5px;">{platform['platform_name']}</h5>
                            <p style="margin: 5px 0;"><strong>Data:</strong> {platform['assigned_date']}</p>
                            <p style="margin: 5px 0;"><strong>Descrição:</strong> {platform.get('description', '-')}</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )