from sqlalchemy.orm import Session

from backend.config import settings
from backend.models.db import Employee
from backend.rag.faiss_index import faiss_store
from backend.services.embeddings import embed_text
from backend.services.gigachat import gigachat_client


SYSTEM_PROMPT = (
    "Ты HR-ассистент. Отвечай только на основе предоставленного контекста и данных сотрудника. "
    "Не выдумывай. Если ответа нет в контексте, так и скажи и предложи обратиться в HR. "
    "В конце ответа коротко укажи, что источник обязателен."
)


def build_user_prompt(question: str, employee: Employee, contexts: list[dict]) -> str:
    context_block = "\n\n".join(
        f"[{item['document']} | {item['section']}]\n{item['text']}" for item in contexts
    )
    employee_block = (
        f"ФИО: {employee.full_name}\n"
        f"Должность: {employee.position}\n"
        f"Подразделение: {employee.department}\n"
        f"Остаток отпуска: {employee.vacation_days}\n"
        f"Ближайший отпуск: {employee.nearest_vacation}\n"
        f"ДР: {employee.birthday}\n"
    )
    return (
        f"Вопрос сотрудника: {question}\n\n"
        f"Данные сотрудника:\n{employee_block}\n"
        f"Контекст документов:\n{context_block}\n\n"
        "Сформируй ответ сотруднику на русском языке."
    )


def ask_hr_assistant(question: str, employee: Employee, db: Session) -> tuple[str, list[dict], bool]:
    _ = db  # kept for future extension
    query_vector = embed_text(question)
    contexts = faiss_store.search(query_vector, settings.rag_top_k)

    if not contexts:
        answer = (
            "Не нашёл подтверждённого ответа в базе знаний. "
            "Рекомендую обратиться в HR-отдел и приложить регламент, если он у вас есть."
        )
        return answer, [{"document": "HR escalation", "section": "unanswered"}], True

    prompt = build_user_prompt(question, employee, contexts)
    answer = gigachat_client.chat(SYSTEM_PROMPT, prompt)
    sources = [{"document": item["document"], "section": item["section"]} for item in contexts]
    return answer, sources, False
