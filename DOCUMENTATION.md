# 📚 Documentação Completa - EduTrack AI

## 1. Visão Geral do Projeto

**EduTrack AI** é um aplicativo web educacional personalizado desenvolvido para ajudar estudantes a acompanhar seu progresso acadêmico de forma inteligente. O projeto consiste em um sistema completo com backend em Flask (Python) e frontend responsivo mobile-first.

### 1.1 Objetivo
O objetivo principal é fornecer uma ferramenta que permita aos estudantes gerenciar suas disciplinas acadêmicas, acompanhar tarefas e visualizar o progresso ponderado por carga horária, com insights e previsões de conclusão.

### 1.2 Repositório
- **URL**: https://github.com/VitorNunes1/Projeto---EduTrack-AI
- **Stack**: Flask + SQLAlchemy + SQLite (Backend) | HTML5 + Vanilla JS + Tailwind CSS (Frontend)

---

## 2. Arquitetura do Sistema

### 2.1 Estrura de Diretórios

```
edutrack-ai/
├── backend/                    # API REST Python
│   ├── app.py               # Aplicação principal Flask
│   ├── models.py            # Modelos SQLAlchemy
│   ├── auth.py              # Funções de autenticação
│   ├── progress_calculator.py  # Cálculos de progresso
│   ├── requirements.txt    # Dependências Python
│   ├── smoke_test.py        # Testes básicos
│   └── instance/
│       └── database.db     # Banco SQLite local
│
├── frontend/                 # Interface HTML/JS
│   ├── index.html          # Dashboard principal
│   ├── login.html         # Página de login/cadastro
│   ├── subjects.html      # Gerenciamento de disciplinas
│   ├── tasks.html        # Gerenciamento de tarefas
│   ├── script.js        # Cliente API + funções UX
│   └── style.css        # Estilos CSS (tema light/dark)
│
└── run.bat                 # Script de inicialização (Windows)
```

### 2.2 Modelo Cliente-Servidor

```
┌─────────────────┐      HTTP/REST       ┌─────────────────┐
│   Frontend      │ ◄─────────────────► │   Backend        │
│   (Browser)     │    JSON + JWT      │   (Flask)       │
│                 │                    │                 │
│  - HTML5        │                    │  - Python 3.10+ │
│  - Tailwind CSS│                    │  - Flask        │
│  - Chart.js     │                    │  - SQLAlchemy   │
│  - Vanilla JS  │                    │  - Flask-JWT    │
└─────────────────┘                    └─────────────────┘
        │                                         │
        ▼                                         ▼
   localStorage                            SQLite Database
   (Token JWT)                            (instance/database.db)
```

---

## 3. Backend - API Flask

### 3.1 Arquivo: app.py

**Descrição**: Aplicação principal Flask que expõe a API REST.

**Porta**: 5000 (desenvolvimento)

**Endpoints disponíveis**:

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | `/api/auth/register` | Cadastro de novo usuário | Não |
| POST | `/api/auth/login` | Login e geração de token JWT | Não |
| GET | `/api/subjects` | Listar disciplinas do usuário | JWT |
| POST | `/api/subjects` | Criar nova disciplina | JWT |
| PUT | `/api/subjects/<id>` | Atualizar disciplina | JWT |
| DELETE | `/api/subjects/<id>` | Excluir disciplina | JWT |
| GET | `/api/tasks/<subject_id>` | Listar tarefas de uma disciplina | JWT |
| POST | `/api/tasks/<subject_id>` | Criar nova tarefa | JWT |
| PUT | `/api/tasks/<task_id>` | Atualizar tarefa | JWT |
| DELETE | `/api/tasks/<task_id>` | Excluir tarefa | JWT |
| GET | `/api/dashboard` | Obter dados do dashboard | JWT |

### 3.2 Arquivo: models.py

**Descrição**: Modelos de banco de dados usando SQLAlchemy.

**Modelos definidos**:

#### User (Usuário)
```
Tabela: user
Campos:
  - id (Integer, PK) - Identificador único
  - email (String 120, UNIQUE) - Email do usuário
  - password_hash (String 128) - Hash da senha (Werkzeug)
  - created_at (DateTime) - Data de criação

Métodos:
  - set_password(password) - Define hash da senha
  - check_password(password) - Verifica senha
```

#### Subject (Disciplina)
```
Tabela: subject
Campos:
  - id (Integer, PK) - Identificador único
  - user_id (Integer, FK) - Referência ao usuário
  - name (String 100) - Nome da disciplina
  - professor (String 100) - Nome do professor
  - carga_horaria (Float) - Carga horária em horas (padrão: 60.0)
  - peso (Float) - Peso para cálculo ponderado (padrão: 1.0)
  - description (Text) - Descrição da disciplina
  - data_inicio (Date) - Data de início
  - data_fim (Date) - Data de término
  - created_at (DateTime) - Data de criação

Relacionamentos:
  - user (relação com User)
  - academic_tasks (relação com AcademicTask, cascade delete)
```

