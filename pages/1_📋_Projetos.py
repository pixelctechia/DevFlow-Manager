# pages/1_📋_Projetos.py
import streamlit as st
from datetime import datetime
import sys
import os

# Adicionar o diretório raiz ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import (
    get_all_projects, get_project_by_id, create_project, update_project, delete_project,
    get_all_project_types, get_all_platforms, add_platform_to_project,
    get_project_platforms_history, search_projects, validate_project_data,
    add_collaborator_to_project, get_project_collaborators, remove_collaborator_from_project,
    get_upcoming_project_deadlines
)
from components.project_timeline import render_project_timeline
from utils.helpers import format_date, format_status
from utils.ui import apply_custom_styles, render_sidebar

def main():
    # Aplicar estilos globais
    apply_custom_styles()
    render_sidebar()
    
    st.title("📋 Gerenciamento de Projetos")
    
    # Mostrar alertas de prazos
    show_deadline_alerts()
    
    # Tabs para diferentes funcionalidades
    tab1, tab2, tab3 = st.tabs(["Visualizar Projetos", "Novo Projeto", "Editar Projeto"])
    
    with tab1:
        show_projects_list()
    
    with tab2:
        create_new_project_form()
    
    with tab3:
        edit_project_form()

def show_deadline_alerts():
    """Mostra alertas de prazos se houver projetos vencendo em breve"""
    upcoming_projects = get_upcoming_project_deadlines(7)
    
    if upcoming_projects:
        st.warning(f"⚠️ {len(upcoming_projects)} projeto(s) vencendo em até 7 dias:")
        for project in upcoming_projects:
            st.caption(f"- {project.name} (vence em {format_date(project.end_date)})")

def show_projects_list():
    """Exibe a lista de projetos com opções de filtro"""
    st.header("Lista de Projetos")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input("Buscar projetos", placeholder="Nome ou descrição...")
    
    with col2:
        # Carregar tipos de projeto para o filtro
        project_types = get_all_project_types()
        type_options = {pt.name: pt.id for pt in project_types}
        type_options_with_all = {"Todos": None, **type_options}
        selected_type_name = st.selectbox("Filtrar por tipo", options=list(type_options_with_all.keys()))
        selected_type_id = type_options_with_all[selected_type_name]
    
    with col3:
        status_options = ["Todos", "Planejamento", "Em Desenvolvimento", "Testes", "Implantação", "Concluído", "Cancelado"]
        selected_status = st.selectbox("Filtrar por status", options=status_options)
        # Converter "Todos" para None
        if selected_status == "Todos":
            selected_status = None
    
    # Aplicar filtros
    if selected_type_id is None and selected_status is None and not search_query:
        projects = get_all_projects()
    else:
        projects = search_projects(
            query=search_query if search_query else None,
            status=selected_status,
            project_type_id=selected_type_id
        )
    
    if not projects:
        st.info("Nenhum projeto encontrado.")
        return
    
    # Exibir projetos em cards
    for project in projects:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                st.subheader(f"{project.name}")
                if project.description:
                    st.caption(project.description)
            
            with col2:
                st.write(f"**Tipo:** {project.project_type_name}")
                st.write(f"**Status:** {format_status(project.status)}")
            
            with col3:
                st.write(f"**Início:** {format_date(project.start_date)}")
                if project.end_date:
                    st.write(f"**Término:** {format_date(project.end_date)}")
                else:
                    st.write("**Término:** Em andamento")
            
            with col4:
                if st.button(f"Ver Detalhes", key=f"details_{project.id}"):
                    show_project_details(project.id)
            
            st.divider()

