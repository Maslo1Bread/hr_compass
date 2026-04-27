from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth.jwt import create_access_token, verify_password
from backend.database import get_db
from backend.models.db import Employee
from backend.models.schemas import LoginRequest, TokenResponse


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    employee = (
        db.query(Employee)
        .filter((Employee.email == payload.login) | (Employee.tab_number == payload.login))
        .first()
    )
    if not employee or not verify_password(payload.password, employee.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login or password")
    token = create_access_token(employee.email)
    return TokenResponse(access_token=token)
