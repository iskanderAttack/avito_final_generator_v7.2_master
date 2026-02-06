# ERD (MVP) — логическая схема данных

## Сущности

### users
- id (PK)
- email (unique)
- password_hash
- full_name
- role (`admin`, `manager`)
- is_active
- created_at

### lead_sources
- id (PK)
- type (`yandex_maps`, `2gis`, `website`)
- name
- config_json
- is_active
- created_at

### leads
- id (PK)
- external_id (nullable)
- name
- category
- address
- city
- region
- phone
- email
- website
- inn (nullable)
- ogrn (nullable)
- source_id (FK -> lead_sources.id)
- source_url
- confidence_score
- dedup_hash
- current_status_id (FK -> lead_statuses.id)
- assigned_to_user_id (FK -> users.id, nullable)
- created_at
- updated_at

### lead_statuses
- id (PK)
- code (unique)
- title
- is_final
- sort_order

### lead_status_history
- id (PK)
- lead_id (FK -> leads.id)
- from_status_id (FK -> lead_statuses.id, nullable)
- to_status_id (FK -> lead_statuses.id)
- changed_by_user_id (FK -> users.id)
- comment
- created_at

### call_tasks
- id (PK)
- lead_id (FK -> leads.id)
- assigned_to_user_id (FK -> users.id)
- due_at
- priority
- status (`open`, `done`, `overdue`)
- created_at

### call_logs
- id (PK)
- lead_id (FK -> leads.id)
- user_id (FK -> users.id)
- call_result_code
- comment
- duration_sec (nullable)
- created_at

### call_scripts
- id (PK)
- title
- body_md
- is_active
- created_by_user_id (FK -> users.id)
- created_at

### lead_script_links
- id (PK)
- lead_id (FK -> leads.id)
- script_id (FK -> call_scripts.id)
- assigned_at

### audit_logs
- id (PK)
- user_id (FK -> users.id)
- action
- entity_type
- entity_id
- payload_json
- created_at

## Основные связи
- `lead_sources 1 -> N leads`
- `users 1 -> N leads (assigned_to_user_id)`
- `leads 1 -> N lead_status_history`
- `leads 1 -> N call_logs`
- `leads 1 -> N call_tasks`
- `users 1 -> N call_logs`
- `users 1 -> N audit_logs`
