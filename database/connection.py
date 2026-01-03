# database/connection.py
import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime, timedelta
import csv
import json
from .models import ProjectType, Platform, Project, ProjectPlatform

def get_db_path():
    """Retorna o caminho do banco de dados, permitindo override via variável de ambiente"""
    db_name = os.environ.get('DB_NAME', 'devflow_manager.db')
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), db_name)

@contextmanager
def get_db_connection():
    """Obtém conexão com o banco de dados SQLite"""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Inicializa o banco de dados executando o script de criação"""
    db_path = get_db_path()
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database_setup.sql')
    
    # Conectar ao banco
    conn = sqlite3.connect(db_path)
    
    # Ler e executar o script de criação
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()
    
    conn.executescript(schema)
    
    # Adicionar tabela de notificações se não existir
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        type TEXT DEFAULT 'info',
        is_read BOOLEAN DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS project_collaborators (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        user_email TEXT,
        role TEXT DEFAULT 'member',
        added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
    );
    """)
    
    conn.commit()
    conn.close()

# Funções CRUD para Project Types (mantidas como antes)
def create_project_type(name, description=None):
    """Cria um novo tipo de projeto"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO project_types (name, description) VALUES (?, ?)",
            (name, description)
        )
        conn.commit()
        return cursor.lastrowid

def get_all_project_types():
    """Retorna todos os tipos de projetos"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM project_types ORDER BY name")
        rows = cursor.fetchall()
        return [ProjectType(id=row['id'], name=row['name'], description=row['description'], 
                           created_at=row['created_at'], updated_at=row['updated_at'] if 'updated_at' in row.keys() else None) for row in rows]

def get_project_type_by_id(project_type_id):
    """Retorna um tipo de projeto específico pelo ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM project_types WHERE id = ?", (project_type_id,))
        row = cursor.fetchone()
        if row:
            return ProjectType(id=row['id'], name=row['name'], description=row['description'],
                              created_at=row['created_at'], updated_at=row['updated_at'] if 'updated_at' in row.keys() else None)
        return None

def update_project_type(project_type_id, name, description=None):
    """Atualiza um tipo de projeto existente"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE project_types SET name = ?, description = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (name, description, project_type_id)
        )
        conn.commit()
        return cursor.rowcount > 0

def delete_project_type(project_type_id):
    """Exclui um tipo de projeto"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM project_types WHERE id = ?", (project_type_id,))
        conn.commit()
        return cursor.rowcount > 0

# Funções CRUD para Platforms (mantidas como antes)
def create_platform(name, description=None):
    """Cria uma nova plataforma"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO platforms (name, description) VALUES (?, ?)",
            (name, description)
        )
        conn.commit()
        return cursor.lastrowid

def get_all_platforms():
    """Retorna todas as plataformas"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM platforms ORDER BY name")
        rows = cursor.fetchall()
        return [Platform(id=row['id'], name=row['name'], description=row['description'],
                        created_at=row['created_at'], updated_at=row['updated_at'] if 'updated_at' in row.keys() else None) for row in rows]

def get_platform_by_id(platform_id):
    """Retorna uma plataforma específica pelo ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM platforms WHERE id = ?", (platform_id,))
        row = cursor.fetchone()
        if row:
            return Platform(id=row['id'], name=row['name'], description=row['description'],
                           created_at=row['created_at'], updated_at=row['updated_at'] if 'updated_at' in row.keys() else None)
        return None

def update_platform(platform_id, name, description=None):
    """Atualiza uma plataforma existente"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE platforms SET name = ?, description = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (name, description, platform_id)
        )
        conn.commit()
        return cursor.rowcount > 0

def delete_platform(platform_id):
    """Exclui uma plataforma"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM platforms WHERE id = ?", (platform_id,))
        conn.commit()
        return cursor.rowcount > 0

