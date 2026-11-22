from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path("C:/Users/kurro/.gemini/antigravity/scratch/haru-post-tool-ai-handoff-20261121")
OUT = ROOT / "outputs"
BRAIN = Path("C:/Users/kurro/.gemini/antigravity/brain/37b73ff8-3d00-4627-bc53-b533c97e2644")
SIZE = 1254

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

def draw_horizontal_colored_text(draw, center_xy, segments, size, stroke_fill="white", stroke_width=5, mincho=True):
    f = font(size, bold=True, mincho=mincho)
    widths = [f.getlength(text) for text, _ in segments]
    total_w = sum(widths)
    cur_x = center_xy[0] - total_w / 2.0
    cy = center_xy[1]
    for (text, color), w in zip(segments, widths):
        draw.text((cur_x, cy), text, font=f, fill=color, stroke_width=stroke_width, stroke_fill=stroke_fill, anchor="lm")
        cur_x += w

def cover_image(im, size):
    ratio = max(size[0] / im.width, size[1] / im.height)
    im = im.resize((round(im.width * ratio), round(im.height * ratio)), Image.Resampling.LANCZOS)
    x = (im.width - size[0]) // 2
    y = (im.height - size[1]) // 2
    return im.crop((x, y, x + size[0], y + size[1]))

