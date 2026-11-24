"""Ses: Türkçe TTS (Piper), efektler (sentez), müzik ve miks."""
import math
import os
import subprocess
import numpy as np
from scipy.signal import resample_poly, butter, sosfilt

SR = 48000
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE_DIR = os.environ.get("TTS_MODEL_DIR", os.path.join(ROOT, "assets", "voices"))
DEFAULT_VOICE = os.environ.get("TTS_VOICE", "tr_TR-fettah-medium")

_VOICES = {}


def voice_path(name):
    for root, _, files in os.walk(VOICE_DIR):
        if name + ".onnx" in files:
            return os.path.join(root, name + ".onnx")
    raise FileNotFoundError(f"{name}.onnx bulunamadı: {VOICE_DIR} (README'deki indirme adımına bakın)")


def _voice(name):
    if name not in _VOICES:
        from piper import PiperVoice
        _VOICES[name] = PiperVoice.load(voice_path(name))
    return _VOICES[name]


def tts(text, voice=DEFAULT_VOICE, speed=1.0, seed_noise=0.55):
    """Metni seslendir -> float32 mono @ 48 kHz."""
    from piper import SynthesisConfig
    v = _voice(voice)
    cfg = SynthesisConfig(length_scale=1.0 / speed, noise_scale=seed_noise, noise_w_scale=0.7, normalize_audio=True)
    chunks = []
    sr = v.config.sample_rate
    for ch in v.synthesize(text, cfg):
        chunks.append(ch.audio_float_array.astype(np.float32))
    a = np.concatenate(chunks) if chunks else np.zeros(1, np.float32)
    a = resample_poly(a, SR // 150, sr // 150).astype(np.float32) if sr != SR else a
    # baştaki/sondaki sessizliği kırp
    thr = 0.01
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx):
        a = a[max(0, idx[0] - int(0.02 * SR)): min(len(a), idx[-1] + int(0.06 * SR))]
    return a


# ---------------------------------------------------------------- efekt sentezi
def _env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))
    return e


def sfx_whoosh(dur=0.55, up=True, gain=0.35):
    n = int(dur * SR)
    rng = np.random.default_rng(7)
    noise = rng.standard_normal(n).astype(np.float32)
    out = np.zeros(n, np.float32)
    # kayan bant geçiren: parça parça filtre
    steps = 24
    for i in range(steps):
        s0, s1 = i * n // steps, (i + 1) * n // steps
        u = i / (steps - 1)
        f = 400 + (3500 if up else 1500) * (u if up else 1 - u)
        sos = butter(2, [max(60, f * 0.6), min(SR / 2 - 100, f * 1.4)], btype="band", fs=SR, output="sos")
        out[s0:s1] = sosfilt(sos, noise[max(0, s0 - 2000):s1])[-(s1 - s0):]
    t = np.linspace(0, 1, n)
    env = np.sin(np.pi * t) ** 1.6
    return (out * env / (np.abs(out).max() + 1e-6) * gain).astype(np.float32)


def sfx_pop(freq=880, dur=0.12, gain=0.22):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = freq * (1 + 0.6 * np.exp(-t * 40))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * _env(n, 0.002, 0.035) * gain).astype(np.float32)


def sfx_ding(freq=1318.5, dur=0.6, gain=0.16):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 2.01 * t) + 0.15 * np.sin(2 * np.pi * freq * 3.0 * t)
    return (s * _env(n, 0.002, 0.18) * gain).astype(np.float32)


