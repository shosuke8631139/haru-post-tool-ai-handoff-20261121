from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(r"C:\Users\kurro\.gemini\antigravity\scratch\haru-post-tool-ai-handoff-20261121")
BRAIN = Path(r"C:\Users\kurro\.gemini\antigravity\brain\37b73ff8-3d00-4627-bc53-b533c97e2644")
OUT = ROOT / "outputs"

SIZE = 1254

FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"
FONT_M = r"C:\Windows\Fonts\BIZ-UDMinchoM.ttc"


def get_font(size, bold=True, mincho=False):
    if mincho:
        return ImageFont.truetype(FONT_M, size)
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def draw_stroked_text(draw, xy, text, size, fill, stroke_fill="white", stroke_width=3, bold=True, mincho=False, anchor="mm", align="center", spacing=4):
    f = get_font(size, bold=bold, mincho=mincho)
    draw.multiline_text(xy, text, font=f, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill, anchor=anchor, align=align, spacing=spacing)


def draw_card_with_shadow(canvas, box, radius=20, fill=(255, 253, 246), outline=(220, 205, 180), width=2):
    x1, y1, x2, y2 = box
    w = x2 - x1
    h = y2 - y1
    
    # Soft drop shadow
    shadow = Image.new("RGBA", (w + 24, h + 24), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle((8, 8, w + 16, h + 16), radius + 2, fill=(0, 0, 0, 35))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    canvas.alpha_composite(shadow, (x1 - 4, y1 - 2))

    # Main card
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(card)
    c_draw.rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=fill, outline=outline, width=width)
    canvas.alpha_composite(card, (x1, y1))


