# pages/3_📊_Relatórios.py
import streamlit as st
import sys
import os

# Adicionar o diretório raiz ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_project_statistics, get_all_projects
from utils.helpers import format_status
import plotly.express as px
from utils.ui import apply_custom_styles, render_sidebar

def main():
    apply_custom_styles()
    render_sidebar()
    st.title("📊 Relatórios")
    
    # Carregar estatísticas
    stats = get_project_statistics()
    projects = get_all_projects()
    
    # KPIs principais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Projetos", stats['total_projects'])
    
    with col2:
        active_projects = len([p for p in projects if p.status not in ['Concluído', 'Cancelado']])
        st.metric("Projetos Ativos", active_projects)
    
    with col3:
        completed_projects = len([p for p in projects if p.status == 'Concluído'])
        st.metric("Projetos Concluídos", completed_projects)
    
    # Gráficos
    st.divider()
    st.header("Análise de Projetos")
    
    # Gráfico de projetos por status
    if stats['status_counts']:
        status_df = {
            'Status': list(stats['status_counts'].keys()),
            'Quantidade': list(stats['status_counts'].values())
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribuição por Status")
            fig_status = px.pie(
                values=status_df['Quantidade'], 
                names=status_df['Status'],
                title="Projetos por Status"
            )
            st.plotly_chart(fig_status, key="chart_status")
        
        with col2:
            st.subheader("Distribuição por Tipo")
            if stats['type_counts']:
                type_df = {
                    'Tipo': list(stats['type_counts'].keys()),
                    'Quantidade': list(stats['type_counts'].values())
                }
                fig_type = px.bar(
                    x=type_df['Quantidade'], 
                    y=type_df['Tipo'],
                    orientation='h',
                    title="Projetos por Tipo"
                )
                st.plotly_chart(fig_type, key="chart_type")
    
    # Detalhes dos projetos
    st.divider()
    st.header("Detalhes dos Projetos")
    
    if projects:
        # Converter para DataFrame para melhor visualização
        project_data = []
        for project in projects:
            project_data.append({
                'Nome': project.name,
                'Tipo': project.project_type_name,
                'Status': format_status(project.status),
                'Início': project.start_date,
                'Término': project.end_date or 'Em andamento'
            })
        
        st.dataframe(project_data)
    else:
        st.info("Nenhum projeto cadastrado para exibir relatórios.")

if __name__ == "__main__":
    main()