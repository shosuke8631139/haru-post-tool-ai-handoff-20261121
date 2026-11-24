import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

base_path = r"C:\Users\kurro\.gemini\antigravity\brain\ddf0d915-c14e-4824-bb8a-3fe210f00490\harumichi_sakurajimao_rich_dont_buy_fresh_composition_1795473372638.jpg"
im = Image.open(base_path).convert("RGBA")

FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"

def font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)

def fill_bubble(box, bg_color=(254, 251, 243, 255), radius=8, outline="#E2D7C3", width=2):
    x1, y1, x2, y2 = box
    mask = Image.new("L", (x2 - x1, y2 - y1), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle((1, 1, x2 - x1 - 1, y2 - y1 - 1), radius=radius, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1))
    patch = Image.new("RGBA", (x2 - x1, y2 - y1), bg_color)
    im.paste(patch, (x1, y1), mask)
    if outline:
        d_im = ImageDraw.Draw(im)
        d_im.rounded_rectangle(box, radius=radius, outline=outline, width=width)

# 1. メイン看板 (上部)
fill_bubble((145, 48, 865, 155), bg_color=(255, 253, 245, 255), radius=12, outline=None)
d = ImageDraw.Draw(im)
d.text((505, 85), "金持ちが「絶対買わない」もの", font=font(44), fill="#3C2114", anchor="mm")
d.text((505, 130), "知っている人だけが得をする！６つの黄金ルール", font=font(22), fill="#6B4B32", anchor="mm")

# 2. カード01
fill_bubble((45, 338, 175, 415), outline=None)
fill_bubble((180, 338, 310, 415), outline=None)
d = ImageDraw.Draw(im)
d.text((110, 372), "シンプル\n供養で十分", font=font(14), fill="#1A1A1A", anchor="mm", align="center")
d.text((245, 372), "立派すぎる\n豪華祭壇", font=font(14), fill="#1A1A1A", anchor="mm", align="center")

# 3. カード02
fill_bubble((45, 538, 175, 615), outline=None)
fill_bubble((180, 538, 310, 615), outline=None)
d = ImageDraw.Draw(im)
d.text((110, 572), "身軽な\n賃貸・中古", font=font(14), fill="#1A1A1A", anchor="mm", align="center")
d.text((245, 572), "35年新築\nローン地獄", font=font(14), fill="#1A1A1A", anchor="mm", align="center")

# 4. カード03
fill_bubble((42, 720, 175, 805), outline=None)
fill_bubble((180, 720, 310, 805), outline=None)
fill_bubble((48, 650, 106, 715), bg_color=(95, 142, 85, 255), radius=4, outline=None)
d = ImageDraw.Draw(im)
d.text((77, 682), "良書", font=font(15), fill="white", anchor="mm")
d.text((108, 755), "千円の良書\n＋本業実務", font=font(14), fill="#1A1A1A", anchor="mm", align="center")
d.text((245, 755), "不安を煽る\n高額情報商材", font=font(14), fill="#1A1A1A", anchor="mm", align="center")

# 5. カード04
fill_bubble((45, 910, 175, 990), outline=None)
fill_bubble((180, 910, 310, 990), outline=None)
d = ImageDraw.Draw(im)
d.text((110, 944), "ほっこり\nお茶で団らん", font=font(14), fill="#1A1A1A", anchor="mm", align="center")
d.text((245, 944), "孤独を埋める\n見栄消費", font=font(14), fill="#1A1A1A", anchor="mm", align="center")

# 6. カード05 (丸角バブル全体を美しい1枚のカードとして下まで包む)
fill_bubble((505, 710, 715, 825), radius=14, outline="#D6C6B0", width=2)
d = ImageDraw.Draw(im)
d.text((559, 755), "公的保険\n＋貯蓄", font=font(14), fill="#1A1A1A", anchor="mm", align="center")
d.text((660, 755), "過剰な特約\n民間保険", font=font(14), fill="#1A1A1A", anchor="mm", align="center")

# 7. カード06 (丸角バブル全体を美しい1枚のカードとして下まで包む)
fill_bubble((730, 710, 955, 825), radius=14, outline="#D6C6B0", width=2)
d = ImageDraw.Draw(im)
d.text((788, 755), "新NISA\n自動積立", font=font(14), fill="#1A1A1A", anchor="mm", align="center")
d.text((898, 755), "愚か者の税金\n宝くじ", font=font(14), fill="#1A1A1A", anchor="mm", align="center")

# 8. 下部木製看板
fill_bubble((342, 805, 652, 975), bg_color=(254, 250, 240, 255), radius=10, outline=None)
d = ImageDraw.Draw(im)
d.text((498, 830), "今日から始める実践", font=font(22), fill="#2C180E", anchor="mm")
d.line((370, 847, 625, 847), fill="#C5A47E", width=2)
d.text((380, 874), "☑  余計な固定費を即解約", font=font(17), fill="#1F2A38", anchor="lm")
d.text((380, 910), "□  千円の良書で小さく学ぶ", font=font(17), fill="#1F2A38", anchor="lm")
d.text((380, 946), "□  新NISAでコツコツ自動積立", font=font(17), fill="#1F2A38", anchor="lm")

# 9. 右下リボン
fill_bubble((680, 840, 985, 965), bg_color=(245, 175, 105, 255), radius=14, outline=None)
d = ImageDraw.Draw(im)
d.text((838, 888), "「買わない決断」こそ", font=font(20), fill="white", stroke_width=2, stroke_fill="#9C4410", anchor="mm")
d.text((838, 924), "自由を取り戻す最大の武器！", font=font(20), fill="white", stroke_width=2, stroke_fill="#9C4410", anchor="mm")

out_path = r"C:\Users\kurro\.gemini\antigravity\brain\ddf0d915-c14e-4824-bb8a-3fe210f00490\harumichi_sakurajimao_fresh_japanese.png"
im.convert("RGB").save(out_path, quality=95)
print("Saved perfect Japanese infographic to", out_path)
