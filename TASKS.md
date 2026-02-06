# Backlog (MVP execution)

## Sprint 1 — Foundation
- [ ] Создать структуру `backend/ frontend/ workers/ infra/`.
- [ ] FastAPI skeleton + healthcheck + OpenAPI.
- [ ] JWT auth + роли `admin`, `manager`.
- [ ] PostgreSQL + Alembic миграции.
- [ ] Таблицы: users, leads, lead_statuses, lead_status_history.

## Sprint 2 — Parsing Core
- [ ] Реализовать коннектор Яндекс Карт.
- [ ] Реализовать коннектор сайтов компаний.
- [ ] Подготовить базовый коннектор 2ГИС (пилот).
- [ ] Нормализация полей и валидация форматов контактов.
- [ ] Дедупликация: phone -> website -> name+address.
- [ ] Confidence score 0–100.

## Sprint 3 — Call-center Flow
- [ ] Очередь лидов для менеджера (пакетная выдача).
- [ ] Карточка лида: данные + скрипт звонка + комментарий.
- [ ] Статусы звонка и таймлайн изменений.
- [ ] SLA задачи: перезвон и напоминания.

## Sprint 4 — Delivery
- [ ] Экспорт CSV/XLSX.
- [ ] Экспорт в Google Sheets.
- [ ] Аудит-лог + график активности пользователей.
- [ ] Docker Compose окружение для MVP.
- [ ] Smoke-тесты критического флоу и release checklist.
