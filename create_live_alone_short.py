from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import argparse
import json
import subprocess
import urllib.parse
import urllib.request
import wave


ROOT = Path(__file__).resolve().parent
W, H = 1080, 1920
FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"
NAVY = "#17263A"
IVORY = "#FFF9EF"

NARRATION = (
    "今回ご紹介したいのは、石橋典子さんの『人と暮らせない』です。"
    "誰かと暮らすことが幸せな人もいれば、生活音や相手の機嫌が気になって、自宅でも休めない人がいます。"
    "ひとり暮らしなら、食事を体調に合わせ、部屋を自分が回復できる場所へ整えられます。"
    "連絡や調整が減り、大切なルーティン、仕事、学び、趣味の時間も守れます。"
    "音や光に敏感な人、ひとりでも行動できる人、同居すると休めない人、相手の機嫌を気にしすぎる人には、ひとりの空間が合うかもしれません。"
    "ただし、一緒に住まないことと、誰ともつながらないことは別です。"
    "緊急連絡先、定期的に話せる相手、病気や災害への備えは持っておく。"
    "誰かと暮らすのが正解でも、ひとりが最強でもありません。"
    "住む人数ではなく、自分が安心して眠れ、人とは心地よい距離でつながれる暮らしを選んでいいのだと思います。"
)


def font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def cover(image, size):
    ratio = max(size[0] / image.width, size[1] / image.height)
    resized = image.resize((round(image.width * ratio), round(image.height * ratio)), Image.Resampling.LANCZOS)
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def split_storyboard(source_path, scene_dir):
    scene_dir.mkdir(parents=True, exist_ok=True)
    source = Image.open(source_path).convert("RGB")
    cell_w = source.width // 3
    cell_h = source.height // 2
    paths = []
    for row in range(2):
        for col in range(3):
            index = row * 3 + col + 1
            left = col * cell_w
            top = row * cell_h
            right = source.width if col == 2 else (col + 1) * cell_w
            bottom = source.height if row == 1 else (row + 1) * cell_h
            cell = source.crop((left, top, right, bottom))
            inset = max(5, round(min(cell.size) * 0.012))
            cell = cell.crop((inset, inset, cell.width - inset, cell.height - inset))
            target = scene_dir / f"scene-{index:02}.png"
            cell.save(target)
            paths.append(target)
    return paths


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


