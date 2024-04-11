from sqlalchemy.ext.declarative import declarative_base
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union # noqa

Base = declarative_base()
ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id, self.model.is_deleted == False).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(self.model.is_deleted == False).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> ModelType:
        obj_in_dict = obj_in.dict()
        db_obj = self.model(**obj_in_dict)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def delete(self, db: Session, id: int):
        obj = db.query(self.model).get(id)
        if obj:
            obj.is_deleted = True
            db.commit()
            return obj
        return None


#
# Usercrud inherits crudbase and provides the necessary methods to interact with the database
#
class CRUDUser(CRUDBase[ModelType]):

    def get_by_email(self, db: Session, email: str):
        print(self.model.__name__)
        query = db.query(self.model).filter(self.model.email == email, self.model.is_deleted == False)
        data = query.first()
        return data

    def authenticate_user(self, db: Session, username: str, password: str):
        # Add your authentication logic here
        pass

    # Add any other user-specific operations here
