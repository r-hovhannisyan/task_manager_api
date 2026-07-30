from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers.tasks import router as tasks_router
app = FastAPI()

app.include_router(users_router)
app.include_router(tasks_router)