# Funções CRUD para Projects (atualizadas)
def create_project(name, description, project_type_id, start_date, end_date=None, status="Planejamento"):
    """Cria um novo projeto"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO projects (name, description, project_type_id, start_date, end_date, status) VALUES (?, ?, ?, ?, ?, ?)",
            (name, description, project_type_id, start_date, end_date, status)
        )
        conn.commit()
        project_id = cursor.lastrowid
        
        # Adiciona a plataforma inicial automaticamente se não for custom
        add_platform_to_project(project_id, 10, start_date, f"Plataforma inicial para o projeto {name}")
        
        # Adiciona notificação de criação de projeto
        add_notification(
            f"Novo Projeto: {name}",
            f"O projeto '{name}' foi criado com sucesso.",
            "success"
        )
        
        return project_id

def get_all_projects():
    """Retorna todos os projetos com informações do tipo de projeto"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, pt.name as project_type_name 
            FROM projects p 
            LEFT JOIN project_types pt ON p.project_type_id = pt.id 
            ORDER BY p.created_at DESC
        """)
        rows = cursor.fetchall()
        projects = []
        for row in rows:
            project = Project(
                id=row['id'],
                name=row['name'],
                description=row['description'],
                project_type_id=row['project_type_id'],
                start_date=row['start_date'],
                end_date=row['end_date'],
                status=row['status'],
                created_at=row['created_at'],
                updated_at=row['updated_at'] if 'updated_at' in row.keys() else None
            )
            project.project_type_name = row['project_type_name']
            projects.append(project)
        return projects

def get_project_by_id(project_id):
    """Retorna um projeto específico pelo ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, pt.name as project_type_name 
            FROM projects p 
            LEFT JOIN project_types pt ON p.project_type_id = pt.id 
            WHERE p.id = ?
        """, (project_id,))
        row = cursor.fetchone()
        if row:
            project = Project(
                id=row['id'],
                name=row['name'],
                description=row['description'],
                project_type_id=row['project_type_id'],
                start_date=row['start_date'],
                end_date=row['end_date'],
                status=row['status'],
                created_at=row['created_at'],
                updated_at=row['updated_at'] if 'updated_at' in row.keys() else None
            )
            project.project_type_name = row['project_type_name']
            return project
        return None

def update_project(project_id, name, description, project_type_id, start_date, end_date=None, status=None):
    """Atualiza um projeto existente"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE projects 
               SET name = ?, description = ?, project_type_id = ?, start_date = ?, 
                   end_date = ?, status = ?, updated_at = CURRENT_TIMESTAMP 
               WHERE id = ?""",
            (name, description, project_type_id, start_date, end_date, status, project_id)
        )
        conn.commit()
        return cursor.rowcount > 0

def delete_project(project_id):
    """Exclui um projeto e todos os registros relacionados"""
    project = get_project_by_id(project_id)
    if project:
        add_notification(
            f"Projeto Excluído: {project.name}",
            f"O projeto '{project.name}' foi excluído do sistema.",
            "warning"
        )
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        return cursor.rowcount > 0

def search_projects(query=None, status=None, project_type_id=None):
    """Busca projetos com base em critérios"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        base_query = """
            SELECT p.*, pt.name as project_type_name 
            FROM projects p 
            LEFT JOIN project_types pt ON p.project_type_id = pt.id 
            WHERE 1=1
        """
        params = []
        
        if query:
            base_query += " AND (p.name LIKE ? OR p.description LIKE ?)"
            params.extend([f'%{query}%', f'%{query}%'])
        
        if status:
            base_query += " AND p.status = ?"
            params.append(status)
        
        if project_type_id:
            base_query += " AND p.project_type_id = ?"
            params.append(project_type_id)
        
        base_query += " ORDER BY p.created_at DESC"
        
        cursor.execute(base_query, params)
        rows = cursor.fetchall()
        
        projects = []
        for row in rows:
            project = Project(
                id=row['id'],
                name=row['name'],
                description=row['description'],
                project_type_id=row['project_type_id'],
                start_date=row['start_date'],
                end_date=row['end_date'],
                status=row['status']
            )
            project.project_type_name = row['project_type_name']
            projects.append(project)
        return projects

# Funções CRUD para Project Platforms (atualizadas)
def add_platform_to_project(project_id, platform_id, assigned_date=None, description=None):
    """Adiciona uma plataforma a um projeto (histórico de plataformas)"""
    if assigned_date is None:
        assigned_date = datetime.now().strftime('%Y-%m-%d')
    
    # Verificar se já existe uma plataforma para esta data
    existing_platform = get_platforms_by_project_and_date(project_id, assigned_date)
    if existing_platform and existing_platform['assigned_date'] == assigned_date:
        # Atualizar a plataforma existente
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE project_platforms SET platform_id = ?, description = ? WHERE project_id = ? AND assigned_date = ?",
                (platform_id, description, project_id, assigned_date)
            )
            conn.commit()
            return cursor.lastrowid
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO project_platforms (project_id, platform_id, assigned_date, description) VALUES (?, ?, ?, ?)",
            (project_id, platform_id, assigned_date, description)
        )
        conn.commit()
        return cursor.lastrowid

def get_project_platforms_history(project_id):
    """Retorna o histórico de plataformas de um projeto"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pp.*, p.name as platform_name 
            FROM project_platforms pp 
            LEFT JOIN platforms p ON pp.platform_id = p.id 
            WHERE pp.project_id = ? 
            ORDER BY pp.assigned_date
        """, (project_id,))
        rows = cursor.fetchall()
        return [{'id': row['id'], 'project_id': row['project_id'], 
                'platform_id': row['platform_id'], 'assigned_date': row['assigned_date'], 
                'description': row['description'], 'platform_name': row['platform_name']} 
                for row in rows]

def get_platforms_by_project_and_date(project_id, date):
    """Retorna a plataforma usada em um projeto em uma data específica"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pp.*, p.name as platform_name 
            FROM project_platforms pp 
            LEFT JOIN platforms p ON pp.platform_id = p.id 
            WHERE pp.project_id = ? AND pp.assigned_date <= ? 
            ORDER BY pp.assigned_date DESC LIMIT 1
        """, (project_id, date))
        row = cursor.fetchone()
        if row:
            return {'id': row['id'], 'project_id': row['project_id'], 
                   'platform_id': row['platform_id'], 'assigned_date': row['assigned_date'], 
                   'description': row['description'], 'platform_name': row['platform_name']}
        return None

# Novas funções para exportação e importação
def export_projects_to_csv():
    """Exporta todos os projetos para CSV"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, pt.name as project_type_name 
            FROM projects p 
            LEFT JOIN project_types pt ON p.project_type_id = pt.id 
            ORDER BY p.created_at DESC
        """)
        rows = cursor.fetchall()
        
        import io
        import csv
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Escrever cabeçalhos
        writer.writerow(['ID', 'Nome', 'Descrição', 'Tipo de Projeto', 'Data Início', 'Data Término', 'Status', 'Criado em', 'Atualizado em'])
        
        # Escrever dados
        for row in rows:
            writer.writerow([
                row['id'],
                row['name'],
                row['description'],
                row['project_type_name'],
                row['start_date'],
                row['end_date'],
                row['status'],
                row['created_at'],
                row['updated_at']
            ])
        
        return output.getvalue()

def import_projects_from_csv(csv_content):
    """Importa projetos de um arquivo CSV"""
    import csv
    import io
    
    # Obter tipos de projeto existentes
    project_types = {pt.name: pt.id for pt in get_all_project_types()}
    
    # Ler conteúdo CSV
    csv_file = io.StringIO(csv_content)
    reader = csv.DictReader(csv_file)
    
    imported_count = 0
    errors = []
    
    for row in reader:
        try:
            # Verificar se o tipo de projeto existe
            project_type_name = row['Tipo de Projeto']
            if project_type_name not in project_types:
                errors.append(f"Tipo de projeto '{project_type_name}' não encontrado para o projeto '{row['Nome']}'")
                continue
            
            # Criar projeto
            create_project(
                name=row['Nome'],
                description=row['Descrição'],
                project_type_id=project_types[project_type_name],
                start_date=row['Data Início'],
                end_date=row['Data Término'] if row['Data Término'] else None,
                status=row['Status']
            )
            imported_count += 1
        except Exception as e:
            errors.append(f"Erro ao importar projeto '{row['Nome']}': {str(e)}")
    
    return imported_count, errors

# Funções para notificações
def add_notification(title, message, notification_type="info"):
    """Adiciona uma notificação ao sistema"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notifications (title, message, type) VALUES (?, ?, ?)",
            (title, message, notification_type)
        )
        conn.commit()
        return cursor.lastrowid

