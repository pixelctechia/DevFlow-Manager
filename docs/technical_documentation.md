# Documentação Técnica - DevFlow Manager

## Sumário
1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Estrutura de Arquivos](#estrutura-de-arquivos)
4. [Modelo de Dados](#modelo-de-dados)
5. [Camada de Dados](#camada-de-dados)
6. [Camada de Apresentação](#camada-de-apresentação)
7. [Componentes Reutilizáveis](#componentes-reutilizáveis)
8. [Funções Utilitárias](#funções-utilitárias)
9. [Testes](#testes)
10. [Configuração do Ambiente](#configuração-do-ambiente)
11. [Implantação](#implantação)
12. [Manutenção](#manutenção)

## Visão Geral

O **DevFlow Manager** é um sistema de controle de projetos de desenvolvimento de aplicações, com especial foco em programação e inteligência artificial. O sistema permite registrar informações de projetos, histórico de plataformas utilizadas, tipos de projetos controlados e colaboradores envolvidos.

### Objetivo
Gerenciar e acompanhar projetos de desenvolvimento de software com histórico de plataformas, colaboradores e métricas de desempenho.

### Tecnologias Utilizadas
- **Linguagem**: Python 3.8+
- **Framework Web**: Streamlit 1.31.0
- **Banco de Dados**: SQLite
- **Frontend**: Streamlit UI
- **Formatos de Dados**: CSV, JSON
- **Gerenciamento de Pacotes**: pip

### Características
- Interface web responsiva
- Banco de dados local SQLite
- Exportação e importação de dados
- Sistema de notificações
- Gerenciamento de colaboradores
- Histórico de plataformas por projeto

## Arquitetura do Sistema

O sistema segue uma arquitetura em camadas bem definidas:

```
┌─────────────────┐
│   Interface     │  (Streamlit)
├─────────────────┤
│   Páginas       │  (Streamlit Pages)
├─────────────────┤
│   Componentes   │  (Componentes reutilizáveis)
├─────────────────┤
│   Utilitários   │  (Funções auxiliares)
├─────────────────┤
│   Camada Dados  │  (Funções CRUD e lógica de negócios)
├─────────────────┤
│   Conexão DB    │  (SQLite)
└─────────────────┘
```

### Camadas

#### 1. Camada de Apresentação (Interface)
- **Tecnologia**: Streamlit
- **Responsabilidade**: Interface de usuário, interação e navegação
- **Localização**: `app.py`, `pages/`

#### 2. Camada de Componentes
- **Tecnologia**: Python + Streamlit
- **Responsabilidade**: Componentes reutilizáveis de interface
- **Localização**: `components/`

#### 3. Camada de Utilitários
- **Tecnologia**: Python
- **Responsabilidade**: Funções auxiliares e de apoio
- **Localização**: `utils/`

#### 4. Camada de Dados
- **Tecnologia**: Python + SQLite
- **Responsabilidade**: Acesso ao banco de dados, CRUD, validações
- **Localização**: `database/`

#### 5. Camada de Persistência
- **Tecnologia**: SQLite
- **Responsabilidade**: Armazenamento de dados
- **Localização**: `devflow_manager.db`

## Estrutura de Arquivos

```
DevFlow_Manager/
├── app.py                    # Arquivo principal da aplicação
├── requirements.txt          # Dependências do projeto
├── database_setup.sql        # Script de criação do banco de dados
├── .env                      # Variáveis de ambiente
├── setup.py                  # Script de configuração inicial
├── deploy.py                 # Script de implantação
├── Dockerfile               # Configuração Docker
├── docker-compose.yml       # Configuração Docker Compose
├── README.md                # Documentação do projeto
├── .gitignore               # Arquivos ignorados pelo Git
├── database/                # Módulo de banco de dados
│   ├── __init__.py
│   ├── connection.py        # Funções de conexão e CRUD
│   └── models.py            # Modelos de dados
├── pages/                   # Páginas do Streamlit
│   ├── 1_📋_Projetos.py
│   ├── 2_🔧_Configurações.py
│   ├── 3_📊_Relatórios.py
│   ├── 4_📤_Exportação.py
│   └── 5_🔔_Notificações.py
├── components/              # Componentes reutilizáveis
│   ├── __init__.py
│   └── project_timeline.py  # Componente de linha do tempo
├── utils/                   # Funções utilitárias
│   ├── __init__.py
│   └── helpers.py           # Funções auxiliares
├── tests/                   # Testes do sistema
│   ├── test_database_functions.py
│   └── test_integration.py
└── docs/                    # Documentação
    ├── technical_documentation.md
    └── user_guide.md
```

### Descrição dos Arquivos Principais

#### `app.py`
**Função**: Arquivo principal da aplicação Streamlit
- Configuração da página
- CSS customizado
- Menu lateral
- Dashboard inicial

#### `database/connection.py`
**Função**: Camada de dados com todas as funções de CRUD
- Funções para projetos, tipos, plataformas
- Funções para histórico e colaboradores
- Funções de validação
- Funções de notificações
- Exportação e importação

#### `database/models.py`
**Função**: Classes que representam os modelos de dados
- `ProjectType`, `Platform`, `Project`, `ProjectPlatform`

#### `pages/*.py`
**Função**: Páginas secundárias do Streamlit
- Cada arquivo representa uma página no menu lateral
- Implementam funcionalidades específicas

#### `components/project_timeline.py`
**Função**: Componente reutilizável para exibir histórico de plataformas
- Renderiza linha do tempo visual
- Estilizado com CSS customizado

#### `utils/helpers.py`
**Função**: Funções auxiliares para formatação e validação
- Formatação de datas
- Formatação de status
- Validações auxiliares

## Modelo de Dados

### Diagrama ER
```
projects (1) ─── (N) project_platforms (N) ─── (1) platforms
    │                    │                        │
    │                    │                        │
    └── (N) project_collaborators                │
         │                                       │
         └── (1) users                           └── (N) notifications
```

### Tabelas do Banco de Dados

#### projects
| Campo | Tipo | Descrição | Restrições |
|-------|------|-----------|------------|
| id | INTEGER | Chave primária | PRIMARY KEY AUTOINCREMENT |
| name | TEXT | Nome do projeto | NOT NULL |
| description | TEXT | Descrição do projeto | - |
| project_type_id | INTEGER | Referência para project_types | FOREIGN KEY |
| start_date | DATE | Data de início | NOT NULL |
| end_date | DATE | Data de término | - |
| status | TEXT | Status do projeto | NOT NULL, DEFAULT 'Planejamento' |
| created_at | DATETIME | Data de criação | DEFAULT CURRENT_TIMESTAMP |
| updated_at | DATETIME | Data de atualização | DEFAULT CURRENT_TIMESTAMP |

**Índices**:
- `idx_projects_type_id` (project_type_id)
- `idx_projects_status` (status)

#### project_types
| Campo | Tipo | Descrição | Restrições |
|-------|------|-----------|------------|
| id | INTEGER | Chave primária | PRIMARY KEY AUTOINCREMENT |
| name | TEXT | Nome do tipo de projeto | NOT NULL UNIQUE |
| description | TEXT | Descrição do tipo | - |
| created_at | DATETIME | Data de criação | DEFAULT CURRENT_TIMESTAMP |
| updated_at | DATETIME | Data de atualização | DEFAULT CURRENT_TIMESTAMP |

#### platforms
| Campo | Tipo | Descrição | Restrições |
|-------|------|-----------|------------|
| id | INTEGER | Chave primária | PRIMARY KEY AUTOINCREMENT |
| name | TEXT | Nome da plataforma | NOT NULL UNIQUE |
| description | TEXT | Descrição da plataforma | - |
| created_at | DATETIME | Data de criação | DEFAULT CURRENT_TIMESTAMP |
| updated_at | DATETIME | Data de atualização | DEFAULT CURRENT_TIMESTAMP |

#### project_platforms
| Campo | Tipo | Descrição | Restrições |
|-------|------|-----------|------------|
| id | INTEGER | Chave primária | PRIMARY KEY AUTOINCREMENT |
| project_id | INTEGER | Referência para projects | FOREIGN KEY CASCADE |
| platform_id | INTEGER | Referência para platforms | FOREIGN KEY |
| assigned_date | DATE | Data de atribuição | NOT NULL DEFAULT CURRENT_DATE |
| description | TEXT | Descrição da plataforma no projeto | - |
| created_at | DATETIME | Data de criação | DEFAULT CURRENT_TIMESTAMP |

**Índices**:
- `idx_project_platforms_project_id` (project_id)
- `idx_project_platforms_platform_id` (platform_id)
- `idx_project_platforms_assigned_date` (assigned_date)

#### notifications
| Campo | Tipo | Descrição | Restrições |
|-------|------|-----------|------------|
| id | INTEGER | Chave primária | PRIMARY KEY AUTOINCREMENT |
| title | TEXT | Título da notificação | NOT NULL |
| message | TEXT | Mensagem da notificação | NOT NULL |
| type | TEXT | Tipo da notificação | DEFAULT 'info' |
| is_read | BOOLEAN | Status de leitura | DEFAULT 0 |
| created_at | DATETIME | Data de criação | DEFAULT CURRENT_TIMESTAMP |

#### project_collaborators
| Campo | Tipo | Descrição | Restrições |
|-------|------|-----------|------------|
| id | INTEGER | Chave primária | PRIMARY KEY AUTOINCREMENT |
| project_id | INTEGER | Referência para projects | FOREIGN KEY CASCADE |
| user_name | TEXT | Nome do colaborador | NOT NULL |
| user_email | TEXT | Email do colaborador | - |
| role | TEXT | Função no projeto | DEFAULT 'member' |
| added_at | DATETIME | Data de adição | DEFAULT CURRENT_TIMESTAMP |

### Relacionamentos

#### 1:N (Um para Muitos)
- `project_types` → `projects` (um tipo de projeto pode ter muitos projetos)
- `platforms` → `project_platforms` (uma plataforma pode estar em muitos históricos)
- `projects` → `project_platforms` (um projeto pode ter muitos registros de plataforma)
- `projects` → `project_collaborators` (um projeto pode ter muitos colaboradores)

#### N:N (Muitos para Muitos)
- Implementado através da tabela `project_platforms` entre `projects` e `platforms`
- Implementado através da tabela `project_collaborators` entre `projects` e colaboradores

## Camada de Dados

### Arquivo: `database/connection.py`

A camada de dados é responsável por todas as operações de banco de dados e lógica de negócios.

#### Funções de Projeto

##### `create_project(name, description, project_type_id, start_date, end_date=None, status="Planejamento")`
Cria um novo projeto no sistema.

**Parâmetros**:
- `name` (str): Nome do projeto
- `description` (str): Descrição do projeto
- `project_type_id` (int): ID do tipo de projeto
- `start_date` (str): Data de início (formato YYYY-MM-DD)
- `end_date` (str, opcional): Data de término
- `status` (str): Status inicial do projeto

**Retorno**: ID do projeto criado (int)

**Processo**:
1. Insere projeto na tabela `projects`
2. Adiciona plataforma inicial automaticamente
3. Cria notificação de criação
4. Retorna ID do projeto

##### `get_all_projects()`
Retorna todos os projetos com informações do tipo de projeto.

**Retorno**: Lista de objetos Project

##### `get_project_by_id(project_id)`
Retorna um projeto específico pelo ID.

**Parâmetros**:
- `project_id` (int): ID do projeto

**Retorno**: Objeto Project ou None

##### `update_project(project_id, name, description, project_type_id, start_date, end_date=None, status=None)`
Atualiza um projeto existente.

**Parâmetros**:
- `project_id` (int): ID do projeto a ser atualizado
- `name` (str): Novo nome do projeto
- `description` (str): Nova descrição
- `project_type_id` (int): Novo tipo de projeto
- `start_date` (str): Nova data de início
- `end_date` (str, opcional): Nova data de término
- `status` (str, opcional): Novo status

**Retorno**: Boolean indicando sucesso

##### `delete_project(project_id)`
Exclui um projeto do sistema e todos os registros relacionados.

**Parâmetros**:
- `project_id` (int): ID do projeto a ser excluído

**Retorno**: Boolean indicando sucesso

##### `search_projects(query=None, status=None, project_type_id=None)`
Busca projetos com base em critérios.

**Parâmetros**:
- `query` (str, opcional): Texto para busca em nome/descrição
- `status` (str, opcional): Filtro por status
- `project_type_id` (int, opcional): Filtro por tipo de projeto

**Retorno**: Lista de objetos Project

#### Funções de Histórico de Plataformas

##### `add_platform_to_project(project_id, platform_id, assigned_date=None, description=None)`
Adiciona uma plataforma a um projeto (histórico de plataformas).

**Parâmetros**:
- `project_id` (int): ID do projeto
- `platform_id` (int): ID da plataforma
- `assigned_date` (str, opcional): Data de atribuição (padrão: hoje)
- `description` (str, opcional): Descrição da plataforma no projeto

**Retorno**: ID do registro criado (int)

##### `get_project_platforms_history(project_id)`
Retorna o histórico de plataformas de um projeto.

**Parâmetros**:
- `project_id` (int): ID do projeto

**Retorno**: Lista de dicionários com informações de plataforma

##### `get_platforms_by_project_and_date(project_id, date)`
Retorna a plataforma usada em um projeto em uma data específica.

**Parâmetros**:
- `project_id` (int): ID do projeto
- `date` (str): Data de referência

**Retorno**: Dicionário com informações da plataforma ou None

#### Funções de Colaboradores

##### `add_collaborator_to_project(project_id, user_name, user_email=None, role="member")`
Adiciona um colaborador a um projeto.

**Parâmetros**:
- `project_id` (int): ID do projeto
- `user_name` (str): Nome do colaborador
- `user_email` (str, opcional): Email do colaborador
- `role` (str): Função no projeto

**Retorno**: ID do colaborador adicionado (int)

##### `get_project_collaborators(project_id)`
Retorna os colaboradores de um projeto.

**Parâmetros**:
- `project_id` (int): ID do projeto

**Retorno**: Lista de dicionários com informações de colaboradores

##### `remove_collaborator_from_project(collaborator_id)`
Remove um colaborador de um projeto.

**Parâmetros**:
- `collaborator_id` (int): ID do colaborador

**Retorno**: Boolean indicando sucesso

#### Funções de Notificações

##### `add_notification(title, message, notification_type="info")`
Adiciona uma notificação ao sistema.

**Parâmetros**:
- `title` (str): Título da notificação
- `message` (str): Mensagem da notificação
- `notification_type` (str): Tipo da notificação

**Retorno**: ID da notificação (int)

##### `get_unread_notifications()`
Retorna notificações não lidas.

**Retorno**: Lista de dicionários com informações de notificações

##### `mark_notification_as_read(notification_id)`
Marca uma notificação como lida.

**Parâmetros**:
- `notification_id` (int): ID da notificação

**Retorno**: Boolean indicando sucesso

##### `get_recent_notifications(limit=10)`
Retorna as notificações mais recentes.

**Parâmetros**:
- `limit` (int): Número máximo de notificações

**Retorno**: Lista de dicionários com informações de notificações

#### Funções de Exportação e Importação

##### `export_projects_to_csv()`
Exporta todos os projetos para CSV.

**Retorno**: String CSV com dados dos projetos

##### `import_projects_from_csv(csv_content)`
Importa projetos de um arquivo CSV.

**Parâmetros**:
- `csv_content` (str): Conteúdo CSV

**Retorno**: Tupla (quantidade_importada, lista_erros)

#### Funções de Backup

##### `backup_database()`
Cria um backup do banco de dados.

**Retorno**: Caminho do arquivo de backup (str)

##### `restore_database(backup_path)`
Restaura o banco de dados a partir de um backup.

**Parâmetros**:
- `backup_path` (str): Caminho do backup

**Retorno**: Boolean indicando sucesso

#### Funções de Validação

##### `validate_project_data(name, description, project_type_id, start_date, end_date=None)`
Valida os dados de um projeto antes de salvar.

**Parâmetros**:
- `name` (str): Nome do projeto
- `description` (str): Descrição do projeto
- `project_type_id` (int): ID do tipo de projeto
- `start_date` (str): Data de início
- `end_date` (str, opcional): Data de término

**Retorno**: Lista de erros ou lista vazia se válido

##### `validate_project_type_data(name)`
Valida os dados de um tipo de projeto.

**Parâmetros**:
- `name` (str): Nome do tipo de projeto

**Retorno**: Lista de erros ou lista vazia se válido

##### `validate_platform_data(name)`
Valida os dados de uma plataforma.

**Parâmetros**:
- `name` (str): Nome da plataforma

**Retorno**: Lista de erros ou lista vazia se válido

#### Funções de Estatísticas

##### `get_project_statistics()`
Retorna estatísticas gerais dos projetos.

**Retorno**: Dicionário com estatísticas

##### `get_upcoming_project_deadlines(days=7)`
Retorna projetos com prazos se aproximando.

**Parâmetros**:
- `days` (int): Número de dias para considerar

**Retorno**: Lista de objetos Project

### Arquivo: `database/models.py`

Define as classes que representam os modelos de dados do sistema.

#### Classes

##### `ProjectType`
Representa um tipo de projeto.

**Atributos**:
- `id` (int): ID do tipo
- `name` (str): Nome do tipo
- `description` (str): Descrição do tipo

##### `Platform`
Representa uma plataforma.

**Atributos**:
- `id` (int): ID da plataforma
- `name` (str): Nome da plataforma
- `description` (str): Descrição da plataforma

##### `Project`
Representa um projeto.

**Atributos**:
- `id` (int): ID do projeto
- `name` (str): Nome do projeto
- `description` (str): Descrição do projeto
- `project_type_id` (int): ID do tipo de projeto
- `start_date` (str): Data de início
- `end_date` (str): Data de término
- `status` (str): Status do projeto

##### `ProjectPlatform`
Representa um registro de plataforma em um projeto.

**Atributos**:
- `id` (int): ID do registro
- `project_id` (int): ID do projeto
- `platform_id` (int): ID da plataforma
- `assigned_date` (str): Data de atribuição
- `description` (str): Descrição do registro

## Camada de Apresentação

### Arquivo: `app.py`

Ponto de entrada da aplicação Streamlit com dashboard inicial.

#### Configurações

##### `st.set_page_config()`
Configurações da página:
- Título: "DevFlow Manager"
- Ícone: "📋"
- Layout: wide
- Barra lateral: expandida

##### CSS Customizado
- Cores principais: Roxo (#6B46C1), Branco (#FFFFFF), Rosa claro (#F8BBD9)
- Estilos para botões, títulos, inputs
- Estilos para componente de linha do tempo

#### Funcionalidades

##### Dashboard Inicial
- Título e subtitulo
- Introdução ao sistema
- Estatísticas principais:
  - Total de projetos
  - Projetos ativos
  - Projetos concluídos
  - Status mais comum

##### Menu Lateral
- Links para todas as páginas
- Contador de notificações não lidas
- Informações do banco de dados
- Status de conexão

##### Inicialização
- Carrega variáveis de ambiente
- Inicializa banco de dados
- Exibe informações de status

### Arquivo: `pages/1_📋_Projetos.py`

Página principal de gerenciamento de projetos.

#### Abas
1. **Visualizar Projetos**: Lista e filtros
2. **Novo Projeto**: Formulário de criação
3. **Editar Projeto**: Formulário de edição

#### Funcionalidades

##### Visualizar Projetos
- Filtros por:
  - Busca textual
  - Tipo de projeto
  - Status
- Lista de projetos em cards
- Botão de detalhes para cada projeto

##### Detalhes do Projeto
- Informações básicas
- Histórico de plataformas (linha do tempo)
- Formulário para adicionar plataforma
- Gerenciamento de colaboradores

##### Novo Projeto
- Formulário com validação
- Campos: nome, descrição, tipo, datas, status
- Validação de dados antes de salvar

##### Editar Projeto
- Formulário pré-preenchido
- Edição de todos os campos
- Opção de exclusão

### Arquivo: `pages/2_🔧_Configurações.py`

Página para gerenciamento de configurações.

#### Abas
1. **Tipos de Projetos**: Gerenciamento de tipos
2. **Plataformas**: Gerenciamento de plataformas

#### Funcionalidades

##### Tipos de Projetos
- Listagem de tipos existentes
- Formulário para novo tipo
- Formulário para edição
- Exclusão de tipos

##### Plataformas
- Listagem de plataformas existentes
- Formulário para nova plataforma
- Formulário para edição
- Exclusão de plataformas

### Arquivo: `pages/3_📊_Relatórios.py`

Página para visualização de relatórios e estatísticas.

#### Funcionalidades
- KPIs principais:
  - Total de projetos
  - Projetos ativos
  - Projetos concluídos
- Gráficos:
  - Distribuição por status (pizza)
  - Distribuição por tipo (barra horizontal)
- Tabela detalhada de todos os projetos

### Arquivo: `pages/4_📤_Exportação.py`

Página para exportação e importação de dados.

#### Abas
1. **Exportar Dados**: Exportação para CSV
2. **Importar Dados**: Importação de CSV
3. **Backup**: Backup do banco de dados

#### Funcionalidades

##### Exportar Dados
- Botão para exportar todos os projetos
- Download automático do CSV
- Formatação adequada dos dados

##### Importar Dados
- Upload de arquivo CSV
- Validação do formato
- Importação com feedback de erros

##### Backup
- Botão para criar backup
- Download do arquivo de backup
- Nome automático com timestamp

### Arquivo: `pages/5_🔔_Notificações.py`

Página para visualização e gerenciamento de notificações.

#### Funcionalidades
- Listagem de notificações recentes
- Coloração por tipo de notificação
- Status de leitura
- Botão para marcar como lida

## Componentes Reutilizáveis

### Arquivo: `components/project_timeline.py`

Componente para exibir o histórico de plataformas em formato de linha do tempo.

#### Função: `render_project_timeline(platform_history)`

**Parâmetros**:
- `platform_history`: Lista de dicionários com informações de plataforma

**Funcionalidades**:
- Ordenação por data de atribuição
- Exibição visual com linha do tempo
- Estilização com CSS customizado
- Indicadores visuais por posição

#### Estilização
- Linha vertical indicando sequência
- Indicadores circulares por posição
- Cores consistentes com identidade visual
- Responsividade

## Funções Utilitárias

### Arquivo: `utils/helpers.py`

Funções auxiliares para formatação e manipulação de dados.

#### Funções Disponíveis

##### `format_date(date_str)`
Formata data para exibição no padrão DD/MM/AAAA.

**Parâmetros**:
- `date_str` (str): Data no formato YYYY-MM-DD

**Retorno**: Data formatada (str)

##### `validate_date(date_str)`
Valida formato de data.

**Parâmetros**:
- `date_str` (str): Data para validação

**Retorno**: Boolean indicando validade

##### `format_status(status)`
Formata status para exibição com emojis.

**Parâmetros**:
- `status` (str): Status original

**Retorno**: Status formatado com emoji (str)

##### `truncate_text(text, max_length=100)`
Trunca texto se for muito longo.

**Parâmetros**:
- `text` (str): Texto para truncar
- `max_length` (int): Comprimento máximo

**Retorno**: Texto truncado (str)

##### `format_currency(value)`
Formata valor monetário no padrão brasileiro.

**Parâmetros**:
- `value` (str/float): Valor para formatar

**Retorno**: Valor formatado (str)

## Testes

### Arquivo: `tests/test_database_functions.py`

Testes unitários para as funções de banco de dados.

#### Classes de Teste

##### `TestDatabaseFunctions`
Testes para todas as funções de CRUD e validação.

**Métodos de Setup**:
- `setUp()`: Cria banco de dados temporário
- `tearDown()`: Remove banco de dados temporário

**Testes Implementados**:
- `test_create_and_get_project_type()`: Criação e recuperação de tipos
- `test_create_and_get_platform()`: Criação e recuperação de plataformas
- `test_create_and_get_project()`: Criação e recuperação de projetos
- `test_add_platform_to_project()`: Adição de plataforma a projeto
- `test_validate_project_data()`: Validação de dados de projeto
- `test_validate_project_type_data()`: Validação de tipo de projeto
- `test_validate_platform_data()`: Validação de plataforma
- `test_update_project()`: Atualização de projeto
- `test_delete_project()`: Exclusão de projeto
- `test_notifications()`: Sistema de notificações
- `test_collaborators()`: Sistema de colaboradores

### Arquivo: `tests/test_integration.py`

Testes de integração para verificar o funcionamento conjunto das funcionalidades.

#### Classes de Teste

##### `TestIntegration`
Testes para fluxos completos do sistema.

**Testes Implementados**:
- `test_complete_project_workflow()`: Fluxo completo de projeto
- `test_export_import_workflow()`: Fluxo de exportação/importação

#### Estratégia de Testes

##### Banco de Dados Temporário
- Todos os testes usam banco de dados temporário
- Isolamento entre testes
- Limpeza automática após cada teste

##### Cobertura
- Testes para todas as funções CRUD
- Testes para validações
- Testes para funcionalidades avançadas
- Testes de integração entre módulos

## Configuração do Ambiente

### Requisitos

#### Software
- Python 3.8 ou superior
- Sistema operacional: Windows, macOS ou Linux
- Git (opcional, para versionamento)

#### Hardware
- Memória RAM: 2GB mínimo
- Espaço em disco: 500MB
- Processador: 1GHz mínimo

### Instalação

#### Método 1: Manual

1. **Clonar repositório**
   ```bash
   git clone <url-do-repositorio>
   cd DevFlow_Manager
   ```

2. **Criar ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

3. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Executar aplicação**
   ```bash
   streamlit run app.py
   ```

#### Método 2: Script de Setup

1. **Executar script de configuração**
   ```bash
   python setup.py
   ```

2. **Seguir instruções interativas**

#### Método 3: Script de Implantação

1. **Executar script de implantação**
   ```bash
   python deploy.py
   ```

2. **Seguir instruções automáticas**

### Variáveis de Ambiente

O sistema utiliza um arquivo `.env` para configurações:

```env
# .env
DB_HOST=localhost
DB_NAME=devflow_manager.db
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432
```

**Nota**: Para SQLite, apenas `DB_NAME` é utilizado. As outras variáveis são mantidas para compatibilidade futura.

### Dependências

#### Arquivo: `requirements.txt`

```txt
# requirements.txt
streamlit==1.31.0
python-dotenv==1.0.1
pandas==2.1.4
plotly==5.18.0
```

#### Descrição das Dependências

- **streamlit**: Framework web para interface
- **python-dotenv**: Gerenciamento de variáveis de ambiente
- **pandas**: Manipulação de dados (exportação CSV)
- **plotly**: Visualização de gráficos (relatórios)

## Implantação

### Local

#### Desenvolvimento
```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
streamlit run app.py
```

#### Produção Local
```bash
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

### Containerização

#### Docker

1. **Construir imagem**
   ```bash
   docker build -t devflow-manager .
   ```

2. **Executar container**
   ```bash
   docker run -p 8501:8501 devflow-manager
   ```

#### Docker Compose

1. **Subir serviços**
   ```bash
   docker-compose up -d
   ```

2. **Ver logs**
   ```bash
   docker-compose logs -f
   ```

3. **Parar serviços**
   ```bash
   docker-compose down
   ```

### Produção

#### Configurações Recomendadas
- Usar proxy reverso (nginx, Apache)
- Configurar SSL/TLS
- Implementar backup automático
- Monitorar logs
- Configurar cache (se necessário)

#### Performance
- O sistema é otimizado para até 1000 projetos
- Recomendado backup diário
- Monitoramento de uso de disco

## Manutenção

### Backup e Restauração

#### Backup Manual
```bash
# Copiar arquivo do banco de dados
cp devflow_manager.db backup_$(date +%Y%m%d_%H%M%S).db
```

#### Backup Automático
Utilizar o sistema de backup integrado:
1. Acessar página de exportação
2. Utilizar aba "Backup"
3. Fazer download do arquivo

#### Restauração
1. Parar aplicação
2. Substituir arquivo `devflow_manager.db`
3. Reiniciar aplicação

### Monitoramento

#### Logs
- O sistema não implementa logs em arquivo
- Erros são exibidos no console
- Monitorar saída do Streamlit

#### Métricas
- Estatísticas disponíveis na página de relatórios
- Contagem de projetos, status, tipos
- Alertas de prazos se aproximando

### Atualizações

#### Procedimento
1. Fazer backup do banco de dados
2. Baixar nova versão
3. Instalar dependências
4. Testar funcionalidades
5. Substituir arquivos (se necessário)

#### Compatibilidade
- Manter o mesmo formato de banco de dados
- Manter estrutura de tabelas
- Verificar dependências antes de atualizar

### Troubleshooting

#### Problemas Comuns

##### Banco de Dados Não Inicializa
- Verificar permissões de escrita
- Verificar caminho do arquivo
- Executar `init_db()` manualmente

##### Interface Não Carrega
- Verificar dependências instaladas
- Verificar ambiente virtual ativado
- Verificar porta 8501 disponível

##### Erros de Conexão
- Verificar arquivo `.env`
- Verificar permissões de arquivo
- Verificar existência do banco de dados

#### Soluções

##### Reset de Banco de Dados
```bash
# Remover arquivo de banco de dados
rm devflow_manager.db

# Executar aplicação (cria novo banco)
streamlit run app.py
```

##### Reinstalação de Dependências
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Segurança

#### Considerações
- Dados armazenados localmente
- Não implementa autenticação
- Acesso restrito ao servidor
- Backup regular recomendado

#### Recomendações
- Não expor publicamente sem autenticação
- Implementar proxy com autenticação
- Configurar firewall
- Monitorar acesso

### Desempenho

#### Otimizações
- Consultas SQL otimizadas com índices
- Cache de dados em memória (Streamlit)
- Paginação não implementada (até 1000 projetos)
- Consultas eficientes para listagens

#### Limitações
- Não recomendado para mais de 1000 projetos
- Sem cache de disco
- Sem otimização para alta concorrência
- Interface não otimizada para mobile (funciona, mas não ideal)

### Extensibilidade

#### Adição de Funcionalidades
- Novas páginas em `pages/`
- Novos componentes em `components/`
- Novas funções em `database/connection.py`
- Novas utilidades em `utils/helpers.py`

#### Integrações
- API REST (implementar separadamente)
- Conexão com outros bancos (modificar `connection.py`)
- Integração com serviços externos
- Autenticação e autorização (adicionar camada de segurança)