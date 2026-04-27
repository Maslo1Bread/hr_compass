HR Assistant API (FastAPI + SQLite + FAISS + GigaChat)

1) Установка и запуск
- Скопируйте `.env.example` в `.env` и заполните `GIGACHAT_CREDENTIALS`.
- Запустите `start_windows.bat`.
- API будет доступен на `http://127.0.0.1:8000`.
- Swagger: `http://127.0.0.1:8000/docs`

2) Архитектура
- `backend/main.py` - вход в приложение, middleware, роуты.
- `backend/auth/` - JWT, зависимости авторизации.
- `backend/models/` - SQLAlchemy модели и Pydantic схемы.
- `backend/routes/` - API (`/auth`, `/users`, `/chat`, `/admin`).
- `backend/services/` - бизнес-логика (чат, GigaChat, логи, bootstrap).
- `backend/rag/` - парсинг документов, чанкинг, FAISS индекс.

3) Основные endpoint'ы
- `POST /auth/login` - вход по email + password, выдача JWT.
- `GET /users/me` - профиль сотрудника.
- `POST /chat` - вопрос сотрудника, ответ + источники.
- `POST /admin/documents` - загрузка PDF/DOCX/TXT/MD и индексация.
- `GET /admin/logs` - журнал вопросов/ответов.
- `GET /admin/logs/unanswered` - вопросы без ответа.
- `CRUD /users` - управление сотрудниками (руководитель и HR-менеджер по ролевым правилам).
- `POST /users/{id}/assign-hr` - руководитель назначает сотрудника HR-менеджером.
- `POST /hr-chat/call` - работник вызывает HR и открывает тикет.
- `GET /hr-chat/my` - список HR-чатов для работника/HR-менеджера.
- `GET /hr-chat/{id}/messages` - сообщения по тикету.
- `POST /hr-chat/{id}/messages` - ответ HR-менеджера в тикете.

4) RAG pipeline
- Документ загружается через `/admin/documents`.
- Текст извлекается из PDF/DOCX/TXT/MD.
- Текст режется на чанки.
- Чанки индексируются в FAISS.
- `/chat` делает поиск top-k, формирует prompt c контекстом + профилем сотрудника.
- Ответ генерируется через GigaChat.
- Если контекст не найден - возвращается честный fallback с рекомендацией обратиться в HR.

5) Логи
- Все запросы сохраняются в `chat_logs`.
- `is_unanswered=true` для вопросов без ответа из базы знаний.

6) Роли и права
- `manager`:
  - загружает документы в базу знаний;
  - назначает HR-менеджеров из существующих работников;
  - создает аккаунты работников.
- `hr_manager`:
  - создает аккаунты работников;
  - изменяет данные работников (отпуск, даты и т.д.);
  - ведет переписку с работниками в HR-чатах.
- `worker`:
  - общается с чат-ботом;
  - вызывает HR через HR-чат;
  - просматривает список документов.

7) Интеграция с frontend (без изменения UI)
- Используйте готовый API-клиент: `app/api_client.js`.
- Логика:
  - логин: `login(email, password)`
  - получить профиль: `getMyProfile()`
  - отправить вопрос: `askChat(question)`
- Ответ чата содержит:
  - `answer`
  - `sources` (`document`, `section`)
  - `unanswered`

8) Демо-пользователи (seed)
- `work@portal-test.1221systems.ru` / `password123` (`worker`)
- `dir@portal-test.1221systems.ru` / `password123` (`manager`)
- `hr@portal-test.1221systems.ru` / `password123` (`hr_manager`)