def get_unread_notifications():
    """Retorna notificações não lidas"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notifications WHERE is_read = 0 ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [{'id': row['id'], 'title': row['title'], 'message': row['message'], 
                'type': row['type'], 'created_at': row['created_at']} for row in rows]

def mark_notification_as_read(notification_id):
    """Marca uma notificação como lida"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notification_id,))
        conn.commit()
        return cursor.rowcount > 0

def get_recent_notifications(limit=10):
    """Retorna as notificações mais recentes"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notifications ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        return [{'id': row['id'], 'title': row['title'], 'message': row['message'], 
                'type': row['type'], 'is_read': bool(row['is_read']), 'created_at': row['created_at']} 
                for row in rows]

# Funções para colaboradores
def add_collaborator_to_project(project_id, user_name, user_email=None, role="member"):
    """Adiciona um colaborador a um projeto"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO project_collaborators (project_id, user_name, user_email, role) VALUES (?, ?, ?, ?)",
            (project_id, user_name, user_email, role)
        )
        conn.commit()
        return cursor.lastrowid

def get_project_collaborators(project_id):
    """Retorna os colaboradores de um projeto"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM project_collaborators WHERE project_id = ?", (project_id,))
        rows = cursor.fetchall()
        return [{'id': row['id'], 'project_id': row['project_id'], 'user_name': row['user_name'], 
                'user_email': row['user_email'], 'role': row['role'], 'added_at': row['added_at']} 
                for row in rows]

def remove_collaborator_from_project(collaborator_id):
    """Remove um colaborador de um projeto"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM project_collaborators WHERE id = ?", (collaborator_id,))
        conn.commit()
        return cursor.rowcount > 0

