from sqlalchemy.orm import Session

from backend.auth.jwt import hash_password
from backend.models.db import Employee


def seed_employees(db: Session) -> None:
    demo = {
        "work@portal-test.1221systems.ru": Employee(
            tab_number="1001",
            email="work@portal-test.1221systems.ru",
            full_name="Алексей Рабочев",
            position="Специалист производственного блока",
            department="Производственный блок",
            manager="Мария Директорова",
            vacation_days=14,
            nearest_vacation="15.07.2026 - 28.07.2026",
            birthday="18 октября",
            role="worker",
            password=hash_password("password123"),
        ),
        "dir@portal-test.1221systems.ru": Employee(
            tab_number="2001",
            email="dir@portal-test.1221systems.ru",
            full_name="Мария Директорова",
            position="Руководитель операционного департамента",
            department="Операционный департамент",
            manager="CEO",
            vacation_days=21,
            nearest_vacation="03.08.2026 - 16.08.2026",
            birthday="7 мая",
            role="manager",
            password=hash_password("password123"),
        ),
        "hr@portal-test.1221systems.ru": Employee(
            tab_number="3001",
            email="hr@portal-test.1221systems.ru",
            full_name="Анна HR",
            position="HR-специалист",
            department="HR-департамент",
            manager="Директор по персоналу",
            vacation_days=18,
            nearest_vacation="10.09.2026 - 23.09.2026",
            birthday="12 марта",
            role="hr_manager",
            password=hash_password("password123"),
        ),
    }

    for email, employee in demo.items():
        existing = db.query(Employee).filter(Employee.email == email).first()
        if existing:
            existing.role = employee.role
            continue
        db.add(employee)
    db.commit()
