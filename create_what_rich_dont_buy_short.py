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


def make_card_layer(source_full, crop_box, size=940, is_studio=False, tag_title=None, tag_subtitle=None, tag_color=None):
    if crop_box is None:
        return cover(source_full, (size, size))

    cropped = source_full.crop(crop_box)
    cw, ch = cropped.size
    scale = 1.78
    new_w, new_h = round(cw * scale), round(ch * scale)
    card_res = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)

    plate = Image.new("RGBA", (size, size), (255, 252, 246, 255))
    draw_p = ImageDraw.Draw(plate)

    # Top header inside card
    card_header_color = tag_color if tag_color else ((18, 35, 58) if not is_studio else (28, 124, 130))
    draw_p.rounded_rectangle((35, 30, size - 35, 110), 18, fill=card_header_color)
    draw_p.text((size // 2, 70), tag_title or "", font=font(30, True), fill="white", anchor="mm")

    # Shadow around card
    shadow = Image.new("RGBA", (new_w + 30, new_h + 30), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((10, 10, new_w + 20, new_h + 20), 24, fill=(0, 0, 0, 50))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))

    cx = (size - new_w) // 2
    cy = 138
    plate.alpha_composite(shadow, (cx - 5, cy - 5))
    plate.paste(card_res, (cx, cy))

    # Takeaway box below
    draw_p.rounded_rectangle(
        (35, cy + new_h + 25, size - 35, size - 25),
        22,
        fill=(245, 248, 252) if not is_studio else (244, 252, 250),
        outline=(210, 225, 240) if not is_studio else (200, 235, 230),
        width=2,
    )
    if tag_subtitle:
        lines = tag_subtitle.split("\n")
        title_sub = lines[0] if len(lines) > 0 else ""
        body_sub = "\n".join(lines[1:]) if len(lines) > 1 else ""
        draw_p.text((size // 2, cy + new_h + 65), title_sub, font=font(26, True), fill="#C92A2A" if not is_studio else "#E76F51", anchor="mm")
        if body_sub:
            draw_p.text((size // 2, cy + new_h + 125), body_sub, font=font(22, False), fill="#172334", anchor="mm", align="center", spacing=8)

    return plate


def make_slide(slides_dir, index, source_full, kicker, title, caption, accent, footer_text, crop_box=None, is_studio=False, tag_title=None, tag_subtitle=None):
    card_size = 940
    card_layer = make_card_layer(source_full, crop_box, card_size, is_studio=is_studio, tag_title=tag_title, tag_subtitle=tag_subtitle, tag_color=accent)

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

    audio = OUT / "what_rich_dont_buy_narration.wav"

    # Card crops from clean 1254x1254 handcrafted infographic:
    crop_01 = (46, 346, 424, 584)
    crop_02 = (438, 346, 816, 584)
    crop_03 = (830, 346, 1208, 584)
    crop_05 = (438, 591, 816, 829)
    crop_06 = (830, 591, 1208, 829)

    if args.variant == "personal":
        work = OUT / "what_rich_dont_buy_short"
        infographic = OUT / "金持ちが絶対買わないもの_個人アカウント用.png"
        # BRAND NEW MASTER SCENE: Freedom observation deck overlooking Sakurajima & blue ocean
        master_scene = BRAIN / "slide1_freedom_deck_cinematic_1795425593730.jpg"
        output_name = "金持ちが絶対買わないもの_ショート動画.mp4"
        accents = ["#028C69", "#D28D2B", "#028C69", "#C94A4A", "#028C69", "#C94A4A", "#028C69"]
        footer_text = "HARUMICHI  BOOK NOTE"
        is_studio = False

        slide_specs = [
            (master_scene, None, "BOOK NOTE", "金持ちが買わない黄金ルール", "上位1%の養分にならない！\n生活防衛＆資産形成の決定版", accents[0], None, None),
            (infographic, crop_01, "RULE 01", "立派すぎる葬儀を回避！", "世間体や同調バイアスを排除！\nシンプルな家族葬で十分", accents[1], "RULE 01 : 葬儀・墓地の真実", "【世間体や同調圧力を排除する】\n多額の費用をかけること＝供養ではない。\n事前の冷静な家族葬プランで、生活基盤を守るのが賢明な選択。"),
            (infographic, crop_02, "RULE 02", "大手新築戸建はNG！", "住んだ瞬間に価値2割下落！\nブランド料と35年ローンを回避", accents[2], "RULE 02 : マイホームの罠", "【新築ブランド料・広告費を回避】\n住んだ瞬間に資産価値は2割〜3割下落。\n価値が落ちにくい中古物件か、柔軟な賃貸が富裕層の鉄則。"),
            (infographic, crop_03, "RULE 03", "高額情報教材に手を出すな", "将来の不安につけ込む商材NG！\n千円の良書と本業の実務で磨け", accents[3], "RULE 03 : 不安ビジネスの正体", "【不安解消をお金で買おうとしない】\n数十万円の教材を買っても稼げない。\n千円台の良書と本業の実務経験こそ最大の自己投資。"),
            (infographic, crop_05, "RULE 05", "高額な民間保険を即解約！", "日本には高額療養費制度がある！\n無駄な特約を削り資金確保", accents[4], "RULE 05 : 民間保険の見直し", "【日本の公的保険は世界最高水準】\n高額療養費制度で月々の負担上限は明確。\n不要な特約を解約し、浮いたお金を投資へ回す。"),
            (infographic, crop_06, "RULE 06", "愚か者の税金・宝くじ", "還元率46%の超搾取ギャンブル！\n期待値マイナスには1円も払わない", accents[5], "RULE 06 : 最悪の搾取ギャンブル", "【期待値マイナスに1円も払わない】\n宝くじの還元率はわずか46%。胴元が半分搾取。\n新NISAで資本主義の成長に複利で乗るのが賢者の選択。"),
            (infographic, None, "SUMMARY", "買わない決断こそ最強の投資！", "富裕層との差は意思決定の質！\n新NISAで資本を働かせ自由を掴め", accents[6], None, None),
        ]
    else:
        work = OUT / "what_rich_dont_buy_studio_short"
        infographic = OUT / "金持ちが絶対買わないもの_ダンススタジオ用.png"
        # BRAND NEW MASTER SCENE: Dynamic rooftop freedom stage with Haruka, Robot & Cat
        master_scene = BRAIN / "haruka_rooftop_freedom_slide1_1795425575810.jpg"
        output_name = "金持ちが絶対買わないもの_スタジオ版ショート動画.mp4"
        accents = ["#E07A5F", "#2A9D8F", "#E76F51", "#264653", "#2A9D8F", "#E76F51", "#2A9D8F"]
        footer_text = "HARUKA CLOVER STUDIO"
        is_studio = True

        slide_specs = [
            (master_scene, None, "BOOK NOTE", "金持ちが買わない黄金ルール", "身軽さこそ最強のパフォーマンス！\n生活防衛＆資産形成の決定版", accents[0], None, None),
            (infographic, crop_01, "RULE 01", "立派すぎる葬儀を回避！", "世間体や同調バイアスを排除！\nシンプルな家族葬で十分", accents[1], "RULE 01 : セレモニーの見栄を手放す", "【見栄より心の繋がりを大切に】\n周囲の目に合わせた過剰な出費はストップ。\n心から温かく偲ぶ家族葬で十分気持ちは伝わる。"),
            (infographic, crop_02, "RULE 02", "大手新築戸建はNG！", "住んだ瞬間に価値2割下落！\nブランド料と35年ローンを回避", accents[2], "RULE 02 : 身軽で自由な住まい選び", "【重いローンで身動きを止めない】\nライフステージに合わせて自由に動ける\n中古リノベや賃貸で、身軽な暮らしをキープ！"),
            (infographic, crop_03, "RULE 03", "高額情報教材に手を出すな", "将来の不安につけ込む商材NG！\n千円の良書と本業の実務で磨け", accents[3], "RULE 03 : 不安を煽る教材にサヨナラ", "【買うだけ満足を脱出して実践へ】\n高額教材に頼るより、良書1冊とスタジオでの実践！\n現場で汗を流してアウトプットすることが最大の成長。"),
            (infographic, crop_05, "RULE 05", "高額な民間保険を即解約！", "日本には高額療養費制度がある！\n無駄な特約を削り資金確保", accents[4], "RULE 05 : 不安任せの保険を見直す", "【公的保険＋ダンスで健康な身体へ】\n不安で入った高額特約はカット。\n浮いたお金は自分磨きと未来の自己投資へ！"),
            (infographic, crop_06, "RULE 06", "愚か者の税金・宝くじ", "還元率46%の超搾取ギャンブル！\n期待値マイナスには1円も払わない", accents[5], "RULE 06 : 一攫千金の幻想を手放す", "【確実な自己投資と新NISAへ】\n半分搾取されるギャンブルは卒業！\n新NISAとスキルアップで自分の価値を最大化！"),
            (infographic, None, "SUMMARY", "買わない決断こそ最強の投資！", "富裕層との差は意思決定の質！\n新NISAで資本を働かせ自由を掴め", accents[6], None, None),
        ]

    slides_dir = work / "slides"
    work.mkdir(parents=True, exist_ok=True)
    slides_dir.mkdir(parents=True, exist_ok=True)

    for index, (src, crop_box, kicker, title, caption, accent, tag_title, tag_subtitle) in enumerate(slide_specs, 1):
        source_image = Image.open(src).convert("RGBA")
        make_slide(slides_dir, index, source_image, kicker, title, caption, accent, footer_text, crop_box, is_studio, tag_title, tag_subtitle)

    output, duration = build_video(work, slides_dir, audio, output_name)
    print(f"Generated: {output}")
    print(f"Duration: {duration:.2f}s")


if __name__ == "__main__":
    main()
