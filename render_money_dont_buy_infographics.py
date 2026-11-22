from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(r"C:\Users\kurro\.gemini\antigravity\scratch\haru-post-tool-ai-handoff-20261121")
BRAIN = Path(r"C:\Users\kurro\.gemini\antigravity\brain\37b73ff8-3d00-4627-bc53-b533c97e2644")
OUT = ROOT / "outputs"
DOC_CUTOUTS = Path(r"C:\Users\kurro\Documents\old-house-rental-knowledge\05_manga_archive\sodateru-chintai-proposal\outputs\official_character_cutouts")

SIZE = 1200
FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"
FONT_M = r"C:\Windows\Fonts\BIZ-UDMinchoM.ttc"


def font(size, bold=True, mincho=False):
    if mincho:
        return ImageFont.truetype(FONT_M, size)
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def draw_text_with_stroke(draw, xy, text, size, fill, stroke_fill="white", stroke_width=4, mincho=False, anchor="mm", align="center"):
    f = font(size, bold=True, mincho=mincho)
    draw.text(xy, text, font=f, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill, anchor=anchor, align=align)


def cover_image(im, size):
    ratio = max(size[0] / im.width, size[1] / im.height)
    im = im.resize((round(im.width * ratio), round(im.height * ratio)), Image.Resampling.LANCZOS)
    x = (im.width - size[0]) // 2
    y = (im.height - size[1]) // 2
    return im.crop((x, y, x + size[0], y + size[1]))


cards_data = [
    (
        "01", "立派すぎる葬儀",
        "世間体・感情バイアスを排除！\n過剰な祭壇や生前墓地はNG\n家族葬で十分心は伝わる",
        "【対策】事前相談で適正プラン決定",
        "#C94A4A"
    ),
    (
        "02", "大手新築戸建て",
        "買った瞬間に価値2〜3割下落！\n莫大なCM費やブランド料を回避\n35年ローン地獄を抜け出せ",
        "【対策】価値の落ちない中古や賃貸",
        "#2E7D62"
    ),
    (
        "03", "高額情報教材",
        "将来の不安につけ込む商材NG！\n数十万円の教材を買っても稼げない\n不安の解消はお金で買えない",
        "【対策】千円の良書と本業の実務",
        "#C28527"
    ),
    (
        "04", "孤独を埋める消費",
        "承認欲求をお金で買わない！\nキャバクラ・ホスト・過剰な投げ銭\nお金が切れたら関係も消滅",
        "【対策】家族や仲間との確かな絆",
        "#3B6EA5"
    ),
    (
        "05", "高額な民間保険",
        "高額療養費制度があるから安心！\n月8〜9万円の自己負担上限あり\n不安を煽る不要な特約は即解約",
        "【対策】国民皆保険＋半年分の貯蓄",
        "#7A4D8B"
    ),
    (
        "06", "愚か者の税金・宝くじ",
        "還元率46%の超搾取ギャンブル！\n1等の確率は落雷に遭うより低い\n期待値マイナスに1円も投じない",
        "【対策】新NISAでインデックス投資",
        "#D45438"
    ),
]


