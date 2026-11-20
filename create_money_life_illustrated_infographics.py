from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
PERSONAL_BASE = OUT / "money_life_infographic_personal_illustrated_base.png"
STUDIO_BASE = OUT / "money_life_infographic_studio_illustrated_base.png"

FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"

NAVY = "#13253F"
INK = "#172334"
MUTED = "#445568"
CORAL = "#D25F4C"
TEAL = "#207B80"
BLUE = "#3E7191"
GOLD = "#C78919"
SAGE = "#5F7C55"
PLUM = "#8B5C86"
PINK = "#E24C8B"


def font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def text(draw, xy, value, size, fill=INK, bold=True, anchor="la", align="left", spacing=4, stroke=0, stroke_fill="white"):
    draw.multiline_text(
        xy, value, font=font(size, bold), fill=fill, anchor=anchor, align=align,
        spacing=spacing, stroke_width=stroke, stroke_fill=stroke_fill,
    )


def heading(draw, x, y, number, title, color, max_width=390):
    draw.ellipse((x, y - 17, x + 43, y + 26), fill=color, outline="white", width=2)
    text(draw, (x + 21, y + 5), number, 16, "white", True, "mm")
    text(draw, (x + 56, y + 4), title, 24, color, True, "lm")
    draw.line((x + 56, y + 28, x + max_width, y + 28), fill=color, width=4)


