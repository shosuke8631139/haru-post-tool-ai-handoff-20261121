from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
BG = ROOT / "outputs" / "money_life_short" / "backgrounds"
OUT = ROOT / "outputs"
SIZE = 1254

FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"

NAVY = "#13253F"
INK = "#172334"
MUTED = "#526173"
IVORY = "#FFF9EF"
CREAM = "#F7F0E4"
TEAL = "#2D777A"
CORAL = "#CD6C59"
GOLD = "#CB9632"
SAGE = "#647A5E"
BLUE = "#4E718A"
PLUM = "#8A5D78"


def font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def txt(draw, xy, value, size, fill=INK, bold=True, anchor="la", align="left", spacing=5):
    draw.multiline_text(xy, value, font=font(size, bold), fill=fill, anchor=anchor, align=align, spacing=spacing)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius, fill=fill, outline=outline, width=width)


def cover(im, size):
    ratio = max(size[0] / im.width, size[1] / im.height)
    im = im.resize((round(im.width * ratio), round(im.height * ratio)), Image.Resampling.LANCZOS)
    x = (im.width - size[0]) // 2
    y = (im.height - size[1]) // 2
    return im.crop((x, y, x + size[0], y + size[1]))


def rounded_photo(canvas, source, crop_box, dest_box, radius=34):
    crop = source.crop(crop_box).convert("RGB")
    w, h = dest_box[2] - dest_box[0], dest_box[3] - dest_box[1]
    crop = cover(crop, (w, h))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w, h), radius, fill=255)
    canvas.paste(crop, (dest_box[0], dest_box[1]), mask)
    ImageDraw.Draw(canvas).rounded_rectangle(dest_box, radius, outline=(255, 255, 255, 210), width=4)


def base_canvas(path, veil=226):
    source = Image.open(path).convert("RGB").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    blurred = source.filter(ImageFilter.GaussianBlur(12)).convert("RGBA")
    blurred.alpha_composite(Image.new("RGBA", (SIZE, SIZE), (250, 246, 237, veil)))
    return blurred, source