#### AcademicTask (Tarefa Acadêmica)
```
Tabela: academic_task
Campos:
  - id (Integer, PK) - Identificador único
  - subject_id (Integer, FK) - Referência à disciplina
  - title (String 200) - Título da tarefa
  - description (Text) - Descrição da tarefa
  - data_prevista (Date) - Data prevista para conclusão
  - status (String) - Status: 'pendente', 'em_andamento', 'concluida'
  - created_at (DateTime) - Data de criação

Status possíveis:
  - 'pendente' - Tarefa não iniciada (padrão)
  - 'em_andamento' - Tarefa em progresso
  - 'concluida' - Tarefa concluída
```

### 3.3 Arquivo: auth.py

**Descrição**: Funções de autenticação e autorização.

**Funções exportadas**:

1. `register_user()`
   - Recebe email e senha via JSON
   - Verifica se email já existe
   - Cria novo usuário com senha hasheada
   - Retorna mensagem de sucesso ou erro 400

2. `login_user()`
   - Recebe email e senha via JSON
   - Busca usuário pelo email
   - Verifica senha com hash
   - Gera token JWT com validade de 24 horas
   - Retorna access_token e user_id

3. `get_current_user()`
   - Extrai identity do token JWT
   - Busca usuário no banco
   - Retorna objeto User ou None

### 3.4 Arquivo: progress_calculator.py

**Descrição**: Funções de cálculo de progresso acadêmico.

**Funções exportadas**:

1. `calculate_subject_progress(subject_id, db_session)`
   - Calcula progresso básico de uma disciplina
   - Retorna: dict com progress_pct, total_tasks, completed_tasks

2. `calculate_weighted_progress(user_id, db_session)`
   - Calcula progresso ponderado por carga horária
   - Considera cada disciplina multiplicada por sua carga horária
   - Retorna: dict com weighted_progress, total_carga_horaria, subjects[]

3. `predict_completion_date(user_id, db_session)`
   - Prediz data de conclusão baseada em velocidade média
   - Assume 5% de progresso por semana
   - Retorna: dict com predicted_date, days_remaining, assumption

**Fórmula do Progresso Ponderado**:
```
weighted_progress = Σ(carga_horaria_i × progress_pct_i) / Σ(carga_horaria_i)
```

### 3.5 Arquivo: requirements.txt

**Dependências Python do projeto**:
```
Flask==3.0.3
Flask-CORS==4.0.1
Flask-SQLAlchemy==3.1.1
Flask-JWT-Extended==4.6.0
Werkzeug==3.0.3
python-dotenv==1.0.1
bcrypt==4.1.3
```

---

## 4. Frontend - Interface Web

### 4.1 Arquivo: script.js

**Descrição**: Cliente API e funções de experiência do usuário.

**Constantes**:
- `API_BASE = 'http://localhost:5000/api'`

**Funções principais**:

#### Autenticação
- `register(email, password)` - Cadastra novo usuário
- `login(email, password)` - Faz login e armazena token
- `logout()` - Remove token e redireciona para login

#### Disciplinas (Subjects)
- `getSubjects()` - Lista todas as disciplinas
- `createSubject(payload)` - Cria disciplina
- `updateSubject(id, payload)` - Atualiza disciplina
- `deleteSubject(id)` - Remove disciplina

#### Tarefas (Tasks)
- `getTasks(subjectId)` - Lista tarefas de uma disciplina
- `createTask(subjectId, payload)` - Cria tarefa
- `updateTask(taskId, payload)` - Atualiza tarefa
- `deleteTask(taskId)` - Remove tarefa

#### Dashboard
- `getDashboard()` - Obtém dados do dashboard

#### Utilities
- `showMessage(message, type)` - Exibe notificação toast
- `showLoader(show)` - Mostra/esconde loader
- `toggleTheme()` - Alterna entre tema claro e escuro
- `initCharts(canvasId, data, type)` - Inicializa gráfico Chart.js

### 4.2 Arquivo: style.css

**Descrição**: Estilos CSS com suporte a tema claro/escuro.

**Variáveis CSS (Custom Properties)**:

```css
/* Tema Escuro (padrão) */
:root {
  --bg: #0b1020;
  --bg-soft: #111831;
  --surface: #151f3d;
  --surface-2: #1a274a;
  --text: #f8fafc;
  --text-muted: #94a3b8;
  --border: #2a3a64;
  --primary: #7c8cff;
  --success: #22c55e;
  --warning: #f59e0b;
  --danger: #ef4444;
}

/* Tema Claro */
:root[data-theme="light"] {
  --bg: #f1f5f9;
  --surface: #ffffff;
  --text: #0f172a;
  --text-muted: #475569;
  --border: #dbe2ef;
  --primary: #4f46e5;
}
```

**Componentes estilizados**:
- Cards, botões, inputs
- Tabelas, badges, chips
- Toast notifications
- Loader de carregamento
- Gráficos (Chart.js)
- Modal, navbar
- Status pills (pendente/concluída)

### 4.3 Páginas HTML

#### login.html
- Página de autenticação
- Formulário de login (email/senha)
- Formulário de cadastro para novos usuários
- Redireciona para dashboard após login

#### index.html (Dashboard)
- Visão geral acadêmica
- Cards com métricas:
  - Progresso Geral (%)
  - Carga Horária Total (h)
  - Tarefas Concluídas
  - Tarefas Pendentes