# ========================================================
# 1. STUDIO MASTER INFOGRAPHIC (春ちゃん・ロボット・猫)
# ========================================================
def render_studio():
    # Base background: Blend lovely warm closet artwork with soft veil
    bg_art_path = BRAIN / "haruka_fukusute_slide_illustration_1795311720688.jpg"
    if bg_art_path.exists():
        base_bg = Image.open(bg_art_path).convert("RGBA")
        base_bg = cover_image(base_bg, (SIZE, SIZE)).filter(ImageFilter.GaussianBlur(16))
        veil = Image.new("RGBA", (SIZE, SIZE), (254, 252, 247, 230))
        canvas = Image.alpha_composite(base_bg, veil)
    else:
        canvas = Image.new("RGBA", (SIZE, SIZE), (252, 249, 242, 255))
    
    draw = ImageDraw.Draw(canvas)

    # Top header sky banner (y: 0 to 370)
    sky = Image.new("RGBA", (SIZE, 375), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sky)
    for y in range(375):
        ratio = y / 375.0
        r = int(140 * (1 - ratio) + 252 * ratio)
        g = int(195 * (1 - ratio) + 249 * ratio)
        b = int(248 * (1 - ratio) + 242 * ratio)
        s_draw.line([(0, y), (SIZE, y)], fill=(r, g, b, int(210 * (1 - ratio))))
    canvas.alpha_composite(sky, (0, 0))
    draw = ImageDraw.Draw(canvas)

    # Top Title Plate
    t_box = (50, 20, SIZE - 50, 126)
    draw.rounded_rectangle(t_box, 48, fill=(255, 255, 255), outline=(238, 185, 45), width=5)
    draw.rounded_rectangle((t_box[0] + 6, t_box[1] + 6, t_box[2] - 6, t_box[3] - 6), 42, fill=(255, 253, 246), outline=(252, 236, 192), width=3)

    title_segments = [
        ("服", "#D12626"),
        ("を捨てると、人生が", "#1A1A1A"),
        ("劇的に好転", "#D12626"),
        ("する！", "#1A1A1A")
    ]
    draw_horizontal_colored_text(draw, (SIZE // 2, 73), title_segments, 54, stroke_fill="white", stroke_width=5, mincho=True)

    # Yellow ribbon for subtitle
    r_box = (120, 134, SIZE - 120, 196)
    draw.rounded_rectangle(r_box, 28, fill=(255, 221, 0), outline=(226, 158, 0), width=4)
    draw_text_with_stroke(draw, (SIZE // 2, 165), "クローゼットから「他人軸」を手放し、自由を取り戻す", 31, "#172334", stroke_fill="#FFDD00", stroke_width=1)

    # Place Characters: Haruka on left, Robot on right top, Cat on right bottom
    haruka = Image.open(BRAIN / "char_haruka.png").convert("RGBA")
    h_w, h_h = haruka.size
    h_scale = 210 / float(h_h)
    haruka_res = haruka.resize((round(h_w * h_scale), 210), Image.Resampling.LANCZOS)
    canvas.alpha_composite(haruka_res, (65, 180))

    robot = Image.open(BRAIN / "char_robot.png").convert("RGBA")
    r_w, r_h = robot.size
    r_scale = 135 / float(r_h)
    robot_res = robot.resize((round(r_w * r_scale), 135), Image.Resampling.LANCZOS)
    canvas.alpha_composite(robot_res, (SIZE - 245, 186))

    cat = Image.open(BRAIN / "char_cat.png").convert("RGBA")
    c_w, c_h = cat.size
    c_scale = 120 / float(c_h)
    cat_res = cat.resize((round(c_w * c_scale), 120), Image.Resampling.LANCZOS)
    canvas.alpha_composite(cat_res, (SIZE - 175, 258))

    # Speech bubbles or decorative badge between Haruka and Robot
    mid_badge = (310, 225, 960, 360)
    draw.rounded_rectangle(mid_badge, 28, fill=(255, 255, 255, 248), outline=(215, 139, 66), width=3)
    draw.text(((mid_badge[0] + mid_badge[2]) // 2, 258), "なぜ服を捨てると、お金が増えるのか？", font=font(24, bold=True), fill="#BF3228", anchor="mm")
    draw.text(((mid_badge[0] + mid_badge[2]) // 2, 298), "① 視界のノイズが消える　② 流行・見栄の浪費がゼロに", font=font(19, bold=True), fill="#2C3E50", anchor="mm")
    draw.text(((mid_badge[0] + mid_badge[2]) // 2, 332), "③ 自分軸が定まり「本当に似合う最高の一着」に集中できる", font=font(17, bold=False), fill="#4A5568", anchor="mm")

    # 3 Main Cards (排出期・モヤモヤ期・静寂期) y: 385 to 865
    card_w = 376
    spacing = 18
    left_margin = 44
    c1_x1 = left_margin
    c1_x2 = c1_x1 + card_w
    c2_x1 = c1_x2 + spacing
    c2_x2 = c2_x1 + card_w
    c3_x1 = c2_x2 + spacing
    c3_x2 = c3_x1 + card_w

    cards_y1 = 385
    cards_y2 = 865

    for x1, x2, border_color in [(c1_x1, c1_x2, (45, 119, 67)), (c2_x1, c2_x2, (38, 100, 158)), (c3_x1, c3_x2, (191, 50, 40))]:
        draw.rounded_rectangle((x1, cards_y1, x2, cards_y2), 32, fill=(255, 255, 255, 250), outline=border_color, width=4)

    # Headers
    draw.rounded_rectangle((c1_x1 + 6, cards_y1 + 6, c1_x2 - 6, cards_y1 + 82), 26, fill=(45, 119, 67))
    draw_text_with_stroke(draw, ((c1_x1 + c1_x2) // 2, cards_y1 + 44), "モノの服捨て【排出期】", 26, "white", stroke_fill="#2D7743", stroke_width=0)

    draw.rounded_rectangle((c2_x1 + 6, cards_y1 + 6, c2_x2 - 6, cards_y1 + 82), 26, fill=(38, 100, 158))
    draw_text_with_stroke(draw, ((c2_x1 + c2_x2) // 2, cards_y1 + 44), "思考の服捨て【モヤモヤ期】", 25, "white", stroke_fill="#26649E", stroke_width=0)

    draw.rounded_rectangle((c3_x1 + 6, cards_y1 + 6, c3_x2 - 6, cards_y1 + 82), 26, fill=(191, 50, 40))
    draw_text_with_stroke(draw, ((c3_x1 + c3_x2) // 2, cards_y1 + 44), "心の服捨て【静寂期】", 26, "white", stroke_fill="#BF3228", stroke_width=0)

    def draw_checklist(x1, y_start, items, color):
        y = y_start
        for item in items:
            draw.rounded_rectangle((x1 + 22, y - 14, x1 + 48, y + 12), 6, fill=(255, 255, 255), outline=color, width=3)
            draw.line([(x1 + 27, y), (x1 + 34, y + 7), (x1 + 44, y - 8)], fill=color, width=4)
            draw.text((x1 + 58, y - 2), item, font=font(19, bold=True), fill="#1A2535", anchor="lm")
            y += 50

    draw_checklist(c1_x1, 510, ["靴下・古い靴などから", "1日1個でも手放す", "水槽の濁りを抜く意識", "1年着ない服は即処分"], (45, 119, 67))
    draw_checklist(c2_x1, 510, ["買いながら捨てる循環", "不安は自分軸への蛹", "流行より心地よい定番", "最高の一着を厳選する"], (38, 100, 158))
    draw_checklist(c3_x1, 510, ["大好きな定番だけで十分", "朝の服選びストレスゼロ", "衝動買いがピタリと止まる", "自信に満ちた自分スタイル"], (191, 50, 40))

    def draw_card_pill(x1, x2, y, text_top, text_sub, color, bg_pill):
        draw.rounded_rectangle((x1 + 16, y, x2 - 16, y + 105), 24, fill=bg_pill, outline=color, width=2)
        draw.text(((x1 + x2) // 2, y + 36), text_top, font=font(21, bold=True), fill=color, anchor="mm")
        draw.text(((x1 + x2) // 2, y + 74), text_sub, font=font(18, bold=True), fill="#172334", anchor="mm")

    draw_card_pill(c1_x1, c1_x2, 735, "スペースと心の余白", "脳のノイズが晴れる！", (45, 119, 67), (235, 246, 238))
    draw_card_pill(c2_x1, c2_x2, 735, "クローゼットの新陳代謝", "自分に似合う軸を発見！", (38, 100, 158), (237, 244, 252))
    draw_card_pill(c3_x1, c3_x2, 735, "時間とお金の自由", "軽やかに踊る毎日へ！", (191, 50, 40), (252, 238, 235))

    # Bottom 5 Mindsets Card (y: 885 to 1115)
    draw.rounded_rectangle((c1_x1, 885, c3_x2, 1115), 32, fill=(255, 255, 255, 252), outline=(215, 139, 66), width=4)
    draw.rounded_rectangle((c1_x1 + 6, 891, c3_x2 - 6, 946), 22, fill=(215, 139, 66))
    draw_text_with_stroke(draw, (SIZE // 2, 918), "クローゼットの迷いを断ち切る「3秒で手放す5つの思考」", 24, "white", stroke_fill="#D78B42", stroke_width=0)

    col1_x = c1_x1 + 28
    col2_x = SIZE // 2 + 10
    draw.text((col1_x, 978), "1.「いつか着る」", font=font(18, bold=True), fill="#BF3228", anchor="lm")
    draw.text((col1_x + 165, 978), "→ いつかは来ない。いまを喜ばせる服だけ残す", font=font(15, bold=False), fill="#2C3E50", anchor="lm")
    draw.text((col1_x, 1028), "2.「正しく処分」", font=font(18, bold=True), fill="#BF3228", anchor="lm")
    draw.text((col1_x + 165, 1028), "→ 小銭稼ぎより、時間と心の自由を取り戻す", font=font(15, bold=False), fill="#2C3E50", anchor="lm")
    draw.text((col1_x, 1078), "3.「複数重複」", font=font(18, bold=True), fill="#BF3228", anchor="lm")
    draw.text((col1_x + 165, 1078), "→ 内側の魅力は服を減らしても1ミリも奪われない", font=font(15, bold=False), fill="#2C3E50", anchor="lm")

    draw.text((col2_x, 990), "4.「高かったから」", font=font(18, bold=True), fill="#BF3228", anchor="lm")
    draw.text((col2_x + 185, 990), "→ 過去の出費を忘れ、今の快適さを選ぶ", font=font(15, bold=False), fill="#2C3E50", anchor="lm")
    draw.text((col2_x, 1055), "5.「思い出の服」", font=font(18, bold=True), fill="#BF3228", anchor="lm")
    draw.text((col2_x + 185, 1055), "→ 大切な記憶は布ではなく心の中にある", font=font(15, bold=False), fill="#2C3E50", anchor="lm")

    # Wooden Signboard (y: 1135 to 1242)
    draw.rounded_rectangle((c1_x1 + 30, 1136, c3_x2 - 30, 1242), 26, fill=(255, 248, 238), outline=(125, 78, 38), width=4)
    draw.rounded_rectangle((c1_x1 + 38, 1144, c3_x2 - 38, 1234), 20, fill=(255, 245, 229), outline=(201, 148, 88), width=2)
    draw_text_with_stroke(draw, (SIZE // 2, 1189), "服を手放すことは、自分の人生の主導権を取り戻すこと。", 34, "#1E2A38", stroke_fill="white", stroke_width=4, mincho=True)

    target = OUT / "服捨て_ダンススタジオ用.png"
    canvas.convert("RGB").save(target, format="PNG", quality=98)
    print("Studio masterpiece saved:", target)

# ========================================================
# 2. PERSONAL MASTER INFOGRAPHIC (はるみち＆さくらじまお)
# ========================================================
def render_personal():
    # Warm base background
    bg_art_path = BRAIN / "haruka_fukusute_slide_illustration_1795311720688.jpg"
    if bg_art_path.exists():
        base_bg = Image.open(bg_art_path).convert("RGBA")
        base_bg = cover_image(base_bg, (SIZE, SIZE)).filter(ImageFilter.GaussianBlur(16))
        veil = Image.new("RGBA", (SIZE, SIZE), (255, 250, 242, 230))
        canvas = Image.alpha_composite(base_bg, veil)
    else:
        canvas = Image.new("RGBA", (SIZE, SIZE), (252, 249, 242, 255))
        
    draw = ImageDraw.Draw(canvas)

    # Top header gradient with gentle warm sunset glow
    sky = Image.new("RGBA", (SIZE, 375), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sky)
    for y in range(375):
        ratio = y / 375.0
        r = int(255 * (1 - ratio) + 252 * ratio)
        g = int(200 * (1 - ratio) + 249 * ratio)
        b = int(160 * (1 - ratio) + 242 * ratio)
        s_draw.line([(0, y), (SIZE, y)], fill=(r, g, b, int(210 * (1 - ratio))))
    canvas.alpha_composite(sky, (0, 0))
    draw = ImageDraw.Draw(canvas)

    # Top Title Plate
    t_box = (50, 20, SIZE - 50, 126)
    draw.rounded_rectangle(t_box, 48, fill=(255, 255, 255), outline=(215, 139, 66), width=5)
    draw.rounded_rectangle((t_box[0] + 6, t_box[1] + 6, t_box[2] - 6, t_box[3] - 6), 42, fill=(255, 253, 246), outline=(252, 236, 192), width=3)

    title_segments = [
        ("服", "#D12626"),
        ("を捨てると、人生が", "#1A1A1A"),
        ("劇的に好転", "#D12626"),
        ("する！", "#1A1A1A")
    ]
    draw_horizontal_colored_text(draw, (SIZE // 2, 73), title_segments, 54, stroke_fill="white", stroke_width=5, mincho=True)

    # Yellow ribbon for subtitle
    r_box = (120, 134, SIZE - 120, 196)
    draw.rounded_rectangle(r_box, 28, fill=(255, 221, 0), outline=(226, 158, 0), width=4)
    draw_text_with_stroke(draw, (SIZE // 2, 165), "クローゼットから「他人軸」を追い出し、自由を取り戻す", 31, "#172334", stroke_fill="#FFDD00", stroke_width=1)

    # Place Characters: Sakurajimao on left, Harumichi on right
    sakurajimao = Image.open(BRAIN / "char_sakurajimao.png").convert("RGBA")
    s_w, s_h = sakurajimao.size
    s_scale = 200 / float(s_h)
    sakurajimao_res = sakurajimao.resize((round(s_w * s_scale), 200), Image.Resampling.LANCZOS)
    canvas.alpha_composite(sakurajimao_res, (65, 178))

    harumichi = Image.open(BRAIN / "char_harumichi.png").convert("RGBA")
    h_w, h_h = harumichi.size
    h_scale = 200 / float(h_h)
    harumichi_res = harumichi.resize((round(h_w * h_scale), 200), Image.Resampling.LANCZOS)
    canvas.alpha_composite(harumichi_res, (SIZE - 200, 178))

    # Middle badge between Sakurajimao and Harumichi
    mid_badge = (240, 225, SIZE - 240, 360)
    draw.rounded_rectangle(mid_badge, 28, fill=(255, 255, 255, 248), outline=(215, 139, 66), width=3)
    draw.text(((mid_badge[0] + mid_badge[2]) // 2, 258), "なぜ服を捨てると、お金が増えるのか？", font=font(24, bold=True), fill="#BF3228", anchor="mm")
    draw.text(((mid_badge[0] + mid_badge[2]) // 2, 298), "① 視界のノイズが消える　② 流行・見栄の浪費がゼロに", font=font(19, bold=True), fill="#2C3E50", anchor="mm")
    draw.text(((mid_badge[0] + mid_badge[2]) // 2, 332), "③ クローゼットの歪みを整え、自分のお金と時間の主導権を取り戻す", font=font(17, bold=False), fill="#4A5568", anchor="mm")

    # 3 Main Cards (y: 385 to 865)
    card_w = 376
    spacing = 18
    left_margin = 44
    c1_x1 = left_margin
    c1_x2 = c1_x1 + card_w
    c2_x1 = c1_x2 + spacing
    c2_x2 = c2_x1 + card_w
    c3_x1 = c2_x2 + spacing
    c3_x2 = c3_x1 + card_w

    cards_y1 = 385
    cards_y2 = 865

    for x1, x2, border_color in [(c1_x1, c1_x2, (45, 119, 67)), (c2_x1, c2_x2, (38, 100, 158)), (c3_x1, c3_x2, (191, 50, 40))]:
        draw.rounded_rectangle((x1, cards_y1, x2, cards_y2), 32, fill=(255, 255, 255, 250), outline=border_color, width=4)

    # Headers
    draw.rounded_rectangle((c1_x1 + 6, cards_y1 + 6, c1_x2 - 6, cards_y1 + 82), 26, fill=(45, 119, 67))
    draw_text_with_stroke(draw, ((c1_x1 + c1_x2) // 2, cards_y1 + 44), "01 排出期【まず減らす】", 25, "white", stroke_fill="#2D7743", stroke_width=0)

    draw.rounded_rectangle((c2_x1 + 6, cards_y1 + 6, c2_x2 - 6, cards_y1 + 82), 26, fill=(38, 100, 158))
    draw_text_with_stroke(draw, ((c2_x1 + c2_x2) // 2, cards_y1 + 44), "02 モヤモヤ期【新陳代謝】", 24, "white", stroke_fill="#26649E", stroke_width=0)

    draw.rounded_rectangle((c3_x1 + 6, cards_y1 + 6, c3_x2 - 6, cards_y1 + 82), 26, fill=(191, 50, 40))
    draw_text_with_stroke(draw, ((c3_x1 + c3_x2) // 2, cards_y1 + 44), "03 静寂期【少数精鋭】", 25, "white", stroke_fill="#BF3228", stroke_width=0)

    def draw_checklist_p(x1, y_start, items, color):
        y = y_start
        for item in items:
            draw.rounded_rectangle((x1 + 22, y - 14, x1 + 48, y + 12), 6, fill=(255, 255, 255), outline=color, width=3)
            draw.line([(x1 + 27, y), (x1 + 34, y + 7), (x1 + 44, y - 8)], fill=color, width=4)
            draw.text((x1 + 58, y - 2), item, font=font(19, bold=True), fill="#1A2535", anchor="lm")
            y += 50

    draw_checklist_p(c1_x1, 510, ["靴下・下着・古い靴から", "1日1個でも手放す", "水槽の澄んだ水を抜く", "1年着ない服は即ゴミ袋へ"], (45, 119, 67))
    draw_checklist_p(c2_x1, 510, ["買いながら捨てる新陳代謝", "減らした不安は成長の蛹", "他人の流行より心地よさ", "本当に似合う定番を探す"], (38, 100, 158))
    draw_checklist_p(c3_x1, 510, ["大好きな数着だけで十分", "朝の服選びストレスゼロ", "衝動買いがピタリと消える", "自分軸で自信が湧いてくる"], (191, 50, 40))

    def draw_card_pill_p(x1, x2, y, text_top, text_sub, color, bg_pill):
        draw.rounded_rectangle((x1 + 16, y, x2 - 16, y + 105), 24, fill=bg_pill, outline=color, width=2)
        draw.text(((x1 + x2) // 2, y + 36), text_top, font=font(21, bold=True), fill=color, anchor="mm")
        draw.text(((x1 + x2) // 2, y + 74), text_sub, font=font(18, bold=True), fill="#172334", anchor="mm")

    draw_card_pill_p(c1_x1, c1_x2, 735, "空間と心の余白", "脳の濁りが晴れる！", (45, 119, 67), (235, 246, 238))
    draw_card_pill_p(c2_x1, c2_x2, 735, "自分軸の発見", "似合うスタイルが定まる！", (38, 100, 158), (237, 244, 252))
    draw_card_pill_p(c3_x1, c3_x2, 735, "お金と時間の自由", "貯金も節約も自然に成功！", (191, 50, 40), (252, 238, 235))

    # Bottom 5 Mindsets Card (y: 885 to 1115)
    draw.rounded_rectangle((c1_x1, 885, c3_x2, 1115), 32, fill=(255, 255, 255, 252), outline=(215, 139, 66), width=4)
    draw.rounded_rectangle((c1_x1 + 6, 891, c3_x2 - 6, 946), 22, fill=(215, 139, 66))
    draw_text_with_stroke(draw, (SIZE // 2, 918), "クローゼットの迷いを断ち切る「3秒で手放す5つの思考」", 24, "white", stroke_fill="#D78B42", stroke_width=0)

    col1_x = c1_x1 + 28
    col2_x = SIZE // 2 + 10
    draw.text((col1_x, 978), "1.「いつか着る」", font=font(18, bold=True), fill="#BF3228", anchor="lm")
    draw.text((col1_x + 165, 978), "→ いつかは来ない。いまの自分を喜ばせる服だけ残す", font=font(15, bold=False), fill="#2C3E50", anchor="lm")
    draw.text((col1_x, 1028), "2.「正しく処分」", font=font(18, bold=True), fill="#BF3228", anchor="lm")
    draw.text((col1_x + 165, 1028), "→ 小銭稼ぎより、人生の時間と心の自由を取り戻す", font=font(15, bold=False), fill="#2C3E50", anchor="lm")
    draw.text((col1_x, 1078), "3.「複数重複」", font=font(18, bold=True), fill="#BF3228", anchor="lm")
    draw.text((col1_x + 165, 1078), "→ 内側の魅力は服を減らしても1ミリも奪われない", font=font(15, bold=False), fill="#2C3E50", anchor="lm")

    draw.text((col2_x, 990), "4.「高かったから」", font=font(18, bold=True), fill="#BF3228", anchor="lm")
    draw.text((col2_x + 185, 990), "→ 過去の出費に囚われず、今の快適さを選ぶ", font=font(15, bold=False), fill="#2C3E50", anchor="lm")
    draw.text((col2_x, 1055), "5.「思い出の服」", font=font(18, bold=True), fill="#BF3228", anchor="lm")
    draw.text((col2_x + 185, 1055), "→ 大切な記憶は布ではなく心の中にある", font=font(15, bold=False), fill="#2C3E50", anchor="lm")

    # Bottom Signboard (y: 1135 to 1242)
    draw.rounded_rectangle((c1_x1 + 30, 1136, c3_x2 - 30, 1242), 26, fill=(255, 248, 238), outline=(125, 78, 38), width=4)
    draw.rounded_rectangle((c1_x1 + 38, 1144, c3_x2 - 38, 1234), 20, fill=(255, 245, 229), outline=(201, 148, 88), width=2)
    draw_text_with_stroke(draw, (SIZE // 2, 1189), "まずは今日、着ていない1着を手放してみる。", 36, "#1E2A38", stroke_fill="white", stroke_width=4, mincho=True)

    target = OUT / "服捨て_個人アカウント用.png"
    canvas.convert("RGB").save(target, format="PNG", quality=98)
    print("Personal masterpiece saved:", target)

if __name__ == "__main__":
    render_studio()
    render_personal()