def sfx_vario(rate=2.5, dur=2.0, base=880, climb=1.0, gain=0.14):
    """Vario bip sesi: tırmanış arttıkça frekans ve hız artar."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = base + 380 * climb * (t / dur)
    gate = ((t * (rate + 2 * climb * t / dur)) % 1.0) < 0.45
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * gate
    # kenar yumuşatma
    sos = butter(2, 6000, btype="low", fs=SR, output="sos")
    s = sosfilt(sos, s)
    fade = np.minimum(1, np.minimum(t / 0.05, (dur - t) / 0.1))
    return (s * fade * gain).astype(np.float32)


def sfx_alarm(dur=0.8, gain=0.12):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = np.where((t * 6) % 1 < 0.5, 660, 520)
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5
    sos = butter(2, 2500, btype="low", fs=SR, output="sos")
    s = sosfilt(sos, s)
    return (s * np.minimum(1, (dur - t) / 0.1) * gain).astype(np.float32)


def sfx_thud(gain=0.4):
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * (70 + 60 * np.exp(-t * 30)) * t) * _env(n, 0.002, 0.08)
    rng = np.random.default_rng(3)
    s += rng.standard_normal(n) * _env(n, 0.001, 0.02) * 0.3
    return (s * gain).astype(np.float32)


def sfx_wind(dur, gain=0.05, seed=11):
    n = int(dur * SR)
    rng = np.random.default_rng(seed)
    noise = rng.standard_normal(n).astype(np.float32)
    sos = butter(2, [150, 900], btype="band", fs=SR, output="sos")
    w = sosfilt(sos, noise)
    t = np.arange(n) / SR
    mod = 0.6 + 0.4 * np.sin(2 * np.pi * 0.13 * t) * np.sin(2 * np.pi * 0.07 * t + 1)
    w = w / (np.abs(w).max() + 1e-6) * mod
    return (w * gain).astype(np.float32)


SFX = {
    "whoosh": lambda: sfx_whoosh(),
    "whoosh_down": lambda: sfx_whoosh(0.5, up=False, gain=0.3),
    "pop": lambda: sfx_pop(),
    "pop_low": lambda: sfx_pop(520, gain=0.2),
    "ding": lambda: sfx_ding(),
    "ding2": lambda: sfx_ding(1568, gain=0.14),
    "vario": lambda: sfx_vario(),
    "vario_long": lambda: sfx_vario(dur=3.2, climb=1.4),
    "sink": lambda: sfx_vario(rate=0, dur=1.2, base=420, climb=-0.3, gain=0.09),
    "alarm": lambda: sfx_alarm(),
    "thud": lambda: sfx_thud(),
}


def place(track, clip, t, gain=1.0):
    i = int(t * SR)
    if i >= len(track) or i < 0:
        return
    j = min(len(track), i + len(clip))
    track[i:j] += clip[: j - i] * gain


def write_wav(path, a):
    import soundfile as sf
    sf.write(path, a, SR, subtype="PCM_16")


def mix(voice, sfx, music_file, total, out_path, music_offset=0.0, music_gain_db=-17.0, tmpdir="."):
    """Ses kanallarını ffmpeg ile birleştir: müzik ses altında otomatik kısılır, sonra loudnorm."""
    vpath = os.path.join(tmpdir, "voice.wav")
    spath = os.path.join(tmpdir, "sfx.wav")
    write_wav(vpath, np.clip(voice, -1, 1))
    write_wav(spath, np.clip(sfx, -1, 1))
    fade_out = max(0.0, total - 1.6)
    fc = (
        f"[0:a]highpass=f=75,equalizer=f=220:t=q:w=1.0:g=-2,equalizer=f=3200:t=q:w=1.2:g=3,"
        f"acompressor=threshold=-20dB:ratio=3:attack=4:release=90:makeup=3,aformat=channel_layouts=stereo,asplit=2[v][vsc];"
        f"[2:a]atrim=start={music_offset:.2f}:duration={total + 0.5:.2f},asetpts=PTS-STARTPTS,"
        f"volume={music_gain_db}dB,afade=t=in:st=0:d=0.8,afade=t=out:st={fade_out:.2f}:d=1.5,aformat=channel_layouts=stereo[m];"
        f"[m][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[md];"
        f"[1:a]aformat=channel_layouts=stereo[s];"
        f"[v][md][s]amix=inputs=3:normalize=0,atrim=duration={total:.2f},loudnorm=I=-14:TP=-1.5:LRA=9[out]"
    )
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", vpath, "-i", spath, "-i", music_file,
           "-filter_complex", fc, "-map", "[out]", "-ar", str(SR), "-c:a", "pcm_s16le", out_path]
    subprocess.run(cmd, check=True)
    return out_path
