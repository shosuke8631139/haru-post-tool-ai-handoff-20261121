import asyncio
import edge_tts
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import argparse
import subprocess
import wave
import shutil
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parent
BRAIN = Path(r"C:\Users\kurro\.gemini\antigravity\brain\37b73ff8-3d00-4627-bc53-b533c97e2644")
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
        return cover(source_full, (size, size))
    cropped = source_full.crop(crop_box)
    ratio = 910 / cropped.width
    cw, ch = 910, round(cropped.height * ratio)
    card_res = cropped.resize((cw, ch), Image.Resampling.LANCZOS)

    plate = Image.new("RGBA", (size, size), (255, 252, 246, 255))
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
    return plate


def make_slide(slides_dir, index, source_full, kicker, title, caption, accent, footer_text, crop_box=None, is_info=False, is_studio=False, tag_text=None):
    card_size = 940
    card_layer = make_card_layer(source_full, crop_box, card_size, is_studio=is_studio, tag_text=tag_text, tag_color=accent)

    bg = card_layer.resize((W, H), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(40))
    veil = Image.new("RGBA", (W, H), (18, 30, 48, 175) if not is_studio else (32, 54, 76, 170))
    image = Image.alpha_composite(bg.convert("RGBA"), veil)

    draw = ImageDraw.Draw(image)

    # Top kicker badge
    kicker_font = font(26, True)
    kw = kicker_font.getlength(kicker)
    badge_w = max(240, int(kw + 80))
    bx = (W - badge_w) // 2
    draw.rounded_rectangle((bx, 70, bx + badge_w, 140), 35, fill=accent)
    draw.text((W // 2, 105), kicker, font=kicker_font, fill="white", anchor="mm")

    # Title
    center(draw, (W // 2, 230), title, 48, "white", True, stroke=4)

    # Card
    card_y = 340
    card_round = Image.new("RGBA", (card_size, card_size), (0, 0, 0, 0))
    mask = Image.new("L", (card_size, card_size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, card_size, card_size), 36, fill=255)
    card_round.paste(card_layer, (0, 0), mask)

    shadow = Image.new("RGBA", (card_size + 48, card_size + 48), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((24, 24, card_size + 24, card_size + 24), 40, fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))

    image.alpha_composite(shadow, ((W - shadow.width) // 2, card_y - 12))
    image.alpha_composite(card_round, ((W - card_size) // 2, card_y))

    # Caption panel
    panel_y = card_y + card_size + 60
    panel_h = 360
    draw.rounded_rectangle((70, panel_y, W - 70, panel_y + panel_h), 36, fill=(255, 250, 240, 245))
    draw.rectangle((70, panel_y, 90, panel_y + panel_h), fill=accent)
    center(draw, (W // 2 + 10, panel_y + panel_h // 2), caption, 38 if len(caption) < 45 else 34, NAVY, True, spacing=14)

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
    # 7 slides
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


NARRATION_TEXT = (
    "今回ご紹介したいのは、本要約チャンネルの『金持ちが絶対買わないもの・上位1%の養分にならない6つのルール』です。"
    "まじめに働いているのにお金が残らない原因は、収入ではなく資本主義の搾取構造にあります。"
    "世のビジネスは、見栄や不安、孤独、恐怖を煽り、私たちからお金を吸い上げます。"
    "富裕層が避けるのは、世間体の豪華な葬儀、新築戸建て、高額商材、孤独消費、不要な保険、そして宝くじの6つ。"
    "代わりに激落ちくんや感動パンツなど生活を整えるアイテムを取り入れ、"
    "浮いた資金を新NISAでインデックス投資に回し、資産として働かせる側に回るのです。"
    "富裕層との差は収入ではなく意思決定の質。"
    "今日から感情で買わされるのをやめ、未来の自由を手に入れませんか？"
)


async def synthesize_narration(audio_path):
    mp3_path = audio_path.with_suffix(".mp3")
    print("Synthesizing narration with ja-JP-NanamiNeural (rate=+12%)...")
    comm = edge_tts.Communicate(NARRATION_TEXT, "ja-JP-NanamiNeural", rate="+12%")
    await comm.save(str(mp3_path))
    subprocess.run(
        [ffmpeg, "-y", "-i", str(mp3_path), "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", str(audio_path)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    print("Narration saved to:", audio_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("variant", choices=["personal", "studio"])
    args = parser.parse_args()

    audio = OUT / "what_rich_dont_buy_narration.wav"
    if not audio.exists():
        asyncio.run(synthesize_narration(audio))

    if args.variant == "personal":
        work = OUT / "what_rich_dont_buy_short"
        infographic = OUT / "金持ちが絶対買わないもの_個人アカウント用.png"
        master_scene = infographic
        output_name = "金持ちが絶対買わないもの_ショート動画.mp4"
        accents = ["#028C69", "#D28D2B", "#028C69", "#C94A4A", "#028C69", "#C94A4A", "#028C69"]
        footer_text = "HARUMICHI  BOOK NOTE"
        is_studio = False

        slide_specs = [
            (master_scene, None, "BOOK NOTE", "金持ちが買わない黄金ルール", "上位1%の養分にならない！\n生活防衛＆資産形成の決定版", accents[0], True),
            (infographic, (35, 470, 495, 570), "RULE 01", "立派すぎる葬儀を回避！", "世間体や同調バイアスを排除！\nシンプルな家族葬で十分", accents[1], False),
            (infographic, (35, 580, 495, 680), "RULE 02", "大手新築戸建はNG！", "住んだ瞬間に価値2割下落！\nブランド料と35年ローンを回避", accents[2], False),
            (infographic, (35, 690, 495, 790), "RULE 03", "高額情報教材に手を出すな", "将来の不安につけ込む商材NG！\n千円の良書と本業の実務で磨け", accents[3], False),
            (infographic, (505, 430, 965, 535), "RULE 05", "高額な民間保険を即解約！", "日本には高額療養費制度がある！\n無駄な特約を削り資金確保", accents[4], False),
            (infographic, (505, 540, 965, 648), "RULE 06", "愚か者の税金・宝くじ", "還元率46%の超搾取ギャンブル！\n期待値マイナスには1円も払わない", accents[5], False),
            (infographic, None, "SUMMARY", "買わない決断こそ最強の投資！", "富裕層との差は意思決定の質！\n新NISAで資本を働かせ自由を掴め", accents[6], True),
        ]
    else:
        work = OUT / "what_rich_dont_buy_studio_short"
        infographic = OUT / "金持ちが絶対買わないもの_ダンススタジオ用.png"
        master_scene = BRAIN / "slide1_rooftop_dance_jump_1795389403154.jpg"
        output_name = "金持ちが絶対買わないもの_スタジオ版ショート動画.mp4"
        accents = ["#E07A5F", "#2A9D8F", "#E76F51", "#264653", "#2A9D8F", "#E76F51", "#2A9D8F"]
        footer_text = "HARUKA CLOVER STUDIO"
        is_studio = True

        slide_specs = [
            (master_scene, None, "BOOK NOTE", "金持ちが買わない黄金ルール", "身軽さこそ最強のパフォーマンス！\n生活防衛＆資産形成の決定版", accents[0], False),
            (infographic, (15, 390, 485, 530), "RULE 01", "立派すぎる葬儀を回避！", "世間体や同調バイアスを排除！\nシンプルな家族葬で十分", accents[1], False),
            (infographic, (15, 540, 485, 680), "RULE 02", "大手新築戸建はNG！", "住んだ瞬間に価値2割下落！\nブランド料と35年ローンを回避", accents[2], False),
            (infographic, (15, 690, 485, 830), "RULE 03", "高額情報教材に手を出すな", "将来の不安につけ込む商材NG！\n千円の良書と本業の実務で磨け", accents[3], False),
            (infographic, (505, 540, 975, 680), "RULE 05", "高額な民間保険を即解約！", "日本には高額療養費制度がある！\n無駄な特約を削り資金確保", accents[4], False),
            (infographic, (505, 690, 975, 830), "RULE 06", "愚か者の税金・宝くじ", "還元率46%の超搾取ギャンブル！\n期待値マイナスには1円も払わない", accents[5], False),
            (infographic, None, "SUMMARY", "買わない決断こそ最強の投資！", "富裕層との差は意思決定の質！\n新NISAで資本を働かせ自由を掴め", accents[6], True),
        ]

    slides_dir = work / "slides"
    work.mkdir(parents=True, exist_ok=True)
    slides_dir.mkdir(parents=True, exist_ok=True)

    for index, (src, crop_box, kicker, title, caption, accent, is_info) in enumerate(slide_specs, 1):
        source_image = Image.open(src).convert("RGBA")
        make_slide(slides_dir, index, source_image, kicker, title, caption, accent, footer_text, crop_box, is_info, is_studio)

    output, duration = build_video(work, slides_dir, audio, output_name)
    print(f"Generated: {output}")
    print(f"Duration: {duration:.2f}s")


if __name__ == "__main__":
    main()
