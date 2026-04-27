from sqlalchemy.orm import Session

from backend.auth.jwt import hash_password
from backend.models.db import Employee


def seed_employees(db: Session) -> None:
    if db.query(Employee).count() > 0:
        return

    demo = [
        Employee(
            tab_number="1001",
            email="work@portal-test.1221systems.ru",
            full_name="Алексей Рабочев",
            position="Специалист производственного блока",
            department="Производственный блок",
            manager="Мария Директорова",
            vacation_days=14,
            nearest_vacation="15.07.2026 - 28.07.2026",
            birthday="18 октября",
            role="employee",
            password=hash_password("password123"),
        ),
        Employee(
            tab_number="3001",
            email="hr@portal-test.1221systems.ru",
            full_name="Анна HR",
            position="HR-специалист",
            department="HR-департамент",
            manager="Директор по персоналу",
            vacation_days=18,
            nearest_vacation="10.09.2026 - 23.09.2026",
            birthday="12 марта",
            role="admin",
            password=hash_password("password123"),
        ),
    ]
    db.add_all(demo)
    db.commit()
