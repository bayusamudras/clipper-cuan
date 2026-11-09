#!/usr/bin/env python3
"""Buat transkrip SRT berpotongan pendek (2-5 kata) dengan waktu per kata, siap ditempel ke Potong Hook.
Pakai:  pip install faster-whisper
        python tools/transkrip.py video.mp4 [id|en] > video.srt
"""
import sys
from faster_whisper import WhisperModel

def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02}:{int(m):02}:{s:06.3f}".replace(".", ",")

src = sys.argv[1]; lang = sys.argv[2] if len(sys.argv) > 2 else "id"
model = WhisperModel("small", compute_type="int8")
segs, _ = model.transcribe(src, language=lang, word_timestamps=True, vad_filter=True)
words = [w for s in segs for w in s.words]
cues, cur = [], []
for w in words:
    if cur and (w.start - cur[-1].end > .35 or len(cur) >= 5 or (cur[-1].word.strip()[-1:] in ".?!," and len(cur) >= 2)):
        cues.append(cur); cur = []
    cur.append(w)
if cur: cues.append(cur)
for i, c in enumerate(cues, 1):
    print(i); print(f"{ts(c[0].start)} --> {ts(c[-1].end)}"); print("".join(x.word for x in c).strip()); print()
