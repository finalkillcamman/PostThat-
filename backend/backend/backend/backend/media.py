import os, subprocess

UPLOADS = "uploads"

def save_file(user, file):
    os.makedirs(f"{UPLOADS}/{user}", exist_ok=True)
    path = f"{UPLOADS}/{user}/{file.filename}"
    return path

def trim(src, start, end, out):
    subprocess.run([
        "ffmpeg","-y","-i",src,
        "-ss",start,"-to",end,
        "-c","copy",out
    ])

def merge(list_file, out):
    subprocess.run([
        "ffmpeg","-y","-f","concat",
        "-safe","0","-i",list_file,
        "-c","copy",out
    ])
