from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "outputs" / "scientific_job_short"
SLIDES = WORK / "slides"
SLIDES.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
NAVY = "#0B1734"
BLUE = "#1677FF"
CYAN = "#17B7D6"
GOLD = "#FFB000"
CORAL = "#FF5A5F"
GREEN = "#31B66B"
INK = "#10203A"
MUTED = "#5B6B84"
WHITE = "#FFFFFF"
PAPER = "#F6F8FC"
FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"


def font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def gradient(top, bottom):
    image = Image.new("RGB", (W, H), top)
    draw = ImageDraw.Draw(image)
    a = ImageColor.getrgb(top)
    b = ImageColor.getrgb(bottom)
    for y in range(H):
        t = y / (H - 1)
        color = tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))
        draw.line((0, y, W, y), fill=color)
    return image


class ImageColor:
    @staticmethod
    def getrgb(value):
        value = value.lstrip("#")
        return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))


def fit_cover(image, size=(W, H)):
    ratio = max(size[0] / image.width, size[1] / image.height)
    resized = image.resize((int(image.width * ratio), int(image.height * ratio)), Image.Resampling.LANCZOS)
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def rounded(draw, box, radius=30, fill=WHITE, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def center_text(draw, xy, text, fnt, fill=INK, anchor="mm", stroke_width=0, stroke_fill=None):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor, align="center", stroke_width=stroke_width, stroke_fill=stroke_fill)


def wrap(draw, text, fnt, max_width):
    lines, current = [], ""
    for ch in text:
        test = current + ch
        if draw.textbbox((0, 0), test, font=fnt)[2] <= max_width or not current:
            current = test
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return "\n".join(lines)