def show_project_details(project_id):
    """Exibe os detalhes completos de um projeto"""
    project = get_project_by_id(project_id)
    if not project:
        st.error("Projeto não encontrado.")
        return
    
    st.subheader(f"Detalhes do Projeto: {project.name}")
    
    # Informações básicas do projeto
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Nome:** {project.name}")
        st.write(f"**Descrição:** {project.description if project.description else 'Não informada'}")
        st.write(f"**Tipo:** {project.project_type_name}")
        st.write(f"**Status:** {format_status(project.status)}")
    
    with col2:
        st.write(f"**Data de Início:** {format_date(project.start_date)}")
        st.write(f"**Data de Término:** {format_date(project.end_date) if project.end_date else 'Em andamento'}")
        st.write(f"**Criado em:** {format_date(project.created_at.split()[0])}")
        if project.updated_at:
            st.write(f"**Atualizado em:** {format_date(project.updated_at.split()[0])}")
    
    # Histórico de plataformas
    st.subheader("Histórico de Plataformas")
    platform_history = get_project_platforms_history(project_id)
    render_project_timeline(platform_history)
    
    # Formulário para adicionar nova plataforma
    st.subheader("Adicionar Nova Plataforma")
    platforms = get_all_platforms()
    platform_options = {p.name: p.id for p in platforms}
    
    col1, col2 = st.columns(2)
    with col1:
        selected_platform = st.selectbox("Plataforma", options=list(platform_options.keys()))
    with col2:
        assigned_date = st.date_input("Data de Atribuição", value=datetime.today())
    
    description = st.text_area("Descrição (opcional)")
    
    if st.button("Adicionar Plataforma ao Projeto"):
        try:
            platform_id = platform_options[selected_platform]
            add_platform_to_project(
                project_id, 
                platform_id, 
                assigned_date.strftime('%Y-%m-%d'), 
                description if description.strip() else None
            )
            st.success("Plataforma adicionada ao projeto com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao adicionar plataforma: {e}")
    
    # Gerenciamento de colaboradores
    st.subheader("Colaboradores do Projeto")
    
    # Adicionar novo colaborador
    col1, col2, col3 = st.columns(3)
    with col1:
        collaborator_name = st.text_input("Nome do Colaborador", key=f"collab_name_{project_id}")
    with col2:
        collaborator_email = st.text_input("Email (opcional)", key=f"collab_email_{project_id}")
    with col3:
        role_options = ["Membro", "Administrador", "Observador"]
        collaborator_role = st.selectbox("Função", options=role_options, key=f"collab_role_{project_id}")
    
    if st.button("Adicionar Colaborador", key=f"add_collab_{project_id}"):
        if collaborator_name.strip():
            try:
                add_collaborator_to_project(
                    project_id,
                    collaborator_name.strip(),
                    collaborator_email.strip() if collaborator_email.strip() else None,
                    collaborator_role.lower()
                )
                st.success(f"Colaborador '{collaborator_name}' adicionado ao projeto!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao adicionar colaborador: {e}")
        else:
            st.error("Nome do colaborador é obrigatório")
    
    # Listar colaboradores existentes
    collaborators = get_project_collaborators(project_id)
    if collaborators:
        st.write("**Colaboradores atuais:**")
        for collab in collaborators:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.write(f"**{collab['user_name']}**")
                    if collab['user_email']:
                        st.caption(f"📧 {collab['user_email']}")
                
                with col2:
                    st.write(f"**Função:** {collab['role'].title()}")
                    st.write(f"**Adicionado em:** {format_date(collab['added_at'].split()[0])}")
                
                with col3:
                    if st.button(f"Remover", key=f"remove_collab_{collab['id']}", type="secondary"):
                        if st.checkbox("Confirmar remoção", key=f"confirm_remove_{collab['id']}"):
                            try:
                                remove_collaborator_from_project(collab['id'])
                                st.success(f"Colaborador '{collab['user_name']}' removido do projeto!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao remover colaborador: {e}")

def create_new_project_form():
    """Formulário para criação de novo projeto"""
    st.header("Criar Novo Projeto")
    
    # Carregar dados necessários
    project_types = get_all_project_types()
    
    if not project_types:
        st.error("Nenhum tipo de projeto cadastrado. Por favor, cadastre tipos de projeto primeiro.")
        return
    
    # Campos do formulário
    name = st.text_input("Nome do Projeto", max_chars=200, key="create_name")
    description = st.text_area("Descrição do Projeto", key="create_desc")
    
    col1, col2 = st.columns(2)
    
    with col1:
        project_type_options = {pt.name: pt.id for pt in project_types}
        selected_type = st.selectbox("Tipo de Projeto", options=list(project_type_options.keys()), key="create_type")
        start_date = st.date_input("Data de Início", value=datetime.today(), key="create_start")
    
    with col2:
        end_date = st.date_input("Data de Término (opcional)", value=None, key="create_end")
        status_options = ["Planejamento", "Em Desenvolvimento", "Testes", "Implantação", "Concluído", "Cancelado"]
        status = st.selectbox("Status", options=status_options, index=0, key="create_status")
    
    if st.button("Criar Projeto"):
        # Validação dos dados
        errors = validate_project_data(
            name, description, project_type_options[selected_type], 
            start_date.strftime('%Y-%m-%d'), 
            end_date.strftime('%Y-%m-%d') if end_date else None
        )
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                project_id = create_project(
                    name=name,
                    description=description,
                    project_type_id=project_type_options[selected_type],
                    start_date=start_date.strftime('%Y-%m-%d'),
                    end_date=end_date.strftime('%Y-%m-%d') if end_date else None,
                    status=status
                )
                st.success(f"Projeto '{name}' criado com sucesso! ID: {project_id}")
                # Limpar o formulário
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao criar projeto: {e}")

