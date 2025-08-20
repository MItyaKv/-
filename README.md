# -# Task Manager (FastAPI)

Простое REST API для управления задачами (CRUD) с тестами.

## Возможности
- CRUD для задач
- Поля задачи: `id` (UUID), `title`, `description`, `status` (`created`, `in_progress`, `done`)
- Авто-документация Swagger доступна по адресу `/docs`

## Требования
- Python 3.10+
- SQLite (встроенный используется по умолчанию)

## Установка и запуск
```bash
git clone <repo>
cd task-manager
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