# Funções de backup e restauração
def backup_database():
    """Cria um backup do banco de dados"""
    import shutil
    import time
    
    db_path = get_db_path()
    backup_path = get_db_path().replace('.db', f'_backup_{int(time.time())}.db')
    
    shutil.copy2(db_path, backup_path)
    return backup_path

def restore_database(backup_path):
    """Restaura o banco de dados a partir de um backup"""
    import shutil
    
    db_path = get_db_path()
    shutil.copy2(backup_path, db_path)
    return True

# Funções de validação aprimoradas
def validate_project_data(name, description, project_type_id, start_date, end_date=None):
    """Valida os dados de um projeto antes de salvar"""
    errors = []
    
    if not name or len(name.strip()) == 0:
        errors.append("Nome do projeto é obrigatório")
    elif len(name.strip()) > 200:
        errors.append("Nome do projeto deve ter no máximo 200 caracteres")
    
    if not project_type_id:
        errors.append("Tipo de projeto é obrigatório")
    
    if not start_date:
        errors.append("Data de início é obrigatória")
    
    # Verificar se a data de início é válida
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        errors.append("Formato de data de início inválido (deve ser YYYY-MM-DD)")
    
    if end_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            if end < start:
                errors.append("Data de término deve ser posterior à data de início")
        except ValueError:
            errors.append("Formato de data de término inválido (deve ser YYYY-MM-DD)")
    
    # Verificar se já existe um projeto com o mesmo nome
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Tentar obter ID do Streamlit se disponível
        current_id = 0
        try:
            import streamlit as st
            current_id = getattr(st, 'current_project_id', 0)
        except:
            pass
            
        cursor.execute("SELECT id FROM projects WHERE name = ? AND id != ?", (name, current_id))
        if cursor.fetchone():
            errors.append("Já existe um projeto com este nome")
    
    return errors

