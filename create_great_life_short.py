import argparse
import shutil
import subprocess
import wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg
import sys

ROOT = Path(r"C:\Users\kurro\.gemini\antigravity\scratch\haru-post-tool-ai-handoff-20261121")
sys.path.append(str(ROOT))
import generate_polished_short_cards as gsc

OUT = ROOT / "outputs"
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 1080, 1920
FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"
NAVY = "#17263A"


def font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def cover(image, size):
    ratio = max(size[0] / image.width, size[1] / image.height)
    resized = image.resize((round(image.width * ratio), round(image.height * ratio)), Image.Resampling.LANCZOS)
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def rounded_square(source, size=940):
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


def make_slide(slides_dir, index, source_card, kicker, title, caption, accent, infographic=False, footer_text="HARUMICHI BOOK NOTE", bg_source=None):
    if isinstance(source_card, (str, Path)):
        source_card = Image.open(source_card)

    if bg_source:
        background = cover(Image.open(bg_source).convert("RGB"), (W, H)).filter(ImageFilter.GaussianBlur(34)).convert("RGBA")
    else:
        background = cover(source_card.convert("RGB"), (W, H)).filter(ImageFilter.GaussianBlur(34)).convert("RGBA")

    veil = Image.new("RGBA", (W, H), (18, 35, 54, 150 if not infographic else 180))
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
    title_size = 52 if len(title.replace("\n", "")) <= 18 else 44
    center(draw, (W // 2, 230), title, title_size, "white", True, stroke=4)

    # Central Card
    card_size = 940 if not infographic else 980
    card_y = 340 if not infographic else 320
    shadow = Image.new("RGBA", (card_size + 48, card_size + 48), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((24, 24, card_size + 24, card_size + 24), 54, fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    image.alpha_composite(shadow, ((W - shadow.width) // 2, card_y - 10))
    image.alpha_composite(rounded_square(source_card, card_size), ((W - card_size) // 2, card_y))

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
        audio = OUT / "great_life_narration_personal.wav"
        work = OUT / "great_life_short"
        infographic = OUT / "グレートライフ_個人アカウント用.png"
        output_name = "グレートライフ_ショート動画.mp4"
        accents = ["#028C69", "#D28D2B", "#028C69", "#C94A4A", "#028C69", "#C94A4A", "#028C69"]
        footer_text = "HARUMICHI  BOOK NOTE"

        slides_dir = work / "slides"
        work.mkdir(parents=True, exist_ok=True)
        slides_dir.mkdir(parents=True, exist_ok=True)

        cards_data = [
            (1, "★ RULE 01 ★", "脚本家になれ！", "望む未来を自ら描く！", "受け身の人生は今すぐ卒業しよう", accents[0], (255, 250, 240, 255)),
            (2, "★ RULE 02 ★", "今すぐ第一歩！", "完璧なタイミングを待つな！", "残された時間で今すぐ踏み出そう", accents[1], (245, 250, 255, 255)),
            (3, "★ RULE 03 ★", "言い訳を排除！", "「時間がない」は即ゴミ箱へ！", "前向きな信念へアップデートしよう", accents[2], (255, 245, 245, 255)),
            (4, "★ RULE 04 ★", "何歳でも遅くない！", "「もう遅い」なんて絶対にない！", "今日が残りの人生で一番若い日だ", accents[3], (255, 252, 240, 255)),
            (5, "★ RULE 05 ★", "人間関係は投資！", "愚痴や悪影響の縁を手放す！", "高め合える仲間と笑顔で生きよう", accents[4], (248, 245, 255, 255)),
            (6, "★ RULE 06 ★", "経済的自由の計画！", "収入の10%先取り貯蓄！", "不用品ゼロで身軽な大冒険へ！", accents[5], (245, 255, 250, 255)),
        ]

        cards = [gsc.draw_personal_card(*c) for c in cards_data]

        slide_specs = [
            (cards[0], "BOOK NOTE", "人生最高の旅にする秘伝", "受け身をやめ、自分が主人公へ！\n望む未来の脚本を自ら描こう", accents[0], False),
            (cards[1], "LESSON 01", "完璧な準備を待つな！", "「今はその時期じゃない」は言い訳！\n残された時間で今すぐ第一歩を", accents[1], False),
            (cards[2], "LESSON 02", "敗北の言い訳を排除せよ", "「時間がない・才能がない」を手放す！\n前向きな強い信念へ更新しよう", accents[2], False),
            (cards[3], "LESSON 03", "何歳からでも人生は変わる", "始めるのに遅すぎることはない！\n今日が人生で一番若い日だ", accents[3], False),
            (cards[4], "LESSON 04", "人間関係を投資と見なせ", "愚痴や悪影響の縁をキッパリ手放す！\n高め合える人との時間に集中しよう", accents[4], False),
            (cards[5], "FREEDOM", "経済的自由の計画を立てよ", "収入の10%先取りと不用品ゼロ！\n自由を手にして最高の冒険へ！", accents[5], False),
            (infographic, "SUMMARY", "グレートライフ", "人生の主導権は自分にある！\n今日から最高の冒険へ漕ぎ出そう！", accents[6], True),
        ]
    else:
        audio = OUT / "great_life_narration_studio.wav"
        work = OUT / "great_life_studio_short"
        infographic = OUT / "グレートライフ_ダンススタジオ用.png"
        output_name = "グレートライフ_スタジオ版ショート動画.mp4"
        accents = ["#E05275", "#2A8A7A", "#E05275", "#D28D2B", "#8A4FB5", "#2A8A7A", "#E05275"]
        footer_text = "HARUKA CLOVER STUDIO"

        slides_dir = work / "slides"
        work.mkdir(parents=True, exist_ok=True)
        slides_dir.mkdir(parents=True, exist_ok=True)

        cards_data = [
            (1, "✨ MAGIC 01 ✨", "主人公になろう！", "自分のストーリーの主人公へ！", "未来の脚本は自分で書く！", accents[0], (255, 248, 250, 255)),
            (2, "✨ MAGIC 02 ✨", "すぐ最初の一歩！", "完璧を待たずにジャンプ！", "ワクワクする方へ飛び込もう！", accents[1], (245, 252, 250, 255)),
            (3, "✨ MAGIC 03 ✨", "言い訳をポイッ！", "できない理由をポイッと手放す！", "前向きな信念へアップデート！", accents[2], (255, 248, 248, 255)),
            (4, "✨ MAGIC 04 ✨", "今日が新しい始まり！", "何歳からだってスタートできる！", "今日が一番新しい始まり！", accents[3], (255, 252, 240, 255)),
            (5, "✨ MAGIC 05 ✨", "大好きな人と生きる！", "プラスのエネルギーを大切に！", "大好きな人と笑顔でハイタッチ！", accents[4], (250, 245, 255, 255)),
            (6, "✨ MAGIC 06 ✨", "シンプルなお金の計画！", "収入の10%先取り＆不用品ゼロ！", "身軽な暮らしで自由を手に入れよう！", accents[5], (245, 255, 250, 255)),
        ]

        cards = [gsc.draw_studio_card(*c) for c in cards_data]

        slide_specs = [
            (cards[0], "MAGIC 01", "ストーリーの主人公になろう！", "他人の目を気にせず自分らしく！\n未来の脚本は自分で書く！", accents[0], False),
            (cards[1], "MAGIC 02", "完璧を待たずに今すぐ一歩！", "準備不足を心配しなくて大丈夫！\nワクワクする方へ飛び込もう！", accents[1], False),
            (cards[2], "MAGIC 03", "できない言い訳をポイッ！", "「時間がない」なんてポイッ！\n明るい信念にアップデート！", accents[2], False),
            (cards[3], "MAGIC 04", "何歳でも新しい始まり！", "遅すぎるなんて絶対にない！\n今日が一番新しい始まり！", accents[3], False),
            (cards[4], "MAGIC 05", "大好きな仲間と輝こう！", "ポジティブなエネルギーを大切に！\n高め合える仲間と笑顔の時間！", accents[4], False),
            (cards[5], "MAGIC 06", "身軽で自由なお金の計画！", "収入10%先取りとシンプルライフ！\n自由を手にして最高のステージへ！", accents[5], False),
            (infographic, "SUMMARY", "グレートライフ", "人生の主導権はあなたにある！\n最高のステージへ一緒に踊り出そう！", accents[6], True),
        ]

    for index, spec in enumerate(slide_specs, 1):
        make_slide(slides_dir, index, spec[0], spec[1], spec[2], spec[3], spec[4], spec[5], footer_text=footer_text, bg_source=infographic)

    output, duration = build_video(work, slides_dir, audio, output_name)
    print(f"Generated: {output}")
    print(f"Duration: {duration:.2f}s")


if __name__ == "__main__":
    main()
