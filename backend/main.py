from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.users import router as users_router
from routes.hobbies import router as hobbies_router

app = FastAPI(title="Hobby Library API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(hobbies_router)

# Serve o frontend como arquivos estáticos
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
