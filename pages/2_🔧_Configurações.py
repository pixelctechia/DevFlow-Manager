# pages/2_🔧_Configurações.py
import streamlit as st
import sys
import os

# Adicionar o diretório raiz ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import (
    get_all_project_types, create_project_type, update_project_type, delete_project_type,
    get_all_platforms, create_platform, update_platform, delete_platform,
    validate_project_type_data, validate_platform_data
)
from utils.ui import apply_custom_styles, render_sidebar

def main():
    apply_custom_styles()
    render_sidebar()
    st.title("🔧 Configurações")
    
    # Tabs para diferentes configurações
    tab1, tab2 = st.tabs(["Tipos de Projetos", "Plataformas"])
    
    with tab1:
        manage_project_types()
    
    with tab2:
        manage_platforms()

def manage_project_types():
    """Gerencia os tipos de projetos"""
    st.header("Tipos de Projetos")
    
    # Listar tipos de projetos existentes
    project_types = get_all_project_types()
    
    if project_types:
        st.subheader("Tipos de Projetos Cadastrados")
        for pt in project_types:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.write(f"**{pt.name}**")
                    if pt.description:
                        st.caption(pt.description)
                
                with col2:
                    st.write(f"ID: {pt.id}")
                    st.write(f"Criado em: {pt.created_at.split()[0] if pt.created_at else 'N/A'}")
                
                with col3:
                    if st.button(f"Editar", key=f"edit_pt_{pt.id}"):
                        st.session_state.editing_project_type = pt.id
                        st.rerun()
                    
                    if st.button(f"Excluir", key=f"delete_pt_{pt.id}", type="secondary"):
                        if st.checkbox("Confirmar exclusão", key=f"confirm_delete_pt_{pt.id}"):
                            try:
                                success = delete_project_type(pt.id)
                                if success:
                                    st.success(f"Tipo de projeto '{pt.name}' excluído com sucesso!")
                                    st.rerun()
                                else:
                                    st.error("Falha ao excluir o tipo de projeto.")
                            except Exception as e:
                                st.error(f"Erro ao excluir tipo de projeto: {e}")
    
    # Formulário para novo tipo de projeto
    st.divider()
    st.subheader("Adicionar Novo Tipo de Projeto")
    
    new_name = st.text_input("Nome do Tipo", key="new_pt_name")
    new_description = st.text_area("Descrição", key="new_pt_desc")
    
    if st.button("Adicionar Tipo de Projeto"):
        errors = validate_project_type_data(new_name)
        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                type_id = create_project_type(new_name, new_description if new_description.strip() else None)
                st.success(f"Tipo de projeto '{new_name}' adicionado com sucesso! ID: {type_id}")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao adicionar tipo de projeto: {e}")
    
    # Formulário para edição de tipo de projeto
    if hasattr(st.session_state, 'editing_project_type'):
        st.divider()
        st.subheader("Editar Tipo de Projeto")
        
        editing_id = st.session_state.editing_project_type
        current_type = next((pt for pt in project_types if pt.id == editing_id), None)
        
        if current_type:
            edit_name = st.text_input("Nome do Tipo", value=current_type.name, key="edit_pt_name")
            edit_description = st.text_area("Descrição", value=current_type.description or "", key="edit_pt_desc")
            
            if st.button("Atualizar Tipo de Projeto"):
                errors = validate_project_type_data(edit_name)
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    try:
                        success = update_project_type(editing_id, edit_name, edit_description if edit_description.strip() else None)
                        if success:
                            st.success(f"Tipo de projeto '{edit_name}' atualizado com sucesso!")
                            del st.session_state.editing_project_type
                            st.rerun()
                        else:
                            st.error("Falha ao atualizar o tipo de projeto.")
                    except Exception as e:
                        st.error(f"Erro ao atualizar tipo de projeto: {e}")
            
            if st.button("Cancelar Edição"):
                del st.session_state.editing_project_type
                st.rerun()

def manage_platforms():
    """Gerencia as plataformas"""
    st.header("Plataformas")
    
    # Listar plataformas existentes
    platforms = get_all_platforms()
    
    if platforms:
        st.subheader("Plataformas Cadastradas")
        for p in platforms:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.write(f"**{p.name}**")
                    if p.description:
                        st.caption(p.description)
                
                with col2:
                    st.write(f"ID: {p.id}")
                    st.write(f"Criado em: {p.created_at.split()[0] if p.created_at else 'N/A'}")
                
                with col3:
                    if st.button(f"Editar", key=f"edit_plat_{p.id}"):
                        st.session_state.editing_platform = p.id
                        st.rerun()
                    
                    if st.button(f"Excluir", key=f"delete_plat_{p.id}", type="secondary"):
                        if st.checkbox("Confirmar exclusão", key=f"confirm_delete_plat_{p.id}"):
                            try:
                                success = delete_platform(p.id)
                                if success:
                                    st.success(f"Plataforma '{p.name}' excluída com sucesso!")
                                    st.rerun()
                                else:
                                    st.error("Falha ao excluir a plataforma.")
                            except Exception as e:
                                st.error(f"Erro ao excluir plataforma: {e}")
    
    # Formulário para nova plataforma
    st.divider()
    st.subheader("Adicionar Nova Plataforma")
    
    new_name = st.text_input("Nome da Plataforma", key="new_plat_name")
    new_description = st.text_area("Descrição", key="new_plat_desc")
    
    if st.button("Adicionar Plataforma"):
        errors = validate_platform_data(new_name)
        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                platform_id = create_platform(new_name, new_description if new_description.strip() else None)
                st.success(f"Plataforma '{new_name}' adicionada com sucesso! ID: {platform_id}")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao adicionar plataforma: {e}")
    
    # Formulário para edição de plataforma
    if hasattr(st.session_state, 'editing_platform'):
        st.divider()
        st.subheader("Editar Plataforma")
        
        editing_id = st.session_state.editing_platform
        current_platform = next((p for p in platforms if p.id == editing_id), None)
        
        if current_platform:
            edit_name = st.text_input("Nome da Plataforma", value=current_platform.name, key="edit_plat_name")
            edit_description = st.text_area("Descrição", value=current_platform.description or "", key="edit_plat_desc")
            
            if st.button("Atualizar Plataforma"):
                errors = validate_platform_data(edit_name)
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    try:
                        success = update_platform(editing_id, edit_name, edit_description if edit_description.strip() else None)
                        if success:
                            st.success(f"Plataforma '{edit_name}' atualizada com sucesso!")
                            del st.session_state.editing_platform
                            st.rerun()
                        else:
                            st.error("Falha ao atualizar a plataforma.")
                    except Exception as e:
                        st.error(f"Erro ao atualizar plataforma: {e}")
            
            if st.button("Cancelar Edição"):
                del st.session_state.editing_platform
                st.rerun()

if __name__ == "__main__":
    main()