def action_line(draw, box, value, color, size=15):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, (y2 - y1) // 2, fill=color)
    text(draw, ((x1 + x2) // 2, (y1 + y2) // 2 + 1), value, size, "white", True, "mm", "center")


def make_personal():
    image = Image.open(PERSONAL_BASE).convert("RGBA")
    draw = ImageDraw.Draw(image)

    text(draw, (627, 56), "お金のある人生は「習慣」でつくる！", 43, "white", True, "ma", "center", 2, 2, NAVY)

    # 01: top-left coral bubble
    heading(draw, 55, 237, "01", "言葉を変える", CORAL, 365)
    text(draw, (238, 309), "×「お金がないから無理」\n○「どうすれば用意できる？」", 20, INK, True, "ma", "center", 7)
    text(draw, (238, 371), "問いを変えると、方法が見える", 15, MUTED, False, "ma", "center", 4, 1, "white")
    action_line(draw, (74, 419, 402, 451), "実践｜必要額・期限・方法を書く", CORAL, 14)

    # 02: top-right green bubble
    heading(draw, 807, 235, "02", "3口座で守る", TEAL, 390)
    text(draw, (1010, 292), "①入れる　②使う　③貯める", 20, INK, True, "ma", "center")
    text(draw, (1010, 330), "残高の錯覚を防ぎ、仕組みで守る", 14, MUTED, False, "ma", "center", 4, 1, "white")
    action_line(draw, (830, 416, 1190, 448), "実践｜給料日に先取りで移す", TEAL, 14)

    # 03: middle-left blue bubble
    heading(draw, 51, 505, "03", "問題は次の一手へ", BLUE, 330)
    text(draw, (191, 574), "原因を確認したら\n「次に何ができる？」へ", 20, INK, True, "ma", "center", 5)
    text(draw, (191, 632), "責め続けず、解決へ動く", 15, MUTED, False, "ma", "center", 4, 1, "white")
    action_line(draw, (55, 686, 335, 718), "実践｜今日の一手を1つ", BLUE, 14)

    # 04: middle-right purple bubble
    heading(draw, 841, 506, "04", "余白は先に予約", PLUM, 365)
    text(draw, (1022, 576), "週1回・30分を先に確保", 20, INK, True, "ma", "center")
    text(draw, (995, 628), "タスクはカレンダーへ\n重要事項は1〜2個に絞る", 14, MUTED, False, "ma", "center", 3, 1, "white")
    action_line(draw, (855, 686, 1193, 718), "実践｜何もしない時間を予定に", PLUM, 14)

    # 05: bottom-left gold bubble
    heading(draw, 47, 765, "05", "支払い＝価値と交換", GOLD, 360)
    text(draw, (227, 836), "学び・経験・人・時間短縮へ", 19, INK, True, "ma", "center")
    text(draw, (227, 883), "浪費か、未来を育てる支出かを考える", 14, MUTED, False, "ma", "center", 4, 1, "white")
    action_line(draw, (61, 963, 390, 995), "実践｜使った後の価値を記録", GOLD, 14)

    # 06: bottom-right teal bubble
    heading(draw, 828, 767, "06", "得意と継続", TEAL, 372)
    text(draw, (1021, 838), "得意は周りの人に聞く", 20, INK, True, "ma", "center")
    text(draw, (1010, 884), "3〜10人の共通語が強み\n楽しさ＋見える化で続ける", 14, MUTED, False, "ma", "center", 3, 1, "white")
    action_line(draw, (846, 963, 1191, 995), "実践｜明日の一つを見える化", TEAL, 14)

    # Central illustrated checklist, using the notebook already present in the art.
    text(draw, (610, 781), "今日の実践チェック", 22, NAVY, True, "ma", "center")
    checklist = [
        "口座の役割を決めた",
        "予定に30分の余白",
        "支出の価値を記録",
        "3人に得意を聞く",
        "明日の一つが見える",
    ]
    for y, line in zip((827, 874, 921, 968, 1015), checklist):
        text(draw, (535, y), line, 14, INK, True, "lm")

    text(draw, (627, 1139), "本の結論", 20, "#FFF0A7", True, "ma", "center")
    text(draw, (627, 1181), "お金がある＝残高の多さではなく\n必要な時に使えて、やりたいことを選べる状態", 22, "white", True, "ma", "center", 4, 2, NAVY)

    image.convert("RGB").save(OUT / "お金のある人生_個人アカウント用.png", quality=96)


def make_studio():
    image = Image.open(STUDIO_BASE).convert("RGBA")
    draw = ImageDraw.Draw(image)

    text(draw, (627, 61), "残高だけで決まらない！", 23, CORAL, True, "ma", "center")
    text(draw, (627, 103), "お金のある人生をつくる 6つの習慣", 39, NAVY, True, "ma", "center")

    # Upper speech bubbles
    heading(draw, 55, 183, "01", "言葉", CORAL, 300)
    text(draw, (201, 235), "「ない」で止めず\nどう用意する？", 18, INK, True, "ma", "center", 4)
    text(draw, (201, 283), "必要額・期限・方法を書く", 14, MUTED, True, "ma", "center")

    heading(draw, 904, 183, "02", "問題解決", BLUE, 300)
    text(draw, (1056, 235), "原因より\n次の一手を見る", 18, INK, True, "ma", "center", 4)
    text(draw, (1056, 283), "今日できる一つを決める", 14, MUTED, True, "ma", "center")

    # Side notes and bubbles
    heading(draw, 34, 389, "03", "3口座", TEAL, 270)
    text(draw, (170, 438), "入れる・使う・貯める", 18, INK, True, "ma", "center")
    text(draw, (170, 476), "残高の錯覚を防ぎ\n給料日に先取りで守る", 14, MUTED, False, "ma", "center", 3)

    heading(draw, 890, 376, "04", "価値", GOLD, 275)
    text(draw, (1008, 429), "支払い＝価値との交換", 16, INK, True, "ma", "center")
    text(draw, (1008, 466), "学び・経験・人へ\n未来を育てる支出を選ぶ", 13, MUTED, False, "ma", "center", 3)

    heading(draw, 36, 568, "05", "余白", SAGE, 280)
    text(draw, (174, 618), "30分を先に予約", 18, INK, True, "ma", "center")
    text(draw, (174, 654), "タスクは見える化\n1日1〜2個へ絞る", 14, MUTED, False, "ma", "center", 3)

    heading(draw, 900, 579, "06", "得意・継続", PLUM, 290)
    text(draw, (1025, 631), "3〜10人に聞く", 18, INK, True, "ma", "center")
    text(draw, (1025, 667), "共通語が強み\n楽しさ＋進捗で続ける", 14, MUTED, False, "ma", "center", 3)

    # Existing clipboard becomes a diagnostic panel.
    text(draw, (172, 797), "お金のある人生度 診断", 20, NAVY, True, "ma", "center")
    diagnosis = [
        "方法を探す問いができる",
        "使う額と貯める額が別",
        "支出の価値を説明できる",
        "来週に余白が入っている",
        "明日の一つが見えている",
    ]
    for y, line in zip((852, 901, 950, 999, 1048), diagnosis):
        text(draw, (90, y), line, 13, INK, True, "lm")

    # Seven illustrated step boxes already present at the bottom.
    steps = ["口座", "固定費", "価値", "余白", "得意", "一つ", "振返り"]
    xs = [132, 246, 360, 475, 590, 705, 820]
    colors = [CORAL, CORAL, GOLD, SAGE, TEAL, BLUE, PLUM]
    for index, (x, label, color) in enumerate(zip(xs, steps, colors), 1):
        text(draw, (x, 1092), f"{index}", 15, color, True, "ma", "center")
        text(draw, (x, 1125), label, 13, INK, True, "ma", "center")

    text(draw, (1045, 968), "本の結論", 20, PINK, True, "ma", "center")
    text(draw, (1045, 1030), "必要な時に使え\nやりたいことを選べる\n人生へ！", 22, NAVY, True, "ma", "center", 5)
    text(draw, (1045, 1113), "少しずつ整えればいい", 14, TEAL, True, "ma", "center")

    image.convert("RGB").save(OUT / "お金のある人生_ダンススタジオ用.png", quality=96)


if __name__ == "__main__":
    make_personal()
    make_studio()
    print(OUT / "お金のある人生_個人アカウント用.png")
    print(OUT / "お金のある人生_ダンススタジオ用.png")
