from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_form(db: Session, form: schemas.FormCreate, user_id: int):
    db_form = models.Form(
        title=form.title,
        description=form.description,
        fields=form.dict()['fields'],
        creator_id=user_id
    )
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form

def submit_form(db: Session, form_id: int, user_id: int, submission: schemas.FormSubmissionCreate):
    db_submission = models.FormSubmission(
        form_id=form_id,
        user_id=user_id,
        responses=submission.dict()['responses']
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission