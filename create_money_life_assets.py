from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "outputs" / "money_life_short"
BG = WORK / "backgrounds"
OUT = ROOT / "outputs"

FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"

NAVY = "#13253F"
TEAL = "#2D7276"
CORAL = "#C86D5A"
SAGE = "#65765B"
GOLD = "#C7953B"
IVORY = "#FFF9EF"
INK = "#172334"
MUTED = "#536171"


def font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def rounded_overlay(image, box, radius, fill, outline=None, width=1, shadow=False):
    if shadow:
        layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        x1, y1, x2, y2 = box
        ld.rounded_rectangle((x1 + 8, y1 + 12, x2 + 8, y2 + 12), radius, fill=(18, 37, 63, 35))
        layer = layer.filter(ImageFilter.GaussianBlur(12))
        image.alpha_composite(layer)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(box, radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, size, fill=INK, bold=True, anchor="la", align="left", spacing=8, stroke=0):
    draw.multiline_text(
        xy,
        value,
        font=font(size, bold),
        fill=fill,
        anchor=anchor,
        align=align,
        spacing=spacing,
        stroke_width=stroke,
        stroke_fill="#FFFFFF" if stroke else None,
    )


def badge(draw, x, y, number, title, color):
    draw.rounded_rectangle((x, y, x + 72, y + 42), 21, fill=color)
    text(draw, (x + 36, y + 22), number, 23, "white", True, "mm")
    text(draw, (x + 88, y + 22), title, 31, color, True, "lm")


def make_infographic(base_path, output_path, studio=False):
    image = Image.open(base_path).convert("RGBA")
    if image.size != (1254, 1254):
        image = image.resize((1254, 1254), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(image)

    # Quiet title plate keeps the generated art visible while making Japanese copy exact.
    rounded_overlay(image, (128, 52, 1128, 210), 68, (255, 252, 245, 235), (19, 37, 63, 65), 2, True)
    draw = ImageDraw.Draw(image)
    text(draw, (628, 96), "お金のある人生は「習慣」でつくる", 50, NAVY, True, "mm", "center")
    text(draw, (628, 161), "収入の前に、言葉・仕組み・時間を整える", 27, TEAL, True, "mm", "center")

    # Generated backgrounds already contain four editorial cards.
    cards = [
        (78, 238, 500, 488, "01", "言葉", CORAL,
         "「お金がない」→\n「どう用意する？」",
         "不足を事実で終わらせず\n方法を探す問いへ変える",
         "必要額・期限・方法を書く"),
        (520, 238, 969, 488, "02", "仕組み", TEAL,
         "入れる・使う・貯める\n口座を3つに分ける",
         "残高＝使える額という\n思い込みを防ぐ",
         "給料日に先取りで移す"),
        (78, 510, 500, 756, "03", "循環", GOLD,
         "支払い＝価値との交換",
         "学び・経験・人へ回し\n未来を育てる支出を選ぶ",
         "使った後の価値を記録"),
        (520, 510, 969, 756, "04", "時間", SAGE,
         "余白を先に予定する\nタスクは見える化",
         "考える力と継続する力を\n仕組みで守る",
         "30分の余白＋1日2つ"),
    ]
    if studio:
        cards = [
            (40, 235, 464, 503, "01", "言葉", CORAL,
             "「お金がない」→\n「どう用意する？」",
             "不足を事実で終わらせず\n方法を探す問いへ変える",
             "必要額・期限・方法を書く"),
            (478, 235, 905, 503, "02", "仕組み", TEAL,
             "入れる・使う・貯める\n口座を3つに分ける",
             "残高＝使える額という\n思い込みを防ぐ",
             "給料日に先取りで移す"),
            (40, 525, 464, 792, "03", "循環", GOLD,
             "支払い＝価値との交換",
             "学び・経験・人へ回し\n未来を育てる支出を選ぶ",
             "使った後の価値を記録"),
            (478, 525, 905, 792, "04", "時間", SAGE,
             "余白を先に予定する\nタスクは見える化",
             "考える力と継続する力を\n仕組みで守る",
             "30分の余白＋1日2つ"),
        ]

    for x1, y1, x2, y2, num, title_value, color, main, detail, action in cards:
        # Subtle translucent fill improves text contrast while preserving texture.
        draw.rounded_rectangle((x1 + 12, y1 + 15, x2 - 12, y2 - 14), 34, fill=(255, 255, 252, 180))
        badge(draw, x1 + 30, y1 + 30, num, title_value, color)
        text(draw, ((x1 + x2) // 2, y1 + 116), main, 25 if studio else 24, INK, True, "mm", "center", 6)
        draw.line((x1 + 56, y1 + 162, x2 - 56, y1 + 162), fill=color, width=2)
        detail_y = y1 + (191 if studio else 184)
        text(draw, ((x1 + x2) // 2, detail_y), detail, 18 if studio else 15, MUTED, False, "mm", "center", 4)
        pill_y = y2 - 49
        draw.rounded_rectangle((x1 + 46, pill_y, x2 - 46, pill_y + 30), 15, fill=color)
        text(draw, ((x1 + x2) // 2, pill_y + 16), "実践｜" + action, 16, "white", True, "mm", "center")

    # Practical action strip, intentionally compact and editorial rather than poster-like.
    footer_y = 1042 if not studio else 1058
    rounded_overlay(image, (56, footer_y, 1198, 1225), 36, (19, 37, 63, 238), None, shadow=True)
    draw = ImageDraw.Draw(image)
    text(draw, (90, footer_y + 27), "本の結論", 23, "#F1C66B", True)
    text(draw, (230, footer_y + 27), "残高の多さより、必要な時に使えて、やりたいことを選べる状態", 22, "white", True)
    draw.line((90, footer_y + 66, 1164, footer_y + 66), fill=(255, 255, 255, 90), width=2)
    text(draw, (90, footer_y + 94), "今日から", 23, "#F1C66B", True)
    text(draw, (90, footer_y + 137), "①口座の役割を決める　　②予定に30分の余白　　③3人に「得意」を聞く", 24, "white", True)

    image.convert("RGB").save(output_path, quality=95)


if __name__ == "__main__":
    make_infographic(BG / "personal-base.png", OUT / "お金のある人生_個人アカウント用.png")
    make_infographic(BG / "studio-base.png", OUT / "お金のある人生_ダンススタジオ用.png", studio=True)
    print(OUT / "お金のある人生_個人アカウント用.png")
    print(OUT / "お金のある人生_ダンススタジオ用.png")
