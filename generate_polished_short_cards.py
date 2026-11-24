from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

ROOT = Path(r"C:\Users\kurro\.gemini\antigravity\scratch\haru-post-tool-ai-handoff-20261121")
OUT = ROOT / "outputs"

FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"

def font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)

NAVY = "#17263A"
WHITE = "#FFFFFF"

# キャラクター素材の読み込み
char_haruka = Image.open(OUT / "raw_haruka_top.png").convert("RGBA")
char_trio = Image.open(OUT / "raw_haruka_bottom.png").convert("RGBA")
char_flower_cat = Image.open(OUT / "raw_flower_cat.png").convert("RGBA")

char_harumichi = Image.open(OUT / "raw_harumichi_top.png").convert("RGBA")
char_sakura = Image.open(OUT / "raw_sakurajimao_top.png").convert("RGBA")


def draw_studio_card(index, badge, title, catch1, catch2, accent, bg_gradient_color):
    W, H = 940, 940
    card = Image.new("RGBA", (W, H), bg_gradient_color)
    draw = ImageDraw.Draw(card)

    # 1. 外枠と内枠（二重ステッチ風フレーム）
    draw.rounded_rectangle((15, 15, W - 15, H - 15), 44, outline=accent, width=4)
    draw.rounded_rectangle((28, 28, W - 28, H - 28), 34, outline="#FFFFFF", width=3)

    # 2. 上部ヘッダーバッジ
    badge_w = 320
    bx = (W - badge_w) // 2
    draw.rounded_rectangle((bx, 45, bx + badge_w, 115), 35, fill=accent)
    draw.text((W // 2, 80), badge, font=font(30, True), fill="white", anchor="mm")

    # 3. 大見出しタイトル
    draw.text((W // 2, 165), title, font=font(44, True), fill=NAVY, anchor="mm", stroke_width=3, stroke_fill="white")

    # 4. 中央の情景アートプレート（白い角丸キャンバス）
    plate = Image.new("RGBA", (840, 480), (255, 255, 255, 240))
    p_draw = ImageDraw.Draw(plate)
    p_draw.rounded_rectangle((0, 0, 840, 480), 28, fill=(255, 253, 248, 245), outline="#EAD5C3", width=2)

    # カードごとの特大シンボル・イラストの描画
    if index == 1:
        # 日記帳と光るペン
        p_draw.rounded_rectangle((260, 80, 580, 380), 20, fill="#FFF9E6", outline="#D4A359", width=4)
        p_draw.line((420, 80, 420, 380), fill="#D4A359", width=4) # 綴じ目
        p_draw.text((340, 210), "MY\nSTORY", font=font(28, True), fill="#A67838", anchor="mm", align="center")
        p_draw.text((500, 210), "★ 未来の\n　 脚本 ★", font=font(24, True), fill="#D45B72", anchor="mm", align="center")
        # ペン
        p_draw.line((550, 60, 640, 160), fill="#2C818A", width=12)
        p_draw.polygon([(640, 160), (660, 175), (635, 185)], fill="#E5A93C")
    elif index == 2:
        # 虹のステップとスニーカー
        colors = ["#FF6B6B", "#FFA94D", "#FFD43B", "#69DB7C", "#4DABF7", "#748FFC"]
        for i, c in enumerate(colors):
            p_draw.arc((120 + i*20, 60 + i*15, 720 - i*20, 420 - i*15), start=180, end=360, fill=c, width=12)
        p_draw.rounded_rectangle((320, 260, 520, 350), 25, fill="#2C818A")
        p_draw.text((420, 305), "STEP 01 踏み出す！", font=font(22, True), fill="white", anchor="mm")
    elif index == 3:
        # ゴミ箱ダンク＆紙飛行機
        p_draw.polygon([(340, 200), (500, 200), (480, 380), (360, 380)], fill="#868E96")
        p_draw.rectangle((320, 180, 520, 200), fill="#495057")
        p_draw.text((420, 280), "言い訳\nポイッ！", font=font(24, True), fill="white", anchor="mm", align="center")
        # 紙飛行機
        p_draw.polygon([(520, 140), (620, 80), (580, 160)], fill="#339AF0")
    elif index == 4:
        # 輝く太陽と若葉
        p_draw.ellipse((340, 100, 500, 260), fill="#FFA94D", outline="#FFD43B", width=6)
        p_draw.ellipse((360, 120, 480, 240), fill="#FFE066")
        # 若葉
        p_draw.arc((400, 260, 440, 360), 0, 180, fill="#2B8A3E", width=8)
        p_draw.ellipse((410, 280, 460, 320), fill="#51CF66")
        p_draw.text((420, 400), "START! 今日が一番若い日", font=font(24, True), fill="#2B8A3E", anchor="mm")
    elif index == 5:
        # ハイタッチと笑顔の花
        p_draw.ellipse((280, 160, 400, 280), fill="#FFD8A8")
        p_draw.ellipse((440, 160, 560, 280), fill="#FFD8A8")
        p_draw.text((420, 220), "HIGH FIVE!", font=font(32, True), fill="#E03131", anchor="mm")
        p_draw.text((420, 340), "✨ 最高の仲間と笑顔の時間 ✨", font=font(24, True), fill="#A61E4D", anchor="mm")
    elif index == 6:
        # 宝箱と金貨
        p_draw.rounded_rectangle((280, 200, 560, 370), 20, fill="#A67838", outline="#5C3D1E", width=4)
        p_draw.rounded_rectangle((260, 160, 580, 220), 16, fill="#C7953B", outline="#5C3D1E", width=4)
        for cx, cy in [(350, 180), (420, 165), (490, 180), (380, 145), (450, 145)]:
            p_draw.ellipse((cx-24, cy-24, cx+24, cy+24), fill="#FFD43B", outline="#E5A93C", width=3)
            p_draw.text((cx, cy), "¥", font=font(20, True), fill="#A67838", anchor="mm")
        p_draw.text((420, 410), "貯蓄10% & 不用品ゼロ生活！", font=font(24, True), fill="#5C3D1E", anchor="mm")

    # キャラクター配置（左下・右下に配置）
    # 左下にハルちゃん
    h_h = 240
    h_w = int(char_haruka.width * (h_h / char_haruka.height))
    h_res = char_haruka.resize((h_w, h_h), Image.Resampling.LANCZOS)
    plate.alpha_composite(h_res, (20, 480 - h_h))

    # 右下に花ロボ＆鈴猫
    p_h = 170
    p_w = int(char_flower_cat.width * (p_h / char_flower_cat.height))
    p_res = char_flower_cat.resize((p_w, p_h), Image.Resampling.LANCZOS)
    plate.alpha_composite(p_res, (840 - p_w - 20, 480 - p_h - 10))

    card.paste(plate, (50, 220), plate)

    # 5. 下部のメッセージパネル
    c_draw = ImageDraw.Draw(card)
    panel_y = 730
    c_draw.rounded_rectangle((50, panel_y, W - 50, panel_y + 160), 26, fill="#FFFFFF", outline=accent, width=3)
    c_draw.rectangle((50, panel_y, 66, panel_y + 160), fill=accent)
    c_draw.text((W // 2, panel_y + 50), catch1, font=font(34, True), fill=NAVY, anchor="mm")
    c_draw.text((W // 2, panel_y + 110), catch2, font=font(34, True), fill=accent, anchor="mm")

    return card


def draw_personal_card(index, badge, title, catch1, catch2, accent, bg_color):
    W, H = 940, 940
    card = Image.new("RGBA", (W, H), bg_color)
    draw = ImageDraw.Draw(card)

    # 外枠
    draw.rounded_rectangle((15, 15, W - 15, H - 15), 44, outline=accent, width=4)
    draw.rounded_rectangle((28, 28, W - 28, H - 28), 34, outline="#FFFFFF", width=3)

    # バッジ
    badge_w = 320
    bx = (W - badge_w) // 2
    draw.rounded_rectangle((bx, 45, bx + badge_w, 115), 35, fill=accent)
    draw.text((W // 2, 80), badge, font=font(30, True), fill="white", anchor="mm")

    # タイトル
    draw.text((W // 2, 165), title, font=font(44, True), fill=NAVY, anchor="mm", stroke_width=3, stroke_fill="white")

    # 中央プレート
    plate = Image.new("RGBA", (840, 480), (255, 252, 245, 245))
    p_draw = ImageDraw.Draw(plate)
    p_draw.rounded_rectangle((0, 0, 840, 480), 28, fill=(255, 250, 240, 248), outline="#D5C0A0", width=2)

    # 海・航海・冒険のアートワーク
    if index == 1:
        # 航海日誌と羽ペン
        p_draw.rounded_rectangle((260, 80, 580, 380), 18, fill="#FBF4E4", outline="#8C6D3F", width=4)
        p_draw.text((420, 210), "LOGBOOK\n人生の脚本", font=font(30, True), fill="#5C4018", anchor="mm", align="center")
        p_draw.line((540, 60, 630, 160), fill="#B83A4B", width=10)
    elif index == 2:
        # 帆船の船首と羅針盤
        p_draw.ellipse((320, 100, 520, 300), fill="#FFFDF8", outline="#C7953B", width=6)
        p_draw.polygon([(420, 130), (440, 200), (420, 190)], fill="#C93B2B")
        p_draw.polygon([(420, 270), (400, 200), (420, 210)], fill="#1E5084")
        p_draw.text((420, 360), "出航！今すぐ第一歩を踏み出す", font=font(24, True), fill="#1E5084", anchor="mm")
    elif index == 3:
        # 言い訳を海へポイッ
        p_draw.polygon([(340, 220), (500, 220), (480, 380), (360, 380)], fill="#7F8C8D")
        p_draw.text((420, 300), "言い訳\n即廃棄！", font=font(26, True), fill="white", anchor="mm", align="center")
        p_draw.arc((300, 80, 540, 200), 180, 360, fill="#2980B9", width=6)
    elif index == 4:
        # 水平線の朝日
        p_draw.arc((200, 150, 640, 450), 180, 360, fill="#E67E22", width=12)
        p_draw.ellipse((340, 180, 500, 340), fill="#F39C12")
        p_draw.text((420, 390), "今日が残りの人生で一番若い日！", font=font(24, True), fill="#D35400", anchor="mm")
    elif index == 5:
        # 信頼の固い握手
        p_draw.ellipse((300, 150, 540, 320), fill="#EDF2F7", outline="#4A5568", width=4)
        p_draw.text((420, 235), "PARTNERSHIP", font=font(26, True), fill="#2B6CB0", anchor="mm")
        p_draw.text((420, 380), "高め合える仲間との絆に投資する！", font=font(24, True), fill="#2D3748", anchor="mm")
    elif index == 6:
        # 黄金の宝箱と金貨
        p_draw.rounded_rectangle((280, 200, 560, 370), 20, fill="#8C6D3F", outline="#4A3515", width=4)
        for cx, cy in [(350, 175), (420, 160), (490, 175)]:
            p_draw.ellipse((cx-22, cy-22, cx+22, cy+22), fill="#F1C40F", outline="#D4AC0D", width=3)
            p_draw.text((cx, cy), "★", font=font(18, True), fill="#7D6608", anchor="mm")
        p_draw.text((420, 410), "収入10%先取り貯蓄＆不用品ゼロ！", font=font(24, True), fill="#4A3515", anchor="mm")

    # キャラクター配置
    # 左下にさくらじまお
    s_h = 210
    s_w = int(char_sakura.width * (s_h / char_sakura.height))
    s_res = char_sakura.resize((s_w, s_h), Image.Resampling.LANCZOS)
    plate.alpha_composite(s_res, (25, 480 - s_h))

    # 右下にはるみち
    h_h = 250
    h_w = int(char_harumichi.width * (h_h / char_harumichi.height))
    h_res = char_harumichi.resize((h_w, h_h), Image.Resampling.LANCZOS)
    plate.alpha_composite(h_res, (840 - h_w - 20, 480 - h_h))

    card.paste(plate, (50, 220), plate)

    # メッセージパネル
    c_draw = ImageDraw.Draw(card)
    panel_y = 730
    c_draw.rounded_rectangle((50, panel_y, W - 50, panel_y + 160), 26, fill="#FFFFFF", outline=accent, width=3)
    c_draw.rectangle((50, panel_y, 66, panel_y + 160), fill=accent)
    c_draw.text((W // 2, panel_y + 50), catch1, font=font(34, True), fill=NAVY, anchor="mm")
    c_draw.text((W // 2, panel_y + 110), catch2, font=font(34, True), fill=accent, anchor="mm")

    return card

print("Module loaded.")