- Gráfico de rosca (progresso por disciplina)
- Previsão de conclusão
- Insight IA (recomendações)
- Lista de disciplinas em foco

#### subjects.html
- CRUD de disciplinas
- Formulário para criar/editar:
  - Nome da disciplina
  - Professor
  - Carga horária
  - Peso
  - Descrição
  - Data de início/término
- Lista de disciplinas com ações

#### tasks.html
- CRUD de tarefas por disciplina
- Seleção de disciplina
- Formulário para criar/editar:
  - Título
  - Descrição
  - Data prevista
  - Status
- Lista de tarefas com ações

---

## 5. Funcionamento do Sistema

### 5.1 Fluxo de Autenticação

```
1. Usuário acessa login.html
2. Escolhe criar conta ou fazer login
3. Sistema verifica credenciais
4. Backend retorna JWT token (24h)
5. Frontend armazena token no localStorage
6. Usuário redirecionado para dashboard
```

### 5.2 Fluxo de Gerenciamento

```
Disciplinas:
1. Usuário cria disciplina com carga horária
2. Sistema associa disciplina ao usuário
3. Usuário pode editar ou excluir

Tarefas:
1. Usuário seleciona disciplina
2. Cria tarefas para essa disciplina
3. Atualiza status (pendente → concluída)
4. Sistema calcula progresso automaticamente
```

### 5.3 Fluxo do Dashboard

```
1. Dashboard chama API /api/dashboard
2. Backend calcula:
   a. Progresso de cada disciplina
   b. Progresso ponderado por carga horária
   c. Previsão de conclusão
3. Frontend exibe:
   a. Gráfico de rosca
   b. Métricas em cards
   c. Insight IA
```

---

## 6. Glossário de Termos

| Termo | Significado |
|-------|-------------|
| API | Application Programming Interface - interface de comunicação |
| JWT | JSON Web Token - token de autenticação stateless |
| CRUD | Create, Read, Update, Delete - operações básicas |
| SQLAlchemy | ORM Python para banco de dados |
| Flask | Framework web Python |
| Tailwind CSS | Framework CSS utility-first |
| Chart.js | Biblioteca JavaScript para gráficos |
| Progresso Ponderado | Média ponderada pela carga horária |
| localStorage | Armazenamento local no navegador |

---

## 7. Configurações de Desenvolvimento

### 7.1 Variáveis de Ambiente

```python
# app.py configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'edutrack-super-secret-key-2026'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Long-lived for demo
```

### 7.2 Banco de Dados

- **Tipo**: SQLite (arquivo local)
- **Localização**: `instance/database.db`
- **Criação**: Automática ao iniciar o app (`db.create_all()`)

### 7.3 Servidor

- **Host**: 127.0.0.1 (localhost)
- **Porta**: 5000
- **Modo**: Debug ativado
- **URL Base**: http://localhost:5000

---

## 8. Executando oProjeto

### 8.1 Instalação de Dependências

```bash
cd edutrack-ai/backend
pip install -r requirements.txt
```

### 8.2 Inicialização do Servidor

```bash
cd edutrack-ai/backend
python app.py
```

### 8.3 Acesso à Aplicação

- Login: http://localhost:5000/edutrack-ai/frontend/login.html
- Dashboard: http://localhost:5000/edutrack-ai/frontend/index.html

---

## 9. Fluxo de Dados Completo

```
┌──────────────┐     POST /api/auth/register      ┌──────────────┐
│  Frontend    │ ─────────────────────────────► │   Backend    │
│  (login)    │                              │   (Flask)    │
└──────────────┘                              └──────────────┘
                                                  │
                                                  ▼
                                            ┌──────────────┐
                                            │  SQLite DB  │
                                            │  (User)    │
                                            └──────────────┘

┌──────────────┐     POST /api/subjects       ┌──────────────┐
│  Frontend    │ ─────────────────────────────► │   Backend    │
│ (subjects)  │                              │   (Flask)    │
└──────────────┘                              └──────────────┘
                                                  │
                                                  ▼
                                            ┌──────────────┐
                                            │  SQLite DB  │
                                            │ (Subject) │
                                            └──────────────┘

┌──────────────┐     GET /api/dashboard       ┌──────────────┐
│  Frontend   │ ──────────────────────────► │   Backend    │
│ (index)    │                            │   (Flask)    │
└──────────────┘                            └──────────────┘
       │                                         │
       │    JSON +                               ▼
       │    weighted_progress            ┌──────────────┐
       │    subjects[]               │   progress_  │
       │    prediction             │ calculator  │
       │                          └──────────────┘
       │                                 │
       ▼                                 ▼
┌──────────────┐                  ┌──────────────┐
│  Dashboard  │                  │  SQLite DB  │
│   (UI)     │                  │(Tasks + Subs)│
└──────────────┘                  └──────────────┘
```

---

## 10. Histórico de Versões

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0.0 | 2026 | MVP - Primeira versão funcional |

---

**Documentação gerada automaticamente para o projeto EduTrack AI**
**Última atualização: 2026**
