from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
import subprocess
import urllib.parse
import urllib.request
import wave

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "outputs" / "money_life_short"
BG = WORK / "backgrounds"
SLIDES = WORK / "slides"
SLIDES.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"
NAVY = "#13253F"
TEAL = "#2D7276"
CORAL = "#C86D5A"
GOLD = "#C7953B"
IVORY = "#FFF9EF"

NARRATION = (
    "今回ご紹介したいのは、三浦さやかさんの『お金のある人生を叶える習慣』です。"
    "この本が伝えるのは、一発逆転ではなく、毎日の仕組みを整えること。"
    "まず『お金がない』で止めず、『どう用意する？』と問い直す。"
    "次に口座を、入れる、使う、貯める、の三つに分けて、流れを見えるようにする。"
    "支払いも、減っただけで終わらせず、学びや経験、人とのつながりなど、どんな価値と交換したかを見る。"
    "そして予定には先に余白を入れ、自分の得意は周りの人に聞く。"
    "やることはカレンダーへ出して、見える化する。"
    "お金のある人生は、残高だけが多い人生ではありません。"
    "必要な時に使え、やりたいことを選べる人生です。"
    "今日から、口座の役割を決め、予定表に三十分の余白を入れてみませんか。"
)


def font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def cover(image, size):
    ratio = max(size[0] / image.width, size[1] / image.height)
    resized = image.resize((round(image.width * ratio), round(image.height * ratio)), Image.Resampling.LANCZOS)
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def rounded_square(source, size=920):
    source = cover(source.convert("RGB"), (size, size))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size, size), 48, fill=255)
    layer = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    layer.paste(source.convert("RGBA"), (0, 0), mask)
    return layer


def center(draw, xy, value, size, fill, bold=True, spacing=10, stroke=0):
    draw.multiline_text(
        xy,
        value,
        font=font(size, bold),
        fill=fill,
        anchor="mm",
        align="center",
        spacing=spacing,
        stroke_width=stroke,
        stroke_fill=NAVY if stroke else None,
    )


