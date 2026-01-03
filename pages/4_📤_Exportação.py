# pages/4_📤_Exportação.py
import streamlit as st
import sys
import os
import pandas as pd

# Adicionar o diretório raiz ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import export_projects_to_csv, import_projects_from_csv, backup_database
from utils.helpers import format_date
from utils.ui import apply_custom_styles, render_sidebar

def main():
    apply_custom_styles()
    render_sidebar()
    st.title("📤 Exportação e Importação de Dados")
    
    # Tabs para diferentes funcionalidades
    tab1, tab2, tab3 = st.tabs(["Exportar Dados", "Importar Dados", "Backup"])
    
    with tab1:
        export_data_section()
    
    with tab2:
        import_data_section()
    
    with tab3:
        backup_section()

def export_data_section():
    """Seção para exportação de dados"""
    st.header("Exportar Projetos")
    
    st.write("Exporte todos os projetos cadastrados para um arquivo CSV.")
    
    if st.button("Exportar Projetos para CSV", type="primary"):
        try:
            csv_data = export_projects_to_csv()
            
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"projetos_devflow_{format_date(str(pd.Timestamp.now().date()))}.csv",
                mime="text/csv"
            )
            
            st.success("Dados exportados com sucesso! Clique no botão acima para baixar.")
        except Exception as e:
            st.error(f"Erro ao exportar dados: {e}")

def import_data_section():
    """Seção para importação de dados"""
    st.header("Importar Projetos")
    
    st.write("Importe projetos de um arquivo CSV. O arquivo deve conter as colunas: ID, Nome, Descrição, Tipo de Projeto, Data Início, Data Término, Status")
    
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
    
    if uploaded_file is not None:
        try:
            # Ler o conteúdo do arquivo
            stringio = uploaded_file.getvalue().decode("utf-8")
            
            if st.button("Importar Projetos", type="primary"):
                imported_count, errors = import_projects_from_csv(stringio)
                
                if imported_count > 0:
                    st.success(f"{imported_count} projetos importados com sucesso!")
                
                if errors:
                    st.error("Erros encontrados durante a importação:")
                    for error in errors:
                        st.error(error)
                
                if imported_count == 0 and not errors:
                    st.info("Nenhum projeto foi importado.")
        
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

def backup_section():
    """Seção para backup de dados"""
    st.header("Backup do Banco de Dados")
    
    st.write("Crie um backup completo do banco de dados para segurança.")
    
    if st.button("Criar Backup", type="secondary"):
        try:
            backup_path = backup_database()
            file_name = os.path.basename(backup_path)
            
            with open(backup_path, "rb") as file:
                st.download_button(
                    label="Download Backup",
                    data=file.read(),
                    file_name=file_name,
                    mime="application/octet-stream"
                )
            
            st.success(f"Backup criado com sucesso! Clique no botão acima para baixar: {file_name}")
        except Exception as e:
            st.error(f"Erro ao criar backup: {e}")

if __name__ == "__main__":
    main()