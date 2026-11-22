from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import argparse
import subprocess
import wave
import shutil

ROOT = Path(__file__).resolve().parent
BRAIN = Path(r"C:\Users\kurro\.gemini\antigravity\brain\37b73ff8-3d00-4627-bc53-b533c97e2644")
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


def make_card_layer(source_full, crop_box, size=940, is_studio=False, tag_text=None, tag_color=None):
    if crop_box is None:
        source_sq = cover(source_full, (size, size))
    else:
        cropped = source_full.crop(crop_box)
        if is_studio:
            plate = Image.new("RGBA", (size, size), (255, 252, 246, 255))
            garden_bg = cropped.resize((size, size), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(30))
            plate = Image.blend(plate, garden_bg.convert("RGBA"), 0.28)

            ratio = 910 / cropped.width
            cw, ch = 910, round(cropped.height * ratio)
            card_res = cropped.resize((cw, ch), Image.Resampling.LANCZOS)

            shadow = Image.new("RGBA", (cw + 40, ch + 40), (0, 0, 0, 0))
            ImageDraw.Draw(shadow).rounded_rectangle((20, 20, cw + 20, ch + 20), 28, fill=(0, 0, 0, 80))
            shadow = shadow.filter(ImageFilter.GaussianBlur(16))

            px = (size - cw) // 2
            py = (size - ch) // 2
            plate.alpha_composite(shadow, (px - 20, py - 12))
            plate.paste(card_res, (px, py))

            if tag_text and tag_color:
                draw_p = ImageDraw.Draw(plate)
                draw_p.rounded_rectangle((px, py - 60, px + 260, py - 16), 18, fill=tag_color)
                draw_p.text((px + 130, py - 38), tag_text, font=font(20, True), fill="white", anchor="mm")
            source_sq = plate
        else:
            plate = Image.new("RGB", (size, size), (251, 244, 230))
            ratio = 880 / cropped.width
            cw, ch = 880, round(cropped.height * ratio)
            card_res = cropped.resize((cw, ch), Image.Resampling.LANCZOS)
            plate.paste(card_res, ((size - cw) // 2, (size - ch) // 2))
            source_sq = plate

    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size, size), 48, fill=255)
    layer = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    layer.paste(source_sq.convert("RGBA"), (0, 0), mask)
    return layer