def render_personal():
    bg_path = BRAIN / "personal_account_bg_1795387130278.jpg"
    base_bg = Image.open(bg_path).convert("RGBA")
    base_bg = cover_image(base_bg, (SIZE, SIZE))

    veil = Image.new("RGBA", (SIZE, SIZE), (255, 253, 248, 140))
    canvas = Image.alpha_composite(base_bg, veil)
    draw = ImageDraw.Draw(canvas)

    # --- ヘッダータイトル ---
    title_bg = Image.new("RGBA", (840, 160), (255, 255, 255, 230))
    t_draw = ImageDraw.Draw(title_bg)
    t_draw.rounded_rectangle((0, 0, 840, 160), 32, fill=(255, 255, 255, 230), outline="#B38038", width=3)
    canvas.alpha_composite(title_bg, (180, 35))

    draw_text_with_stroke(draw, (600, 72), "金持ちが絶対買わないもの", 52, "#17263A", stroke_fill="white", stroke_width=8, mincho=True)
    draw_text_with_stroke(draw, (600, 140), "６つの黄金ルール", 60, "#C22A2A", stroke_fill="white", stroke_width=8, mincho=True)

    ribbon = Image.new("RGBA", (780, 46), (23, 38, 58, 240))
    r_draw = ImageDraw.Draw(ribbon)
    r_draw.rounded_rectangle((0, 0, 780, 46), 16, outline="#E8C36A", width=2)
    canvas.alpha_composite(ribbon, (210, 208))
    draw_text_with_stroke(draw, (600, 231), "上位1%の投資家の養分にならない！生活防衛＆資産形成術", 24, "#FFF3D6", stroke_fill="#17263A", stroke_width=1)

    # キャラクター配置
    s_path = DOC_CUTOUTS / "sakurajimao_official_cutout.png"
    if not s_path.exists():
        s_path = BRAIN / "char_sakurajimao.png"
    sakurajimao = Image.open(s_path).convert("RGBA")
    s_w, s_h = sakurajimao.size
    s_res = sakurajimao.resize((round(s_w * 265 / s_h), 265), Image.Resampling.LANCZOS)
    canvas.alpha_composite(s_res, (15, 10))

    h_path = DOC_CUTOUTS / "harumichi_official_cutout.png"
    if not h_path.exists():
        h_path = BRAIN / "char_harumichi.png"
    harumichi = Image.open(h_path).convert("RGBA")
    hw, hh = harumichi.size
    h_res = harumichi.resize((round(hw * 270 / hh), 270), Image.Resampling.LANCZOS)
    canvas.alpha_composite(h_res, (960, 10))

    # --- 6枚のカード ---
    card_w, card_h = 360, 280
    start_x, start_y = 40, 275
    spacing_x, spacing_y = 20, 18

    for i, (num, title, desc, tip, accent) in enumerate(cards_data):
        row = i // 3
        col = i % 3
        cx = start_x + col * (card_w + spacing_x)
        cy = start_y + row * (card_h + spacing_y)

        card = Image.new("RGBA", (card_w, card_h), (255, 253, 247, 248))
        cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((0, 0, card_w, card_h), 22, outline="#C7B299", width=2)

        # 番号バッジ
        cd.rounded_rectangle((12, 12, 85, 48), 14, fill=accent)
        cd.text((48, 30), num, font=font(24, True), fill="white", anchor="mm")
        # タイトル
        cd.text((98, 30), title, font=font(25, True, mincho=True), fill="#17263A", anchor="lm")
        # 区切り線
        cd.line((14, 60, card_w - 14, 60), fill=accent, width=3)

        # 本文
        cd.multiline_text(
            (card_w // 2, 135),
            desc,
            font=font(21, True),
            fill="#2B303A",
            anchor="mm",
            align="center",
            spacing=8,
        )

        # 対策枠 (下部)
        cd.rounded_rectangle((14, 215, card_w - 14, 265), 14, fill="#F2EBE0")
        cd.text((card_w // 2, 240), tip, font=font(18, True), fill=accent, anchor="mm")

        canvas.alpha_composite(card, (cx, cy))

    # --- 下段セクション ---
    todo_bg = Image.new("RGBA", (440, 290), (255, 252, 245, 248))
    td = ImageDraw.Draw(todo_bg)
    td.rounded_rectangle((0, 0, 440, 290), 24, outline="#B38038", width=3)
    td.rounded_rectangle((20, 14, 180, 56), 16, fill="#C22A2A")
    td.text((100, 35), "今日から実践", font=font(24, True), fill="white", anchor="mm")

    items = [
        "1. 感情で買わされていた支出を1つ解約",
        "2. 激落ちくん等の生活一軍アイテム導入",
        "3. 浮いた資金を新NISAで自動積立＆放置",
    ]
    for idx, it in enumerate(items):
        td.text((25, 100 + idx * 58), it, font=font(20, True), fill="#17263A", anchor="lm")

    canvas.alpha_composite(todo_bg, (40, 875))

    conc_bg = Image.new("RGBA", (660, 290), (23, 38, 58, 248))
    cd = ImageDraw.Draw(conc_bg)
    cd.rounded_rectangle((0, 0, 660, 290), 24, outline="#E8C36A", width=3)
    cd.rounded_rectangle((20, 14, 160, 56), 16, fill="#C22A2A")
    cd.text((90, 35), "結　論", font=font(26, True), fill="white", anchor="mm")

    conclusion_text = (
        "富裕層との決定的な差は\n"
        "「収入」ではなく『意思決定の質』！\n\n"
        "感情や世間体で買わされるのを断ち切り、\n"
        "新NISAで資本を働かせる側に回れ！"
    )
    cd.multiline_text((330, 172), conclusion_text, font=font(26, True), fill="#FFF4D9", anchor="mm", align="center", spacing=10)

    canvas.alpha_composite(conc_bg, (500, 875))

    out_file = OUT / "金持ちが絶対買わないもの_個人アカウント用.png"
    canvas.convert("RGB").save(out_file, quality=95)
    print("Saved:", out_file)


def render_studio():
    bg_path = BRAIN / "dance_studio_bg_1795387137944.jpg"
    base_bg = Image.open(bg_path).convert("RGBA")
    base_bg = cover_image(base_bg, (SIZE, SIZE))

    veil = Image.new("RGBA", (SIZE, SIZE), (255, 254, 250, 140))
    canvas = Image.alpha_composite(base_bg, veil)
    draw = ImageDraw.Draw(canvas)

    # --- ヘッダータイトル ---
    title_bg = Image.new("RGBA", (820, 160), (255, 255, 255, 235))
    t_draw = ImageDraw.Draw(title_bg)
    t_draw.rounded_rectangle((0, 0, 820, 160), 32, fill=(255, 255, 255, 235), outline="#E07A5F", width=3)
    canvas.alpha_composite(title_bg, (190, 35))

    draw_text_with_stroke(draw, (600, 72), "金持ちが絶対買わないもの", 52, "#1D2D44", stroke_fill="white", stroke_width=8, mincho=True)
    draw_text_with_stroke(draw, (600, 140), "６つの黄金ルール", 60, "#E05A47", stroke_fill="white", stroke_width=8, mincho=True)

    ribbon = Image.new("RGBA", (760, 46), (224, 90, 71, 240))
    r_draw = ImageDraw.Draw(ribbon)
    r_draw.rounded_rectangle((0, 0, 760, 46), 16, outline="#FFF", width=2)
    canvas.alpha_composite(ribbon, (220, 208))
    draw_text_with_stroke(draw, (600, 231), "上位1%の投資家の養分にならない！生活防衛＆資産形成術", 24, "white", stroke_fill="#E05A47", stroke_width=2)

    # キャラクター配置
    haruka = Image.open(BRAIN / "char_haruka.png").convert("RGBA")
    hw, hh = haruka.size
    h_res = haruka.resize((round(hw * 280 / hh), 280), Image.Resampling.LANCZOS)
    canvas.alpha_composite(h_res, (15, 10))

    robot = Image.open(BRAIN / "char_robot.png").convert("RGBA")
    rw, rh = robot.size
    r_res = robot.resize((round(rw * 145 / rh), 145), Image.Resampling.LANCZOS)
    canvas.alpha_composite(r_res, (1030, 20))

    cat = Image.open(BRAIN / "char_cat.png").convert("RGBA")
    cw, ch = cat.size
    c_res = cat.resize((round(cw * 135 / ch), 135), Image.Resampling.LANCZOS)
    canvas.alpha_composite(c_res, (1045, 150))

    # --- 6枚のカード ---
    card_w, card_h = 360, 280
    start_x, start_y = 40, 275
    spacing_x, spacing_y = 20, 18

    for i, (num, title, desc, tip, accent) in enumerate(cards_data):
        row = i // 3
        col = i % 3
        cx = start_x + col * (card_w + spacing_x)
        cy = start_y + row * (card_h + spacing_y)

        card = Image.new("RGBA", (card_w, card_h), (255, 255, 255, 248))
        cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((0, 0, card_w, card_h), 22, outline="#E8D5C4", width=2)

        cd.rounded_rectangle((12, 12, 85, 48), 14, fill=accent)
        cd.text((48, 30), num, font=font(24, True), fill="white", anchor="mm")
        cd.text((98, 30), title, font=font(25, True, mincho=True), fill="#1D2D44", anchor="lm")
        cd.line((14, 60, card_w - 14, 60), fill=accent, width=3)

        cd.multiline_text(
            (card_w // 2, 135),
            desc,
            font=font(21, True),
            fill="#2B303A",
            anchor="mm",
            align="center",
            spacing=8,
        )

        cd.rounded_rectangle((14, 215, card_w - 14, 265), 14, fill="#FBF3EC")
        cd.text((card_w // 2, 240), tip, font=font(18, True), fill=accent, anchor="mm")

        canvas.alpha_composite(card, (cx, cy))

    # --- 下段セクション ---
    todo_bg = Image.new("RGBA", (440, 290), (255, 255, 255, 248))
    td = ImageDraw.Draw(todo_bg)
    td.rounded_rectangle((0, 0, 440, 290), 24, outline="#E07A5F", width=3)
    td.rounded_rectangle((20, 14, 180, 56), 16, fill="#E07A5F")
    td.text((100, 35), "今日から実践", font=font(24, True), fill="white", anchor="mm")

    items = [
        "1. 感情で買わされていた支出を1つ解約",
        "2. 激落ちくん等の生活一軍アイテム導入",
        "3. 浮いた資金を新NISAで自動積立＆放置",
    ]
    for idx, it in enumerate(items):
        td.text((25, 100 + idx * 58), it, font=font(20, True), fill="#1D2D44", anchor="lm")

    canvas.alpha_composite(todo_bg, (40, 875))

    conc_bg = Image.new("RGBA", (660, 290), (45, 133, 128, 248))
    cd = ImageDraw.Draw(conc_bg)
    cd.rounded_rectangle((0, 0, 660, 290), 24, outline="#FFF", width=3)
    cd.rounded_rectangle((20, 14, 160, 56), 16, fill="#E07A5F")
    cd.text((90, 35), "結　論", font=font(26, True), fill="white", anchor="mm")

    conclusion_text = (
        "富裕層との決定的な差は\n"
        "「収入」ではなく『意思決定の質』！\n\n"
        "感情や世間体で買わされるのを断ち切り、\n"
        "新NISAで資本を働かせる側に回れ！"
    )
    cd.multiline_text((330, 172), conclusion_text, font=font(26, True), fill="white", anchor="mm", align="center", spacing=10)

    canvas.alpha_composite(conc_bg, (500, 875))

    out_file = OUT / "金持ちが絶対買わないもの_ダンススタジオ用.png"
    canvas.convert("RGB").save(out_file, quality=95)
    print("Saved:", out_file)


if __name__ == "__main__":
    render_personal()
    render_studio()
