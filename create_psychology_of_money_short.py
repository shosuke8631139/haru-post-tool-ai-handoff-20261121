from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import argparse
import subprocess
import wave
import shutil
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

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


def make_slide(slides_dir, index, source_path, kicker, title, caption, accent, infographic=False, footer_text="HARUMICHI  BOOK NOTE"):
    source = Image.open(source_path).convert("RGB")
    background = cover(source, (W, H)).filter(ImageFilter.GaussianBlur(34)).convert("RGBA")
    veil = Image.new("RGBA", (W, H), (18, 35, 54, 148 if not infographic else 180))
    image = Image.alpha_composite(background, veil)
    draw = ImageDraw.Draw(image)

    # Top kicker badge
    kicker_font = font(26, True)
    kw = kicker_font.getlength(kicker)
    badge_w = max(240, int(kw + 80))
    bx = (W - badge_w) // 2
    draw.rounded_rectangle((bx, 70, bx + badge_w, 140), 35, fill=accent)
    draw.text((W // 2, 105), kicker, font=kicker_font, fill="white", anchor="mm")

    # Title
    title_size = 54 if len(title.replace("\n", "")) <= 18 else 46
    center(draw, (W // 2, 230), title, title_size, "white", True, stroke=4)

    # Central Card
    card_size = 940 if not infographic else 980
    card_y = 340 if not infographic else 320
    shadow = Image.new("RGBA", (card_size + 48, card_size + 48), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((24, 24, card_size + 24, card_size + 24), 54, fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    image.alpha_composite(shadow, ((W - shadow.width) // 2, card_y - 10))
    image.alpha_composite(rounded_square(source, card_size), ((W - card_size) // 2, card_y))

    # Caption panel below
    draw = ImageDraw.Draw(image)
    panel_y = card_y + card_size + 55
    panel_h = 360
    draw.rounded_rectangle((70, panel_y, W - 70, panel_y + panel_h), 40, fill=(255, 250, 240, 245))
    draw.rectangle((70, panel_y, 90, panel_y + panel_h), fill=accent)
    caption_size = 38 if len(caption.replace("\n", "")) < 48 else 33
    center(draw, (W // 2 + 10, panel_y + panel_h // 2), caption, caption_size, NAVY, True, spacing=14)

    # Footer pill
    draw.rounded_rectangle((300, 1840, W - 300, 1888), 24, fill=(255, 255, 255, 50))
    center(draw, (W // 2, 1864), footer_text, 20, "#FFE8B8", True)

    out_path = slides_dir / f"slide-{index:02}.png"
    image.convert("RGB").save(out_path, quality=95)
    return out_path


def wav_duration(path):
    with wave.open(str(path), "rb") as audio:
        return audio.getnframes() / audio.getframerate()


def build_video(work, slides_dir, audio_path, output_name):
    total = wav_duration(audio_path)
    weights = [0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.16]
    durations = [total * weight for weight in weights]
    segments = []

    for index, duration in enumerate(durations, 1):
        slide = slides_dir / f"slide-{index:02}.png"
        seg = work / f"segment-{index:02}.mp4"
        cmd = [
            ffmpeg, "-y", "-loop", "1", "-i", str(slide),
            "-c:v", "libx264", "-t", f"{duration:.3f}",
            "-pix_fmt", "yuv420p", "-vf", f"scale={W}:{H}",
            "-r", "30", str(seg)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        segments.append(seg)

    concat_txt = work / "concat.txt"
    concat_txt.write_text("\n".join(f"file '{s.name}'" for s in segments), encoding="utf-8")

    silent = work / "silent.mp4"
    subprocess.run(
        [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(silent)],
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
    shutil.copy2(output, OUT / output_name)
    return output, wav_duration(audio_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("variant", choices=["personal", "studio"])
    args = parser.parse_args()

    if args.variant == "personal":
        audio = OUT / "psychology_of_money_narration_personal.wav"
        work = OUT / "psychology_of_money_short"
        storyboard = OUT / "サイコロジー・オブ・マネー_個人用ストーリーボード.png"
        infographic = OUT / "サイコロジー・オブ・マネー_個人アカウント用.png"
        output_name = "サイコロジー・オブ・マネー_ショート動画.mp4"
        accents = ["#028C69", "#D28D2B", "#028C69", "#C94A4A", "#028C69", "#C94A4A", "#028C69"]
        footer_text = "HARUMICHI  BOOK NOTE"

        scenes = work / "backgrounds"
        slides_dir = work / "slides"
        work.mkdir(parents=True, exist_ok=True)
        slides_dir.mkdir(parents=True, exist_ok=True)
        scene_paths = split_storyboard(storyboard, scenes)

        slide_specs = [
            (scene_paths[0], "BOOK NOTE", "お金がもたらす最大の価値", "好きな時に好きな人と過ごす！\n真の幸福とは「時間の自由」", accents[0], False),
            (scene_paths[1], "LESSON 01", "知能より感情のコントロール", "MBAエリート破産vs清掃員の8億円！\n成功を分けるのはIQではなく規律", accents[1], False),
            (scene_paths[2], "LESSON 02", "時間を味方にする複利の力", "バフェットの富の99%は50歳以降！\n地味な継続こそが莫大な富を生む", accents[2], False),
            (scene_paths[3], "LESSON 03", "暴落でも黙ってじっと待て！", "最大のリターンより破滅しないこと！\n嵐が過ぎるまで市場にとどまれ", accents[3], False),
            (scene_paths[4], "LESSON 04", "市場の変動は「入場料」だ", "下落の恐怖は罰金ではない！\n未来のリターンを得るためのコスト", accents[4], False),
            (scene_paths[5], "FREEDOM", "使わなかったお金こそ真の富！", "見栄の消費を手放して\n自分の人生の主導権を取り戻そう！", accents[5], False),
            (infographic, "SUMMARY", "サイコロジー・オブ・マネー", "富とは「選択の自由」！\n時間を味方にする者が最後に勝つ。", accents[6], True),
        ]
    else:
        audio = OUT / "psychology_of_money_narration_studio.wav"
        work = OUT / "psychology_of_money_studio_short"
        storyboard = OUT / "サイコロジー・オブ・マネー_スタジオ用ストーリーボード.png"
        infographic = OUT / "サイコロジー・オブ・マネー_ダンススタジオ用.png"
        output_name = "サイコロジー・オブ・マネー_スタジオ版ショート動画.mp4"
        accents = ["#E07A5F", "#2A9D8F", "#E76F51", "#264653", "#2A9D8F", "#E76F51", "#2A9D8F"]
        footer_text = "HARUKA CLOVER STUDIO"

        scenes = work / "backgrounds"
        slides_dir = work / "slides"
        work.mkdir(parents=True, exist_ok=True)
        slides_dir.mkdir(parents=True, exist_ok=True)
        scene_paths = split_storyboard(storyboard, scenes)

        slide_specs = [
            (scene_paths[0], "BOOK NOTE", "お金がもたらす最高の配当！", "自分の時間を自分でコントロール！\n自由こそが何よりの贅沢", accents[0], False),
            (scene_paths[1], "LESSON 01", "高度な知識より感情の管理！", "パニック売りを回避してコツコツ貯める！\n身軽な習慣が未来の安心を創る", accents[1], False),
            (scene_paths[2], "LESSON 02", "小さな種が時間をかけて大樹へ", "富の99%は複利の力で育つ！\n焦らずじっくり待つのが成功の秘訣", accents[2], False),
            (scene_paths[3], "LESSON 03", "荒波が来ても慌てずキープ！", "市場の嵐でも売らずに耐え抜く！\n退場しない者が最後に笑う", accents[3], False),
            (scene_paths[4], "LESSON 04", "下落の恐怖は「入場料」！", "夢を叶えるための必要なコスト！\nブレない心で成長の波に乗ろう", accents[4], False),
            (scene_paths[5], "FREEDOM", "見栄を手放し、本当の自由へ！", "使わなかったお金こそ最大の自由！\n自分らしい暮らしと夢を掴もう！", accents[5], False),
            (infographic, "SUMMARY", "サイコロジー・オブ・マネー", "富とは「選択の自由」！\n時間を味方にする者が最後に勝つ。", accents[6], True),
        ]

    for index, spec in enumerate(slide_specs, 1):
        make_slide(slides_dir, index, *spec, footer_text=footer_text)

    output, duration = build_video(work, slides_dir, audio, output_name)
    print(f"Generated: {output}")
    print(f"Duration: {duration:.2f}s")


if __name__ == "__main__":
    main()
