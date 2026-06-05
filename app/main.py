from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import mechanical, utilities, mywork

app = FastAPI(title="L'Atelier de Bing")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(mechanical.router)
app.include_router(utilities.router)
app.include_router(mywork.router)

#@app.get("/")
#async def home():
#    return {"message": "L'Atelier de Bing is running"}

@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={}
    )