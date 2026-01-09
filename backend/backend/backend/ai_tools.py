import subprocess

def highlight(src, out):
    subprocess.run([
        "ffmpeg","-y",
        "-i",src,
        "-vf","select='gt(scene,0.4)',setpts=N/FRAME_RATE/TB",
        out
    ])
