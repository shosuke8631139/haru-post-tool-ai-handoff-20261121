from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

ROOT = Path(r"C:\Users\kurro\.gemini\antigravity\scratch\haru-post-tool-ai-handoff-20261121")
OUT = ROOT / "outputs"
BASE_PATH = r"C:\Users\kurro\.gemini\antigravity\brain\ddf0d915-c14e-4824-bb8a-3fe210f00490\.user_uploaded\media_1795474119289_a9fbccd4.jpg"

im = Image.open(BASE_PATH).convert("RGBA")
draw = ImageDraw.Draw(im)

FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"

def font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)

NAVY = "#17263A"
WHITE = "#FFFFFF"

# 1. メインタイトルの背景を白/金グラデーションプレートで覆う
title_bg = Image.new("RGBA", (580, 155), (255, 252, 245, 248))
t_draw = ImageDraw.Draw(title_bg)
t_draw.rounded_rectangle((0, 0, 580, 155), 28, fill=(255, 252, 245, 250), outline="#E5A93C", width=3)
im.paste(title_bg, (275, 135), title_bg)

draw = ImageDraw.Draw(im)

# タイトル描画
draw.text((565, 180), "グレートライフ", font=font(44, True), fill=NAVY, anchor="mm", stroke_width=2, stroke_fill="white")
draw.text((455, 240), "6", font=font(64, True), fill="#E05275", anchor="mm", stroke_width=4, stroke_fill="white")
draw.text((585, 242), "つの魔法", font=font(46, True), fill="#1E5084", anchor="mm", stroke_width=3, stroke_fill="white")

# 2. サブ帯の更新
draw.rounded_rectangle((115, 296, 905, 344), 16, fill="#1B2B44")
draw.text((510, 320), "一度きりの人生！自分らしく最高に輝く6つのルール", font=font(22, True), fill="#FFE49E", anchor="mm")

# 3. カード01〜06のテキストパネル更新
cards_info = [
    (15, 350, "01", "主人公になろう！", "他人の目や受け身を卒業！", "望む未来の脚本を自ら描く", "#E05275"),
    (515, 350, "02", "すぐ第一歩を踏み出す！", "完璧なタイミングを待たない！", "残された時間でワクワクへ挑戦", "#2A8A7A"),
    (15, 505, "03", "言い訳をポイッと排除！", "「できない・時間ない」をポイ！", "前向きな信念へアップデート", "#3B70A2"),
    (515, 505, "04", "何歳でも新しい始まり！", "「もう遅い」なんて絶対にない！", "今日が残りの人生で一番若い日", "#D28D2B"),
    (15, 660, "05", "大好きな人と生きる！", "愚痴や悪影響の縁を手放す！", "高め合える仲間と笑顔の時間", "#8A4FB5"),
    (515, 660, "06", "シンプルなお金の計画！", "収入10%先取り＆不用品ゼロ！", "身軽な暮らしで経済的自由へ", "#E05275"),
]

for x, y, num, title, sub1, sub2, accent in cards_info:
    card_bg = Image.new("RGBA", (345, 132), (255, 252, 245, 248))
    cb_draw = ImageDraw.Draw(card_bg)
    cb_draw.rounded_rectangle((0, 0, 345, 132), 16, fill=(255, 252, 245, 250))
    im.paste(card_bg, (x + 8, y + 8), card_bg)

    cd = ImageDraw.Draw(im)
    cd.rounded_rectangle((x + 14, y + 14, x + 82, y + 54), 18, fill=accent)
    cd.text((x + 48, y + 34), num, font=font(24, True), fill=WHITE, anchor="mm")
    cd.text((x + 92, y + 34), title, font=font(26, True), fill=NAVY, anchor="lm")
    cd.text((x + 24, y + 78), sub1, font=font(19, True), fill="#2C3E50", anchor="lm")
    cd.text((x + 24, y + 110), sub2, font=font(19, True), fill="#4A5568", anchor="lm")

# 4. 下部看板「今日から」と「結論」
draw.rectangle((82, 855, 315, 975), fill=(255, 252, 245, 245))
draw.text((95, 875), "☑ 望みノートを1行書く", font=font(17, True), fill=NAVY, anchor="lm")
draw.text((95, 915), "☑ 部屋の不用品を1つ処分", font=font(17, True), fill=NAVY, anchor="lm")
draw.text((95, 955), "☑ 収入の10%先取り貯蓄", font=font(17, True), fill=NAVY, anchor="lm")

draw.rectangle((360, 855, 715, 980), fill=(255, 252, 245, 245))
draw.text((375, 882), "人生の主人公はあなた！他人に脚本を渡さず、", font=font(16, True), fill=NAVY, anchor="lm")
draw.text((375, 918), "今日から望むストーリーを自ら描こう！", font=font(17, True), fill="#C93B2B", anchor="lm")
draw.text((375, 954), "最高のステージへ、一緒に踊り出そう！", font=font(18, True), fill=NAVY, anchor="lm")

out_file = OUT / "グレートライフ_ダンススタジオ用.png"
im.convert("RGB").save(out_file, quality=95)
print(f"Studio poster generated: {out_file}")
