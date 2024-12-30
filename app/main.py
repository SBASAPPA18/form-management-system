from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import engine, get_db
from .auth import authenticate_user, create_access_token, get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/auth/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/forms/create", response_model=schemas.FormResponse)
def create_form(form: schemas.FormCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_form(db=db, form=form, user_id=current_user.id)

@app.post("/forms/submit/{form_id}")
def submit_form(form_id: int, submission: schemas.FormSubmissionCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.submit_form(db=db, form_id=form_id, user_id=current_user.id, submission=submission)

@app.get("/forms/", response_model=List[schemas.FormResponse])
def get_forms(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Form).filter(models.Form.creator_id == current_user.id).all()

@app.get("/forms/{form_id}", response_model=schemas.FormResponse)
def get_form(form_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    form = db.query(models.Form).filter(models.Form.id == form_id, models.Form.creator_id == current_user.id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    return form

@app.delete("/forms/delete/{form_id}")
def delete_form(form_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    form = db.query(models.Form).filter(models.Form.id == form_id, models.Form.creator_id == current_user.id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    db.delete(form)
    db.commit()
    return {"detail": "Form deleted successfully"}

@app.get("/forms/submissions/{form_id}")
def get_form_submissions(form_id: int, page: int = 1, limit: int = 10, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    form = db.query(models.Form).filter(models.Form.id == form_id, models.Form.creator_id == current_user.id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    
    submissions = db.query(models.FormSubmission).filter(models.FormSubmission.form_id == form_id).offset((page-1)*limit).limit(limit).all()
    total_count = db.query(models.FormSubmission).filter(models.FormSubmission.form_id == form_id).count()
    
    return {
        "total_count": total_count,
        "page": page,
        "limit": limit,
        "submissions": [
            {
                "submission_id": str(submission.id),
                "submitted_at": submission.submitted_at,
                "data": submission.responses
            } for submission in submissions
        ]
    }