def habit_card(draw, box, number, title, key, body, action, color):
    x1, y1, x2, y2 = box
    rounded(draw, box, 28, (255, 255, 252, 244), color, 2)
    rounded(draw, (x1 + 16, y1 + 15, x1 + 68, y1 + 51), 18, color)
    txt(draw, (x1 + 42, y1 + 34), number, 18, "white", True, "mm")
    txt(draw, (x1 + 81, y1 + 34), title, 22, color, True, "lm")
    draw.line((x1 + 18, y1 + 62, x2 - 18, y1 + 62), fill=color, width=2)
    txt(draw, ((x1 + x2) // 2, y1 + 100), key, 19, INK, True, "mm", "center", 4)
    txt(draw, (x1 + 23, y1 + 142), body, 15, MUTED, False, "la", "left", 4)
    rounded(draw, (x1 + 18, y2 - 42, x2 - 18, y2 - 13), 15, color)
    txt(draw, ((x1 + x2) // 2, y2 - 27), "実践｜" + action, 14, "white", True, "mm", "center")


def mini_habit(draw, box, number, title, key, reason, action, color):
    x1, y1, x2, y2 = box
    rounded(draw, box, 24, (255, 255, 252, 244), color, 2)
    rounded(draw, (x1 + 14, y1 + 14, x1 + 55, y1 + 45), 15, color)
    txt(draw, (x1 + 34, y1 + 30), number, 15, "white", True, "mm")
    txt(draw, (x1 + 65, y1 + 30), title, 18, color, True, "lm")
    txt(draw, ((x1 + x2) // 2, y1 + 80), key, 16, INK, True, "mm", "center", 4)
    draw.line((x1 + 25, y1 + 121, x2 - 25, y1 + 121), fill=color, width=1)
    txt(draw, ((x1 + x2) // 2, y1 + 158), reason, 14, MUTED, False, "mm", "center", 4)
    rounded(draw, (x1 + 14, y2 - 37, x2 - 14, y2 - 11), 13, color)
    txt(draw, ((x1 + x2) // 2, y2 - 24), action, 13, "white", True, "mm", "center")


def make_personal():
    image, source = base_canvas(BG / "personal-base.png", 220)
    draw = ImageDraw.Draw(image)

    rounded(draw, (28, 24, 1226, 190), 42, NAVY)
    txt(draw, (62, 68), "お金のある人生を叶える", 31, "#F7DFC0", True)
    txt(draw, (62, 117), "6つの習慣", 56, "white", True)
    txt(draw, (430, 127), "収入の前に、受け取り・活かせる自分をつくる", 23, "#D9EBE8", True)
    rounded(draw, (1020, 52, 1190, 157), 28, "#F1C76C")
    txt(draw, (1105, 84), "結論", 20, NAVY, True, "mm")
    txt(draw, (1105, 124), "残高より\n選べる状態", 18, NAVY, True, "mm", "center", 2)

    rounded_photo(image, source, (560, 560, 1254, 1170), (35, 212, 354, 456), 34)
    draw = ImageDraw.Draw(image)
    rounded(draw, (54, 405, 335, 443), 19, (19, 37, 63, 225))
    txt(draw, (194, 424), "自分を責める前に、仕組みを変える", 15, "white", True, "mm")

    rounded(draw, (35, 474, 354, 799), 28, (255, 255, 252, 244), CORAL, 2)
    txt(draw, (60, 506), "こんな状態、ありませんか？", 22, CORAL, True)
    worries = [
        "「お金がない」で思考が止まる",
        "残高を全部使える額だと思う",
        "予定を詰め、考える余白がない",
        "自分の得意が分からない",
    ]
    y = 550
    for line in worries:
        rounded(draw, (59, y - 3, 84, y + 22), 6, (255, 244, 239, 255), CORAL, 2)
        txt(draw, (95, y + 9), line, 16, INK, False, "lm")
        y += 52
    rounded(draw, (57, 742, 332, 779), 18, CORAL)
    txt(draw, (194, 761), "不足 → 方法を探す問いへ", 17, "white", True, "mm")

    rounded(draw, (35, 815, 354, 1111), 28, (255, 255, 252, 244), TEAL, 2)
    txt(draw, (60, 846), "お金の土台チェック", 23, TEAL, True)
    checks = [
        "口座ごとの役割を言える",
        "支出で得た価値を説明できる",
        "来週に30分の余白がある",
        "得意を3人に聞いた",
    ]
    y = 889
    for line in checks:
        draw.rectangle((60, y - 9, 82, y + 13), outline=TEAL, width=2)
        txt(draw, (94, y + 2), line, 15, INK, False, "lm")
        y += 44
    rounded(draw, (58, 1064, 332, 1094), 15, "#E3F0EC")
    txt(draw, (195, 1079), "3つ以上なら、選べる土台が育っている", 13, TEAL, True, "mm")

    cards = [
        ((376, 212, 783, 495), "01", "言葉を変える", "× 無理　→　○ どう用意する？", "問いが変わると、金額・時期・方法の\n選択肢が見えてくる。", "必要額・期限・方法を書く", CORAL),
        ((803, 212, 1219, 495), "02", "問題は次の一手へ", "原因確認 → 次に何ができる？", "責め続けるより、解決策を探す。\n余裕は対応できる力から生まれる。", "今日できる一手を1つ", BLUE),
        ((376, 510, 783, 793), "03", "3口座に分ける", "①入れる　②使う　③貯める", "残高＝使える額、を防ぐ。\n給料日に先取りし、未来分を守る。", "口座の役割を決める", TEAL),
        ((803, 510, 1219, 793), "04", "価値へ循環させる", "支払い＝減る → 価値と交換", "学び・経験・人・時間短縮へ。\n浪費か、未来を育てる支出かを見る。", "使った後の価値を記録", GOLD),
        ((376, 808, 783, 1111), "05", "余白を先に入れる", "余白は、先に確保する予定", "考える・試す・方向を確かめる。\nタスクは頭からカレンダーへ出す。", "週1回、30分を予約", SAGE),
        ((803, 808, 1219, 1111), "06", "得意と継続", "得意は周りの人が知っている", "3〜10人に聞き、共通語を探す。\n楽しさ＋見える化が継続力になる。", "明日の一つを見える化", PLUM),
    ]
    for args in cards:
        habit_card(draw, *args)

    rounded(draw, (28, 1127, 1226, 1231), 32, NAVY)
    txt(draw, (58, 1153), "本の結論", 21, "#F1C76C", True)
    txt(draw, (196, 1153), "お金がある＝残高が多いことではなく、必要な時に使えて、やりたいことを選べる状態", 20, "white", True)
    txt(draw, (58, 1197), "今日の一歩", 18, "#9FDDD6", True)
    txt(draw, (196, 1197), "口座の役割を決める　｜　予定に30分の余白　｜　信頼できる3人に得意を聞く", 18, "white", True)

    image.convert("RGB").save(OUT / "お金のある人生_個人アカウント用.png", quality=96)


def make_studio():
    image, source = base_canvas(BG / "studio-base.png", 224)
    draw = ImageDraw.Draw(image)

    rounded(draw, (28, 24, 1226, 198), 42, (255, 252, 245, 248), NAVY, 2)
    txt(draw, (55, 60), "残高だけを増やしても、自由は増えない", 21, CORAL, True)
    txt(draw, (55, 101), "お金のある人生をつくる習慣MAP", 43, NAVY, True)
    txt(draw, (55, 159), "言葉・仕組み・使い方・時間・強みを整える", 22, TEAL, True)
    rounded_photo(image, source, (530, 650, 1254, 1254), (935, 43, 1199, 181), 30)
    draw = ImageDraw.Draw(image)

    colors = [CORAL, BLUE, TEAL, GOLD, SAGE, PLUM]
    cards = [
        ("01", "言葉", "「ない」で止めず\nどう用意する？", "問いが変わると\n金額・時期・方法が見える", "必要額・期限・方法を書く"),
        ("02", "問題解決", "原因より\n次の一手を見る", "責め続けず\n解決へ動ける自分をつくる", "今日できる一つを決める"),
        ("03", "3口座", "入れる・使う・貯める\n流れを分ける", "残高の錯覚を防ぎ\n意志より仕組みで守る", "給料日に先取り移動"),
        ("04", "価値", "支払いを\n価値との交換で見る", "浪費と、未来を育てる\n支出を分けて考える", "学び・経験・人へ使う"),
        ("05", "余白", "30分を先に予約\nタスクは見える化", "考える・試す時間を守り\n次の選択肢をつくる", "1日1〜2個へ絞る"),
        ("06", "得意・継続", "3〜10人に聞く\n共通語が強み", "楽しさ＋見える化で\n小さな前進を続ける", "楽しさ＋進捗を見える化"),
    ]
    xs = [(34, 300), (315, 581), (596, 862)]
    ys = [(220, 472), (488, 740)]
    i = 0
    for y1, y2 in ys:
        for x1, x2 in xs:
            number, title, key, reason, action = cards[i]
            mini_habit(draw, (x1, y1, x2, y2), number, title, key, reason, action, colors[i])
            i += 1

    rounded(draw, (882, 220, 1220, 740), 30, (255, 255, 252, 246), CORAL, 2)
    txt(draw, (1051, 254), "お金のある人生度 診断", 23, CORAL, True, "mm")
    txt(draw, (1051, 291), "当てはまるものに ✓", 15, MUTED, False, "mm")
    diagnosis = [
        ("言葉", "方法を探す問いができる"),
        ("口座", "使う額と貯める額が別"),
        ("支出", "得た価値を言葉にできる"),
        ("時間", "来週に余白が入っている"),
        ("強み", "周りから聞いたことがある"),
        ("継続", "明日やる一つが見える"),
    ]
    y = 337
    for label, line in diagnosis:
        draw.rectangle((905, y - 12, 930, y + 13), outline=TEAL, width=2)
        rounded(draw, (943, y - 14, 1005, y + 15), 12, "#E6F1EF")
        txt(draw, (974, y + 1), label, 13, TEAL, True, "mm")
        txt(draw, (1018, y + 1), line, 13, INK, False, "lm")
        y += 57
    rounded(draw, (905, 680, 1197, 719), 19, CORAL)
    txt(draw, (1051, 700), "4つ以上：選べる土台が育っている", 14, "white", True, "mm")

    rounded(draw, (28, 760, 1226, 1139), 34, (255, 252, 245, 246), NAVY, 2)
    txt(draw, (56, 798), "7日間で試す｜小さな習慣チャレンジ", 27, NAVY, True)
    txt(draw, (56, 838), "全部を一度に変えず、1日1つだけ。終わったら ✓ をつける。", 17, MUTED, False)
    days = [
        ("DAY 1", "口座に\n役割をつける"),
        ("DAY 2", "固定費を\n1つ確認"),
        ("DAY 3", "支出を価値で\n記録する"),
        ("DAY 4", "30分の余白を\n予約する"),
        ("DAY 5", "得意を3人に\n聞いてみる"),
        ("DAY 6", "明日の一つを\n見える化"),
        ("DAY 7", "一週間を\n振り返る"),
    ]
    gap = 11
    start_x = 48
    card_w = 157
    for idx, (day, task) in enumerate(days):
        x1 = start_x + idx * (card_w + gap)
        x2 = x1 + card_w
        color = colors[idx % len(colors)]
        rounded(draw, (x1, 877, x2, 1107), 23, (255, 255, 255, 248), color, 2)
        rounded(draw, (x1 + 17, 892, x2 - 17, 927), 17, color)
        txt(draw, ((x1 + x2) // 2, 910), day, 14, "white", True, "mm")
        txt(draw, ((x1 + x2) // 2, 981), task, 16, INK, True, "mm", "center", 5)
        draw.rectangle((x1 + 61, 1060, x1 + 86, 1085), outline=color, width=2)

    rounded(draw, (28, 1155, 1226, 1232), 30, NAVY)
    txt(draw, (55, 1181), "本の結論", 19, "#F1C76C", True)
    txt(draw, (188, 1181), "必要な時に使え、やりたいことを選べ、問題が起きても次の一手を考えられる人生へ", 19, "white", True)
    txt(draw, (1177, 1212), "少しずつ整えればいい", 15, "#9FDDD6", True, "ra")

    image.convert("RGB").save(OUT / "お金のある人生_ダンススタジオ用.png", quality=96)


if __name__ == "__main__":
    make_personal()
    make_studio()
    print(OUT / "お金のある人生_個人アカウント用.png")
    print(OUT / "お金のある人生_ダンススタジオ用.png")
