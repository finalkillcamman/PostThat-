from fastapi import FastAPI, UploadFile, File, Form, Request, Depends
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from passlib.hash import bcrypt
import os, sqlite3, subprocess

APP = "PostThat"
BASE = os.getcwd()
UPLOADS = os.path.join(BASE, "uploads")
DB = os.path.join(BASE, "users.db")

os.makedirs(UPLOADS, exist_ok=True)

app = FastAPI()

db = sqlite3.connect(DB, check_same_thread=False)
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (u TEXT UNIQUE, p TEXT)")
db.commit()

def user(req: Request):
    return req.cookies.get("u")

def page(body):
    return f"""
<!DOCTYPE html>
<html>
<head>
<title>{APP}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="manifest" href="/manifest.json">
<style>
body {{
background: radial-gradient(circle at top,#1a002a,#050008);
color:#e0c9ff;
font-family:Arial;
text-align:center;
padding:20px;
}}
h1 {{color:#b46bff;text-shadow:0 0 12px #7a1cff}}
.box {{
background:rgba(255,255,255,0.05);
padding:20px;
border-radius:10px;
max-width:520px;
margin:20px auto;
}}
input,button {{
padding:10px;
margin:6px;
border-radius:6px;
border:none;
}}
button {{
background:linear-gradient(135deg,#7a1cff,#b46bff);
font-weight:bold;
cursor:pointer;
}}
a {{color:#cfa8ff;text-decoration:none}}
</style>
</head>
<body>
<h1>{APP}</h1>
{body}
</body>
</html>
"""

@app.get("/manifest.json")
def manifest():
    return {
        "name": APP,
        "short_name": APP,
        "start_url": "/",
        "display": "standalone",
        "background_color": "#050008",
        "theme_color": "#7a1cff"
    }

@app.get("/", response_class=HTMLResponse)
def home(u: str = Depends(user)):
    if not u:
        return page("""
<div class="box">
<form method="post" action="/login">
<input name="u" placeholder="Username" required>
<input name="p" type="password" placeholder="Password" required>
<button>Login</button>
</form>
<form method="post" action="/register">
<input name="u" placeholder="New username" required>
<input name="p" type="password" placeholder="New password" required>
<button>Register</button>
</form>
</div>
""")

    ud = os.path.join(UPLOADS, u)
    os.makedirs(ud, exist_ok=True)
    files = os.listdir(ud)

    listing = "".join(
        f"<li>{f} <a href='/download/{f}'>Download</a></li>"
        for f in files
    )

    return page(f"""
<div class="box">
<form action="/upload" method="post" enctype="multipart/form-data">
<input type="file" name="file" required>
<button>Upload</button>
</form>

<form action="/trim" method="post">
<input name="file" placeholder="file.mp4" required>
<input name="start" placeholder="start sec" required>
<input name="end" placeholder="end sec" required>
<button>Trim</button>
</form>

<form action="/merge" method="post">
<input name="files" placeholder="a.mp4,b.mp4" required>
<button>Merge</button>
</form>

<ul>{listing}</ul>
<a href="/logout">Logout</a>
</div>
""")

@app.post("/register")
def register(u: str = Form(...), p: str = Form(...)):
    try:
        cur.execute("INSERT INTO users VALUES (?,?)", (u, bcrypt.hash(p)))
        db.commit()
        return RedirectResponse("/", 302)
    except:
        return HTMLResponse("User exists")

@app.post("/login")
def login(u: str = Form(...), p: str = Form(...)):
    cur.execute("SELECT p FROM users WHERE u=?", (u,))
    r = cur.fetchone()
    if r and bcrypt.verify(p, r[0]):
        res = RedirectResponse("/", 302)
        res.set_cookie("u", u)
        return res
    return HTMLResponse("Invalid")

@app.get("/logout")
def logout():
    r = RedirectResponse("/", 302)
    r.delete_cookie("u")
    return r

@app.post("/upload")
async def upload(file: UploadFile = File(...), u: str = Depends(user)):
    path = os.path.join(UPLOADS, u)
    with open(os.path.join(path, file.filename), "wb") as f:
        f.write(await file.read())
    return RedirectResponse("/", 302)

@app.get("/download/{f}")
def download(f: str, u: str = Depends(user)):
    return FileResponse(os.path.join(UPLOADS, u, f), filename=f)

@app.post("/trim")
def trim(file: str = Form(...), start: str = Form(...), end: str = Form(...), u: str = Depends(user)):
    d = os.path.join(UPLOADS, u)
    out = os.path.join(d, "trim_" + file)
    subprocess.run(["ffmpeg","-y","-i",os.path.join(d,file),"-ss",start,"-to",end,"-c","copy",out])
    return RedirectResponse("/", 302)

@app.post("/merge")
def merge(files: str = Form(...), u: str = Depends(user)):
    d = os.path.join(UPLOADS, u)
    lst = os.path.join(d, "list.txt")
    with open(lst, "w") as f:
        for x in files.split(","):
            f.write(f"file '{os.path.join(d,x)}'\n")
    out = os.path.join(d, "merged.mp4")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",lst,"-c","copy",out])
    return RedirectResponse("/", 302)