def make_slide(slides_dir, index, source_path, kicker, title, caption, accent, infographic=False):
    source = Image.open(source_path).convert("RGB")
    background = cover(source, (W, H)).filter(ImageFilter.GaussianBlur(34)).convert("RGBA")
    veil = Image.new("RGBA", (W, H), (18, 35, 54, 148 if not infographic else 180))
    image = Image.alpha_composite(background, veil)
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((70, 78, 370, 142), 32, fill=accent)
    center(draw, (220, 111), kicker, 29, "white")
    title_size = 58 if len(title.replace("\n", "")) <= 18 else 49
    center(draw, (W // 2, 238), title, title_size, "white", True, 11, 2)

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
    draw.rounded_rectangle((70, panel_y, 1010, 1805), 46, fill=(255, 249, 239, 240))
    draw.rectangle((70, panel_y, 88, 1805), fill=accent)
    caption_size = 42 if len(caption.replace("\n", "")) < 52 else 35
    center(draw, (W // 2 + 8, (panel_y + 1805) // 2 - 4), caption, caption_size, NAVY, True, 18)

    draw.rounded_rectangle((330, 1840, 750, 1886), 23, fill=(255, 255, 255, 48))
    center(draw, (540, 1863), "HARUMICHI  BOOK NOTE", 21, "#F6E7C5")
    image.convert("RGB").save(slides_dir / f"slide-{index:02}.png", quality=95)


def synthesize(output):
    output.parent.mkdir(parents=True, exist_ok=True)
    speaker = 888753763
    query_url = "http://127.0.0.1:10101/audio_query?" + urllib.parse.urlencode({"text": NARRATION, "speaker": speaker})
    req = urllib.request.Request(query_url, method="POST")
    with urllib.request.urlopen(req, timeout=120) as response:
        query = json.loads(response.read().decode("utf-8"))
    query["speedScale"] = 1.09
    query["intonationScale"] = 0.86
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


def build_video(work, slides_dir, audio_path, output_name):
    import imageio_ffmpeg

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    total = wav_duration(audio_path)
    weights = [0.13, 0.13, 0.13, 0.14, 0.15, 0.14, 0.18]
    durations = [total * weight for weight in weights]
    segments = []
    for index, duration in enumerate(durations, 1):
        slide = slides_dir / f"slide-{index:02}.png"
        segment = work / f"segment-{index:02}.mp4"
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

    concat = work / "concat.txt"
    concat.write_text("\n".join(f"file '{p.as_posix()}'" for p in segments), encoding="utf-8")
    silent = work / "silent.mp4"
    subprocess.run(
        [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(silent)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    output = work / output_name
    subprocess.run(
        [
            ffmpeg, "-y", "-i", str(silent), "-i", str(audio_path),
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(output),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    return output, total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("variant", choices=["personal", "studio"])
    args = parser.parse_args()

    if args.variant == "personal":
        work = ROOT / "outputs" / "live_alone_short"
        storyboard = ROOT / "outputs" / "人と暮らせない_個人用ストーリーボード.png"
        infographic = ROOT / "outputs" / "人と暮らせない_個人アカウント用.png"
        output_name = "人と暮らせない_ショート動画.mp4"
        accents = ["#C96C58", "#C7953B", "#477765", "#487C89", "#73618E", "#B76C55", "#C96C58"]
    else:
        work = ROOT / "outputs" / "live_alone_studio_short"
        storyboard = ROOT / "outputs" / "人と暮らせない_スタジオ用ストーリーボード.png"
        infographic = ROOT / "outputs" / "人と暮らせない_ダンススタジオ用.png"
        output_name = "人と暮らせない_スタジオ版ショート動画.mp4"
        accents = ["#D45B72", "#D78B42", "#2D8580", "#7D5AA6", "#2C818A", "#D45B72", "#D45B72"]

    scenes = work / "backgrounds"
    slides_dir = work / "slides"
    work.mkdir(parents=True, exist_ok=True)
    slides_dir.mkdir(parents=True, exist_ok=True)
    scene_paths = split_storyboard(storyboard, scenes)

    slide_specs = [
        (scene_paths[0], "BOOK NOTE", "ひとりが正解、ではない", "自分が安心して休める\n暮らし方を選んでいい", accents[0], False),
        (scene_paths[1], "FOOD", "食事を体調に合わせる", "食べる物も時間も\n自分の体の声から決められる", accents[1], False),
        (scene_paths[2], "HOME", "部屋を、回復の場所へ", "好きな物だけを選び\n探し物と視覚のノイズを減らす", accents[2], False),
        (scene_paths[3], "ROUTINE", "時間と習慣を守る", "連絡や調整を減らし\n朝と夜の小さな習慣を続ける", accents[3], False),
        (scene_paths[4], "FOUR SIGNS", "向いている4つのサイン", "刺激に敏感／ひとりで行動できる\n同居すると休めない／機嫌を気にしすぎる", accents[4], False),
        (scene_paths[5], "LIFELINE", "ひとりでも、孤立しない", "緊急連絡先・話せる相手・防災準備\n必要なつながりは残しておく", accents[5], False),
        (infographic, "SAVE", "住む人数より、心が休まるか", "ひとりで住む。\n人とは、心地よい距離でつながる。", accents[6], True),
    ]
    for index, spec in enumerate(slide_specs, 1):
        make_slide(slides_dir, index, *spec)

    audio = ROOT / "outputs" / "live_alone_narration_v2.wav"
    if not audio.exists():
        synthesize(audio)
    output, duration = build_video(work, slides_dir, audio, output_name)
    print(output)
    print(f"duration={duration:.2f}s")


if __name__ == "__main__":
    main()