def make_slide(index, source_path, kicker, title, caption, accent, infographic=False):
    source = Image.open(source_path).convert("RGB")
    background = cover(source, (W, H)).filter(ImageFilter.GaussianBlur(32)).convert("RGBA")
    veil = Image.new("RGBA", (W, H), (19, 37, 63, 155 if not infographic else 185))
    image = Image.alpha_composite(background, veil)
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((70, 78, 360, 142), 32, fill=accent)
    center(draw, (215, 111), kicker, 30, "white")
    center(draw, (W // 2, 232), title, 59 if len(title) < 20 else 51, "white", True, 11, 2)

    card_size = 940 if not infographic else 990
    card_y = 350 if not infographic else 330
    shadow = Image.new("RGBA", (card_size + 50, card_size + 50), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((25, 25, card_size + 25, card_size + 25), 58, fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(20))
    image.alpha_composite(shadow, ((W - shadow.width) // 2, card_y - 8))
    image.alpha_composite(rounded_square(source, card_size), ((W - card_size) // 2, card_y))

    draw = ImageDraw.Draw(image)
    panel_y = card_y + card_size + 68
    draw.rounded_rectangle((70, panel_y, 1010, 1805), 46, fill=(255, 249, 239, 238))
    draw.rectangle((70, panel_y, 88, 1805), fill=accent)
    center(draw, (W // 2 + 8, (panel_y + 1805) // 2 - 4), caption, 43 if len(caption) < 45 else 37, NAVY, True, 18)

    draw.rounded_rectangle((330, 1840, 750, 1886), 23, fill=(255, 255, 255, 48))
    center(draw, (540, 1863), "HARUMICHI  BOOK NOTE", 21, "#F6E7C5")
    image.convert("RGB").save(SLIDES / f"slide-{index:02}.png", quality=95)


def synthesize():
    output = WORK / "narration.wav"
    (WORK / "narration.txt").write_text(NARRATION, encoding="utf-8")
    speaker = 888753763
    query_url = "http://127.0.0.1:10101/audio_query?" + urllib.parse.urlencode({"text": NARRATION, "speaker": speaker})
    req = urllib.request.Request(query_url, method="POST")
    with urllib.request.urlopen(req, timeout=120) as response:
        query = json.loads(response.read().decode("utf-8"))
    query["speedScale"] = 1.05
    query["intonationScale"] = 0.88
    query["tempoDynamicsScale"] = 1.0
    query["pitchScale"] = -0.02
    query["prePhonemeLength"] = 0.12
    query["postPhonemeLength"] = 0.20
    synthesis_url = "http://127.0.0.1:10101/synthesis?" + urllib.parse.urlencode(
        {"speaker": speaker, "enable_interrogative_upspeak": "true"}
    )
    req = urllib.request.Request(
        synthesis_url,
        data=json.dumps(query, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as response:
        output.write_bytes(response.read())
    return output


def wav_duration(path):
    with wave.open(str(path), "rb") as audio:
        return audio.getnframes() / audio.getframerate()


def build_video(audio_path):
    import imageio_ffmpeg

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    total = wav_duration(audio_path)
    weights = [0.15, 0.18, 0.18, 0.16, 0.17, 0.16]
    durations = [total * weight for weight in weights]
    segments = []
    for index, duration in enumerate(durations, 1):
        slide = SLIDES / f"slide-{index:02}.png"
        segment = WORK / f"segment-{index:02}.mp4"
        frames = max(1, round(duration * 30))
        zoom = "min(zoom+0.00012,1.018)" if index % 2 else "min(zoom+0.00010,1.015)"
        subprocess.run(
            [
                ffmpeg, "-y", "-loop", "1", "-i", str(slide),
                "-vf", f"zoompan=z='{zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30,format=yuv420p",
                "-t", f"{duration:.3f}", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "20", str(segment),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        segments.append(segment)

    concat = WORK / "concat.txt"
    concat.write_text("\n".join(f"file '{p.as_posix()}'" for p in segments), encoding="utf-8")
    silent = WORK / "silent.mp4"
    subprocess.run(
        [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(silent)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    output = WORK / "お金のある人生_ショート動画.mp4"
    subprocess.run(
        [
            ffmpeg, "-y", "-i", str(silent), "-i", str(audio_path),
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(output),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return output, total


if __name__ == "__main__":
    slides = [
        (BG / "scene-01.png", "BOOK NOTE", "お金のある人生は\n「習慣」でつくる", "一発逆転より\n毎日の言葉・仕組み・時間を整える", CORAL, False),
        (BG / "scene-02.png", "MONEY FLOW", "意志より、3つの口座", "入れる・使う・貯める\n役割を分けると、お金の流れが見える", TEAL, False),
        (BG / "scene-03.png", "VALUE", "支払う＝価値と交換", "学び・経験・人とのつながりへ\n未来を育てる使い方を選ぶ", GOLD, False),
        (BG / "scene-04.png", "MARGIN", "余白は、先に予定する", "考える時間を確保すると\n次の選択肢とアイデアが生まれる", "#597789", False),
        (BG / "scene-05.png", "STRENGTH", "得意は、周りに聞く", "楽しさと見える化が\n長くやり抜く力を支えてくれる", "#6C7657", False),
        (ROOT / "outputs" / "お金のある人生_個人アカウント用.png", "SAVE", "今日から始める3つ", "口座の役割を決める\n予定に30分の余白を入れる\n3人に「私の得意」を聞く", CORAL, True),
    ]
    for i, args in enumerate(slides, 1):
        make_slide(i, *args)
    audio = WORK / "narration.wav"
    if not audio.exists():
        audio = synthesize()
    video, duration = build_video(audio)
    print(video)
    print(f"duration={duration:.2f}s")
