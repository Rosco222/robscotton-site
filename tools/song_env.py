"""Works out how loud each song is, 20 times a second, so the gramophone can move in time.
Run from the repo root when a song's MP3 changes:  python3 tools/song_env.py
Writes tools/lyrics/<song-id>.env (one base-36 digit per 1/20 s). Needs ffmpeg and numpy."""
import subprocess, glob, os, numpy as np
for mp3 in sorted(glob.glob('site/audio/*.mp3')):
    sid = os.path.basename(mp3)[:-4]
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp3, '-ac', '1', '-ar', '8000', '-f', 's16le', '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
    n = len(a) // 400
    rms = np.sqrt((a[:n * 400].reshape(n, 400) ** 2).mean(1))
    floor, top = np.percentile(rms, 8), np.percentile(rms, 99.5)
    v = np.clip((rms - floor) / max(1e-6, top - floor), 0, 1) ** 0.8
    open(f'tools/lyrics/{sid}.env', 'w').write(''.join('0123456789abcdefghijklmnopqrstuvwxyz'[int(round(x * 35))] for x in v))
    print(sid, n / 20, 'seconds')
