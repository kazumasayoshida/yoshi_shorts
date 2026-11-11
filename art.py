"""オリジナル素材（茶トラ白ねこアバター・アイコン・小物イラスト）をSVGで描いてPNG化する。"""
import os, subprocess, functools

ORANGE = "#F2A65A"
STRIPE = "#D9792B"
LINE = "#5A3A22"
PINK = "#F49AA6"
WHITE = "#FFFFFF"

ART_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_art")


def _render(svg, name, width):
    os.makedirs(ART_DIR, exist_ok=True)
    svg_path = os.path.join(ART_DIR, name + ".svg")
    png_path = os.path.join(ART_DIR, f"{name}_{width}.png")
    with open(svg_path, "w") as f:
        f.write(svg)
    subprocess.run(["rsvg-convert", "-w", str(width), "-o", png_path, svg_path], check=True)
    return png_path


def cat_svg(mouth="closed", eyes="open", arm="point", lanyard="#2E9E6B"):
    s = []
    s.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 460">')
    sw = f'stroke="{LINE}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"'
    # しっぽ
    s.append(f'<path d="M300 400 C380 400 400 330 370 290" fill="none" stroke="{LINE}" stroke-width="34" stroke-linecap="round"/>')
    s.append(f'<path d="M300 400 C380 400 400 330 370 290" fill="none" stroke="{ORANGE}" stroke-width="22" stroke-linecap="round"/>')
    s.append(f'<path d="M378 352 l16 4 M384 322 l15 -2" stroke="{STRIPE}" stroke-width="7" stroke-linecap="round"/>')
    # からだ
    s.append(f'<ellipse cx="210" cy="365" rx="108" ry="85" fill="{ORANGE}" {sw}/>')
    s.append(f'<ellipse cx="210" cy="380" rx="62" ry="68" fill="{WHITE}"/>')
    s.append(f'<path d="M118 340 q14 4 22 -6 M120 372 q14 4 20 -6" stroke="{STRIPE}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    # あし
    s.append(f'<ellipse cx="165" cy="445" rx="34" ry="16" fill="{WHITE}" {sw}/>')
    s.append(f'<ellipse cx="255" cy="445" rx="34" ry="16" fill="{WHITE}" {sw}/>')
    # 腕
    def paw(x, y):
        return f'<ellipse cx="{x}" cy="{y}" rx="24" ry="21" fill="{WHITE}" {sw}/>'
    if arm in ("down", "point"):
        s.append(f'<path d="M140 320 Q128 350 140 380" stroke="{LINE}" stroke-width="40" fill="none" stroke-linecap="round"/>')
        s.append(f'<path d="M140 320 Q128 350 140 380" stroke="{ORANGE}" stroke-width="28" fill="none" stroke-linecap="round"/>')
        s.append(paw(146, 388))
    if arm == "down":
        s.append(f'<path d="M280 320 Q292 350 280 380" stroke="{LINE}" stroke-width="40" fill="none" stroke-linecap="round"/>')
        s.append(f'<path d="M280 320 Q292 350 280 380" stroke="{ORANGE}" stroke-width="28" fill="none" stroke-linecap="round"/>')
        s.append(paw(274, 388))
    if arm == "point":
        s.append(f'<path d="M285 318 Q330 300 352 248" stroke="{LINE}" stroke-width="40" fill="none" stroke-linecap="round"/>')
        s.append(f'<path d="M285 318 Q330 300 352 248" stroke="{ORANGE}" stroke-width="28" fill="none" stroke-linecap="round"/>')
        s.append(f'<path d="M340 300 l14 -8" stroke="{STRIPE}" stroke-width="7" stroke-linecap="round"/>')
        s.append(paw(356, 238))
    if arm == "up":
        for (a, b, c, px, py) in [("M138 318", "Q80 300", "62 222", 58, 210), ("M282 318", "Q340 300", "358 222", 362, 210)]:
            s.append(f'<path d="{a} {b} {c}" stroke="{LINE}" stroke-width="40" fill="none" stroke-linecap="round"/>')
            s.append(f'<path d="{a} {b} {c}" stroke="{ORANGE}" stroke-width="28" fill="none" stroke-linecap="round"/>')
            s.append(paw(px, py))
    # 首ひもと笛（トレーナーらしさ）
    s.append(f'<path d="M160 275 L210 335 L260 275" fill="none" stroke="{lanyard}" stroke-width="9" stroke-linejoin="round"/>')
    s.append(f'<rect x="196" y="330" width="34" height="20" rx="9" fill="#C9CED6" stroke="{LINE}" stroke-width="4"/>')
    s.append(f'<circle cx="203" cy="340" r="4" fill="{LINE}"/>')
    # 耳
    s.append(f'<path d="M95 130 L100 30 L180 85 Z" fill="{ORANGE}" {sw}/>')
    s.append(f'<path d="M325 130 L320 30 L240 85 Z" fill="{ORANGE}" {sw}/>')
    s.append(f'<path d="M112 108 L114 58 L158 88 Z" fill="{PINK}"/>')
    s.append(f'<path d="M308 108 L306 58 L262 88 Z" fill="{PINK}"/>')
    # 頭
    s.append(f'<ellipse cx="210" cy="180" rx="140" ry="115" fill="{ORANGE}" {sw}/>')
    # しま模様（おでこ・ほっぺ）
    s.append(f'<path d="M210 68 v34 M182 74 q6 16 4 30 M238 74 q-6 16 -4 30" stroke="{STRIPE}" stroke-width="9" fill="none" stroke-linecap="round"/>')
    s.append(f'<path d="M72 170 h30 M76 196 h26 M348 170 h-30 M344 196 h-26" stroke="{STRIPE}" stroke-width="8" stroke-linecap="round"/>')
    # 白いマズル＋鼻すじ（茶トラ白）
    s.append(f'<path d="M210 118 C196 150 190 170 186 190 L234 190 C230 170 224 150 210 118 Z" fill="{WHITE}"/>')
    s.append(f'<ellipse cx="210" cy="232" rx="82" ry="58" fill="{WHITE}"/>')
    # 目
    if eyes == "happy":
        s.append(f'<path d="M140 178 q22 -26 44 0 M236 178 q22 -26 44 0" stroke="{LINE}" stroke-width="9" fill="none" stroke-linecap="round"/>')
    else:
        for cx in (160, 260):
            s.append(f'<ellipse cx="{cx}" cy="170" rx="19" ry="24" fill="{LINE}"/>')
            s.append(f'<circle cx="{cx + 6}" cy="161" r="7" fill="{WHITE}"/>')
    # ほっぺ
    s.append(f'<ellipse cx="128" cy="222" rx="20" ry="12" fill="{PINK}" opacity="0.7"/>')
    s.append(f'<ellipse cx="292" cy="222" rx="20" ry="12" fill="{PINK}" opacity="0.7"/>')
    # 鼻・口
    s.append(f'<path d="M198 204 h24 l-12 13 Z" fill="{PINK}" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>')
    if mouth == "open":
        s.append(f'<path d="M188 230 q22 40 44 0 Z" fill="#B5485A" stroke="{LINE}" stroke-width="5" stroke-linejoin="round"/>')
        s.append(f'<path d="M198 248 q12 10 24 0" fill="{PINK}"/>')
    else:
        s.append(f'<path d="M210 217 v10 M186 228 q12 14 24 0 q12 14 24 0" stroke="{LINE}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    # ひげ
    s.append(f'<path d="M110 232 l-48 -8 M112 246 l-46 6 M310 232 l48 -8 M308 246 l46 6" stroke="{LINE}" stroke-width="3" stroke-linecap="round" opacity="0.55"/>')
    s.append('</svg>')
    return "\n".join(s)


@functools.lru_cache(maxsize=None)
def cat_png(mouth, eyes, arm, lanyard, width=380):
    name = f"cat_{mouth}_{eyes}_{arm}_{lanyard.strip('#')}"
    return _render(cat_svg(mouth, eyes, arm, lanyard), name, width)


# ── タグ用アイコン（白い線画、色つき丸の中に置く） ──
ICONS = {
    "question": '<path d="M38 38 q0 -18 22 -18 q22 0 22 18 q0 14 -18 20 v10" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round"/><circle cx="64" cy="94" r="7" fill="#fff"/>',
    "bulb": '<path d="M60 18 a30 30 0 0 1 18 54 v10 h-36 v-10 a30 30 0 0 1 18 -54 Z" fill="none" stroke="#fff" stroke-width="8" stroke-linejoin="round"/><path d="M46 96 h28 M50 106 h20" stroke="#fff" stroke-width="8" stroke-linecap="round"/>',
    "play": '<circle cx="60" cy="60" r="40" fill="none" stroke="#fff" stroke-width="8"/><path d="M50 40 L82 60 L50 80 Z" fill="#fff"/>',
    "star": '<path d="M60 14 L72 46 L106 47 L79 68 L89 101 L60 82 L31 101 L41 68 L14 47 L48 46 Z" fill="#fff"/>',
    "heart": '<path d="M60 100 C20 74 14 50 26 36 C38 22 54 26 60 40 C66 26 82 22 94 36 C106 50 100 74 60 100 Z" fill="#fff"/>',
    "chat": '<path d="M18 26 h84 a8 8 0 0 1 8 8 v42 a8 8 0 0 1 -8 8 h-50 l-20 18 v-18 h-14 a8 8 0 0 1 -8 -8 v-42 a8 8 0 0 1 8 -8 Z" fill="none" stroke="#fff" stroke-width="8" stroke-linejoin="round"/><circle cx="40" cy="55" r="6" fill="#fff"/><circle cx="60" cy="55" r="6" fill="#fff"/><circle cx="80" cy="55" r="6" fill="#fff"/>',
}


@functools.lru_cache(maxsize=None)
def icon_png(kind, color, width=120):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">'
           f'<circle cx="60" cy="60" r="60" fill="{color}"/>'
           f'<g transform="translate(12 12) scale(0.8)">{ICONS[kind]}</g></svg>')
    return _render(svg, f"icon_{kind}_{color.strip('#')}", width)


# ── テーマ小物イラスト ──
PROPS = {
    "flamingo": '''
<ellipse cx="150" cy="300" rx="120" ry="14" fill="#000" opacity="0.08"/>
<path d="M150 170 L150 295" stroke="#E86A87" stroke-width="9" stroke-linecap="round"/>
<path d="M150 175 L118 205 L150 230" stroke="#E86A87" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M140 295 h22" stroke="#E86A87" stroke-width="9" stroke-linecap="round"/>
<ellipse cx="160" cy="150" rx="62" ry="40" fill="#F7A8BC" stroke="#5A3A22" stroke-width="5"/>
<path d="M150 140 q-30 -10 -24 -26" stroke="#E86A87" stroke-width="0" fill="none"/>
<path d="M118 140 C90 120 100 70 120 60 C140 50 150 70 140 82" stroke="#5A3A22" stroke-width="22" fill="none" stroke-linecap="round"/>
<path d="M118 140 C90 120 100 70 120 60 C140 50 150 70 140 82" stroke="#F7A8BC" stroke-width="12" fill="none" stroke-linecap="round"/>
<circle cx="128" cy="62" r="20" fill="#F7A8BC" stroke="#5A3A22" stroke-width="5"/>
<circle cx="132" cy="58" r="4" fill="#5A3A22"/>
<path d="M144 60 q20 4 18 22 q-6 -10 -18 -8 Z" fill="#5A3A22"/>
<path d="M190 140 q30 -6 40 14 q-20 -4 -36 8" fill="#E86A87"/>''',
    "daruma": '''
<ellipse cx="150" cy="300" rx="110" ry="14" fill="#000" opacity="0.08"/>
<path d="M150 50 C230 50 260 140 250 210 C240 280 200 300 150 300 C100 300 60 280 50 210 C40 140 70 50 150 50 Z" fill="#E0443E" stroke="#5A3A22" stroke-width="6"/>
<ellipse cx="150" cy="140" rx="62" ry="54" fill="#FFF4E6" stroke="#5A3A22" stroke-width="5"/>
<circle cx="125" cy="135" r="16" fill="#fff" stroke="#5A3A22" stroke-width="4"/><circle cx="125" cy="135" r="7" fill="#5A3A22"/>
<circle cx="175" cy="135" r="16" fill="#fff" stroke="#5A3A22" stroke-width="4"/><circle cx="175" cy="135" r="7" fill="#5A3A22"/>
<path d="M105 112 q20 -12 36 0 M159 112 q20 -12 36 0" stroke="#5A3A22" stroke-width="6" fill="none" stroke-linecap="round"/>
<path d="M135 172 q15 8 30 0" stroke="#5A3A22" stroke-width="5" fill="none" stroke-linecap="round"/>
<path d="M105 225 q45 22 90 0" stroke="#F7C948" stroke-width="10" fill="none" stroke-linecap="round"/>''',
    "praise": '''
<ellipse cx="150" cy="300" rx="110" ry="14" fill="#000" opacity="0.08"/>
<path d="M40 60 h220 a20 20 0 0 1 20 20 v120 a20 20 0 0 1 -20 20 h-140 l-50 50 v-50 h-30 a20 20 0 0 1 -20 -20 v-120 a20 20 0 0 1 20 -20 Z" fill="#fff" stroke="#5A3A22" stroke-width="6" stroke-linejoin="round"/>
<path d="M150 190 C100 160 92 130 104 114 C116 98 140 102 150 120 C160 102 184 98 196 114 C208 130 200 160 150 190 Z" fill="#F49AA6" stroke="#5A3A22" stroke-width="5"/>
<path d="M66 96 l8 18 l18 2 l-14 12 l4 18 l-16 -10 l-16 10 l4 -18 l-14 -12 l18 -2 Z" fill="#F7C948"/>
<path d="M232 150 l6 13 l13 1 l-10 9 l3 13 l-12 -7 l-12 7 l3 -13 l-10 -9 l13 -1 Z" fill="#F7C948"/>''',
}


@functools.lru_cache(maxsize=None)
def prop_png(kind, width=300):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 320">{PROPS[kind]}</svg>'
    return _render(svg, f"prop_{kind}", width)
