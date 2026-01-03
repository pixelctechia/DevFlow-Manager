# DevFlow Manager

**Sistema de Gestão de Soluções Web**

O **DevFlow Manager** é um sistema completo para controle e gerenciamento de projetos de desenvolvimento web (SaaS, MicroSaaS, Landing Pages, Sites), permitindo o acompanhamento de prazos, colaboradores, histórico de plataformas e relatórios detalhados.

## 📋 Características

- **Dashboard Interativo**: Visão geral dos projetos, status e métricas.
- **Gestão de Projetos**: Cadastro, edição e exclusão de projetos.
- **Linha do Tempo**: Histórico visual das plataformas utilizadas em cada projeto.
- **Colaboradores**: Gerenciamento de equipe por projeto.
- **Relatórios**: Gráficos e tabelas para análise de desempenho.
- **Exportação/Importação**: Backup de dados em CSV e SQLite.
- **Notificações**: Alertas de prazos e atualizações do sistema.

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.8+
- **Framework Web**: Streamlit
- **Banco de Dados**: SQLite
- **Visualização de Dados**: Plotly
- **Interface**: CSS Customizado (Tema Roxo/Branco)

## 📁 Estrutura de Arquivos

```
DevFlow Manager/
├── app.py                    # Aplicação principal
├── requirements.txt          # Dependências
├── database_setup.sql        # Script SQL inicial
├── .gitignore               # Arquivos ignorados pelo Git
├── README.md                # Documentação
├── database/                # Lógica de banco de dados
│   ├── connection.py        # CRUD
│   └── models.py            # Modelos
├── pages/                   # Páginas do sistema
│   ├── 1_📋_Projetos.py
│   ├── 2_🔧_Configurações.py
│   ├── 3_📊_Relatórios.py
│   ├── 4_📤_Exportação.py
│   └── 5_🔔_Notificações.py
├── components/              # Componentes visuais
├── utils/                   # Utilitários e helpers
├── tests/                   # Testes automatizados
└── docs/                    # Documentação técnica
```

## 🚀 Instalação e Execução

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/pixelctechia/DevFlow-Manager.git
   cd DevFlow-Manager
   ```

2. **Crie e ative um ambiente virtual (recomendado):**
   ```bash
   # Windows
   python -m venv .venv
   .\.venv\Scripts\activate

   # Linux/Mac
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação:**
   ```bash
   streamlit run app.py
   ```

## 📄 Licença

Este projeto é de uso privado/interno.

---
**Desenvolvido por PixelC Tech**
