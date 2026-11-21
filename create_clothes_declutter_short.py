from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import argparse
import subprocess
import wave

ROOT = Path(__file__).resolve().parent
W, H = 1080, 1920
FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"
NAVY = "#17263A"
IVORY = "#FFF9EF"


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


def make_slide(slides_dir, index, source_path, kicker, title, caption, accent, footer_text, infographic=False):
    source = Image.open(source_path).convert("RGB")
    background = cover(source, (W, H)).filter(ImageFilter.GaussianBlur(34)).convert("RGBA")
    veil = Image.new("RGBA", (W, H), (18, 35, 54, 148 if not infographic else 180))
    image = Image.alpha_composite(background, veil)
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((70, 78, 370, 142), 32, fill=accent)
    center(draw, (220, 111), kicker, 29, "white")
    title_size = 58 if len(title.replace("\n", "")) <= 18 else 48
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

    draw.rounded_rectangle((300, 1840, 780, 1886), 23, fill=(255, 255, 255, 48))
    center(draw, (540, 1863), footer_text, 21, "#F6E7C5")
    image.convert("RGB").save(slides_dir / f"slide-{index:02}.png", quality=95)


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

    audio = ROOT / "outputs" / "clothes_declutter_narration.wav"
    if not audio.exists():
        raise FileNotFoundError(f"Narration audio not found: {audio}")

    if args.variant == "personal":
        work = ROOT / "outputs" / "clothes_declutter_short"
        storyboard = ROOT / "outputs" / "服捨て_個人用ストーリーボード.png"
        infographic = ROOT / "outputs" / "服捨て_個人アカウント用.png"
        output_name = "服捨て_ショート動画.mp4"
        accents = ["#C96C58", "#487C89", "#C7953B", "#477765", "#8C5383", "#C96C58", "#C96C58"]
        footer_text = "HARUMICHI  BOOK NOTE"
        slide_specs = [
            (0, "BOOK NOTE", "服捨てで人生激変！", "「服はあるのに着る服がない…」\n原因はクローゼットに潜む他人軸", accents[0], False),
            (1, "PHASE 1", "まずは排出期から！", "靴下や靴など簡単な物から手放す\n1日1個でも確実に空間ができる", accents[1], False),
            (2, "PHASE 2", "買いながら捨てる新陳代謝", "減らした不安はモヤモヤ期の証\n試行錯誤で本当に似合う服を見つける", accents[2], False),
            (3, "MINDSET", "5つの思い込みを手放す", "「高かった服」「いつか着る服」\n過去の執着を捨て今の快適さを選ぶ", accents[3], False),
            (4, "PHASE 3", "心満たされる静寂期", "大好きな少数精鋭の定番だけ\n毎朝の迷いも他人の視線もゼロに！", accents[4], False),
            (5, "FREEDOM", "人生の主導権を取り戻す", "服を手放すことは自分を解き放つこと\n自分軸で軽やかに未来へ歩き出そう！", accents[5], False),
            (6, "SUMMARY", "服捨て メソッドまとめ", "服を捨てると、人生とお金が好転する\nまずは着ていない1着から手放そう！", accents[6], True),
        ]
    else:
        work = ROOT / "outputs" / "clothes_declutter_studio_short"
        storyboard = ROOT / "outputs" / "服捨て_スタジオ用ストーリーボード.png"
        infographic = ROOT / "outputs" / "服捨て_ダンススタジオ用.png"
        output_name = "服捨て_スタジオ版ショート動画.mp4"
        accents = ["#D45B72", "#2C818A", "#D78B42", "#2D8580", "#7D5AA6", "#D45B72", "#D45B72"]
        footer_text = "HARUKA CLOVER STUDIO"
        slide_specs = [
            (0, "BOOK NOTE", "服捨てで自分を解き放つ！", "着る服がない悩みの正体とは？\nクローゼットの他人軸を追い出そう", accents[0], False),
            (1, "PHASE 1", "簡単な物から即手放す", "シューズや古着からすっきり排出！\n水槽の濁りを抜いて視界クリアに", accents[1], False),
            (2, "PHASE 2", "買いながら新陳代謝！", "モヤモヤ期は自分軸への蛹の期間\n動いて踊れる最高の一着を探そう", accents[2], False),
            (3, "MINDSET", "3秒で手放す5つの執着", "高かった衣装やいつかの服も手放す\n内側の輝きは服を減らしても奪われない", accents[3], False),
            (4, "PHASE 3", "心地よい静寂期へ", "お気に入りの定番スタイルで\n朝の迷いと無駄な出費が劇的ゼロ！", accents[4], False),
            (5, "LIBERATION", "軽やかに自分らしく踊る！", "服を手放し人生の主導権を取り戻す\n心も体も軽く、最高のステージへ！", accents[5], False),
            (6, "SUMMARY", "服捨て メソッドまとめ", "服を捨てると、人生とお金が好転する\nまずは着ていない1着から手放そう！", accents[6], True),
        ]

    scenes = work / "backgrounds"
    slides_dir = work / "slides"
    work.mkdir(parents=True, exist_ok=True)
    slides_dir.mkdir(parents=True, exist_ok=True)
    scene_paths = split_storyboard(storyboard, scenes)

    for index, (scene_idx, kicker, title, caption, accent, is_info) in enumerate(slide_specs, 1):
        src = infographic if is_info else scene_paths[scene_idx]
        make_slide(slides_dir, index, src, kicker, title, caption, accent, footer_text, is_info)

    output, duration = build_video(work, slides_dir, audio, output_name)
    print(f"Generated: {output}")
    print(f"Duration: {duration:.2f}s")


if __name__ == "__main__":
    main()
