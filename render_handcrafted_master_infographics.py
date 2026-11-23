from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(r"C:\Users\kurro\.gemini\antigravity\scratch\haru-post-tool-ai-handoff-20261121")
BRAIN = Path(r"C:\Users\kurro\.gemini\antigravity\brain\37b73ff8-3d00-4627-bc53-b533c97e2644")
OUT = ROOT / "outputs"

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


def blend_box(canvas, box, bg_color):
    # Soft rounded rectangle to seamlessly cover previous text
    x1, y1, x2, y2 = box
    w = x2 - x1
    h = y2 - y1
    patch = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(patch)
    p_draw.rounded_rectangle((0, 0, w, h), 16, fill=bg_color)
    patch = patch.filter(ImageFilter.GaussianBlur(3))
    canvas.alpha_composite(patch, (x1, y1))


def render_personal_handcrafted():
    print("Generating Personal Handcrafted Infographic...")
    base_path = OUT / "1億円貯める方法_個人アカウント用.png"
    im = Image.open(base_path).convert("RGBA")
    draw = ImageDraw.Draw(im)

    # 1. RETOUCH TITLE PLATE (x: 240 to 980, y: 70 to 325)
    # Background of plate is warm cream parchment with gold border
    title_patch = Image.new("RGBA", (740, 220), (0, 0, 0, 0))
    tp_draw = ImageDraw.Draw(title_patch)
    tp_draw.rounded_rectangle((10, 10, 730, 210), 24, fill=(255, 248, 235, 245), outline=(218, 165, 32), width=4)
    tp_draw.rounded_rectangle((16, 16, 724, 204), 18, fill=(255, 252, 245, 235), outline=(245, 220, 150), width=2)
    im.alpha_composite(title_patch, (245, 80))
    draw = ImageDraw.Draw(im)

    # Top line in plate: "上位1%の養分になるな！"
    draw_stroked_text(draw, (615, 118), "上位1%の養分になるな！", 26, "#B91C1C", stroke_fill="white", stroke_width=3, bold=True, mincho=False, anchor="mm")

    # Main Big Title: "金持ちが「絶対買わない」もの"
    draw_stroked_text(draw, (615, 168), "金持ちが「絶対買わない」もの", 46, "#1A2535", stroke_fill="white", stroke_width=5, bold=True, mincho=True, anchor="mm")

    # Subtitle Ribbon: "6つの黄金ルール"
    draw_stroked_text(draw, (615, 224), "6つの黄金ルール", 38, "#C2410C", stroke_fill="white", stroke_width=4, bold=True, mincho=True, anchor="mm")

    # Bottom dark ribbon: "知っている人だけが得をする！資本主義の生活防衛ルート"
    ribbon_box = (250, 260, 980, 298)
    draw.rounded_rectangle(ribbon_box, 14, fill=(18, 35, 58), outline=(218, 165, 32), width=2)
    draw_stroked_text(draw, (615, 279), "知っている人だけが得をする！資本主義の生活防衛ルート", 20, "#FFDF73", stroke_fill="#12233A", stroke_width=1, bold=True, anchor="mm")

    # 2. RETOUCH THE 6 CARDS (3 columns x 2 rows)
    # Card 01: x=60..425, y=355..575
    # Card 02: x=445..810, y=355..575
    # Card 03: x=830..1195, y=355..575
    # Card 04: x=60..425, y=580..800
    # Card 05: x=445..810, y=580..800
    # Card 06: x=830..1195, y=580..800

    cards_p = [
        # (box, num, title, color, sub_highlight, body_text)
        (
            (62, 358, 423, 572),
            "01", "立派すぎる葬儀", "#C92A2A",
            "世間体や見栄を排除！",
            "過剰な祭壇・生前墓地はNG\nシンプルな家族葬で十分\n事前相談で適正プラン決定"
        ),
        (
            (447, 358, 808, 572),
            "02", "大手新築一戸建て", "#2B8A3E",
            "買った瞬間に2割下落！",
            "莫大なCM費・ブランド料を回避\n35年ローン地獄を抜け出す\n価値の落ちない中古や賃貸"
        ),
        (
            (832, 358, 1193, 572),
            "03", "高額情報教材", "#1971C2",
            "不安につけ込む商材NG！",
            "高額教材を買っても稼げない\n不安の解消はお金で買えない\n千円の良書と本業の実務"
        ),
        (
            (62, 582, 423, 796),
            "04", "孤独を埋める消費", "#862E9C",
            "夜の街・過剰課金をゼロに",
            "他人の承認はお金で買えない\n買った関係は虚無しか残らない\n本当の仲間と豊かな時間"
        ),
        (
            (447, 582, 808, 796),
            "05", "不要な民間保険", "#D97706",
            "不安任せの特約は即解約！",
            "日本には高額療養費制度がある\n自己負担上限を理解して安心\n浮いた固定費を投資へ回す"
        ),
        (
            (832, 582, 1193, 796),
            "06", "搾取宝くじ", "#C2410C",
            "還元率46%の愚か者の税金",
            "胴元が半分抜く超搾取ゲーム\n期待値マイナスに1円も払わない\n新NISAでインデックス投資"
        ),
    ]

    for (bx1, by1, bx2, by2), num, title, color, sub_h, body in cards_p:
        # Patch the text region inside the card (preserve lower illustration!)
        # Card width is 361px, text area is y: by1+4 to by1+145
        t_patch = Image.new("RGBA", (bx2 - bx1 - 16, 138), (0, 0, 0, 0))
        tp_d = ImageDraw.Draw(t_patch)
        tp_d.rounded_rectangle((0, 0, bx2 - bx1 - 16, 138), 14, fill=(255, 252, 246, 248), outline=(235, 225, 210), width=1)
        im.alpha_composite(t_patch, (bx1 + 8, by1 + 6))
        draw = ImageDraw.Draw(im)

        # Number Badge (pill shape)
        badge_w = 46
        badge_h = 32
        badge_x = bx1 + 18
        badge_y = by1 + 12
        draw.rounded_rectangle((badge_x, badge_y, badge_x + badge_w, badge_y + badge_h), 14, fill=color)
        draw_stroked_text(draw, (badge_x + badge_w // 2, badge_y + badge_h // 2), num, 19, "white", stroke_fill=color, stroke_width=1, bold=True, anchor="mm")

        # Title
        title_x = badge_x + badge_w + 10
        title_y = badge_y + badge_h // 2
        draw_stroked_text(draw, (title_x, title_y), title, 22, "#1A2535", stroke_fill="white", stroke_width=2, bold=True, anchor="lm")

        # Sub Highlight (colored pill or ribbon)
        sub_box = (bx1 + 18, by1 + 48, bx2 - 18, by1 + 76)
        draw.rounded_rectangle(sub_box, 8, fill=(254, 242, 242) if color == "#C92A2A" else ((240, 253, 244) if color == "#2B8A3E" else (245, 247, 252)))
        draw_stroked_text(draw, ((sub_box[0] + sub_box[2]) // 2, (sub_box[1] + sub_box[3]) // 2), sub_h, 16, color, stroke_fill="white", stroke_width=1, bold=True, anchor="mm")

        # Body Text
        draw_stroked_text(draw, (bx1 + 22, by1 + 86), body, 15, "#2C3E50", stroke_fill="white", stroke_width=1, bold=False, anchor="la", align="left", spacing=4)

    # 3. RETOUCH BOTTOM FOOTER (y: 810 to 1050)
    # Left "今日から" wooden sign: x=65..430, y=815..1035
    # Right "結論" scroll: x=445..980, y=815..1035

    # Today Checklist patch
    c_patch = Image.new("RGBA", (340, 165), (0, 0, 0, 0))
    cp_d = ImageDraw.Draw(c_patch)
    cp_d.rounded_rectangle((0, 0, 340, 165), 16, fill=(255, 248, 235, 250), outline=(139, 69, 19), width=2)
    im.alpha_composite(c_patch, (75, 850))
    draw = ImageDraw.Draw(im)

    draw_stroked_text(draw, (245, 875), "今日からできる防衛", 20, "#B91C1C", stroke_fill="white", stroke_width=2, bold=True, anchor="mm")
    checks = [
        "☑ 不要な民間保険を即解約",
        "☑ 固定費・不要サブスク削減",
        "☑ 新NISAで自動積立を設定",
    ]
    for i, ck in enumerate(checks):
        draw_stroked_text(draw, (95, 915 + i * 32), ck, 17, "#1A2535", stroke_fill="white", stroke_width=1, bold=True, anchor="lm")

    # Conclusion Scroll patch
    k_patch = Image.new("RGBA", (510, 165), (0, 0, 0, 0))
    kp_d = ImageDraw.Draw(k_patch)
    kp_d.rounded_rectangle((0, 0, 510, 165), 18, fill=(255, 250, 240, 250), outline=(184, 115, 51), width=3)
    im.alpha_composite(k_patch, (455, 850))
    draw = ImageDraw.Draw(im)

    draw_stroked_text(draw, (710, 875), "本の結論", 24, "#C2410C", stroke_fill="white", stroke_width=2, bold=True, anchor="mm")
    conclusion_text = (
        "「買わない決断」とはケチではなく、\n"
        "資本主義の理不尽な搾取から解放され、\n"
        "人生の主導権を取り戻す最大の武器。"
    )
    draw_stroked_text(draw, (710, 940), conclusion_text, 20, "#1A2535", stroke_fill="white", stroke_width=1, bold=True, anchor="mm", align="center", spacing=6)

    out_file = OUT / "金持ちが絶対買わないもの_個人アカウント用.png"
    im.convert("RGB").save(out_file, format="PNG", quality=98)
    print("Personal Handcrafted Infographic successfully saved:", out_file)


def render_studio_handcrafted():
    print("Generating Studio Handcrafted Infographic...")
    base_path = OUT / "1億円貯める方法_ダンススタジオ用.png"
    im = Image.open(base_path).convert("RGBA")
    draw = ImageDraw.Draw(im)

    # 1. RETOUCH TITLE PLATE (x: 240 to 980, y: 70 to 325)
    title_patch = Image.new("RGBA", (740, 220), (0, 0, 0, 0))
    tp_draw = ImageDraw.Draw(title_patch)
    tp_draw.rounded_rectangle((10, 10, 730, 210), 24, fill=(255, 252, 245, 245), outline=(28, 124, 130), width=4)
    tp_draw.rounded_rectangle((16, 16, 724, 204), 18, fill=(245, 253, 253, 235), outline=(190, 230, 230), width=2)
    im.alpha_composite(title_patch, (245, 80))
    draw = ImageDraw.Draw(im)

    # Top line: "Studio Haru 人生を身軽にする知恵"
    draw_stroked_text(draw, (615, 118), "Studio Haru 人生を身軽にする知恵", 25, "#1C7C82", stroke_fill="white", stroke_width=3, bold=True, mincho=False, anchor="mm")

    # Main Title: "お金持ちが「絶対買わない」もの"
    draw_stroked_text(draw, (615, 168), "お金持ちが「絶対買わない」もの", 44, "#172334", stroke_fill="white", stroke_width=5, bold=True, mincho=True, anchor="mm")

    # Subtitle Ribbon: "6つの黄金ルール"
    draw_stroked_text(draw, (615, 224), "6つの黄金ルール", 38, "#E76F51", stroke_fill="white", stroke_width=4, bold=True, mincho=True, anchor="mm")

    # Bottom ribbon: "無駄な浪費を手放して、本当に大切なことに全集中！"
    ribbon_box = (250, 260, 980, 298)
    draw.rounded_rectangle(ribbon_box, 14, fill=(28, 124, 130), outline=(231, 111, 81), width=2)
    draw_stroked_text(draw, (615, 279), "無駄な浪費を手放して、本当に大切なことに全集中！", 20, "white", stroke_fill="#124E52", stroke_width=1, bold=True, anchor="mm")

    # 2. RETOUCH THE 6 CARDS
    cards_s = [
        (
            (62, 358, 423, 572),
            "01", "立派すぎる葬儀", "#E63946",
            "見栄の過剰出費をストップ！",
            "世間体のプレッシャーを排除\n心温まる家族葬で十分伝わる\n事前の冷静な相談がカギ"
        ),
        (
            (447, 358, 808, 572),
            "02", "重い新築マイホーム", "#2A9D8F",
            "高額ローンで身動き止めない！",
            "買った瞬間に資産価値2割下落\n自由に動ける中古リノベや賃貸\n身軽さこそ最大の強み"
        ),
        (
            (832, 358, 1193, 572),
            "03", "不安を煽る高額教材", "#3A86FF",
            "買うだけ満足は即卒業！",
            "高額商材に頼らず良書1冊\nスタジオで汗を流して学ぶ\n実践とアウトプットで成長"
        ),
        (
            (62, 582, 423, 796),
            "04", "寂しさの孤独消費", "#F4A261",
            "見せかけの承認欲求はゼロ！",
            "夜の街や過剰課金は虚しいだけ\nお金で買えない本物の繋がり\n仲間と本気で踊る時間へ"
        ),
        (
            (447, 582, 808, 796),
            "05", "過剰な民間保険", "#2A9D8F",
            "公的保険＋ダンスで健康へ！",
            "高額療養費制度があるから安心\n不要な特約はカットして身軽に\n浮いたお金を自分磨きへ"
        ),
        (
            (832, 582, 1193, 796),
            "06", "搾取宝くじ", "#E76F51",
            "半分抜かれるギャンブル卒業！",
            "期待値マイナスには手を出さない\n新NISAで手堅く資産形成\nダンススキルへの自己投資！"
        ),
    ]

    for (bx1, by1, bx2, by2), num, title, color, sub_h, body in cards_s:
        t_patch = Image.new("RGBA", (bx2 - bx1 - 16, 138), (0, 0, 0, 0))
        tp_d = ImageDraw.Draw(t_patch)
        tp_d.rounded_rectangle((0, 0, bx2 - bx1 - 16, 138), 14, fill=(255, 253, 248, 248), outline=(225, 235, 235), width=1)
        im.alpha_composite(t_patch, (bx1 + 8, by1 + 6))
        draw = ImageDraw.Draw(im)

        badge_w = 46
        badge_h = 32
        badge_x = bx1 + 18
        badge_y = by1 + 12
        draw.rounded_rectangle((badge_x, badge_y, badge_x + badge_w, badge_y + badge_h), 14, fill=color)
        draw_stroked_text(draw, (badge_x + badge_w // 2, badge_y + badge_h // 2), num, 19, "white", stroke_fill=color, stroke_width=1, bold=True, anchor="mm")

        title_x = badge_x + badge_w + 10
        title_y = badge_y + badge_h // 2
        draw_stroked_text(draw, (title_x, title_y), title, 22, "#172334", stroke_fill="white", stroke_width=2, bold=True, anchor="lm")

        sub_box = (bx1 + 18, by1 + 48, bx2 - 18, by1 + 76)
        draw.rounded_rectangle(sub_box, 8, fill=(255, 245, 242) if color in ["#E63946", "#E76F51", "#F4A261"] else (240, 252, 250))
        draw_stroked_text(draw, ((sub_box[0] + sub_box[2]) // 2, (sub_box[1] + sub_box[3]) // 2), sub_h, 16, color, stroke_fill="white", stroke_width=1, bold=True, anchor="mm")

        draw_stroked_text(draw, (bx1 + 22, by1 + 86), body, 15, "#2C3E50", stroke_fill="white", stroke_width=1, bold=False, anchor="la", align="left", spacing=4)

    # 3. RETOUCH BOTTOM FOOTER
    c_patch = Image.new("RGBA", (340, 165), (0, 0, 0, 0))
    cp_d = ImageDraw.Draw(c_patch)
    cp_d.rounded_rectangle((0, 0, 340, 165), 16, fill=(255, 250, 242, 250), outline=(139, 69, 19), width=2)
    im.alpha_composite(c_patch, (75, 850))
    draw = ImageDraw.Draw(im)

    draw_stroked_text(draw, (245, 875), "今日からできるアクション", 19, "#E76F51", stroke_fill="white", stroke_width=2, bold=True, anchor="mm")
    checks_s = [
        "☑ 不要なサブスクを即解約",
        "☑ 見栄の浪費をストップ",
        "☑ 身軽に大好きなダンスへ！",
    ]
    for i, ck in enumerate(checks_s):
        draw_stroked_text(draw, (95, 915 + i * 32), ck, 17, "#172334", stroke_fill="white", stroke_width=1, bold=True, anchor="lm")

    k_patch = Image.new("RGBA", (510, 165), (0, 0, 0, 0))
    kp_d = ImageDraw.Draw(k_patch)
    kp_d.rounded_rectangle((0, 0, 510, 165), 18, fill=(248, 253, 252, 250), outline=(28, 124, 130), width=3)
    im.alpha_composite(k_patch, (455, 850))
    draw = ImageDraw.Draw(im)

    draw_stroked_text(draw, (710, 875), "スタジオの合言葉", 24, "#1C7C82", stroke_fill="white", stroke_width=2, bold=True, anchor="mm")
    conclusion_studio = (
        "持ち物を軽く、心を自由に。\n"
        "無駄な支出を手放して、\n"
        "大好きなダンスと夢に全集中！"
    )
    draw_stroked_text(draw, (710, 940), conclusion_studio, 20, "#172334", stroke_fill="white", stroke_width=1, bold=True, anchor="mm", align="center", spacing=6)

    out_file = OUT / "金持ちが絶対買わないもの_ダンススタジオ用.png"
    im.convert("RGB").save(out_file, format="PNG", quality=98)
    print("Studio Handcrafted Infographic successfully saved:", out_file)


if __name__ == "__main__":
    render_personal_handcrafted()
    render_studio_handcrafted()
