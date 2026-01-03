# tests/test_integration.py
"""
Testes de integração para o DevFlow Manager
"""
import unittest
import tempfile
import os
import sys
from datetime import datetime

# Adicionar o diretório raiz ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import (
    init_db, create_project_type, create_platform, create_project,
    add_platform_to_project, get_project_by_id, get_project_platforms_history,
    get_all_projects, search_projects, add_collaborator_to_project,
    get_project_collaborators, export_projects_to_csv, import_projects_from_csv
)

class TestIntegration(unittest.TestCase):
    """Testes de integração do sistema"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        # Criar um banco de dados temporário para testes
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Configurar variáveis de ambiente para usar o banco temporário
        os.environ['DB_NAME'] = self.temp_db.name
        init_db()
    
    def tearDown(self):
        """Limpeza após cada teste"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_complete_project_workflow(self):
        """Testa o fluxo completo de um projeto"""
        # 1. Criar tipos de projeto e plataformas
        web_type_id = create_project_type("Site Institucional Teste", "Website institucional para empresas")
        react_platform_id = create_platform("React Teste", "Biblioteca JavaScript para interfaces")
        wordpress_platform_id = create_platform("WordPress Teste", "Plataforma CMS baseada em WordPress")
        
        self.assertIsNotNone(web_type_id)
        self.assertIsNotNone(react_platform_id)
        self.assertIsNotNone(wordpress_platform_id)
        
        # 2. Criar projeto
        project_id = create_project(
            "Projeto Cliente ABC",
            "Site institucional para o cliente ABC",
            web_type_id,
            "2026-01-04",
            "2026-03-01",
            "Em Desenvolvimento"
        )
        
        self.assertIsNotNone(project_id)
        
        # 3. Adicionar colaboradores
        collab1_id = add_collaborator_to_project(project_id, "Maria Santos", "maria@empresa.com", "desenvolvedor")
        collab2_id = add_collaborator_to_project(project_id, "Carlos Oliveira", "carlos@empresa.com", "designer")
        
        self.assertIsNotNone(collab1_id)
        self.assertIsNotNone(collab2_id)
        
        # 4. Adicionar histórico de plataformas
        add_platform_to_project(project_id, wordpress_platform_id, "2026-01-05", "Início com WordPress")
        add_platform_to_project(project_id, react_platform_id, "2026-02-01", "Migração para React")
        
        # 5. Verificar dados completos
        project = get_project_by_id(project_id)
        self.assertIsNotNone(project)
        self.assertEqual(project.name, "Projeto Cliente ABC")
        self.assertEqual(project.project_type_id, web_type_id)
        self.assertEqual(project.status, "Em Desenvolvimento")
        
        # 6. Verificar colaboradores
        collaborators = get_project_collaborators(project_id)
        self.assertEqual(len(collaborators), 2)
        
        # 7. Verificar histórico de plataformas
        platform_history = get_project_platforms_history(project_id)
        self.assertEqual(len(platform_history), 3)  # 1 original + 2 adicionadas
        
        # 8. Verificar busca
        found_projects = search_projects(query="Cliente ABC")
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0].name, "Projeto Cliente ABC")
    
    def test_export_import_workflow(self):
        """Testa o fluxo de exportação e importação de dados"""
        # Criar dados para exportar
        web_type_id = create_project_type("Site Institucional Teste", "Website institucional")
        project_id = create_project(
            "Projeto Exportação",
            "Projeto para testar exportação",
            web_type_id,
            "2026-01-04",
            "2026-02-01",
            "Planejamento"
        )
        
        # Exportar dados
        csv_data = export_projects_to_csv()
        self.assertIsNotNone(csv_data)
        self.assertIn("Projeto Exportação", csv_data)
        
        # Limpar banco de dados
        from database.connection import get_db_connection
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM projects")
            cursor.execute("DELETE FROM project_types WHERE id != ?", (web_type_id,))
            conn.commit()
        
        # Importar dados (mesmo que o tipo já exista)
        imported_count, errors = import_projects_from_csv(csv_data)
        self.assertEqual(imported_count, 1)  # 1 projeto recuperado após exclusão
        self.assertEqual(len(errors), 0)
        
        # Verificar que os dados originais ainda existem
        projects = get_all_projects()
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0].name, "Projeto Exportação")

if __name__ == '__main__':
    unittest.main()