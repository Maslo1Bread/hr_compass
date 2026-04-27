from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.auth.deps import get_current_employee, require_admin
from backend.auth.jwt import hash_password
from backend.database import get_db
from backend.models.db import Employee
from backend.models.schemas import EmployeeCreate, EmployeeOut, EmployeeUpdate


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=EmployeeOut)
def me(employee: Employee = Depends(get_current_employee)):
    return employee


@router.get("/", response_model=list[EmployeeOut], dependencies=[Depends(require_admin)])
def list_users(db: Session = Depends(get_db)):
    return db.query(Employee).order_by(Employee.id).all()


@router.post("/", response_model=EmployeeOut, dependencies=[Depends(require_admin)])
def create_user(payload: EmployeeCreate, db: Session = Depends(get_db)):
    exists = (
        db.query(Employee)
        .filter((Employee.email == payload.email) | (Employee.tab_number == payload.tab_number))
        .first()
    )
    if exists:
        raise HTTPException(status_code=400, detail="Employee with this email/tab number already exists")

    employee = Employee(
        **payload.model_dump(exclude={"password"}),
        password=hash_password(payload.password),
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@router.put("/{user_id}", response_model=EmployeeOut, dependencies=[Depends(require_admin)])
def update_user(user_id: int, payload: EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == user_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    data = payload.model_dump(exclude_unset=True)
    if "password" in data:
        data["password"] = hash_password(data["password"])
    for key, value in data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)
    return employee


@router.delete("/{user_id}", dependencies=[Depends(require_admin)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == user_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"ok": True}
