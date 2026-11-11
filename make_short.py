"""台本JSON → 縦型ショート動画(1080x1920, 30fps)を生成する。
茶トラ白ねこアバターが口パクで解説し、ナレーションはVOICEVOXで合成する。
使い方: python3 make_short.py scripts.json out_dir [id ...]
環境変数 FRAMES_ONLY=1 で静止画プレビューだけ出力。
"""
import io, json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import art
import voice

W, H, FPS = 1080, 1920, 30
PAD = 0.45  # 各カット後の間（秒）
LEAD = 0.15
FONT_BLACK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_MED = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"
BG = (250, 247, 242)
INK = (38, 38, 44)
CHANNEL = "よっしーの「1分からだ育て」"
ROLE = "理学療法士 / 体軸キッズ&ジュニアトレーナー"

TAG_ICON = [("こんな子", "question"), ("なぜ", "bulb"), ("あそび", "play"),
            ("レベルアップ", "star"), ("声かけ", "chat"), ("今日から", "heart")]


def font(path, size):
    return ImageFont.truetype(path, size, index=0)


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for ch in text:
        if draw.textlength(cur + ch, font=fnt) > max_w and cur:
            if ch in "、。！？」）ぁぃぅぇぉっゃゅょァィゥェォッャュョー":
                lines.append(cur + ch)
                cur = ""
                continue
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    if len(lines) > 1 and len(lines[-1]) <= 2:
        lines[-1] = lines[-2][-2:] + lines[-1]
        lines[-2] = lines[-2][:-2]
    return lines


def pose_for(s, i):
    beat = s["beats"][i]
    if "pose" in beat:
        return beat["pose"]
    if i == len(s["beats"]) - 1:
        return {"arm": "up", "eyes": "happy"}
    return {"arm": "point" if i % 2 == 0 else "down", "eyes": "open"}


def icon_for(tag):
    for key, kind in TAG_ICON:
        if key in tag:
            return kind
    return "star"


def paste(img, path, xy):
    im = Image.open(path).convert("RGBA")
    img.paste(im, xy, im)


