"""Bir bölümü (ders) MP4 olarak üret.

Kullanım:
    python -m engine.build 18                 # tam video
    python -m engine.build 18 --still 3.5 9   # sadece belirli saniyelerden PNG kare
    python -m engine.build all                # tüm set
"""
import argparse
import importlib
import json
import os
import subprocess
import sys
import time

import numpy as np
import skia

from . import audio
from .core import SCENES, SceneState
from .gfx import W, H, FPS, ease_out, ease_io, clamp, smooth, remap
from . import ui
from . import scenes  # noqa: F401  (sahneleri kaydeder)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC = os.path.join(ROOT, "assets", "music", "muzik_ana.mp3")
LEAD_IN = 0.5
GAP = 0.24
OUTRO_HOLD = 2.2
TRANS = 0.42


def load_episode(no):
    from episodes import SERIES
    for e in SERIES:
        if e["no"] == no:
            mod = importlib.import_module(f"episodes.{e['module']}")
            ep = dict(mod.EP)
            ep.update({"no": no, "total": len(SERIES)})
            nxt = [x for x in SERIES if x["no"] == no + 1]
            ep["next_title"] = nxt[0]["title"] if nxt else None
            return ep
    raise SystemExit(f"Bölüm bulunamadı: {no}")


def build_timeline(ep, durs):
    beats = ep["beats"]
    t = LEAD_IN
    tl = []
    for i, (b, d) in enumerate(zip(beats, durs)):
        start = t + b.get("delay", 0.0)
        end = start + d
        tl.append({"i": i, "start": start, "end": end, "beat": b})
        t = end + b.get("gap", GAP)
    total = tl[-1]["end"] + ep.get("outro_hold", OUTRO_HOLD)
    # sahne grupları
    groups = []
    for item in tl:
        b = item["beat"]
        if "scene" in b or not groups:
            groups.append({"scene": b.get("scene", "hook"), "beats": [item]})
        else:
            groups[-1]["beats"].append(item)
    for gi, g in enumerate(groups):
        g["t0"] = 0.0 if gi == 0 else g["beats"][0]["start"] - 0.12
        g["t1"] = total if gi == len(groups) - 1 else groups[gi + 1]["beats"][0]["start"] - 0.12
        phases = []
        for k, item in enumerate(g["beats"]):
            s = 0.0 if k == 0 else item["start"] - g["t0"] - 0.05
            e = (g["beats"][k + 1]["start"] - g["t0"] - 0.05) if k + 1 < len(g["beats"]) else g["t1"] - g["t0"]
            phases.append((s, e, item["beat"].get("p", {})))
        g["phases"] = phases
    return tl, groups, total


def synth_audio(ep, tmpdir, voice=None):
    voice = voice or ep.get("voice", audio.DEFAULT_VOICE)
    clips = []
    for b in ep["beats"]:
        clips.append(audio.tts(b["say"], voice=voice, speed=b.get("speed", ep.get("speed", 1.04))))
    return clips


def make_tracks(ep, tl, groups, total, clips):
    n = int((total + 1) * audio.SR)
    voice = np.zeros(n, np.float32)
    sfx = np.zeros(n, np.float32)
    cache = {}

    def S(name):
        if name not in cache:
            cache[name] = audio.SFX[name]()
        return cache[name]

    for item, clip in zip(tl, clips):
        audio.place(voice, clip, item["start"])
        b = item["beat"]
        for name, off, *g in b.get("sfx", []):
            audio.place(sfx, S(name), item["start"] + off, g[0] if g else 1.0)
        if b.get("k"):
            audio.place(sfx, S("pop"), item["start"] + 0.08, 0.6)
    for gi, g in enumerate(groups):
        if gi > 0:
            audio.place(sfx, S("whoosh"), max(0, g["t0"] - 0.18), 0.7)
    audio.place(sfx, S("whoosh"), 0.0, 0.8)
    wind = audio.sfx_wind(n / audio.SR + 0.01, gain=ep.get("wind", 0.035))[:n]
    sfx[:len(wind)] += wind
    return voice, sfx


