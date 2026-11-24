"""Yamaç paraşütü kanadı + pilot için basit 3D model ve yazılım render.

Model koordinatları (metre): x = pilotun sağı, y = yukarı, z = uçuş yönü (ileri).
Orijin = pilotun karabina noktası (askıların bağlandığı yer).
"""
import math
import numpy as np
import skia
from .gfx import C, P, clamp, smooth, hexrgb, PAL

LINE_LEN = 7.0          # karabina -> kanat mesafesi
R_ARC = 5.6             # kanat kemer yarıçapı
PHI_MAX = 1.02          # kanat ucu kemer açısı (rad)
C0 = 2.6                # merkez veter (chord)

DEFAULT_COLORS = {
    "main": "#FF6A1A",     # turuncu
    "center": "#F8FAFC",   # beyaz orta bant
    "tip": "#1E3A8A",      # lacivert uçlar
    "stripe": "#22D3EE",   # camgöbeği şerit
    "under": 0.62,         # alt yüzey koyulaştırma
}


def _rx(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def _ry(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def _rz(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def _airfoil(u, t=0.16, m=0.045, p=0.32):
    yt = 5 * t * (0.2969 * np.sqrt(u) - 0.1260 * u - 0.3516 * u ** 2 + 0.2843 * u ** 3 - 0.1036 * u ** 4)
    yc = np.where(u < p, m / p ** 2 * (2 * p * u - u ** 2), m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * u - u ** 2))
    return yc + yt, yc - yt


class Glider:
    def __init__(self, ns=44, nc=13, colors=None):
        self.ns, self.nc = ns, nc
        self.s = np.linspace(-1, 1, ns)
        k = np.arange(nc)
        self.u = (1 - np.cos(np.pi * k / (nc - 1))) / 2            # 0 (hücum kenarı) .. 1 (firar kenarı)
        up, lo = _airfoil(self.u)
        # halka: üst yüzey TE->LE, alt yüzey LE->TE
        self.ring_u = np.concatenate([self.u[::-1], self.u[1:]])
        self.ring_y = np.concatenate([up[::-1], lo[1:]])
        self.ring_upper = np.concatenate([np.ones(nc, bool), np.zeros(nc - 1, bool)])
        self.colors = dict(DEFAULT_COLORS)
        if colors:
            self.colors.update(colors)
        self._cell_colors()

    def _cell_colors(self):
        cols = []
        cells = 22
        for j in range(self.ns - 1):
            sm = (self.s[j] + self.s[j + 1]) / 2
            a = abs(sm)
            cell = int((sm + 1) / 2 * cells)
            if a < 0.16:
                base = self.colors["center"]
            elif a > 0.80:
                base = self.colors["tip"]
            elif 0.66 < a < 0.72:
                base = self.colors["stripe"]
            else:
                base = self.colors["main"]
            rgb = np.array(hexrgb(PAL.get(base, base)), float)
            seam = ((sm + 1) / 2 * cells) % 1.0
            cols.append((rgb, seam < 0.12 or seam > 0.88, cell))
        self.cell_rgb = cols

    # ------------------------------------------------------------ geometri
    def geometry(self, brake_l=0.0, brake_r=0.0, fold_l=0.0, fold_r=0.0, fold_pos=0.42, ears=0.0,
                 front=0.0, stall=0.0, inflate=1.0, crumple=0.0, t=0.0, flat=0.0):
        s = self.s[:, None]
        phimax = PHI_MAX + 0.45 * stall - 0.55 * flat
        phi = s * phimax
        chord = C0 * np.sqrt(np.maximum(0.05, 1 - 0.86 * s ** 2))
        zq = -0.38 * s ** 2
        R = R_ARC * (1 + 2.5 * flat)
        u = self.ring_u[None, :]
        thick = self.ring_y[None, :] * (0.12 + 0.88 * inflate) * (1 - 0.85 * flat)
        # firar kenarı fren bükümü (alt yön)
        side_b = np.where(s < 0, brake_l, brake_r) + stall * 0.9
        defl = side_b * np.clip((u - 0.55) / 0.45, 0, 1) ** 2 * 0.32 * (0.35 + 0.65 * np.abs(s))
        # kesit 2D koordinatları: zeta (ileri), eta (yukarı, yay normali)
        zeta = chord * (0.25 - u)
        eta = chord * (thick - defl)
        # önden kapanma: hücum kenarı tarafı aşağı-geri katlanır
        if front > 0:
            uf = 0.42
            zf = chord * (0.25 - uf)
            g = front * math.radians(165) * (1 - 0.55 * s ** 2)
            mask = u < uf
            dz, de = zeta - zf, eta
            cg, sg = np.cos(-g), np.sin(-g)
            nz = zf + dz * cg - de * sg
            ne = dz * sg + de * cg
            zeta = np.where(mask, nz, zeta)
            eta = np.where(mask, ne, eta)
        # buruşma
        if crumple > 0:
            jit = np.sin(9.0 * s + 2.2 * u + t * 6.0) * np.cos(6.5 * s - t * 4.5 + 2.6 * u)
            eta = eta + crumple * 0.13 * jit * chord
        n_x, n_y = np.sin(phi), np.cos(phi)
        X = R * np.sin(phi) + n_x * eta
        Y = R * (np.cos(phi) - 1) + n_y * eta
        Z = zq + zeta + 0 * X
        pts = np.stack([X, Y, Z], axis=-1)  # (ns, ring, 3)
        # kanat ucu katlama (asimetrik kapanma / kulak katlama)
        folds = []
        if fold_l > 0:
            folds.append((-1, -fold_pos, fold_l * math.radians(118)))
        if fold_r > 0:
            folds.append((1, fold_pos, fold_r * math.radians(118)))
        if ears > 0:
            folds.append((-1, -0.64, ears * math.radians(112)))
            folds.append((1, 0.64, ears * math.radians(112)))
        for side, sf, beta in folds:
            phf = sf * phimax
            px, py = R * math.sin(phf), R * (math.cos(phf) - 1)
            sel = (self.s < sf) if side < 0 else (self.s > sf)
            ang = beta if side < 0 else -beta
            ca, sa = math.cos(ang), math.sin(ang)
            sub = pts[sel]
            dx, dy = sub[..., 0] - px, sub[..., 1] - py
            # hafif çapraz katlama: hücum kenarı daha çok katlanır
            sub[..., 0] = px + dx * ca - dy * sa
            sub[..., 1] = py + dx * sa + dy * ca
            sub[..., 1] -= 0.15 * beta * (1 - self.ring_u[None, :])
            pts[sel] = sub
        # yükseklik: karabinaya göre
        pts[..., 1] += LINE_LEN
        return pts

    # ------------------------------------------------------------ hatlar
    def line_set(self, pts, brake_l=0.0, brake_r=0.0, hands=None):
        nc = self.nc
        segs = []
        ring_lower = lambda uidx: nc - 1 + uidx  # alt yüzeydeki indeks (uidx: self.u indeksi)
        rows = [(1, 0.12, "A"), (4, 0.0, "B"), (7, -0.12, "C")]
        spans = np.linspace(0.04, 0.9, 7)
        tops = {}
        for side in (-1, 1):
            for (ui, dz, name) in rows:
                top = np.array([side * 0.24, 1.15, dz])
                tops[(side, name)] = top
                for sp in spans:
                    j = int(round((side * sp + 1) / 2 * (self.ns - 1)))
                    a = pts[j, ring_lower(ui)]
                    segs.append((a, top, name))
                segs.append((top, np.array([side * 0.21, 0.0, 0.0]), "riser"))
            # fren hatları
            b = brake_l if side < 0 else brake_r
            hand = np.array([side * 0.32, 0.55 - 0.75 * b, -0.08 - 0.1 * b])
            if hands is not None and hands.get(side) is not None:
                hand = np.array(hands[side], float)
            pulley = np.array([side * 0.26, 1.05, -0.2])
            for sp in np.linspace(0.42, 0.96, 5):
                j = int(round((side * sp + 1) / 2 * (self.ns - 1)))
                a = pts[j, ring_lower(nc - 1)]
                segs.append((a, pulley, "brake"))
            segs.append((pulley, hand, "hand"))
        return segs

    # ------------------------------------------------------------ pilot
    @staticmethod
    def pilot_parts(brake_l=0.0, brake_r=0.0, pose="seated", run=0.0, t=0.0, weight=0.0, bar=0.0, hands=None):
        """(merkez1, merkez2, yarıçap, renk) kapsülleri. weight: -1 sol .. 1 sağ ağırlık."""
        wx = 0.12 * weight
        parts = []
        helmet = np.array([wx * 1.4, 0.42, 0.06])
        parts.append((helmet, helmet, 0.17, "helmet"))
        parts.append((np.array([wx, 0.18, 0.0]), np.array([wx * 0.6, -0.30, -0.02]), 0.19, "suit"))
        parts.append((np.array([wx, 0.12, -0.2]), np.array([wx * 0.6, -0.45, -0.22]), 0.21, "harness"))
        stand = 0.0 if pose == "seated" else (1.0 if pose in ("standing", "run") else float(pose))
        hip = np.array([wx * 0.5 * (1 - stand), -0.42, 0.0])
        if stand < 0.5:
            parts.append((hip + [0, 0, -0.05], hip + [0, -0.06 - 0.3 * stand, 0.45 * (1 - 2 * stand)], 0.24, "harness"))
        for sx in (-1, 1):
            ph = run * math.sin(t * 9.0 + (0 if sx < 0 else math.pi))
            knee_s = np.array([sx * 0.13, -0.5 + 0.05 * bar, 0.52 + 0.1 * bar])
            foot_s = np.array([sx * 0.13, -0.88 + 0.35 * bar, 0.62 + 0.42 * bar])
            knee_r = np.array([sx * 0.12, -0.88, 0.12 + 0.25 * ph])
            foot_r = np.array([sx * 0.12, -1.32 + 0.12 * max(0, ph), 0.0 + 0.35 * ph])
            knee = knee_s + (knee_r - knee_s) * stand
            foot = foot_s + (foot_r - foot_s) * stand
            parts.append((hip + [sx * 0.13, 0, 0.05 * (1 - stand)], knee, 0.11, "suit"))
            parts.append((knee, foot, 0.09, "suit"))
            parts.append((foot, foot + [0, 0, 0.08], 0.075, "boot"))
        for sx, b in ((-1, brake_l), (1, brake_r)):
            sh = np.array([sx * 0.22 + wx, 0.18, 0.02])
            hand = np.array([sx * 0.32, 0.55 - 0.75 * b, -0.08 - 0.1 * b])
            if hands is not None and hands.get(sx) is not None:
                hand = np.array(hands[sx], float)
            elbow = (sh + hand) / 2 + [sx * 0.12, -0.12, 0.05]
            parts.append((sh, elbow, 0.07, "suit"))
            parts.append((elbow, hand, 0.06, "suit"))
            parts.append((hand, hand, 0.06, "glove"))
        return parts


PILOT_COLORS = {"helmet": "#F8FAFC", "suit": "#1F2937", "harness": "#0F172A", "boot": "#7C2D12", "glove": "#111827"}


def _att_matrix(pitch, roll, heading):
    # pitch>0: kanat öne (dalış); roll>0: sağa yatış; heading: dikey eksende dönüş
    return _ry(heading) @ _rz(-roll) @ _rx(pitch)


def _cam_matrix(yaw, elev):
    return _rx(elev) @ _ry(yaw)


SIDE = -math.pi / 2
SIDE_34 = -math.pi / 2 + 0.62
REAR_34 = math.pi - 0.5

_SURF_CACHE = {}


def render(c, x, y, scale, *, yaw=-math.pi / 2, elev=0.12, pitch=0.0, roll=0.0, heading=0.0,
           anchor="pilot", alpha=1.0, glider=None, pilot=True, lines=True, pose="seated", run=0.0,
           weight=0.0, t=0.0, ss=2, shadow=None, light=(-0.35, 0.8, 0.45), pilot_scale=1.0, pilot_turn=0.0,
           bar=0.0, hands=None, hl=None, line_alpha=1.0, **geo):
    """Kanat+pilotu (x,y) ekran noktasına çiz.

    yaw: kamera yönü (-pi/2 = yandan, kanat sağa uçar; 0 = önden; pi = arkadan)
         3/4 görünüm için SIDE_34 = -pi/2 + 0.6
    elev: kamera yükseklik açısı (pozitif = yukarıdan bakış)
    anchor: 'pilot' (x,y = karabina) ya da 'center' (kanat ile pilot ortası) ya da 'wing'
    geo: Glider.geometry parametreleri (brake_l, brake_r, fold_l, fold_r, ears, front, stall, inflate, crumple, flat)
    """
    if alpha <= 0.003:
        return
    g = glider or _default_glider()
    bl, br = geo.get("brake_l", 0.0), geo.get("brake_r", 0.0)
    pts = g.geometry(t=t, **geo)
    R = _cam_matrix(yaw, elev) @ _att_matrix(pitch, roll, heading)
    RP = _cam_matrix(yaw, elev) @ _att_matrix(max(-0.12, min(0.12, pitch * 0.2)), roll, heading) @ _ry(pilot_turn)
    V = pts.reshape(-1, 3) @ R.T
    ns, nr = pts.shape[0], pts.shape[1]
    V = V.reshape(ns, nr, 3)
    if anchor == "center":
        off = (np.array([0, LINE_LEN / 2, 0]) @ R.T)
    elif anchor == "wing":
        off = (np.array([0, LINE_LEN, 0]) @ R.T)
    else:
        off = np.zeros(3)
    sx = lambda v: (x - (v[..., 0] - off[0]) * scale, y - (v[..., 1] - off[1]) * scale)
    SX, SY = sx(V)

    # ekran sınır kutusu
    pil_pts = np.array([[0, 0.6, 0], [0, -1.4, 0]]) @ R.T
    allx = np.concatenate([SX.ravel(), x - (pil_pts[:, 0] - off[0]) * scale])
    ally = np.concatenate([SY.ravel(), y - (pil_pts[:, 1] - off[1]) * scale])
    pad = 0.6 * scale + 6
    bx0, by0 = float(allx.min() - pad), float(ally.min() - pad)
    bx1, by1 = float(allx.max() + pad), float(ally.max() + pad)
    bx0, by0 = max(bx0, -200), max(by0, -200)
    bx1, by1 = min(bx1, 1080 + 200), min(by1, 1920 + 200)
    bw, bh = int(bx1 - bx0) + 1, int(by1 - by0) + 1
    if bw <= 2 or bh <= 2:
        return
    key = (bw * ss // 64 + 1, bh * ss // 64 + 1)
    surf = _SURF_CACHE.get(key)
    if surf is None:
        surf = skia.Surface(key[0] * 64, key[1] * 64)
        if len(_SURF_CACHE) > 40:
            _SURF_CACHE.clear()
        _SURF_CACHE[key] = surf
    oc = surf.getCanvas()
    oc.clear(skia.ColorTRANSPARENT)
    oc.save()
    oc.scale(ss, ss)
    oc.translate(-bx0, -by0)

    # --- kanat üçgenleri
    L = np.array(light, float)
    L /= np.linalg.norm(L)
    A = V[:-1, :-1]
    B = V[1:, :-1]
    Cc = V[1:, 1:]
    D = V[:-1, 1:]
    nrm = np.cross(Cc - A, B - D)
    nl = np.linalg.norm(nrm, axis=-1, keepdims=True) + 1e-9
    nrm = nrm / nl
    lam = np.abs((nrm * L).sum(-1))
    facing = nrm[..., 2]
    depth = (A[..., 2] + Cc[..., 2]) / 2
    upper = np.broadcast_to(g.ring_upper[None, :-1], depth.shape)
    ring_u = g.ring_u[None, :-1]
    order = np.argsort(depth.ravel())
    cols = np.zeros(depth.shape + (3,))
    for j in range(ns - 1):
        rgb, seam, _ = g.cell_rgb[j]
        cols[j] = rgb
        if seam:
            cols[j] *= 0.86
    under = g.colors["under"]
    cols = np.where(upper[..., None], cols, cols * under)
    # hücre ağızları (alt yüzeyde hücum kenarına yakın)
    mouth = (~upper) & (np.broadcast_to(ring_u, depth.shape) < 0.07)
    cols = np.where(mouth[..., None], np.array([30, 24, 30.0]), cols)
    shade_k = 0.58 + 0.42 * lam + 0.10 * np.clip(facing, 0, 1)
    cols = np.clip(cols * shade_k[..., None], 0, 255)
    a8 = int(255 * clamp(alpha))
    sxA, syA = SX[:-1, :-1].ravel(), SY[:-1, :-1].ravel()
    sxB, syB = SX[1:, :-1].ravel(), SY[1:, :-1].ravel()
    sxC, syC = SX[1:, 1:].ravel(), SY[1:, 1:].ravel()
    sxD, syD = SX[:-1, 1:].ravel(), SY[:-1, 1:].ravel()
    cflat = cols.reshape(-1, 3).astype(int)
    positions, colors = [], []
    Pt = skia.Point
    for i in order:
        col = (a8 << 24) | (int(cflat[i, 0]) << 16) | (int(cflat[i, 1]) << 8) | int(cflat[i, 2])
        positions += [Pt(sxA[i], syA[i]), Pt(sxB[i], syB[i]), Pt(sxC[i], syC[i]),
                      Pt(sxA[i], syA[i]), Pt(sxC[i], syC[i]), Pt(sxD[i], syD[i])]
        colors += [col] * 6

    def draw_canopy():
        verts = skia.Vertices(skia.Vertices.kTriangles_VertexMode, positions, None, colors)
        oc.drawVertices(verts, skia.Paint(AntiAlias=True), skia.BlendMode.kDst)

    def draw_lines():
        if not lines:
            return
        segs = g.line_set(pts, bl, br, hands)
        path_l, path_r, path_b = skia.Path(), skia.Path(), skia.Path()
        hl_paths = {}
        for a, b, kind in segs:
            av = a @ R.T
            bv = (b @ RP.T) if kind == "hand" else (b @ R.T)
            ax, ay = x - (av[0] - off[0]) * scale, y - (av[1] - off[1]) * scale
            bx, by = x - (bv[0] - off[0]) * scale, y - (bv[1] - off[1]) * scale
            grp = "brake" if kind in ("brake", "hand") else kind
            if hl and grp in hl:
                pth = hl_paths.setdefault(grp, skia.Path())
            else:
                pth = path_b if kind in ("brake", "hand") else (path_r if kind == "riser" else path_l)
            pth.moveTo(ax, ay)
            pth.lineTo(bx, by)
        lw = max(0.6, scale * 0.012)
        la = alpha * line_alpha * (0.35 if hl else 1.0)
        oc.drawPath(path_l, P("#334155", 0.75 * la, stroke=lw))
        oc.drawPath(path_b, P("#B91C1C", 0.65 * la, stroke=lw))
        oc.drawPath(path_r, P("#0F172A", alpha, stroke=max(1.5, scale * 0.05), cap="butt"))
        for grp, pth in hl_paths.items():
            col = hl[grp] if isinstance(hl, dict) else "#FFD23F"
            oc.drawPath(pth, P(col, 0.35 * alpha, stroke=lw * 6, blur=lw * 2))
            oc.drawPath(pth, P(col, alpha, stroke=lw * 2.2))

    def draw_pilot():
        if not pilot:
            return
        parts = Glider.pilot_parts(bl, br, pose, run, t, weight, bar, hands)
        if bar > 0.05:
            # hızlandırıcı barı: A askısından ayaklara
            for sx in (-1, 1):
                top = np.array([sx * 0.22, 0.9, 0.08]) @ R.T
                foot = np.array([sx * 0.13, -0.88 + 0.35 * bar, 0.62 + 0.42 * bar]) @ RP.T
                oc.drawLine(x - (top[0] - off[0]) * scale, y - (top[1] - off[1]) * scale,
                            x - (foot[0] - off[0]) * scale, y - (foot[1] - off[1]) * scale, P("#FFD23F", alpha, stroke=max(1, scale * 0.025)))
        items = []
        for p1, p2, r, kind in parts:
            v1, v2 = (np.array(p1) * pilot_scale) @ RP.T, (np.array(p2) * pilot_scale) @ RP.T
            items.append(((v1[2] + v2[2]) / 2, v1, v2, r * pilot_scale, kind))
        items.sort(key=lambda it: it[0])
        for _, v1, v2, r, kind in items:
            x1, y1 = x - (v1[0] - off[0]) * scale, y - (v1[1] - off[1]) * scale
            x2, y2 = x - (v2[0] - off[0]) * scale, y - (v2[1] - off[1]) * scale
            col = PILOT_COLORS[kind]
            rr = r * scale
            if abs(x1 - x2) + abs(y1 - y2) < 0.5:
                if kind == "helmet":
                    oc.drawCircle(x1, y1, rr, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial(
                        skia.Point(x1 - rr * 0.35, y1 - rr * 0.4), rr * 1.3, [C("#FFFFFF", alpha), C("#CBD5E1", alpha)])))
                    # hilal vizör + turuncu şerit (kask içine kırpılmış)
                    fwd = np.array([0, 0, 1.0]) @ RP.T
                    vx, vy = -fwd[0], -fwd[1]
                    oc.save()
                    clip = skia.Path()
                    clip.addCircle(x1, y1, rr)
                    oc.clipPath(clip, skia.ClipOp.kIntersect, True)
                    if fwd[2] > -0.5:
                        oc.drawCircle(x1 + vx * rr * 0.9, y1 + vy * rr * 0.9 + rr * 0.25, rr * 0.8,
                                      P("#0F172A", alpha * clamp(0.75 + fwd[2] * 0.5)))
                    oc.drawCircle(x1 - vx * rr * 0.85, y1 - vy * rr * 0.85 - rr * 0.35, rr * 0.55, P(PAL["orange"], alpha))
                    oc.restore()
                    oc.drawCircle(x1, y1, rr, P("#0F172A", 0.5 * alpha, stroke=max(1, rr * 0.08)))
                else:
                    oc.drawCircle(x1, y1, rr, P(col, alpha))
            else:
                oc.drawLine(x1, y1, x2, y2, P(col, alpha, stroke=2 * rr))

    if elev > 0.6:
        draw_pilot()
        draw_lines()
        draw_canopy()
    else:
        draw_canopy()
        draw_lines()
        draw_pilot()
    oc.restore()
    img = surf.makeImageSnapshot()
    src = skia.Rect.MakeWH(bw * ss, bh * ss)
    dst = skia.Rect.MakeXYWH(bx0, by0, bw, bh)
    if shadow:
        c.drawImageRect(img, src, dst.makeOffset(shadow[0], shadow[1]), skia.SamplingOptions(skia.FilterMode.kLinear),
                        skia.Paint(ImageFilter=skia.ImageFilters.DropShadowOnly(0, 0, shadow[2], shadow[2], C("#000000", shadow[3]))))
    c.drawImageRect(img, src, dst, skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(AntiAlias=True))

    def proj(p, pilot_frame=False):
        v = np.array(p, float) @ (RP.T if pilot_frame else R.T)
        return (x - (v[0] - off[0]) * scale, y - (v[1] - off[1]) * scale)

    def surf_pt(kind, sv):
        j = int(round((clamp(sv, -1, 1) + 1) / 2 * (ns - 1)))
        k = {"le": g.nc - 1, "te": 0, "top": g.nc // 2, "mouth": g.nc}[kind]
        return (float(SX[j, k]), float(SY[j, k]))
    return {"proj": proj, "surf": surf_pt, "pilot": proj([0, 0, 0]), "bbox": (bx0, by0, bx1, by1)}


_G = None


def _default_glider():
    global _G
    if _G is None:
        _G = Glider()
    return _G


def project_point(p, x, y, scale, yaw=-math.pi / 2, elev=0.12, pitch=0.0, roll=0.0, heading=0.0, anchor="pilot"):
    """Model noktasını ekrana yansıt (etiket/ok konumlamak için)."""
    R = _cam_matrix(yaw, elev) @ _att_matrix(pitch, roll, heading)
    v = np.array(p, float) @ R.T
    if anchor == "center":
        off = np.array([0, LINE_LEN / 2, 0]) @ R.T
    elif anchor == "wing":
        off = np.array([0, LINE_LEN, 0]) @ R.T
    else:
        off = np.zeros(3)
    return x - (v[0] - off[0]) * scale, y - (v[1] - off[1]) * scale
