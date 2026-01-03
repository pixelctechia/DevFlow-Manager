# database/models.py
"""
Modelos de dados para o DevFlow Manager
"""

class ProjectType:
    """Modelo para tipos de projetos"""
    def __init__(self, id=None, name=None, description=None, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

class Platform:
    """Modelo para plataformas"""
    def __init__(self, id=None, name=None, description=None, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

class Project:
    """Modelo para projetos"""
    def __init__(self, id=None, name=None, description=None, project_type_id=None, 
                 start_date=None, end_date=None, status=None, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.project_type_id = project_type_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

class ProjectPlatform:
    """Modelo para histórico de plataformas por projeto"""
    def __init__(self, id=None, project_id=None, platform_id=None, 
                 assigned_date=None, description=None):
        self.id = id
        self.project_id = project_id
        self.platform_id = platform_id
        self.assigned_date = assigned_date
        self.description = description