def validate_project_type_data(name):
    """Valida os dados de um tipo de projeto antes de salvar"""
    errors = []
    
    if not name or len(name.strip()) == 0:
        errors.append("Nome do tipo de projeto é obrigatório")
    elif len(name.strip()) > 100:
        errors.append("Nome do tipo de projeto deve ter no máximo 100 caracteres")
    
    # Verificar se já existe um tipo de projeto com o mesmo nome
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Tentar obter ID do Streamlit se disponível
        current_id = 0
        try:
            import streamlit as st
            current_id = getattr(st, 'current_project_type_id', 0)
        except:
            pass
            
        cursor.execute("SELECT id FROM project_types WHERE name = ? AND id != ?", (name, current_id))
        if cursor.fetchone():
            errors.append("Já existe um tipo de projeto com este nome")
    
    return errors

def validate_platform_data(name):
    """Valida os dados de uma plataforma antes de salvar"""
    errors = []
    
    if not name or len(name.strip()) == 0:
        errors.append("Nome da plataforma é obrigatório")
    elif len(name.strip()) > 100:
        errors.append("Nome da plataforma deve ter no máximo 100 caracteres")
    
    # Verificar se já existe uma plataforma com o mesmo nome
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Tentar obter ID do Streamlit se disponível
        current_id = 0
        try:
            import streamlit as st
            current_id = getattr(st, 'current_platform_id', 0)
        except:
            pass
            
        cursor.execute("SELECT id FROM platforms WHERE name = ? AND id != ?", (name, current_id))
        if cursor.fetchone():
            errors.append("Já existe uma plataforma com este nome")
    
    return errors

# Funções auxiliares
def get_project_statistics():
    """Retorna estatísticas gerais dos projetos"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Total de projetos
        cursor.execute("SELECT COUNT(*) as total FROM projects")
        total_projects = cursor.fetchone()['total']
        
        # Projetos por status
        cursor.execute("SELECT status, COUNT(*) as count FROM projects GROUP BY status")
        status_counts = {row['status']: row['count'] for row in cursor.fetchall()}
        
        # Projetos por tipo
        cursor.execute("""
            SELECT pt.name as type_name, COUNT(*) as count 
            FROM projects p 
            LEFT JOIN project_types pt ON p.project_type_id = pt.id 
            GROUP BY p.project_type_id, pt.name
        """)
        type_counts = {row['type_name']: row['count'] for row in cursor.fetchall()}
        
        # Projetos vencendo esta semana
        week_from_now = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        cursor.execute("SELECT COUNT(*) as count FROM projects WHERE end_date IS NOT NULL AND end_date <= ? AND status != 'Concluído'", (week_from_now,))
        expiring_projects = cursor.fetchone()['count']
        
        return {
            'total_projects': total_projects,
            'status_counts': status_counts,
            'type_counts': type_counts,
            'expiring_projects': expiring_projects
        }

def get_upcoming_project_deadlines(days=7):
    """Retorna projetos com prazos se aproximando"""
    target_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, pt.name as project_type_name 
            FROM projects p 
            LEFT JOIN project_types pt ON p.project_type_id = pt.id 
            WHERE p.end_date IS NOT NULL 
            AND p.end_date <= ? 
            AND p.end_date >= ? 
            AND p.status != 'Concluído'
            ORDER BY p.end_date
        """, (target_date, datetime.now().strftime('%Y-%m-%d')))
        rows = cursor.fetchall()
        
        projects = []
        for row in rows:
            project = Project(
                id=row['id'],
                name=row['name'],
                description=row['description'],
                project_type_id=row['project_type_id'],
                start_date=row['start_date'],
                end_date=row['end_date'],
                status=row['status']
            )
            project.project_type_name = row['project_type_name']
            projects.append(project)
        return projects