def make_slide(slides_dir, index, source_path, kicker, title, caption, accent, footer_text, crop_box=None, infographic=False, is_studio=False):
    source_full = Image.open(source_path).convert("RGB")
    card_size = 940 if not infographic else 980
    card_y = 345 if not infographic else 325

    tag_text = kicker if (crop_box and is_studio) else None
    card_layer = make_card_layer(source_full, crop_box, card_size, is_studio, tag_text, accent)

    bg_source = source_full.crop(crop_box) if crop_box else source_full
    background = cover(bg_source, (W, H)).filter(ImageFilter.GaussianBlur(34)).convert("RGBA")
    veil = Image.new("RGBA", (W, H), (18, 35, 54, 150 if not infographic else 180))
    image = Image.alpha_composite(background, veil)
    draw = ImageDraw.Draw(image)

    # Top tag (BOOK NOTE / RULE 01 etc.)
    draw.rounded_rectangle((70, 78, 370, 142), 32, fill=accent)
    center(draw, (220, 111), kicker, 29, "white")
    title_size = 56 if len(title.replace("\n", "")) <= 18 else 46
    center(draw, (W // 2, 238), title, title_size, "white", True, 11, 2)

    # Main Card shadow & paste
    shadow = Image.new("RGBA", (card_size + 50, card_size + 50), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((25, 25, card_size + 25, card_size + 25), 58, fill=(0, 0, 0, 115))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    image.alpha_composite(shadow, ((W - shadow.width) // 2, card_y - 8))
    image.alpha_composite(card_layer, ((W - card_size) // 2, card_y))

    # Caption panel
    draw = ImageDraw.Draw(image)
    panel_y = card_y + card_size + 65
    draw.rounded_rectangle((70, panel_y, 1010, 1805), 46, fill=(255, 249, 239, 240))
    draw.rectangle((70, panel_y, 88, 1805), fill=accent)
    caption_size = 42 if len(caption.replace("\n", "")) < 52 else 36
    center(draw, (W // 2 + 8, (panel_y + 1805) // 2 - 4), caption, caption_size, NAVY, True, 18)

    # Footer tag
    draw.rounded_rectangle((300, 1840, 780, 1886), 23, fill=(255, 255, 255, 48))
    center(draw, (540, 1863), footer_text, 21, "#F6E7C5")
    target_path = slides_dir / f"slide-{index:02}.png"
    image.convert("RGB").save(target_path, quality=95)
    return target_path


def wav_duration(path):
    with wave.open(str(path), "rb") as audio:
        return audio.getnframes() / audio.getframerate()


def build_video(work, slides_dir, audio_path, output_name):
    import imageio_ffmpeg

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    total = wav_duration(audio_path)
    weights = [0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.16]
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
    shutil.copy2(output, ROOT / "outputs" / output_name)
    return output, total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("variant", choices=["personal", "studio"])
    args = parser.parse_args()

    audio = ROOT / "outputs" / "one_hundred_million_narration.wav"
    if not audio.exists():
        raise FileNotFoundError(f"Narration audio not found: {audio}")

    if args.variant == "personal":
        work = ROOT / "outputs" / "100m_yen_short"
        infographic = ROOT / "outputs" / "1億円貯める方法_個人アカウント用.png"
        master_scene = BRAIN / "harumichi_sakurajimao_study_master_v2_1795344094254.jpg"
        output_name = "1億円貯める方法_ショート動画.mp4"
        accents = ["#C96C58", "#487C89", "#C7953B", "#477765", "#8C5383", "#2C818A", "#C96C58"]
        footer_text = "HARUMICHI  BOOK NOTE"
        is_studio = False

        slide_specs = [
            (master_scene, None, "BOOK NOTE", "1億円貯める超現実ルート！", "普通の会社員が億り人になる方法\n橘玲・大橋弘祐著の決定版！", accents[0], False),
            (infographic, (20, 418, 420, 715), "RULE 01", "人的資本の最大化！", "安定した給料こそ最大の投資資金！\n本業スキルを磨いて収入の原資をつくる", accents[1], False),
            (infographic, (425, 418, 830, 715), "RULE 02", "固定費と見栄の徹底削減", "食費の節約より住居・車・通信費！\n生活水準を上げずに支出を劇的カット", accents[2], False),
            (infographic, (830, 418, 1235, 715), "RULE 03", "不要な保険を即解約！", "高額療養費制度があるから安心！\n無駄な保険料や手数料の吸い取られを防ぐ", accents[3], False),
            (infographic, (20, 715, 420, 1010), "RULE 04", "全世界株式インデックス", "個別株や銀行の投資信託窓口はNG！\n手数料最安の全世界株式（オルカン）一択", accents[4], False),
            (infographic, (425, 715, 830, 1010), "RULE 05", "新NISAで自動積立＆放置", "給料日に自動積立を設定したら\n相場は見ずに複利の力でひたすら放置！", accents[5], False),
            (infographic, None, "SUMMARY", "1億円貯める 6つの黄金ルール", "「1億円」は贅沢のためではなく\n人生の主導権と自由を取り戻す武器！", accents[6], True),
        ]
    else:
        work = ROOT / "outputs" / "100m_yen_studio_short"
        infographic = ROOT / "outputs" / "1億円貯める方法_ダンススタジオ用.png"
        master_scene = BRAIN / "one_hundred_million_yen_study_square_v2_1795337798798.jpg"
        output_name = "1億円貯める方法_スタジオ版ショート動画.mp4"
        accents = ["#D45B72", "#2C818A", "#D78B42", "#2D8580", "#7D5AA6", "#E07A5F", "#D45B72"]
        footer_text = "HARUKA CLOVER STUDIO"
        is_studio = True

        slide_specs = [
            (master_scene, None, "BOOK NOTE", "会社員が1億円貯める方法！", "橘玲・大橋弘祐著の話題書！\n資本主義のルールを味方につけて自由に！", accents[0], False),
            (infographic, (12, 435, 620, 630), "RULE 01", "人的資本を最大化する！", "毎月の安定給与こそが最大の武器！\n自分の価値を高めて投資の原資を生み出す", accents[1], False),
            (infographic, (635, 435, 1240, 630), "RULE 02", "固定費と見栄をカット！", "食費より家賃・自動車・スマホ代！\n生活水準をむやみに上げず支出を絞る", accents[2], False),
            (infographic, (12, 635, 620, 830), "RULE 03", "無駄な保険は即見直し！", "日本の高額療養費制度を活用！\n手数料で資産を減らされるのを防ぐ", accents[3], False),
            (infographic, (635, 635, 1240, 830), "RULE 04", "全世界株式インデックス！", "プロも勝てないインデックス投資\n手数料最安の全世界株式（オルカン）で勝負", accents[4], False),
            (infographic, (12, 835, 620, 1030), "RULE 05", "新NISA自動積立で放置！", "毎月コツコツ複利の波に乗る！\n日々の値動きは見ずに長期で育てる", accents[5], False),
            (infographic, None, "SUMMARY", "1億円貯める 6つの黄金ルール", "「1億円」は理不尽から解放され\n自分の人生を自由に選ぶための最高の武器！", accents[6], True),
        ]

    slides_dir = work / "slides"
    work.mkdir(parents=True, exist_ok=True)
    slides_dir.mkdir(parents=True, exist_ok=True)

    for index, (src, crop_box, kicker, title, caption, accent, is_info) in enumerate(slide_specs, 1):
        make_slide(slides_dir, index, src, kicker, title, caption, accent, footer_text, crop_box, is_info, is_studio)

    output, duration = build_video(work, slides_dir, audio, output_name)
    print(f"Generated: {output}")
    print(f"Duration: {duration:.2f}s")


if __name__ == "__main__":
    main()
