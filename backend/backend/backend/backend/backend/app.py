from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import RedirectResponse, FileResponse
from auth import register, verify
from media import save_file, trim, merge
from ai_tools import highlight
from cloud import upload
import os

app = FastAPI()

def current_user(req: Request):
    return req.cookies.get("user")

@app.post("/register")
def do_register(u=Form(...), p=Form(...)):
    register(u, p)
    return RedirectResponse("/", 302)

@app.post("/login")
def do_login(u=Form(...), p=Form(...)):
    if verify(u, p):
        r = RedirectResponse("/", 302)
        r.set_cookie("user", u)
        return r
    return "Invalid"

@app.post("/upload")
async def upload_media(file: UploadFile = File(...), user=Form(...)):
    path = save_file(user, file)
    data = await file.read()
    open(path,"wb").write(data)
    upload(os.getenv("S3_BUCKET"), f"{user}/{file.filename}", data)
    return RedirectResponse("/", 302)
