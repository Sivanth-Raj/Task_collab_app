import models, schemas
from sqlalchemy.orm import Session
from auth import get_password_hash
from datetime import datetime



def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def getusercreatedtasks(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.created_by == user_id).all()

def getuserassignedtasks(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.assigned_to == user_id).all()

def create_task(db: Session, task: schemas.TaskCreate):
    task_obj = models.Task(
        title=task.title,
        description=task.description,
        deadline=datetime.fromisoformat(task.deadline) if isinstance(task.deadline, str) else task.deadline,
        priority=task.priority,
        status=task.status,
        created_by=task.created_by,
        assigned_to=task.assigned_to
    )
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj

def update_task_status(db: Session, task_id: int, status: str):
    task = db.query(models.Task).get(task_id)
    if not task:
        return None
    task.status = status
    db.commit()
    db.refresh(task)
    return task

def get_task_stats(db: Session, user_id: int):
    total = db.query(models.Task).filter(models.Task.assigned_to == user_id).count()
    completed = db.query(models.Task).filter(models.Task.assigned_to == user_id, models.Task.status == "Completed").count()
    pending = total - completed
    return {"total": total, "completed": completed, "pending": pending}

def delete_task(db: Session, task_id: int, user_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.created_by == user_id).first()
    if task:
        db.delete(task)
        db.commit()


