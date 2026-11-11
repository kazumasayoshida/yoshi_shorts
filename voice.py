"""ナレーション合成。
既定は VOICEVOX ENGINE（HTTP API）を使う。GitHub Actions ではエンジンをサービスとして起動する。
環境変数:
  VOICEVOX_URL     エンジンのURL（既定 http://localhost:50021）
  VOICE_STYLE      話者スタイルID（既定 56 = 猫使アル・おちつき / 55 = ノーマル / 57 = うきうき）
  VOICE_SPEED      話速（既定 1.08）
  VOICE_BACKEND    "openjtalk" にすると見た目確認用の仮音声
"""
import io, json, os, time, urllib.parse, urllib.request, wave
import numpy as np

VOICEVOX_URL = os.environ.get("VOICEVOX_URL", "http://localhost:50021")
STYLE_ID = int(os.environ.get("VOICE_STYLE", "56"))
SPEED = float(os.environ.get("VOICE_SPEED", "1.08"))
INTONATION = float(os.environ.get("VOICE_INTONATION", "1.15"))
BACKEND = os.environ.get("VOICE_BACKEND", "voicevox")
SR = 24000
CREDIT = "VOICEVOX:猫使アル"


def _post(path, params, body=None):
    url = f"{VOICEVOX_URL}{path}?{urllib.parse.urlencode(params)}"
    data = json.dumps(body).encode() if body is not None else b""
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except OSError:
            if attempt == 4:
                raise
            time.sleep(3)


def tts(text, style_id=None):
    if BACKEND == "openjtalk":
        import pyopenjtalk
        x, sr = pyopenjtalk.tts(text, speed=1.12)
        n = int(len(x) * SR / sr)
        return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32) / 32768.0
    sid = STYLE_ID if style_id is None else style_id
    q = json.loads(_post("/audio_query", {"text": text, "speaker": sid}))
    q["speedScale"] = SPEED
    q["intonationScale"] = INTONATION
    q["prePhonemeLength"] = 0.05
    q["postPhonemeLength"] = 0.05
    q["outputSamplingRate"] = SR
    q["outputStereo"] = False
    wav_bytes = _post("/synthesis", {"speaker": sid}, q)
    with wave.open(io.BytesIO(wav_bytes)) as w:
        sr = w.getframerate()
        pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    x = pcm.astype(np.float32) / 32768.0
    if sr != SR:  # 念のためサンプリング周波数をそろえる
        n = int(len(x) * SR / sr)
        x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
    return x
