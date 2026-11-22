import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(r"C:\Users\kurro\.gemini\antigravity\scratch\haru-post-tool-ai-handoff-20261121")
BRAIN = Path(r"C:\Users\kurro\.gemini\antigravity\brain\37b73ff8-3d00-4627-bc53-b533c97e2644")
OUT = ROOT / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

SIZE = 1254

FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"
FONT_M = r"C:\Windows\Fonts\BIZ-UDMinchoM.ttc"


def get_font(size, bold=True, mincho=False):
    if mincho:
        return ImageFont.truetype(FONT_M, size)
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def draw_text_stroked(draw, xy, text, size, fill, stroke_fill="white", stroke_width=3, bold=True, mincho=False, anchor="la"):
    f = get_font(size, bold=bold, mincho=mincho)
    draw.text(xy, text, font=f, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill, anchor=anchor)


# 6 Rules Data
RULES_DATA_PERSONAL = [
    {
        "num": "01",
        "bad_title": "立派すぎる葬儀・生前墓地",
        "bad_sub": "世間体や見栄の高額請求を回避",
        "good_title": "シンプルな家族葬＆事前相談",
        "good_sub": "金額ではなく心で偲ぶのが真の供養",
    },
    {
        "num": "02",
        "bad_title": "大手新築一戸建て",
        "bad_sub": "買った瞬間に価値2割下落・35年ローン",
        "good_title": "資産価値の落ちない中古・賃貸",
        "good_sub": "身軽に動けて負債リスクをゼロに",
    },
    {
        "num": "03",
        "bad_title": "高額な資格・オンライン教材",
        "bad_sub": "将来の不安につけ込む搾取ビジネス",
        "good_title": "数千円の良書と本業の実務経験",
        "good_sub": "不安解消は買えない。行動で実力を積む",
    },
    {
        "num": "04",
        "bad_title": "心の隙間を埋める孤独消費",
        "bad_sub": "夜の街・過剰課金・見栄のブランド品",
        "good_title": "仲間や家族と過ごす温かい時間",
        "good_sub": "お金で買った関係は消える。本物の絆へ",
    },
    {
        "num": "05",
        "bad_title": "「なんとなく不安」な民間保険",
        "bad_sub": "過剰な特約で毎月数万円の流出",
        "good_title": "高額療養費制度＋浮いたお金を投資",
        "good_sub": "最強の公的保険を知り生活防衛資金へ",
    },
    {
        "num": "06",
        "bad_title": "期待値46%の搾取宝くじ",
        "bad_sub": "胴元が半分抜く「愚か者の税金」",
        "good_title": "新NISAでインデックス投資",
        "good_sub": "勝率の高い世界成長に複利で乗る",
    },
]

RULES_DATA_STUDIO = [
    {
        "num": "01",
        "bad_title": "見栄や世間体の高額セレモニー",
        "bad_sub": "周囲に合わせた過剰な出費はストップ",
        "good_title": "温かい家族葬＆身の丈の選択",
        "good_sub": "感謝の気持ちは金額に関係なく伝わる",
    },
    {
        "num": "02",
        "bad_title": "重い縛りになる新築マイホーム",
        "bad_sub": "高額ローンで身動きが取れなくなる罠",
        "good_title": "身軽で自由な中古リノベや賃貸",
        "good_sub": "ライフステージに合わせて自由に動ける",
    },
    {
        "num": "03",
        "bad_title": "不安を煽る数十万円の教材",
        "bad_sub": "買うだけで満足して身につかない出費",
        "good_title": "良書1冊＋現場で踊って学ぶ！",
        "good_sub": "日々の実践とアウトプットが最大の成長",
    },
    {
        "num": "04",
        "bad_title": "寂しさや見栄の一時的な浪費",
        "bad_sub": "見せかけの承認欲求に使うお金はゼロに",
        "good_title": "スタジオの仲間と本気で踊る時間",
        "good_sub": "心を通わせる本物の繋がりが人生を潤す",
    },
    {
        "num": "05",
        "bad_title": "内容を知らない過剰な民間保険",
        "bad_sub": "不安任せで毎月のお金が消えていく",
        "good_title": "公的保険＋ダンスで健康な身体づくり",
        "good_sub": "浮いたお金は自分磨きと未来の投資へ",
    },
    {
        "num": "06",
        "bad_title": "一攫千金を夢見る宝くじ・ギャンブル",
        "bad_sub": "半分搾取されるマイナスサムゲーム",
        "good_title": "新NISA＋ダンススキルへの自己投資",
        "good_sub": "コツコツ積み上げて自分の価値を最大化！",
    },
]