class Renderer:
    def __init__(self, ep, tl, groups, total):
        self.ep, self.tl, self.groups, self.total = ep, tl, groups, total
        self.surface = skia.Surface(W, H)
        self.snap = {}

    def group_at(self, t):
        for gi, g in enumerate(self.groups):
            if g["t0"] <= t < g["t1"]:
                return gi
        return len(self.groups) - 1

    def draw_scene(self, c, gi, t):
        g = self.groups[gi]
        fn = SCENES[g["scene"]]
        st = SceneState(min(t, g["t1"] - 1e-3), g["t0"], g["t1"], g["phases"], self.ep, g["beats"])
        c.save()
        fn(c, st)
        c.restore()

    def snapshot(self, gi):
        if gi not in self.snap:
            s = skia.Surface(W, H)
            self.draw_scene(s.getCanvas(), gi, self.groups[gi]["t1"] - 0.001)
            self.snap = {gi: s.makeImageSnapshot()}
        return self.snap[gi]

    def frame(self, t):
        c = self.surface.getCanvas()
        gi = self.group_at(t)
        self.draw_scene(c, gi, t)
        g = self.groups[gi]
        if gi > 0 and t - g["t0"] < TRANS:
            k = (t - g["t0"]) / TRANS
            img = self.snapshot(gi - 1)
            e = ease_io(k)
            c.save()
            c.translate(540, 960)
            sc = 1 + 0.10 * e
            c.scale(sc, sc)
            c.translate(-540, -960)
            c.drawImage(img, 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(Alphaf=1 - e))
            c.restore()
            # ışık süpürmesi
            c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=skia.ColorSetARGB(int(60 * (1 - abs(2 * k - 1))), 255, 255, 255)))
        # üst katmanlar
        scene_name = g["scene"]
        ui.vignette(c, 0.28 if scene_name not in ("hook", "outro") else 0.2)
        ha = smooth(remap(t, 0.5, 1.1))
        ui.header(c, self.ep["no"], self.ep["total"], t / self.total, ha)
        for idx, item in enumerate(self.tl):
            b = item["beat"]
            nxt = self.tl[idx + 1]["start"] if idx + 1 < len(self.tl) else self.total + 1
            if item["start"] - 0.1 <= t < nxt + 0.3:
                if b.get("k"):
                    same = idx + 1 < len(self.tl) and self.tl[idx + 1]["beat"].get("k") == b.get("k")
                    t_out = None if (same or idx == len(self.tl) - 1) else nxt
                    ui.kicker(c, b["k"], item["start"], t_out, t, y=b.get("ky", 330))
                ui.subtitles(c, b.get("sub", b["say"]), item["start"], item["end"], t, y=b.get("suby", 1505))
        return self.surface


def render(ep_no, out_dir, stills=None, crf=19, preset="medium", voice=None, fps=FPS):
    ep = load_episode(ep_no)
    tmp = os.path.join(out_dir, f".tmp_{ep_no:02d}")
    os.makedirs(tmp, exist_ok=True)
    t0 = time.time()
    clips = synth_audio(ep, tmp, voice)
    durs = [len(cl) / audio.SR for cl in clips]
    tl, groups, total = build_timeline(ep, durs)
    rd = Renderer(ep, tl, groups, total)
    slug = ep.get("slug", f"ders{ep_no:02d}")
    if stills == "beats":
        stills = [round(it["start"] + 0.65 * (it["end"] - it["start"]), 2) for it in tl]
    if stills:
        paths = []
        for st in stills:
            surf = rd.frame(float(st))
            p = os.path.join(out_dir, f"kare_{ep_no:02d}_{float(st):05.1f}.png")
            surf.makeImageSnapshot().save(p)
            paths.append(p)
        print("Kareler:", *paths, sep="\n  ")
        print(f"Toplam süre: {total:.1f} sn")
        return paths
    voice_tr, sfx_tr = make_tracks(ep, tl, groups, total, clips)
    mix_path = os.path.join(tmp, "mix.wav")
    audio.mix(voice_tr, sfx_tr, MUSIC, total, mix_path, music_offset=ep.get("music_offset", (ep_no * 23) % 95), tmpdir=tmp)
    out = os.path.join(out_dir, f"{ep_no:02d}_{slug}.mp4")
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
           "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-i", mix_path,
           "-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-pix_fmt", "yuv420p", "-profile:v", "high",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    nf = int(total * fps)
    for fi in range(nf):
        surf = rd.frame(fi / fps)
        proc.stdin.write(surf.toarray().tobytes())
    proc.stdin.close()
    proc.wait()
    # altyazı dosyası (SRT) — Instagram/YouTube'a yüklemek için
    srt = os.path.join(out_dir, f"{ep_no:02d}_{slug}.srt")
    with open(srt, "w", encoding="utf-8") as f:
        for i, item in enumerate(tl, 1):
            def ts(x):
                h, r = divmod(x, 3600)
                m, s = divmod(r, 60)
                return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"
            f.write(f"{i}\n{ts(item['start'])} --> {ts(item['end'])}\n{item['beat'].get('sub', item['beat']['say'])}\n\n")
    meta = {"no": ep_no, "title": ep["title"], "duration": round(total, 2), "file": os.path.basename(out),
            "render_seconds": round(time.time() - t0, 1)}
    with open(os.path.join(tmp, "meta.json"), "w") as f:
        json.dump(meta, f, ensure_ascii=False)
    print(f"✓ {out}  ({total:.1f} sn, {time.time() - t0:.0f} sn'de üretildi)")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes", nargs="+", help="bölüm numaraları ya da 'all'")
    ap.add_argument("--out", default=os.path.join(ROOT, "videolar"))
    ap.add_argument("--still", nargs="*", type=float, help="sadece bu saniyelerden PNG kare üret")
    ap.add_argument("--beat-stills", action="store_true", help="her cümleden bir PNG kare üret")
    ap.add_argument("--crf", type=int, default=19)
    ap.add_argument("--preset", default="medium")
    ap.add_argument("--voice", default=None)
    a = ap.parse_args()
    sys.path.insert(0, ROOT)
    from episodes import SERIES
    eps = [e["no"] for e in SERIES] if a.episodes == ["all"] else [int(x) for x in a.episodes]
    os.makedirs(a.out, exist_ok=True)
    for no in eps:
        render(no, a.out, stills="beats" if a.beat_stills else a.still, crf=a.crf, preset=a.preset, voice=a.voice)


if __name__ == "__main__":
    main()
