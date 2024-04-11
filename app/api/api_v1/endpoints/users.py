from fastapi import Depends, HTTPException, APIRouter, Request, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List



from app.models.users import User
from app.db.session import SessionLocal
from app.schemas import user as schemas
from app.models.base import CRUDUser
from sqlalchemy.exc import IntegrityError
from app.core.authentication import hash_password, check_password, create_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/auth")
router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


crud_user = CRUDUser(User)

@router.post("/auth")
async def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_user.get_by_email(db, email=form_data.username)
    print(user)
    if not user or not check_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/", response_model=schemas.UserBase)
def create_user(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_user = crud_user.get_by_email(db, email=user.email)
    print(db_user, "create_user")
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = hash_password(user.password)
    try:
        return crud_user.create(db, obj_in=user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered integrity error")


@router.get("/", response_model=List[schemas.UserBase])
def read_users(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.UserBase)
def read_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=schemas.UserBase)
def update_user(request: Request, user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.update(db, db_obj=db_user, obj_in=user)


@router.delete("/{user_id}", response_model=schemas.UserBase)
def delete_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.remove(db, id=user_id)
