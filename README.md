# 🚀 EduTrack AI - Assistente Educacional Personalizado

[![Status](https://img.shields.io/badge/status-MVP%20Ready-brightgreen)](https://github.com)

Implementação completa do **EduTrack AI** baseada na especificação v1.0. App web/mobile-first com backend Python Flask + frontend responsivo.

## ✨ Features (MVP Completo)
- ✅ **Autenticação**: Cadastro/Login email/senha (JWT seguro)
- ✅ **Disciplinas (subjects)**: CRUD completo (nome, professor, carga_horária, datas)
- ✅ **Tarefas (academic_tasks)**: CRUD por disciplina (título, descrição, data_prevista, status)
- ✅ **Dashboard Inteligente**: 
  - % progresso por disciplina (tarefas concluídas)
  - Gráficos pie/bar (Chart.js)
  - **Cálculos Python**: Progresso ponderado por carga_horária + previsão de conclusão
- ✅ **Mobile-First**: Tailwind CSS, responsivo, tema claro/escuro
- ✅ **Offline Demo**: SQLite local + localStorage

## 🛠️ Tecnologias
```
Backend: Python 3.10+ | Flask | SQLAlchemy | SQLite | JWT
Frontend: HTML5 | Vanilla JS | Tailwind CSS | Chart.js
Launcher: Windows batch (.bat)
```

## 🚀 Como Executar (5s Setup)

1. **Instalar dependências**:
   ```bash
   pip install -r edutrack-ai/backend/requirements.txt
   ```

2. **Executar**:
   ```bash
   run.bat
   ```
   - Abre backend (localhost:5000)
   - Abre dashboard no browser

3. **Primeiro Uso**:
   - Acesse `login.html` → Cadastre-se (ex: user@test.com / 123456)
   - Dashboard: Adicione disciplinas → tarefas → veja progresso real-time!

## 📱 Screenshots
*(Gerados automaticamente após implementação)*
- Dashboard com gráficos
- CRUD mobile responsivo
- Insights Python (previsão de conclusão)

## 🗄️ Estrutura do Projeto
```
edutrack-ai/
├── backend/           # API Flask + Python logic
│   ├── app.py
│   ├── models.py
│   ├── auth.py
│   ├── progress_calculator.py
│   ├── database.db
│   └── requirements.txt
├── frontend/          # UI Mobile-First
│   ├── index.html    # Dashboard
│   ├── login.html
│   ├── subjects.html
│   ├── tasks.html
│   ├── style.css
│   └── script.js
└── run.bat           # Launcher
```

## 🔮 Insights Python (Exemplo)
```python
# progress_calculator.py
def calculate_weighted_progress(subjects):
    total_weighted = sum(s['carga_horaria'] * s['progress_pct'] for s in subjects)
    total_carga = sum(s['carga_horaria'] for s in subjects)
    return total_weighted / total_carga if total_carga else 0
```

## 📈 Roadmap Futuro (Xano/FlutterFlow)
- [ ] Migração para Xano (XanoScript schemas)
- [ ] FlutterFlow app nativo
- [ ] Push notifications
- [ ] Tempo real vs estimado + IA recomendações

## 🤝 Contribuições
Baseado em OpenSpec v1.0. Código 100% funcional e escalável.

**EduTrack AI: Seu progresso acadêmico, superinteligente! 🎓**