def add_badge(draw, text, y, fill=BLUE):
    fnt = font(35)
    box = draw.textbbox((0, 0), text, font=fnt)
    width = box[2] - box[0] + 58
    rounded(draw, ((W-width)//2, y, (W+width)//2, y+70), 35, fill)
    center_text(draw, (W//2, y+36), text, fnt, WHITE)


def save(image, index):
    image.convert("RGB").save(SLIDES / f"slide-{index:02}.png", quality=95)


def cover_slide():
    hero = fit_cover(Image.open(WORK / "hero.png").convert("RGB"))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(720):
        alpha = int(210 * (1 - y / 720))
        od.line((0, y, W, y), fill=(7, 19, 45, alpha))
    for y in range(1450, H):
        alpha = int(165 * ((y - 1450) / (H - 1450)))
        od.line((0, y, W, y), fill=(7, 19, 45, alpha))
    image = Image.alpha_composite(hero.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(image)
    add_badge(draw, "60秒でわかる本", 90, GOLD)
    center_text(draw, (W//2, 275), "その仕事、\n本当にあなたの適職？", font(78), WHITE, stroke_width=3, stroke_fill=NAVY)
    center_text(draw, (W//2, 520), "鈴木祐『新版 科学的な適職』", font(38), "#E7F2FF", stroke_width=2, stroke_fill=NAVY)
    center_text(draw, (W//2, 1810), "職業名より、幸せに働ける条件を見る", font(39), WHITE, stroke_width=2, stroke_fill=NAVY)
    save(image, 1)


def myths_slide():
    image = gradient("#EFF6FF", "#FFFFFF")
    draw = ImageDraw.Draw(image)
    add_badge(draw, "仕事選びの落とし穴", 90, CORAL)
    center_text(draw, (W//2, 245), "この4つだけで\n決めていませんか？", font(72), NAVY)
    labels = [("高収入", "お金だけでは\n満足は続かない", BLUE), ("楽", "負荷ゼロは\n退屈につながる", CYAN), ("将来性", "10年後は\n誰にも読めない", GOLD), ("好き", "情熱は後から\n育つこともある", CORAL)]
    coords = [(70, 520), (555, 520), (70, 1010), (555, 1010)]
    for (title, desc, color), (x, y) in zip(labels, coords):
        rounded(draw, (x, y, x+455, y+410), 38, WHITE, "#DCE5F1", 3)
        center_text(draw, (x+227, y+90), "×", font(70), color)
        center_text(draw, (x+227, y+185), title, font(58), NAVY)
        center_text(draw, (x+227, y+310), desc, font(35), MUTED)
    rounded(draw, (70, 1510, 1010, 1775), 38, NAVY)
    center_text(draw, (W//2, 1642), "大切なのは\n“何になるか”より“どう働くか”", font(44), WHITE)
    save(image, 2)


def conditions_slide():
    image = gradient("#081A3B", "#123B6B")
    draw = ImageDraw.Draw(image)
    add_badge(draw, "幸せに働く3条件", 90, BLUE)
    center_text(draw, (W//2, 250), "適職を見つける\n3つのメーター", font(68), WHITE)
    cards = [
        ("01", "自由度", "時間・場所・進め方を\n自分で選べる", BLUE, "◉"),
        ("02", "明確さ", "評価・役割・ゴールが\nはっきりしている", GOLD, "✓"),
        ("03", "多様性", "複数の能力を使い\n仕事全体に関われる", GREEN, "◆"),
    ]
    for i, (num, title, desc, color, icon) in enumerate(cards):
        y = 520 + i*390
        rounded(draw, (65, y, 1015, y+320), 42, WHITE)
        rounded(draw, (100, y+45, 280, y+275), 38, color)
        center_text(draw, (190, y+125), icon, font(72), WHITE)
        center_text(draw, (190, y+225), num, font(32), WHITE)
        draw.text((330, y+65), title, font=font(66), fill=NAVY)
        draw.text((330, y+165), desc, font=font(36, False), fill=MUTED, spacing=12)
    center_text(draw, (W//2, 1765), "同じ職種でも、働く条件で幸福度は変わる", font(35), "#DCEBFF")
    save(image, 3)


def infographic_slide():
    image = gradient("#EAF3FF", "#FFFFFF")
    draw = ImageDraw.Draw(image)
    add_badge(draw, "保存版インフォグラフィック", 70, NAVY)
    center_text(draw, (W//2, 210), "3条件を一枚で確認", font(57), NAVY)
    source = Image.open(ROOT / "outputs" / "科学的な適職_個人アカウント用.png").convert("RGB")
    source.thumbnail((940, 940), Image.Resampling.LANCZOS)
    shadow = Image.new("RGBA", (source.width+40, source.height+40), (0,0,0,0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((20,20,source.width+20,source.height+20), 28, fill=(15,23,42,65))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    y = 340
    image.paste(shadow, ((W-shadow.width)//2, y-5), shadow)
    image.paste(source, ((W-source.width)//2, y))
    rounded(draw, (70, 1370, 1010, 1765), 42, NAVY)
    center_text(draw, (W//2, 1450), "見るべき7項目", font(43), "#8BC7FF")
    center_text(draw, (W//2, 1570), "収入・通勤・自由度・明確さ\n多様性・健康・人間関係", font(45), WHITE)
    center_text(draw, (W//2, 1708), "それぞれ10点満点で採点する", font(36), "#FFE19A")
    save(image, 4)


def action_slide():
    image = gradient("#FFF8E7", "#FFFFFF")
    draw = ImageDraw.Draw(image)
    add_badge(draw, "今日からできること", 90, GOLD)
    center_text(draw, (W//2, 260), "いちばん低い1項目を\n小さく改善する", font(70), NAVY)
    items = [
        ("自由度が低い", "作業の順番を自分で決める", BLUE),
        ("明確さが低い", "完了条件を上司に確認する", GOLD),
        ("多様性が低い", "小さな改善案を一つ試す", GREEN),
    ]
    for i, (problem, action, color) in enumerate(items):
        y = 590 + i*330
        rounded(draw, (70, y, 1010, y+265), 38, WHITE, "#E7D9B8", 3)
        rounded(draw, (105, y+55, 390, y+135), 38, color)
        center_text(draw, (247, y+96), problem, font(32), WHITE)
        draw.text((115, y+165), "→", font=font(46), fill=color)
        draw.text((205, y+165), action, font=font(39), fill=INK)
    rounded(draw, (70, 1620, 1010, 1790), 38, "#FFF0BF")
    center_text(draw, (W//2, 1705), "職場全体を変えなくても\n自分の半径数メートルは動かせる", font(38), NAVY)
    save(image, 5)


def final_slide():
    image = gradient("#0B1734", "#1C4F88")
    draw = ImageDraw.Draw(image)
    for r, color, alpha in [(420, BLUE, 55), (280, CYAN, 65), (150, GOLD, 80)]:
        layer = Image.new("RGBA", (W, H), (0,0,0,0))
        ld = ImageDraw.Draw(layer)
        rgb = ImageColor.getrgb(color)
        ld.ellipse((W//2-r, 440-r, W//2+r, 440+r), fill=(*rgb, alpha))
        image = Image.alpha_composite(image.convert("RGBA"), layer)
    draw = ImageDraw.Draw(image)
    add_badge(draw, "『新版 科学的な適職』", 115, BLUE)
    center_text(draw, (W//2, 510), "適職は\n完璧な職業名ではない", font(78), WHITE)
    rounded(draw, (90, 860, 990, 1230), 46, WHITE)
    center_text(draw, (W//2, 990), "自分が幸せに働ける条件を知り", font(40), MUTED)
    center_text(draw, (W//2, 1105), "その条件へ近づけていくこと", font(49), NAVY)
    center_text(draw, (W//2, 1430), "あなたの仕事には\n自由度・明確さ・多様性が\nどれくらいありますか？", font(54), "#EAF4FF")
    rounded(draw, (210, 1740, 870, 1830), 45, GOLD)
    center_text(draw, (W//2, 1786), "保存して、あとで採点", font(37), NAVY)
    save(image, 6)


if __name__ == "__main__":
    cover_slide()
    myths_slide()
    conditions_slide()
    infographic_slide()
    action_slide()
    final_slide()
    print(SLIDES)
