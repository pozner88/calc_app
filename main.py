from fastapi import FastAPI
from routers import router
from database import Base, engine
from fastapi.responses import RedirectResponse

Base.metadata.bind = engine

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="calculator API"
)

app.include_router(router)


@app.get('/')
def index():
    return RedirectResponse('/docs')
