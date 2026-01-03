"""
Testes unitários para as funções de banco de dados do DevFlow Manager
"""
import unittest
import tempfile
import os
import sys
from datetime import datetime, timedelta

# Adicionar o diretório raiz ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import (
    init_db, create_project_type, get_all_project_types, get_project_type_by_id,
    create_platform, get_all_platforms, get_platform_by_id,
    create_project, get_all_projects, get_project_by_id,
    add_platform_to_project, get_project_platforms_history,
    validate_project_data, validate_project_type_data, validate_platform_data,
    delete_project, update_project, add_notification, get_recent_notifications,
    add_collaborator_to_project, get_project_collaborators
)

class TestDatabaseFunctions(unittest.TestCase):
    """Testes para as funções de banco de dados"""
    
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
    
    def test_create_and_get_project_type(self):
        """Testa a criação e recuperação de tipos de projeto"""
        # Criar tipo de projeto
        project_type_id = create_project_type("Teste Tipo Unico 1", "Descrição de teste")
        self.assertIsNotNone(project_type_id)
        
        # Recuperar tipo de projeto
        project_type = get_project_type_by_id(project_type_id)
        self.assertIsNotNone(project_type)
        self.assertEqual(project_type.name, "Teste Tipo Unico 1")
        self.assertEqual(project_type.description, "Descrição de teste")
    
    def test_create_and_get_platform(self):
        """Testa a criação e recuperação de plataformas"""
        # Criar plataforma
        platform_id = create_platform("Teste Plataforma Unica 1", "Descrição de teste")
        self.assertIsNotNone(platform_id)
        
        # Recuperar plataforma
        platform = get_platform_by_id(platform_id)
        self.assertIsNotNone(platform)
        self.assertEqual(platform.name, "Teste Plataforma Unica 1")
        self.assertEqual(platform.description, "Descrição de teste")
    
    def test_create_and_get_project(self):
        """Testa a criação e recuperação de projetos"""
        # Criar tipo de projeto
        project_type_id = create_project_type("Tipo de Teste Projeto", "Descrição")
        
        # Criar projeto
        project_id = create_project(
            "Projeto de Teste Unico",
            "Descrição do projeto de teste",
            project_type_id,
            "2026-01-04"
        )
        self.assertIsNotNone(project_id)
        
        # Recuperar projeto
        project = get_project_by_id(project_id)
        self.assertIsNotNone(project)
        self.assertEqual(project.name, "Projeto de Teste Unico")
        self.assertEqual(project.description, "Descrição do projeto de teste")
        self.assertEqual(project.project_type_id, project_type_id)
    
    def test_add_platform_to_project(self):
        """Testa adição de plataforma a um projeto"""
        # Criar tipo de projeto
        project_type_id = create_project_type("Tipo de Teste Add Plat", "Descrição")
        
        # Criar projeto
        project_id = create_project(
            "Projeto de Teste Add Plat",
            "Descrição do projeto de teste",
            project_type_id,
            "2026-01-04"
        )
        
        # Criar plataforma
        platform_id = create_platform("Plataforma Teste Add Plat", "Descrição")
        
        # Adicionar plataforma ao projeto (Usando data diferente da inicial para garantir novo registro)
        platform_history_id = add_platform_to_project(project_id, platform_id, "2026-01-05", "Segunda plataforma")
        self.assertIsNotNone(platform_history_id)
        
        # Verificar histórico
        history = get_project_platforms_history(project_id)
        self.assertEqual(len(history), 2)  # 1 original (2026-01-04) + 1 adicionado (2026-01-05)
        self.assertEqual(history[-1]['platform_id'], platform_id)
    
    def test_validate_project_data(self):
        """Testa a validação de dados de projeto"""
        # Testar dados válidos
        errors = validate_project_data("Nome Valido Unico", "Descrição", 1, "2026-01-04")
        self.assertEqual(errors, [])
        
        # Testar nome vazio
        errors = validate_project_data("", "Descrição", 1, "2026-01-04")
        self.assertIn("Nome do projeto é obrigatório", errors)
        
        # Testar data inválida
        errors = validate_project_data("Nome", "Descrição", 1, "data_invalida")
        self.assertIn("Formato de data de início inválido (deve ser YYYY-MM-DD)", errors)
    
    def test_validate_project_type_data(self):
        """Testa a validação de dados de tipo de projeto"""
        # Testar dados válidos
        errors = validate_project_type_data("Nome Valido Tipo Unico")
        self.assertEqual(errors, [])
        
        # Testar nome vazio
        errors = validate_project_type_data("")
        self.assertIn("Nome do tipo de projeto é obrigatório", errors)
    
    def test_validate_platform_data(self):
        """Testa a validação de dados de plataforma"""
        # Testar dados válidos
        errors = validate_platform_data("Nome Valido Plat Unica")
        self.assertEqual(errors, [])
        
        # Testar nome vazio
        errors = validate_platform_data("")
        self.assertIn("Nome da plataforma é obrigatório", errors)
    
    def test_update_project(self):
        """Testa a atualização de um projeto"""
        # Criar tipo de projeto
        project_type_id = create_project_type("Tipo Original Update", "Descrição")
        new_project_type_id = create_project_type("Tipo Novo Update", "Nova Descrição")
        
        # Criar projeto
        project_id = create_project(
            "Projeto Original Update",
            "Descrição Original",
            project_type_id,
            "2026-01-04"
        )
        
        # Atualizar projeto
        success = update_project(
            project_id,
            "Projeto Atualizado",
            "Descrição Atualizada",
            new_project_type_id,
            "2026-01-05",
            "2026-12-31",
            "Em Desenvolvimento"
        )
        self.assertTrue(success)
        
        # Verificar atualização
        updated_project = get_project_by_id(project_id)
        self.assertEqual(updated_project.name, "Projeto Atualizado")
        self.assertEqual(updated_project.description, "Descrição Atualizada")
        self.assertEqual(updated_project.project_type_id, new_project_type_id)
        self.assertEqual(updated_project.status, "Em Desenvolvimento")
    
    def test_delete_project(self):
        """Testa a exclusão de um projeto"""
        # Criar tipo de projeto
        project_type_id = create_project_type("Tipo de Teste Delete", "Descrição")
        
        # Criar projeto
        project_id = create_project(
            "Projeto para Excluir",
            "Descrição",
            project_type_id,
            "2026-01-04"
        )
        
        # Verificar que o projeto existe
        project = get_project_by_id(project_id)
        self.assertIsNotNone(project)
        
        # Excluir projeto
        success = delete_project(project_id)
        self.assertTrue(success)
        
        # Verificar que o projeto foi excluído
        deleted_project = get_project_by_id(project_id)
        self.assertIsNone(deleted_project)
    
    def test_notifications(self):
        """Testa o sistema de notificações"""
        # Adicionar notificação única para o teste
        unique_title = f"Título de Teste {datetime.now().timestamp()}"
        notification_id = add_notification(unique_title, "Mensagem de Teste", "info")
        self.assertIsNotNone(notification_id)
        
        # Recuperar notificações recentes
        notifications = get_recent_notifications(10)
        self.assertGreater(len(notifications), 0)
        
        # Verificar se a nossa notificação está na lista (deve ser a primeira ou estar lá)
        found = any(n['title'] == unique_title for n in notifications)
        self.assertTrue(found, f"Notificação '{unique_title}' não encontrada")
    
    def test_collaborators(self):
        """Testa o sistema de colaboradores"""
        # Criar tipo de projeto
        project_type_id = create_project_type("Tipo de Teste", "Descrição")
        
        # Criar projeto
        project_id = create_project(
            "Projeto de Teste",
            "Descrição",
            project_type_id,
            "2026-01-04"
        )
        
        # Adicionar colaborador
        collaborator_id = add_collaborator_to_project(project_id, "João Silva", "joao@email.com", "membro")
        self.assertIsNotNone(collaborator_id)
        
        # Recuperar colaboradores
        collaborators = get_project_collaborators(project_id)
        self.assertEqual(len(collaborators), 1)
        self.assertEqual(collaborators[0]['user_name'], "João Silva")

if __name__ == '__main__':
    unittest.main()