def render_personal():
    print("Rendering Personal Infographic...")
    # Base background: Deep Elegant Midnight Blue & Gold aura
    canvas = Image.new("RGBA", (SIZE, SIZE), (13, 27, 42, 255))
    draw = ImageDraw.Draw(canvas)

    # Subtle background gradient & geometric elegance
    for y in range(SIZE):
        ratio = y / float(SIZE)
        r = int(14 * (1 - ratio) + 8 * ratio)
        g = int(28 * (1 - ratio) + 16 * ratio)
        b = int(48 * (1 - ratio) + 32 * ratio)
        draw.line([(0, y), (SIZE, y)], fill=(r, g, b, 255))

    # Decorative background glow behind header
    glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse((SIZE//2 - 400, -100, SIZE//2 + 400, 300), fill=(212, 175, 55, 30))
    glow = glow.filter(ImageFilter.GaussianBlur(50))
    canvas.alpha_composite(glow)
    draw = ImageDraw.Draw(canvas)

    # --- TOP HEADER AREA (y: 20 to 250) ---
    # Center Title Plate
    plate_box = (250, 24, SIZE - 250, 236)
    draw.rounded_rectangle(plate_box, 24, fill=(18, 35, 58, 245), outline=(212, 175, 55), width=3)
    draw.rounded_rectangle((plate_box[0]+4, plate_box[1]+4, plate_box[2]-4, plate_box[3]-4), 20, fill=(24, 44, 72, 240), outline=(160, 130, 40), width=1)

    # Top ribbon badge
    ribbon_box = (SIZE//2 - 270, 38, SIZE//2 + 270, 74)
    draw.rounded_rectangle(ribbon_box, 18, fill=(212, 175, 55))
    draw_text_stroked(draw, (SIZE//2, 56), "上位1%の養分にならない！生活防衛鉄則", 20, "#0D1B2A", stroke_fill="#FFEDB3", stroke_width=1, bold=True, anchor="mm")

    # Main Big Title
    draw_text_stroked(draw, (SIZE//2, 122), "金持ちが絶対買わないもの", 44, "#FFFDF5", stroke_fill="#C79624", stroke_width=4, bold=True, mincho=True, anchor="mm")
    
    # Subtitle Ribbon
    sub_box = (SIZE//2 - 250, 168, SIZE//2 + 250, 214)
    draw.rounded_rectangle(sub_box, 14, fill=(230, 57, 70), outline=(255, 255, 255), width=2)
    draw_text_stroked(draw, (SIZE//2, 191), "❌ 浪費の罠 6選  ➡  ⭕ 富裕層の正解", 23, "white", stroke_fill="#A81824", stroke_width=2, bold=True, anchor="mm")

    # Place Official Characters: Sakurajimao on Left, Harumichi on Right
    sakurajimao_path = BRAIN / "sakurajimao_official.png"
    if sakurajimao_path.exists():
        s_img = Image.open(sakurajimao_path).convert("RGBA")
        sw, sh = s_img.size
        target_h = 230
        target_w = round(sw * (target_h / float(sh)))
        s_res = s_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        canvas.alpha_composite(s_res, (28, 15))

    harumichi_path = BRAIN / "harumichi_official.png"
    if harumichi_path.exists():
        h_img = Image.open(harumichi_path).convert("RGBA")
        hw, hh = h_img.size
        target_h = 230
        target_w = round(hw * (target_h / float(hh)))
        h_res = h_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        canvas.alpha_composite(h_res, (SIZE - target_w - 28, 15))

    # --- 6 WIDE CONTRAST BANNERS (y: 254 to 1106) ---
    start_y = 254
    banner_h = 132
    gap = 10
    banner_w = 1194
    bx1 = (SIZE - banner_w) // 2
    bx2 = bx1 + banner_w

    for i, item in enumerate(RULES_DATA_PERSONAL):
        by1 = start_y + i * (banner_h + gap)
        by2 = by1 + banner_h

        # Base card background (Crisp Ivory/White with elegant dual container)
        draw.rounded_rectangle((bx1, by1, bx2, by2), 20, fill=(255, 255, 255), outline=(200, 210, 225), width=2)

        # Number Badge (Gold Circular Badge on Left)
        num_x = bx1 + 45
        num_y = (by1 + by2) // 2
        draw.ellipse((num_x - 32, num_y - 32, num_x + 32, num_y + 32), fill=(18, 35, 58), outline=(212, 175, 55), width=3)
        draw_text_stroked(draw, (num_x, num_y), item["num"], 25, "#FFDF73", stroke_fill="#12233A", stroke_width=1, bold=True, anchor="mm")

        # Left Column: ❌ BAD TRAP (x: bx1 + 90 to bx1 + 590)
        bad_box = (bx1 + 90, by1 + 10, bx1 + 590, by2 - 10)
        draw.rounded_rectangle(bad_box, 14, fill=(254, 242, 242), outline=(248, 180, 180), width=1)
        
        # Red Tag
        draw.rounded_rectangle((bad_box[0] + 12, bad_box[1] + 12, bad_box[0] + 102, bad_box[1] + 38), 6, fill=(220, 38, 38))
        draw_text_stroked(draw, (bad_box[0] + 57, bad_box[1] + 25), "❌ 買わない", 14, "white", stroke_fill="#B91C1C", stroke_width=1, bold=True, anchor="mm")
        
        # Bad Title & Sub
        draw_text_stroked(draw, (bad_box[0] + 112, bad_box[1] + 25), item["bad_title"], 20, "#7F1D1D", stroke_fill="white", stroke_width=0, bold=True, anchor="lm")
        draw.text((bad_box[0] + 18, bad_box[1] + 62), item["bad_sub"], font=get_font(16, bold=False), fill="#991B1B", anchor="la")

        # Center Arrow
        arrow_cx = bx1 + 610
        draw_text_stroked(draw, (arrow_cx, num_y), "➡", 30, "#C79624", stroke_fill="white", stroke_width=1, bold=True, anchor="mm")

        # Right Column: ⭕ GOOD SOLUTION (x: bx1 + 630 to bx2 - 16)
        good_box = (bx1 + 630, by1 + 10, bx2 - 16, by2 - 10)
        draw.rounded_rectangle(good_box, 14, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
        
        # Green Tag
        draw.rounded_rectangle((good_box[0] + 12, good_box[1] + 12, good_box[0] + 96, good_box[1] + 38), 6, fill=(22, 101, 52))
        draw_text_stroked(draw, (good_box[0] + 54, good_box[1] + 25), "⭕ 正解", 14, "white", stroke_fill="#15803D", stroke_width=1, bold=True, anchor="mm")
        
        # Good Title & Sub
        draw_text_stroked(draw, (good_box[0] + 106, good_box[1] + 25), item["good_title"], 20, "#14532D", stroke_fill="white", stroke_width=0, bold=True, anchor="lm")
        draw.text((good_box[0] + 18, good_box[1] + 62), item["good_sub"], font=get_font(16, bold=False), fill="#166534", anchor="la")

    # --- BOTTOM FOOTER CONCLUSION (y: 1114 to 1234) ---
    foot_box = (bx1, 1114, bx2, 1234)
    draw.rounded_rectangle(foot_box, 20, fill=(24, 44, 72), outline=(212, 175, 55), width=3)
    
    # Conclusion badge
    draw.rounded_rectangle((foot_box[0] + 20, foot_box[1] + 16, foot_box[0] + 140, foot_box[1] + 54), 10, fill=(212, 175, 55))
    draw_text_stroked(draw, (foot_box[0] + 80, foot_box[1] + 35), "富裕層の鉄則", 16, "#0D1B2A", stroke_fill="#FFF3CC", stroke_width=1, bold=True, anchor="mm")

    # Main Conclusion sentence
    draw_text_stroked(draw, (foot_box[0] + 160, foot_box[1] + 35), "「見栄・不安・孤独」にお金を使わず、「時間・健康・投資」に集中する！", 23, "#FFFDF5", stroke_fill="#0D1B2A", stroke_width=2, bold=True, anchor="lm")

    # Action prompt
    action_box = (foot_box[0] + 20, foot_box[1] + 66, foot_box[1] + 1150, foot_box[3] - 14)
    draw.rounded_rectangle((foot_box[0] + 20, foot_box[1] + 68, foot_box[2] - 20, foot_box[3] - 14), 12, fill=(13, 27, 42))
    draw_text_stroked(draw, (SIZE // 2, foot_box[1] + 93), "👉 今日の一歩：不要な民間保険やサブスクを今すぐ見直して、生活防衛資金をつくろう！", 19, "#FFDF73", stroke_fill="#0D1B2A", stroke_width=1, bold=True, anchor="mm")

    out_file = OUT / "金持ちが絶対買わないもの_個人アカウント用.png"
    canvas.convert("RGB").save(out_file, quality=98)
    print(f"Personal Infographic saved: {out_file}")


def render_studio():
    print("Rendering Studio Infographic...")
    # Base background: Fresh Stylish Studio Teal & Coral Glow
    canvas = Image.new("RGBA", (SIZE, SIZE), (242, 248, 248, 255))
    draw = ImageDraw.Draw(canvas)

    # Gradient from soft mint teal to warm sunrise cream
    for y in range(SIZE):
        ratio = y / float(SIZE)
        r = int(230 * (1 - ratio) + 252 * ratio)
        g = int(246 * (1 - ratio) + 248 * ratio)
        b = int(246 * (1 - ratio) + 242 * ratio)
        draw.line([(0, y), (SIZE, y)], fill=(r, g, b, 255))

    # Decorative background shapes for youth dance energy
    glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse((SIZE//2 - 450, -120, SIZE//2 + 450, 320), fill=(28, 124, 130, 25))
    g_draw.ellipse((SIZE - 300, 300, SIZE + 100, 700), fill=(231, 111, 81, 20))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    canvas.alpha_composite(glow)
    draw = ImageDraw.Draw(canvas)

    # --- TOP HEADER AREA (y: 20 to 250) ---
    # Center Title Plate
    plate_box = (250, 24, SIZE - 250, 236)
    draw.rounded_rectangle(plate_box, 24, fill=(255, 255, 255, 250), outline=(28, 124, 130), width=3)
    draw.rounded_rectangle((plate_box[0]+4, plate_box[1]+4, plate_box[2]-4, plate_box[3]-4), 20, fill=(245, 252, 252, 240), outline=(200, 230, 230), width=1)

    # Top ribbon badge
    ribbon_box = (SIZE//2 - 270, 38, SIZE//2 + 270, 74)
    draw.rounded_rectangle(ribbon_box, 18, fill=(28, 124, 130))
    draw_text_stroked(draw, (SIZE//2, 56), "Studio Haru 人生を身軽にするスマート習慣", 20, "white", stroke_fill="#135256", stroke_width=1, bold=True, anchor="mm")

    # Main Big Title
    draw_text_stroked(draw, (SIZE//2, 122), "お金持ちが絶対買わないもの", 44, "#172334", stroke_fill="white", stroke_width=5, bold=True, mincho=True, anchor="mm")
    
    # Subtitle Ribbon
    sub_box = (SIZE//2 - 250, 168, SIZE//2 + 250, 214)
    draw.rounded_rectangle(sub_box, 14, fill=(231, 111, 81), outline=(255, 255, 255), width=2)
    draw_text_stroked(draw, (SIZE//2, 191), "❌ 手放す浪費 6選  ➡  ⭕ 価値ある自己投資", 23, "white", stroke_fill="#B84226", stroke_width=2, bold=True, anchor="mm")

    # Place Official Characters: Haruka on Left, Robot & Cat on Right
    # Haruka
    haruka_path = BRAIN / "char_haruka.png"
    if haruka_path.exists():
        h_img = Image.open(haruka_path).convert("RGBA")
        hw, hh = h_img.size
        target_h = 226
        target_w = round(hw * (target_h / float(hh)))
        h_res = h_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        canvas.alpha_composite(h_res, (40, 18))

    # Robot (Mirai) and Cat
    robot_path = BRAIN / "char_robot.png"
    cat_path = BRAIN / "char_cat.png"
    if robot_path.exists():
        r_img = Image.open(robot_path).convert("RGBA")
        rw, rh = r_img.size
        r_res = r_img.resize((round(rw * 1.05), round(rh * 1.05)), Image.Resampling.LANCZOS)
        canvas.alpha_composite(r_res, (SIZE - 230, 24))

    if cat_path.exists():
        c_img = Image.open(cat_path).convert("RGBA")
        cw, ch = c_img.size
        c_res = c_img.resize((round(cw * 1.15), round(ch * 1.15)), Image.Resampling.LANCZOS)
        canvas.alpha_composite(c_res, (SIZE - 170, 128))

    # --- 6 WIDE CONTRAST BANNERS (y: 254 to 1106) ---
    start_y = 254
    banner_h = 132
    gap = 10
    banner_w = 1194
    bx1 = (SIZE - banner_w) // 2
    bx2 = bx1 + banner_w

    for i, item in enumerate(RULES_DATA_STUDIO):
        by1 = start_y + i * (banner_h + gap)
        by2 = by1 + banner_h

        # Base card background
        draw.rounded_rectangle((bx1, by1, bx2, by2), 20, fill=(255, 255, 255), outline=(210, 230, 230), width=2)

        # Number Badge (Teal Circular Badge on Left)
        num_x = bx1 + 45
        num_y = (by1 + by2) // 2
        draw.ellipse((num_x - 32, num_y - 32, num_x + 32, num_y + 32), fill=(28, 124, 130), outline=(231, 111, 81), width=3)
        draw_text_stroked(draw, (num_x, num_y), item["num"], 25, "white", stroke_fill="#135256", stroke_width=1, bold=True, anchor="mm")

        # Left Column: ❌ BAD TRAP (Coral Pink tone)
        bad_box = (bx1 + 90, by1 + 10, bx1 + 590, by2 - 10)
        draw.rounded_rectangle(bad_box, 14, fill=(255, 245, 242), outline=(250, 205, 195), width=1)
        
        # Coral Tag
        draw.rounded_rectangle((bad_box[0] + 12, bad_box[1] + 12, bad_box[0] + 102, bad_box[1] + 38), 6, fill=(225, 75, 45))
        draw_text_stroked(draw, (bad_box[0] + 57, bad_box[1] + 25), "❌ 手放す", 14, "white", stroke_fill="#B84226", stroke_width=1, bold=True, anchor="mm")
        
        # Bad Title & Sub
        draw_text_stroked(draw, (bad_box[0] + 112, bad_box[1] + 25), item["bad_title"], 20, "#8C2B18", stroke_fill="white", stroke_width=0, bold=True, anchor="lm")
        draw.text((bad_box[0] + 18, bad_box[1] + 62), item["bad_sub"], font=get_font(16, bold=False), fill="#A63820", anchor="la")

        # Center Arrow
        arrow_cx = bx1 + 610
        draw_text_stroked(draw, (arrow_cx, num_y), "➡", 30, "#E76F51", stroke_fill="white", stroke_width=1, bold=True, anchor="mm")

        # Right Column: ⭕ GOOD SOLUTION (Teal Green tone)
        good_box = (bx1 + 630, by1 + 10, bx2 - 16, by2 - 10)
        draw.rounded_rectangle(good_box, 14, fill=(240, 252, 250), outline=(195, 235, 230), width=1)
        
        # Teal Tag
        draw.rounded_rectangle((good_box[0] + 12, good_box[1] + 12, good_box[0] + 106, good_box[1] + 38), 6, fill=(20, 115, 120))
        draw_text_stroked(draw, (good_box[0] + 59, good_box[1] + 25), "⭕ ハル流正解", 14, "white", stroke_fill="#105054", stroke_width=1, bold=True, anchor="mm")
        
        # Good Title & Sub
        draw_text_stroked(draw, (good_box[0] + 116, good_box[1] + 25), item["good_title"], 20, "#0F464A", stroke_fill="white", stroke_width=0, bold=True, anchor="lm")
        draw.text((good_box[0] + 18, good_box[1] + 62), item["good_sub"], font=get_font(16, bold=False), fill="#175F64", anchor="la")

    # --- BOTTOM FOOTER CONCLUSION (y: 1114 to 1234) ---
    foot_box = (bx1, 1114, bx2, 1234)
    draw.rounded_rectangle(foot_box, 20, fill=(28, 124, 130), outline=(231, 111, 81), width=3)
    
    # Conclusion badge
    draw.rounded_rectangle((foot_box[0] + 20, foot_box[1] + 16, foot_box[0] + 155, foot_box[1] + 54), 10, fill=(231, 111, 81))
    draw_text_stroked(draw, (foot_box[0] + 87, foot_box[1] + 35), "スタジオの合言葉", 16, "white", stroke_fill="#9C3018", stroke_width=1, bold=True, anchor="mm")

    # Main Conclusion sentence
    draw_text_stroked(draw, (foot_box[0] + 175, foot_box[1] + 35), "持ち物を軽く、心を自由に。無駄な支出を手放して、夢と自己投資に全集中！", 23, "#FFFFFF", stroke_fill="#135256", stroke_width=2, bold=True, anchor="lm")

    # Action prompt
    draw.rounded_rectangle((foot_box[0] + 20, foot_box[1] + 68, foot_box[2] - 20, foot_box[3] - 14), 12, fill=(20, 95, 100))
    draw_text_stroked(draw, (SIZE // 2, foot_box[1] + 93), "✨ 今日のアクション：見栄や不要な出費を削って、大好きなダンスや体験にお金を使おう！", 19, "#FFF8E7", stroke_fill="#104548", stroke_width=1, bold=True, anchor="mm")

    out_file = OUT / "金持ちが絶対買わないもの_ダンススタジオ用.png"
    canvas.convert("RGB").save(out_file, quality=98)
    print(f"Studio Infographic saved: {out_file}")


if __name__ == "__main__":
    render_personal()
    render_studio()
