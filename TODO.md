# EduTrack AI — TODO

## ✅ Concluído
- [x] Backend Flask com JWT, modelos `User`, `Subject`, `AcademicTask` (snake_case conforme spec)
- [x] Endpoints REST completos: auth, subjects (CRUD), tasks (CRUD), dashboard
- [x] `Subject` com todos os campos da spec: `name`, `professor`, `carga_horaria`, `peso`, `description`, `data_inicio`, `data_fim`
- [x] Cascade delete (Subject → AcademicTasks) corrigido
- [x] Dashboard com progresso ponderado por peso/carga, previsão de conclusão e insight inteligente
- [x] Frontend redesenhado com design system profissional (tokens CSS, Inter, dark/light)
- [x] `login.html`: split design + toggle login/registro + tema
- [x] `index.html`: 4 metric cards, doughnut chart, previsão IA, lista por disciplina, tema toggle
- [x] `subjects.html`: CRUD completo (todos os campos), busca, ordenação, visualização Cartões/Tabela
- [x] `tasks.html`: filtros (disciplina, busca, status, ordenação), métricas, edição/exclusão, indicador de atrasada
- [x] `script.js`: API helper com tratamento de erros, toasts, loader global, theme toggle, auth guard, charts
- [x] Smoke test (`smoke_test.py`) — 14 cenários, **todos OK**

## 🔮 Backlog futuro (fora do MVP atual)
- [ ] Tempo estimado/real por tarefa + recomendações IA comparativas
- [ ] Geração de relatórios PDF semanais
- [ ] Push notifications de prazos
- [ ] Recuperação de senha por e-mail
