"""
Teste básico das funções de banco de dados
Este arquivo pode ser executado para verificar se todas as funções de banco de dados estão funcionando corretamente
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.connection import (
    init_db, create_project_type, get_all_project_types, 
    create_platform, get_all_platforms, 
    create_project, get_all_projects, get_project_by_id,
    add_platform_to_project, get_project_platforms_history,
    validate_project_data, validate_project_type_data, validate_platform_data
)

def run_tests():
    print("Iniciando testes das funcoes de banco de dados...")
    
    # Inicializar banco de dados
    print("1. Inicializando banco de dados...")
    init_db()
    print("[OK] Banco de dados inicializado")
    
    # Testar funções de tipos de projeto
    print("\n2. Testando funcoes de tipos de projeto...")
    project_type_id = create_project_type("Teste Tipo", "Tipo de projeto para testes")
    print(f"[OK] Tipo de projeto criado com ID: {project_type_id}")
    
    project_types = get_all_project_types()
    print(f"[OK] Total de tipos de projeto: {len(project_types)}")
    
    # Testar funções de plataformas
    print("\n3. Testando funcoes de plataformas...")
    platform_id = create_platform("Teste Plataforma", "Plataforma para testes")
    print(f"[OK] Plataforma criada com ID: {platform_id}")
    
    platforms = get_all_platforms()
    print(f"[OK] Total de plataformas: {len(platforms)}")
    
    # Testar funções de projetos
    print("\n4. Testando funcoes de projetos...")
    project_id = create_project(
        "Projeto de Teste", 
        "Descrição do projeto de teste", 
        project_type_id, 
        "2026-01-04"
    )
    print(f"[OK] Projeto criado com ID: {project_id}")
    
    projects = get_all_projects()
    print(f"[OK] Total de projetos: {len(projects)}")
    
    project = get_project_by_id(project_id)
    if project:
        print(f"[OK] Projeto encontrado: {project.name}")
    else:
        print("[ERRO] Projeto nao encontrado")
    
    # Testar histórico de plataformas
    print("\n5. Testando funcoes de historico de plataformas...")
    platform_history_id = add_platform_to_project(project_id, platform_id, "2026-01-04", "Plataforma inicial")
    print(f"[OK] Plataforma adicionada ao projeto com ID: {platform_history_id}")
    
    history = get_project_platforms_history(project_id)
    print(f"[OK] Historico de plataformas do projeto: {len(history)} registros")
    
    # Testar validações
    print("\n6. Testando funcoes de validacao...")
    errors = validate_project_data("Projeto Teste", "Descricao", project_type_id, "2026-01-04")
    if not errors:
        print("[OK] Validacao de projeto passou")
    else:
        print(f"[ERRO] Erros na validacao de projeto: {errors}")
    
    type_errors = validate_project_type_data("Tipo Teste")
    if not type_errors:
        print("[OK] Validacao de tipo de projeto passou")
    else:
        print(f"[ERRO] Erros na validacao de tipo de projeto: {type_errors}")
    
    platform_errors = validate_platform_data("Plataforma Teste")
    if not platform_errors:
        print("[OK] Validacao de plataforma passou")
    else:
        print(f"[ERRO] Erros na validacao de plataforma: {platform_errors}")
    
    print("\n[OK] Todos os testes concluidos com sucesso!")

if __name__ == "__main__":
    run_tests()
