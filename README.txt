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
- `POST /auth/login` - вход по email или tab number + password, выдача JWT.
- `GET /users/me` - профиль сотрудника.
- `POST /chat` - вопрос сотрудника, ответ + источники.
- `POST /admin/documents` - загрузка PDF/DOCX/TXT/MD и индексация.
- `GET /admin/logs` - журнал вопросов/ответов.
- `GET /admin/logs/unanswered` - вопросы без ответа.
- `CRUD /users` - админ-управление сотрудниками.

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

6) Интеграция с frontend (без изменения UI)
- Используйте готовый API-клиент: `app/api_client.js`.
- Логика:
  - логин: `login(login, password)`
  - получить профиль: `getMyProfile()`
  - отправить вопрос: `askChat(question)`
- Ответ чата содержит:
  - `answer`
  - `sources` (`document`, `section`)
  - `unanswered`

7) Демо-пользователи (seed)
- `work@portal-test.1221systems.ru` / `1001` / `password123`
- `hr@portal-test.1221systems.ru` / `3001` / `password123` (admin)