def edit_project_form():
    """Formulário para edição de projeto existente"""
    st.header("Editar Projeto")
    
    # Carregar projetos para seleção
    projects = get_all_projects()
    
    if not projects:
        st.info("Nenhum projeto encontrado para edição.")
        return
    
    project_options = {f"{p.name} (ID: {p.id})": p.id for p in projects}
    selected_project_key = st.selectbox("Selecione o Projeto", options=list(project_options.keys()))
    selected_project_id = project_options[selected_project_key]
    
    # Carregar dados do projeto selecionado
    project = get_project_by_id(selected_project_id)
    if not project:
        st.error("Projeto não encontrado.")
        return
    
    # Carregar dados necessários
    project_types = get_all_project_types()
    project_type_options = {pt.name: pt.id for pt in project_types}
    
    # Campos do formulário com dados atuais
    name = st.text_input("Nome do Projeto", value=project.name, max_chars=200, key="edit_name")
    description = st.text_area("Descrição do Projeto", value=project.description or "", key="edit_desc")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Encontrar o tipo de projeto atual
        current_type_name = next((name for name, id in project_type_options.items() if id == project.project_type_id), list(project_type_options.keys())[0])
        selected_type = st.selectbox("Tipo de Projeto", options=list(project_type_options.keys()), index=list(project_type_options.keys()).index(current_type_name), key="edit_type")
        start_date = st.date_input("Data de Início", value=datetime.strptime(project.start_date, '%Y-%m-%d'), key="edit_start")
    
    with col2:
        end_date = st.date_input("Data de Término (opcional)", value=datetime.strptime(project.end_date, '%Y-%m-%d') if project.end_date else None, key="edit_end")
        status_options = ["Planejamento", "Em Desenvolvimento", "Testes", "Implantação", "Concluído", "Cancelado"]
        current_status_index = status_options.index(project.status) if project.status in status_options else 0
        status = st.selectbox("Status", options=status_options, index=current_status_index, key="edit_status")
    
    if st.button("Atualizar Projeto"):
        # Validação dos dados
        errors = validate_project_data(
            name, description, project_type_options[selected_type], 
            start_date.strftime('%Y-%m-%d'), 
            end_date.strftime('%Y-%m-%d') if end_date else None
        )
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                success = update_project(
                    project_id=project.id,
                    name=name,
                    description=description,
                    project_type_id=project_type_options[selected_type],
                    start_date=start_date.strftime('%Y-%m-%d'),
                    end_date=end_date.strftime('%Y-%m-%d') if end_date else None,
                    status=status
                )
                if success:
                    st.success(f"Projeto '{name}' atualizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Falha ao atualizar o projeto.")
            except Exception as e:
                st.error(f"Erro ao atualizar projeto: {e}")
    
    # Opção para excluir projeto
    st.divider()
    st.subheader("Zona de Perigo")
    
    with st.expander("Excluir Projeto", expanded=False):
        st.warning("Esta ação é irreversível e excluirá o projeto e todos os seus dados.")
        confirm_delete = st.checkbox("Estou ciente e quero excluir este projeto", key="confirm_delete_check")
        
        # Botão só ativa se checkbox estiver marcado
        if st.button("Confirmar Exclusão Definitiva", type="primary", disabled=not confirm_delete, key="btn_delete_project_final"):
            try:
                success = delete_project(selected_project_id)
                if success:
                    st.success("Projeto excluído com sucesso!")
                    # Pequena pausa para o usuário ver a mensagem antes do rerun
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Falha ao excluir o projeto.")
            except Exception as e:
                st.error(f"Erro ao excluir projeto: {e}")

if __name__ == "__main__":
    main()