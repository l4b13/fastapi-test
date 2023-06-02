from sqlalchemy.orm import Session
import argon2

from . import models, schemas
from .enums import *

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = argon2.hash_password(bytes(user.password, 'utf-8'))
    # hashed_password = user.password
    db_user = models.User(email = user.email, hashed_password = hashed_password, role = user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_first(db: Session):
    hashed_password = argon2.hash_password(bytes("superuser", 'utf-8'))
    # hashed_password = user.password
    db_user = models.User(email = "superuser@fastapi.app", hashed_password = hashed_password, role = LRoles[2])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).update({
        models.User.email: user.email,
        models.User.hashed_password: argon2.hash_password(bytes(user.password, 'utf-8')),
        models.User.role: user.role
    })
    db.commit()
    return db_user

def delete_user(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return