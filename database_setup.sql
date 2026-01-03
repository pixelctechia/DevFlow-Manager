-- Script para criação do banco de dados SQLite para o DevFlow_Manager

-- Tabela de tipos de projeto
CREATE TABLE IF NOT EXISTS project_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de plataformas
CREATE TABLE IF NOT EXISTS platforms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de projetos
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    project_type_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    status TEXT NOT NULL DEFAULT 'Planejamento',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_type_id) REFERENCES project_types (id)
);

-- Tabela de plataformas por projeto (histórico de mudanças)
CREATE TABLE IF NOT EXISTS project_platforms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    platform_id INTEGER NOT NULL,
    assigned_date DATE NOT NULL DEFAULT CURRENT_DATE,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
    FOREIGN KEY (platform_id) REFERENCES platforms (id)
);

-- Índices para melhorar performance
CREATE INDEX IF NOT EXISTS idx_projects_type_id ON projects(project_type_id);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
CREATE INDEX IF NOT EXISTS idx_project_platforms_project_id ON project_platforms(project_id);
CREATE INDEX IF NOT EXISTS idx_project_platforms_platform_id ON project_platforms(platform_id);
CREATE INDEX IF NOT EXISTS idx_project_platforms_assigned_date ON project_platforms(assigned_date);

-- Inserir tipos de projeto padrão
INSERT OR IGNORE INTO project_types (name, description) VALUES 
('Site Institucional', 'Website institucional para empresas'),
('Landing Page', 'Página de captura para campanhas específicas'),
('Microsite', 'Pequeno site com finalidade específica'),
('Chatbot', 'Sistema de atendimento automatizado'),
('Ferramenta de IA', 'Aplicação baseada em inteligência artificial'),
('Automação', 'Sistema de automação de processos'),
('E-commerce', 'Loja virtual para vendas online'),
('Aplicativo Web', 'Aplicação web interativa'),
('API', 'Interface de programação de aplicações'),
('Integração', 'Sistema de integração entre plataformas');

-- Inserir plataformas padrão
INSERT OR IGNORE INTO platforms (name, description) VALUES 
('WordPress', 'Plataforma CMS baseada em WordPress'),
('React', 'Biblioteca JavaScript para interfaces'),
('Next.js', 'Framework React com renderização server-side'),
('Node.js', 'Ambiente de execução JavaScript no servidor'),
('Python Django', 'Framework web em Python'),
('Python Flask', 'Framework web leve em Python'),
('Vue.js', 'Framework JavaScript progressivo'),
('Angular', 'Framework TypeScript para aplicações web'),
('Laravel', 'Framework PHP para desenvolvimento web'),
('Custom', 'Solução desenvolvida sob medida');
