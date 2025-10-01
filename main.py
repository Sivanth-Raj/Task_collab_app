from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
import csv_utils
from fastapi.responses import StreamingResponse
from fastapi import status
from fastapi import Request



from database import SessionLocal, engine
import crud, models, schemas, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db), user: schemas.UserOut = Depends(auth.get_current_user)):
    users = db.query(models.User).all()  # fetch all registered users
    tasks_created = crud.getusercreatedtasks(db, user.id)
    tasks_assigned = crud.getuserassignedtasks(db, user.id)
    completed = sum(1 for t in tasks_created if t.status == "Completed")
    pending = sum(1 for t in tasks_created if t.status == "Pending")
    total = len(tasks_created)
    stats = {"completed": completed, "pending": pending, "total": total}
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "taskscreated": tasks_created,
        "tasksassigned": tasks_assigned,
        "all_users": users,
        "now": datetime.now(),
        "stats": stats
        
    })
@app.post("/add-task")
async def add_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    deadline: str = Form(...),
    priority: str = Form(...),
    assigned_to: int = Form(...),
    db: Session = Depends(get_db),
    user: schemas.UserOut = Depends(auth.get_current_user)
):
    task = schemas.TaskCreate(
        
        title=title,
        description=description,
        deadline=deadline,
        priority=priority,
        status="Pending",
        assigned_to=assigned_to,
        created_by=user.id
    )
    task_obj = crud.create_task(db, task)
    users = db.query(models.User).all()
    # Detect AJAX request
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        # Render new row HTML
        from fastapi.templating import Jinja2Templates
        templates = Jinja2Templates(directory="templates")
        return templates.TemplateResponse("single_task_row.html", {
            "request": request,
            "task": task_obj,
            "all_users": users
        })
    else:
        # Normal browser form: fallback
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    
@app.post("/update-task/{task_id}")
def update_task(task_id: int, task_status: str = Form(...), db: Session = Depends(get_db)):
    # Update the task status string in the database
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        task.status = task_status  # Use the form string value directly
        db.commit()
        db.refresh(task)
        crud.update_task_status(db, task_id, task_status)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/")
def dashboard(request: Request, db: Session = Depends(get_db), user: schemas.UserOut = Depends(auth.get_current_user)):
    # Sample dashboard data, adapt as per your app
    tasks_created = crud.getusercreatedtasks(db, user.id)
    tasks_assigned = crud.getuserassignedtasks(db, user.id)
    stats = crud.get_task_stats(db, user.id)
    return templates.TemplateResponse("dashboard.html",
                                      {"request": request, "user": user,
                                       "tasks_created": tasks_created,
                                       "tasks_assigned": tasks_assigned,
                                       "stats": stats,
                                       "now": datetime.now()})

@app.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "error": None})

@app.post("/signup")
def signup(request: Request, db: Session = Depends(get_db), email: str = Form(...), password: str = Form(...)):
    user = crud.create_user(db, schemas.UserCreate(email=email, password=password))
    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login")
def login(request: Request, db: Session = Depends(get_db), email: str = Form(...), password: str = Form(...)):
    user = auth.authenticate_user(db, email, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Incorrect email or password"})
    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie("access_token", auth.create_access_token({"sub": user.email}))
    return response


@app.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "error": None})

@app.post("/signup")
def signup(request: Request, db: Session = Depends(get_db), email: str = Form(...), password: str = Form(...)):
    user = crud.create_user(db, schemas.UserCreate(email=email, password=password))
    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/delete-task/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), user: schemas.UserOut = Depends(auth.get_current_user)):
    crud.delete_task(db, task_id, user.id)  # Implement delete_task logic with authorization
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response

@app.get("/export")
def export_csv(db: Session = Depends(get_db), user: schemas.UserOut = Depends(auth.get_current_user)):
    csv_stream = csv_utils.generate_tasks_csv(db, user.id)
    return StreamingResponse(csv_stream, media_type="text/csv", headers={"Content-Disposition": "attachment;filename=tasks.csv"})




