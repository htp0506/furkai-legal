"""Sahne sistemi: zaman çizelgesi, sahne durumu ve kayıt defteri."""
import numbers
from .gfx import clamp, lerp, ease_io

SCENES = {}


def scene(name):
    def deco(fn):
        SCENES[name] = fn
        return fn
    return deco


class SceneState:
    """Bir sahne grubunun o anki durumu.

    t   : grup başından beri geçen süre (sn)
    T   : grup süresi
    ph  : aktif faz (grubun kaçıncı cümlesi)
    pt  : faz ilerlemesi 0..1, pts: faz başından beri sn, pd: faz süresi
    P   : o faza kadar birikmiş parametreler
    """

    def __init__(self, gt, g0, g1, phases, ep, beats=None):
        self.gt = gt
        self.t = gt - g0
        self.T = g1 - g0
        self.phases = phases
        self.ep = ep
        self.beats = beats or []
        ph = 0
        for i, (s, e, _) in enumerate(phases):
            if self.t >= s:
                ph = i
        self.ph = ph
        s, e, _ = phases[ph]
        self.pts = self.t - s
        self.pd = max(0.01, e - s)
        self.pt = clamp(self.pts / self.pd)
        self.P = {}
        for i in range(ph + 1):
            self.P.update(phases[i][2])
        self.prevP = {}
        for i in range(ph):
            self.prevP.update(phases[i][2])

    def at(self, t):
        """Aynı grubun başka bir anındaki durum."""
        g0 = self.gt - self.t
        return SceneState(g0 + t, g0, g0 + self.T, self.phases, self.ep, self.beats)

    def get(self, key, default=None):
        return self.P.get(key, default)

    def v(self, key, default=0.0, dur=0.7, ease=ease_io, delay=0.0):
        """Faz değişiminde parametreyi yumuşakça geçir."""
        cur = self.P.get(key, default)
        if self.ph == 0:
            prev = self.P.get(key + "0", cur)
        else:
            prev = self.prevP.get(key, cur)
        if isinstance(cur, numbers.Number) and isinstance(prev, numbers.Number):
            k = ease(clamp((self.pts - delay) / max(0.01, dur)))
            return lerp(prev, cur, k)
        return cur

    def start(self, i):
        """i. fazın grup içindeki başlangıç zamanı (yoksa çok büyük)."""
        if i < len(self.phases):
            return self.phases[i][0]
        return 1e9

    def since(self, i):
        return self.t - self.start(i)

    def prog(self, i, dur=0.8, delay=0.0):
        return clamp((self.since(i) - delay) / dur)
