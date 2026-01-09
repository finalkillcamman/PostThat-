npm install @capacitor/core @capacitor/cli
npx cap init PostThat com.postthat.app

@echo off
cd /d %~dp0

npx cap add android
npx cap add ios


if not exist venv (
    python -m venv venv
)

call venv\Scripts\activate
pip install -r requirements.txt

start http://127.0.0.1:8000
uvicorn app:app --host 127.0.0.1 --port 8000

PostThat-/
├─ app.py
├─ requirements.txt
└─ uploads/

fastapi
uvicorn
python-multipart
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import uuid

APP_NAME = "PostThat"
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title=APP_NAME)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/", response_class=HTMLResponse)
def home():
    files = os.listdir(UPLOAD_DIR)

    file_links = ""
    for f in files:
        file_links += f"""
        <li>
            {f}
            <a href="/download/{f}">Download</a>
        </li>
        """

    return f"""
    <html>
        <head>
            <title>{APP_NAME}</title>
            <style>
                body {{
                    background: #0b0b0f;
                    color: #caa6ff;
                    font-family: Arial;
                    padding: 30px;
                }}
                h1 {{
                    color: #9b5cff;
                }}
                input, button {{
                    margin-top: 10px;
                }}
                a {{
                    color: #b084ff;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <h1>{APP_NAME}</h1>

            <form action="/upload" enctype="multipart/form-data" method="post">
                <input name="file" type="file" required />
                <br/>
                <button type="submit">Upload</button>
            </form>

            <h2>Media</h2>
            <ul>
                {file_links}
            </ul>
        </body>
    </html>
    """


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    return {"status": "uploaded", "file": filename}


@app.get("/download/{filename}")
def download(filename: str):
    filepath = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(filepath):
        return FileResponse(filepath, filename=filename)
    return {"error": "File not found"}

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