def render_personal_clean():
    print("Building CLEAN Personal Masterpiece Infographic from scratch...")
    # 1. BASE BACKGROUND
    # Upper: Sunrise Sakurajima background
    bg_path = BRAIN / "personal_account_bg_1795387130278.jpg"
    if bg_path.exists():
        bg = Image.open(bg_path).convert("RGBA").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    else:
        bg = Image.new("RGBA", (SIZE, SIZE), (250, 246, 238, 255))

    # Create warm organic cream veil for cards area (y: 340 to 1254)
    canvas = bg.copy()
    veil = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(veil)
    
    # Vertical gradient for veil
    for y in range(320, SIZE):
        ratio = min(1.0, (y - 320) / 100.0)
        alpha = int(245 * ratio)
        v_draw.line([(0, y), (SIZE, y)], fill=(252, 249, 242, alpha))
    canvas.alpha_composite(veil)
    draw = ImageDraw.Draw(canvas)

    # 2. TOP TITLE PLATE (x: 230 to 1024, y: 70 to 325)
    plate_box = (230, 70, 1024, 325)
    draw_card_with_shadow(canvas, plate_box, radius=24, fill=(255, 250, 240, 252), outline=(218, 165, 32), width=4)
    draw = ImageDraw.Draw(canvas)
    # Inner gold border
    draw.rounded_rectangle((plate_box[0] + 6, plate_box[1] + 6, plate_box[2] - 6, plate_box[3] - 6), 18, outline=(245, 225, 160), width=2)

    # Top line inside plate
    draw_stroked_text(draw, (627, 114), "上位1%の養分になるな！", 26, "#B91C1C", stroke_fill="white", stroke_width=3, bold=True, mincho=False, anchor="mm")

    # Main Big Title: "金持ちが「絶対買わない」もの"
    draw_stroked_text(draw, (627, 166), "金持ちが「絶対買わない」もの", 46, "#1A2535", stroke_fill="white", stroke_width=5, bold=True, mincho=True, anchor="mm")

    # Subtitle: "6つの黄金ルール"
    draw_stroked_text(draw, (627, 222), "6つの黄金ルール", 38, "#C2410C", stroke_fill="white", stroke_width=4, bold=True, mincho=True, anchor="mm")

    # Bottom dark ribbon: "知っている人だけが得をする！資本主義の生活防衛ルート"
    ribbon_box = (250, 260, 1004, 302)
    draw.rounded_rectangle(ribbon_box, 14, fill=(18, 35, 58), outline=(218, 165, 32), width=2)
    draw_stroked_text(draw, (627, 281), "知っている人だけが得をする！資本主義の生活防衛ルート", 21, "#FFDF73", stroke_fill="#12233A", stroke_width=1, bold=True, anchor="mm")

    # 3. PLACE OFFICIAL CHARACTERS ON LEFT & RIGHT OF PLATE
    # Sakurajimao on Left
    s_path = BRAIN / "sakurajimao_official.png"
    if s_path.exists():
        s_img = Image.open(s_path).convert("RGBA")
        sw, sh = s_img.size
        s_target_h = 295
        s_target_w = round(sw * (s_target_h / float(sh)))
        s_res = s_img.resize((s_target_w, s_target_h), Image.Resampling.LANCZOS)
        canvas.alpha_composite(s_res, (25, 45))

    # Harumichi on Right
    h_path = BRAIN / "harumichi_official.png"
    if h_path.exists():
        h_img = Image.open(h_path).convert("RGBA")
        hw, hh = h_img.size
        h_target_h = 300
        h_target_w = round(hw * (h_target_h / float(hh)))
        h_res = h_img.resize((h_target_w, h_target_h), Image.Resampling.LANCZOS)
        canvas.alpha_composite(h_res, (SIZE - h_target_w - 20, 38))

    # 4. 6 HANDCRAFTED CARDS (3 columns x 2 rows)
    cards_data = [
        (
            (50, 350, 420, 580),
            "01", "立派すぎる葬儀", "#C92A2A",
            "世間体や見栄を排除！",
            "過剰な祭壇・生前墓地はNG\nシンプルな家族葬で十分\n事前相談で適正プラン決定",
            "⚰️"
        ),
        (
            (442, 350, 812, 580),
            "02", "大手新築一戸建て", "#2B8A3E",
            "買った瞬間に2割下落！",
            "莫大なCM費・ブランド料回避\n35年ローン地獄を抜け出す\n価値の落ちない中古や賃貸",
            "🏠"
        ),
        (
            (834, 350, 1204, 580),
            "03", "高額情報教材", "#1971C2",
            "不安につけ込む商材NG！",
            "高額教材を買っても稼げない\n不安の解消はお金で買えない\n千円の良書と本業の実務",
            "💻"
        ),
        (
            (50, 595, 420, 825),
            "04", "孤独を埋める消費", "#862E9C",
            "夜の街・過剰課金をゼロに",
            "他人の承認はお金で買えない\n買った関係は虚無しか残らない\n本当の仲間と豊かな時間",
            "🍻"
        ),
        (
            (442, 595, 812, 825),
            "05", "不要な民間保険", "#D97706",
            "不安任せの特約は即解約！",
            "日本には高額療養費制度がある\n自己負担上限を理解して安心\n浮いた固定費を投資へ回す",
            "🛡️"
        ),
        (
            (834, 595, 1204, 825),
            "06", "搾取宝くじ", "#C2410C",
            "還元率46%の愚か者の税金",
            "胴元が半分抜く超搾取ゲーム\n期待値マイナスに1円も払わない\n新NISAでインデックス投資",
            "📈"
        ),
    ]

    for box, num, title, color, sub_h, body, icon in cards_data:
        draw_card_with_shadow(canvas, box, radius=20, fill=(255, 253, 246), outline=(225, 215, 195), width=2)
        draw = ImageDraw.Draw(canvas)

        bx1, by1, bx2, by2 = box

        # Number Badge
        badge_w, badge_h = 48, 34
        badge_x = bx1 + 16
        badge_y = by1 + 14
        draw.rounded_rectangle((badge_x, badge_y, badge_x + badge_w, badge_y + badge_h), 14, fill=color)
        draw_stroked_text(draw, (badge_x + badge_w // 2, badge_y + badge_h // 2), num, 20, "white", stroke_fill=color, stroke_width=1, bold=True, anchor="mm")

        # Title
        title_x = badge_x + badge_w + 10
        title_y = badge_y + badge_h // 2
        draw_stroked_text(draw, (title_x, title_y), title, 23, "#1A2535", stroke_fill="white", stroke_width=2, bold=True, anchor="lm")

        # Sub Highlight ribbon
        sub_box = (bx1 + 16, by1 + 56, bx2 - 16, by1 + 86)
        bg_sub = (254, 242, 242) if color in ["#C92A2A", "#C2410C"] else ((240, 253, 244) if color == "#2B8A3E" else (245, 247, 252))
        draw.rounded_rectangle(sub_box, 8, fill=bg_sub, outline=(230, 220, 210), width=1)
        draw_stroked_text(draw, ((sub_box[0] + sub_box[2]) // 2, (sub_box[1] + sub_box[3]) // 2), sub_h, 16, color, stroke_fill="white", stroke_width=1, bold=True, anchor="mm")

        # Body Text
        draw_stroked_text(draw, (bx1 + 20, by1 + 98), body, 15, "#2C3E50", stroke_fill="white", stroke_width=1, bold=False, anchor="la", align="left", spacing=6)

    # 5. BOTTOM FOOTER (y: 845 to 1085)
    # Left: "今日からできる防衛" wooden sign
    foot_left = (50, 845, 420, 1075)
    draw_card_with_shadow(canvas, foot_left, radius=20, fill=(255, 248, 235), outline=(139, 69, 19), width=3)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((foot_left[0] + 6, foot_left[1] + 6, foot_left[2] - 6, foot_left[3] - 6), 16, outline=(220, 160, 100), width=1)

    draw_stroked_text(draw, (235, 882), "今日からできる防衛", 22, "#B91C1C", stroke_fill="white", stroke_width=2, bold=True, anchor="mm")
    checks = [
        "☑ 不要な民間保険を即解約",
        "☑ 固定費・不要サブスク削減",
        "☑ 新NISAで自動積立を設定",
    ]
    for i, ck in enumerate(checks):
        draw_stroked_text(draw, (75, 930 + i * 38), ck, 17, "#1A2535", stroke_fill="white", stroke_width=1, bold=True, anchor="lm")

    # Right: "本の結論" scroll plate
    foot_right = (442, 845, 1040, 1075)
    draw_card_with_shadow(canvas, foot_right, radius=22, fill=(255, 252, 244), outline=(184, 115, 51), width=4)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((foot_right[0] + 6, foot_right[1] + 6, foot_right[2] - 6, foot_right[3] - 6), 16, outline=(245, 220, 150), width=2)

    draw_stroked_text(draw, (741, 885), "本の結論", 26, "#C2410C", stroke_fill="white", stroke_width=2, bold=True, anchor="mm")
    conclusion_text = (
        "「買わない決断」とはケチではなく、\n"
        "資本主義の理不尽な搾取から解放され、\n"
        "人生の主導権を取り戻す最大の武器。"
    )
    draw_stroked_text(draw, (741, 965), conclusion_text, 22, "#1A2535", stroke_fill="white", stroke_width=1, bold=True, anchor="mm", align="center", spacing=8)

    # Chibi character beside conclusion
    if s_path.exists():
        chibi_s = Image.open(s_path).convert("RGBA")
        csw, csh = chibi_s.size
        c_h = 190
        c_w = round(csw * (c_h / float(csh)))
        chibi_res = chibi_s.resize((c_w, c_h), Image.Resampling.LANCZOS)
        canvas.alpha_composite(chibi_res, (1060, 875))

    out_file = OUT / "金持ちが絶対買わないもの_個人アカウント用.png"
    canvas.convert("RGB").save(out_file, format="PNG", quality=98)
    print("Personal Clean Masterpiece saved:", out_file)


def render_studio_clean():
    print("Building CLEAN Studio Masterpiece Infographic from scratch...")
    bg_path = BRAIN / "dance_studio_bg_1795387137944.jpg"
    if bg_path.exists():
        bg = Image.open(bg_path).convert("RGBA").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    else:
        bg = Image.new("RGBA", (SIZE, SIZE), (242, 248, 248, 255))

    canvas = bg.copy()
    veil = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(veil)
    for y in range(320, SIZE):
        ratio = min(1.0, (y - 320) / 100.0)
        alpha = int(245 * ratio)
        v_draw.line([(0, y), (SIZE, y)], fill=(248, 252, 252, alpha))
    canvas.alpha_composite(veil)
    draw = ImageDraw.Draw(canvas)

    # 2. TOP TITLE PLATE
    plate_box = (230, 70, 1024, 325)
    draw_card_with_shadow(canvas, plate_box, radius=24, fill=(255, 253, 248, 252), outline=(28, 124, 130), width=4)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((plate_box[0] + 6, plate_box[1] + 6, plate_box[2] - 6, plate_box[3] - 6), 18, outline=(190, 230, 230), width=2)

    # Top line
    draw_stroked_text(draw, (627, 114), "Studio Haru 人生を身軽にする知恵", 25, "#1C7C82", stroke_fill="white", stroke_width=3, bold=True, mincho=False, anchor="mm")

    # Main Big Title
    draw_stroked_text(draw, (627, 166), "お金持ちが「絶対買わない」もの", 44, "#172334", stroke_fill="white", stroke_width=5, bold=True, mincho=True, anchor="mm")

    # Subtitle
    draw_stroked_text(draw, (627, 222), "6つの黄金ルール", 38, "#E76F51", stroke_fill="white", stroke_width=4, bold=True, mincho=True, anchor="mm")

    # Bottom ribbon
    ribbon_box = (250, 260, 1004, 302)
    draw.rounded_rectangle(ribbon_box, 14, fill=(28, 124, 130), outline=(231, 111, 81), width=2)
    draw_stroked_text(draw, (627, 281), "無駄な浪費を手放して、本当に大切なことに全集中！", 21, "white", stroke_fill="#124E52", stroke_width=1, bold=True, anchor="mm")

    # 3. CHARACTERS
    # Haruka on Left
    h_path = BRAIN / "char_haruka.png"
    if h_path.exists():
        h_img = Image.open(h_path).convert("RGBA")
        hw, hh = h_img.size
        h_target_h = 280
        h_target_w = round(hw * (h_target_h / float(hh)))
        h_res = h_img.resize((h_target_w, h_target_h), Image.Resampling.LANCZOS)
        canvas.alpha_composite(h_res, (35, 55))

    # Robot & Cat on Right
    r_path = BRAIN / "char_robot.png"
    c_path = BRAIN / "char_cat.png"
    if r_path.exists():
        r_img = Image.open(r_path).convert("RGBA")
        rw, rh = r_img.size
        r_res = r_img.resize((round(rw * 1.3), round(rh * 1.3)), Image.Resampling.LANCZOS)
        canvas.alpha_composite(r_res, (SIZE - 200, 45))

    if c_path.exists():
        c_img = Image.open(c_path).convert("RGBA")
        cw, ch = c_img.size
        c_res = c_img.resize((round(cw * 1.35), round(ch * 1.35)), Image.Resampling.LANCZOS)
        canvas.alpha_composite(c_res, (SIZE - 150, 180))

    # 4. 6 CARDS
    cards_data_s = [
        (
            (50, 350, 420, 580),
            "01", "立派すぎる葬儀", "#E63946",
            "見栄の過剰出費をストップ！",
            "世間体のプレッシャーを排除\n心温まる家族葬で十分伝わる\n事前の冷静な相談がカギ",
        ),
        (
            (442, 350, 812, 580),
            "02", "重い新築戸建て", "#2A9D8F",
            "高額ローンで身動き止めない！",
            "買った瞬間に資産価値2割下落\n自由に動ける中古リノベや賃貸\n身軽さこそ最大の強み",
        ),
        (
            (834, 350, 1204, 580),
            "03", "不安を煽る高額教材", "#3A86FF",
            "買うだけ満足は即卒業！",
            "高額商材に頼らず良書1冊\nスタジオで汗を流して学ぶ\n実践とアウトプットで成長",
        ),
        (
            (50, 595, 420, 825),
            "04", "寂しさの孤独消費", "#F4A261",
            "見せかけの承認欲求はゼロ！",
            "夜の街や過剰課金は虚しいだけ\nお金で買えない本物の繋がり\n仲間と本気で踊る時間へ",
        ),
        (
            (442, 595, 812, 825),
            "05", "過剰な民間保険", "#2A9D8F",
            "公的保険＋ダンスで健康へ！",
            "高額療養費制度があるから安心\n不要な特約はカットして身軽に\n浮いたお金を自分磨きへ",
        ),
        (
            (834, 595, 1204, 825),
            "06", "搾取宝くじ", "#E76F51",
            "半分抜かれるギャンブル卒業！",
            "期待値マイナスには手を出さない\n新NISAで手堅く資産形成\nダンススキルへの自己投資！",
        ),
    ]

    for box, num, title, color, sub_h, body in cards_data_s:
        draw_card_with_shadow(canvas, box, radius=20, fill=(255, 253, 248), outline=(215, 230, 230), width=2)
        draw = ImageDraw.Draw(canvas)

        bx1, by1, bx2, by2 = box
        badge_w, badge_h = 48, 34
        badge_x = bx1 + 16
        badge_y = by1 + 14
        draw.rounded_rectangle((badge_x, badge_y, badge_x + badge_w, badge_y + badge_h), 14, fill=color)
        draw_stroked_text(draw, (badge_x + badge_w // 2, badge_y + badge_h // 2), num, 20, "white", stroke_fill=color, stroke_width=1, bold=True, anchor="mm")

        title_x = badge_x + badge_w + 10
        title_y = badge_y + badge_h // 2
        draw_stroked_text(draw, (title_x, title_y), title, 23, "#172334", stroke_fill="white", stroke_width=2, bold=True, anchor="lm")

        sub_box = (bx1 + 16, by1 + 56, bx2 - 16, by1 + 86)
        bg_sub = (255, 245, 242) if color in ["#E63946", "#E76F51", "#F4A261"] else (240, 252, 250)
        draw.rounded_rectangle(sub_box, 8, fill=bg_sub, outline=(225, 235, 235), width=1)
        draw_stroked_text(draw, ((sub_box[0] + sub_box[2]) // 2, (sub_box[1] + sub_box[3]) // 2), sub_h, 16, color, stroke_fill="white", stroke_width=1, bold=True, anchor="mm")

        draw_stroked_text(draw, (bx1 + 20, by1 + 98), body, 15, "#2C3E50", stroke_fill="white", stroke_width=1, bold=False, anchor="la", align="left", spacing=6)

    # 5. BOTTOM FOOTER
    foot_left = (50, 845, 420, 1075)
    draw_card_with_shadow(canvas, foot_left, radius=20, fill=(255, 250, 245), outline=(139, 69, 19), width=3)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((foot_left[0] + 6, foot_left[1] + 6, foot_left[2] - 6, foot_left[3] - 6), 16, outline=(220, 160, 100), width=1)

    draw_stroked_text(draw, (235, 882), "今日からできるアクション", 20, "#E76F51", stroke_fill="white", stroke_width=2, bold=True, anchor="mm")
    checks_s = [
        "☑ 不要なサブスクを即解約",
        "☑ 見栄の浪費をストップ",
        "☑ 身軽に大好きなダンスへ！",
    ]
    for i, ck in enumerate(checks_s):
        draw_stroked_text(draw, (75, 930 + i * 38), ck, 17, "#172334", stroke_fill="white", stroke_width=1, bold=True, anchor="lm")

    foot_right = (442, 845, 1040, 1075)
    draw_card_with_shadow(canvas, foot_right, radius=22, fill=(248, 253, 252), outline=(28, 124, 130), width=4)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((foot_right[0] + 6, foot_right[1] + 6, foot_right[2] - 6, foot_right[3] - 6), 16, outline=(190, 230, 230), width=2)

    draw_stroked_text(draw, (741, 885), "スタジオの合言葉", 26, "#1C7C82", stroke_fill="white", stroke_width=2, bold=True, anchor="mm")
    conclusion_studio = (
        "持ち物を軽く、心を自由に。\n"
        "無駄な支出を手放して、\n"
        "大好きなダンスと夢に全集中！"
    )
    draw_stroked_text(draw, (741, 965), conclusion_studio, 22, "#172334", stroke_fill="white", stroke_width=1, bold=True, anchor="mm", align="center", spacing=8)

    # Chibi character beside conclusion
    if h_path.exists():
        chibi_h = Image.open(h_path).convert("RGBA")
        chw, chh = chibi_h.size
        ch_h = 190
        ch_w = round(chw * (ch_h / float(chh)))
        chibi_res = chibi_h.resize((ch_w, ch_h), Image.Resampling.LANCZOS)
        canvas.alpha_composite(chibi_res, (1060, 875))

    out_file = OUT / "金持ちが絶対買わないもの_ダンススタジオ用.png"
    canvas.convert("RGB").save(out_file, format="PNG", quality=98)
    print("Studio Clean Masterpiece saved:", out_file)


if __name__ == "__main__":
    render_personal_clean()
    render_studio_clean()
