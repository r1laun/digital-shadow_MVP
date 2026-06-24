from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
from analyzer import analyze_threat
from search import search_telegram
from database import init_db, save_result, get_history

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    history = get_history()
    return templates.TemplateResponse("index.html", {"request": request, "history": history})

@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...)):
    posts = await search_telegram(query)
    result = await analyze_threat(query, posts)
    save_result(query, result)
    history = get_history()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result,
        "query": query,
        "history": history
    })

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