def draw_frame(s, i, mouth):
    color_hex = s["color"]
    color = hex2rgb(color_hex)
    beat = s["beats"][i]
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # 背景のやわらかい水玉
    light = tuple(int(c + (255 - c) * 0.85) for c in color)
    for (cx, cy, r) in [(960, 300, 120), (90, 560, 70), (1010, 1180, 90), (520, 1500, 50)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=light)

    # 上部帯
    d.rectangle([0, 0, W, 200], fill=color)
    d.text((W // 2, 80), CHANNEL, font=font(FONT_BLACK, 56), fill="white", anchor="mm")
    d.text((W // 2, 150), ROLE, font=font(FONT_MED, 30), fill="white", anchor="mm")

    # カテゴリチップ
    chip_f = font(FONT_BOLD, 40)
    label = s["pillar"]
    tw = d.textlength(label, font=chip_f)
    x0 = (W - tw) // 2 - 36
    d.rounded_rectangle([x0, 240, x0 + tw + 72, 306], radius=33, outline=color, width=4, fill=BG)
    d.text((W // 2, 273), label, font=chip_f, fill=color, anchor="mm")

    # テーマ
    tf = font(FONT_BLACK, 100)
    y = 330
    for line in s["title"].split("\n"):
        d.text((W // 2, y + 55), line, font=tf, fill=INK, anchor="mm")
        y += 125

    # 吹き出しカード（ねこのセリフ）
    card_top, card_bot = 610, 1210
    d.polygon([(170, card_bot - 4), (270, card_bot - 4), (190, 1290)], fill="white", outline=None)
    d.rounded_rectangle([60, card_top, W - 60, card_bot], radius=40, fill="white", outline=(228, 224, 216), width=3)
    d.line([(172, card_bot), (190, 1290), (268, card_bot)], fill=(228, 224, 216), width=3)
    d.line([(174, card_bot - 1), (266, card_bot - 1)], fill="white", width=5)

    # タグ（アイコン付き）
    paste(img, art.icon_png(icon_for(beat["tag"]), color_hex, 84), (100, card_top + 40))
    tagf = font(FONT_BOLD, 44)
    d.text((200, card_top + 82), beat["tag"], font=tagf, fill=color, anchor="lm")

    # 本文
    cf = font(FONT_BOLD, 64)
    lines = wrap(d, beat["text"], cf, W - 290)
    lh = 96
    area_top, area_bot = card_top + 150, card_bot - 70
    ty = area_top + max(0, (area_bot - area_top - lh * len(lines)) // 2)
    for line in lines:
        d.text((120, ty), line, font=cf, fill=INK)
        ty += lh

    # 進捗ドット（カード下部）
    n = len(s["beats"])
    gap = 40
    sx = W // 2 - gap * (n - 1) // 2
    for k in range(n):
        r = 12 if k == i else 8
        fill = color if k <= i else (220, 216, 208)
        d.ellipse([sx + k * gap - r, card_bot - 40 - r, sx + k * gap + r, card_bot - 40 + r], fill=fill)

    # テーマ小物（右下）とねこ（左下）
    if s.get("prop"):
        paste(img, art.prop_png(s["prop"], 300), (690, 1270))
    p = pose_for(s, i)
    paste(img, art.cat_png(mouth, p["eyes"], p["arm"], color_hex, 360), (70, 1240))
    return img


def mouth_track(seg, n_frames):
    """音声の大きさから口パク（開/閉）を決める"""
    hop = len(seg) / n_frames
    rms = np.array([np.sqrt(np.mean(seg[int(k * hop):int((k + 1) * hop)] ** 2) + 1e-12) for k in range(n_frames)])
    thr = max(rms.max() * 0.18, 1e-4)
    opened = rms > thr
    # 開きっぱなしにならないよう、長く続く区間は3フレームごとに閉じる
    run = 0
    for k in range(n_frames):
        if opened[k]:
            run += 1
            if run % 4 == 0:
                opened[k] = False
        else:
            run = 0
    return opened


def run(cmd, **kw):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, **kw)


def build(s, out_dir):
    work = os.path.join(out_dir, "_work", s["id"])
    os.makedirs(work, exist_ok=True)
    sr = voice.SR
    audio_parts, scene_files = [], []
    for i, beat in enumerate(s["beats"]):
        v = voice.tts(beat.get("say", beat["text"]))
        lead = int(LEAD * sr)
        n_frames = math.ceil(((lead + len(v)) / sr + PAD) * FPS)
        seg = np.zeros(int(round(n_frames / FPS * sr)), dtype=np.float32)
        seg[lead:lead + len(v)] = v
        audio_parts.append(seg)

        closed = np.asarray(draw_frame(s, i, "closed"), dtype=np.uint8).tobytes()
        opened = np.asarray(draw_frame(s, i, "open"), dtype=np.uint8).tobytes()
        track = mouth_track(seg, n_frames)

        tmp = os.path.join(work, f"b{i}.tmp.mp4")
        final = os.path.join(work, f"b{i}.mp4")
        p = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                              "-r", str(FPS), "-i", "-", "-vf", "fade=t=in:st=0:d=0.2,format=yuv420p",
                              "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp],
                             stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for k in range(n_frames):
            p.stdin.write(opened if track[k] else closed)
        p.stdin.close()
        if p.wait() != 0:
            raise RuntimeError(f"ffmpeg failed on beat {i}")
        os.replace(tmp, final)
        scene_files.append(final)

    audio = np.concatenate(audio_parts)
    peak = np.max(np.abs(audio)) or 1.0
    pcm = (audio / peak * 0.9 * 32767).astype(np.int16)
    wav_path = os.path.join(work, "voice.wav")
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(pcm.tobytes())

    lst = os.path.join(work, "list.txt")
    with open(lst, "w") as f:
        for path in scene_files:
            f.write(f"file '{os.path.abspath(path)}'\n")
    video_only = os.path.join(work, "video.mp4")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video_only])
    out = os.path.join(out_dir, f"{s['id']}.mp4")
    tmp = out[:-4] + ".tmp.mp4"
    run(["ffmpeg", "-y", "-i", video_only, "-i", wav_path, "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", tmp])
    os.replace(tmp, out)
    return out, len(audio) / sr


if __name__ == "__main__":
    src, out_dir, *ids = sys.argv[1:]
    os.makedirs(out_dir, exist_ok=True)
    data = json.load(open(src, encoding="utf-8"))
    for s in data:
        if ids and s["id"] not in ids:
            continue
        if os.environ.get("FRAMES_ONLY"):
            for i in range(len(s["beats"])):
                draw_frame(s, i, "open").save(os.path.join(out_dir, f"{s['id']}_b{i}.png"))
            continue
        path, secs = build(s, out_dir)
        print(f"{path}  {secs:.1f}s")
