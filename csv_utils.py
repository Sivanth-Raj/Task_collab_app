import io
import csv
import models
from sqlalchemy.orm import Session

def generate_tasks_csv(db: Session, user_id: int):
    tasks = db.query(models.Task).filter(models.Task.created_by == user_id).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Title', 'Description', 'Deadline', 'Priority', 'Status', 'Assigned To'])
    for task in tasks:
        writer.writerow([task.title, task.description, task.deadline.strftime("%Y-%m-%d %H:%M"), task.priority, task.status, task.assigned_to])
    output.seek(0)
    return output
