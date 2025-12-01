from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.session import Base, engine
from src.auth.router import router as auth_router

app = FastAPI(
    title="HubTorcedor — Auth API",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # pode restringir depois
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria tabelas do banco
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# Routers
app.include_router(auth_router)


@app.get("/")
def root():
    return {"auth-api": "online"}
