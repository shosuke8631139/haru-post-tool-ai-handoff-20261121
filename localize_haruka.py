import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

base_path = r"C:\Users\kurro\.gemini\antigravity\brain\ddf0d915-c14e-4824-bb8a-3fe210f00490\haruka_trio_rich_dont_buy_fresh_composition_final_1795473389385.jpg"
im = Image.open(base_path).convert("RGBA")

FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"

def font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)

def fill_rect(box, bg_color=(255, 255, 255, 255), radius=6):
    x1, y1, x2, y2 = box
    mask = Image.new("L", (x2 - x1, y2 - y1), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle((1, 1, x2 - x1 - 1, y2 - y1 - 1), radius=radius, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1))
    patch = Image.new("RGBA", (x2 - x1, y2 - y1), bg_color)
    im.paste(patch, (x1, y1), mask)

# 1. メインタイトル (上部)
fill_rect((70, 42, 955, 160), bg_color=(245, 250, 255, 250), radius=14)
d = ImageDraw.Draw(im)
d.text((512, 85), "金持ちが「絶対買わない」もの", font=font(46), fill="#111827", anchor="mm")
d.text((512, 132), "知っている人だけが得をする！６つの黄金ルール", font=font(24), fill="#E11D48", anchor="mm")

# 2. カード01 (立派すぎる葬儀)
fill_rect((38, 320, 168, 395))
fill_rect((178, 320, 292, 395))
d = ImageDraw.Draw(im)
d.text((103, 355), "シンプル供養\nで十分安心", font=font(14), fill="#1F2937", anchor="mm", align="center")
d.text((235, 355), "見栄の\n豪華祭壇", font=font(14), fill="#1F2937", anchor="mm", align="center")

# 3. カード02 (大手新築戸建て)
fill_rect((38, 545, 168, 620))
fill_rect((178, 545, 292, 620))
d = ImageDraw.Draw(im)
d.text((103, 580), "身軽な\n賃貸・リノベ", font=font(14), fill="#1F2937", anchor="mm", align="center")
d.text((235, 580), "35年ローン\n新築縛り", font=font(14), fill="#1F2937", anchor="mm", align="center")

# 4. カード03 (高額情報教材)
fill_rect((38, 765, 168, 840))
fill_rect((178, 765, 292, 840))
d = ImageDraw.Draw(im)
d.text((103, 800), "千円の良書\n＋本業実践", font=font(14), fill="#1F2937", anchor="mm", align="center")
d.text((235, 800), "不安を煽る\n高額情報商材", font=font(14), fill="#1F2937", anchor="mm", align="center")

# 5. カード04 (孤独を埋める消費) - x: 975 まで広げる
fill_rect((730, 320, 845, 395))
fill_rect((848, 320, 975, 405))
d = ImageDraw.Draw(im)
d.text((787, 355), "ほっこり\nお茶で団らん", font=font(14), fill="#1F2937", anchor="mm", align="center")
d.text((907, 355), "見栄の浪費\n過剰な夜遊び", font=font(14), fill="#1F2937", anchor="mm", align="center")

# 6. カード05 (高額な民間保険) - x: 975, y: 645 まで広げる
fill_rect((725, 545, 845, 645))
fill_rect((848, 545, 975, 645))
# 保険証の「HEALTH」を青色で優しく消去
fill_rect((752, 470, 810, 495), bg_color=(125, 185, 215, 255), radius=3)
d = ImageDraw.Draw(im)
d.text((781, 482), "保険証", font=font(11), fill="white", anchor="mm")
d.text((785, 582), "公的保険\n＋生活防衛資金", font=font(13), fill="#1F2937", anchor="mm", align="center")
d.text((908, 582), "過剰な特約\n民間保険", font=font(14), fill="#1F2937", anchor="mm", align="center")

# 7. カード06 (愚か者の税金・宝くじ) - x: 975, y: 865 まで広げる
fill_rect((725, 765, 845, 865))
fill_rect((848, 765, 975, 865))
d = ImageDraw.Draw(im)
d.text((785, 802), "新NISA\n自動積立", font=font(14), fill="#1F2937", anchor="mm", align="center")
d.text((908, 802), "期待値マイナス\n宝くじ", font=font(14), fill="#1F2937", anchor="mm", align="center")

# 8. 下部チェックリスト
fill_rect((365, 875, 650, 990), bg_color=(255, 255, 255, 255), radius=8)
d = ImageDraw.Draw(im)
d.text((395, 905), "☑  無駄な固定費を即解約", font=font(16), fill="#1F2937", anchor="lm")
d.text((395, 937), "☑  千円の良書で小さく学ぶ", font=font(16), fill="#1F2937", anchor="lm")
d.text((395, 969), "☑  新NISAでコツコツ自動積立", font=font(16), fill="#1F2937", anchor="lm")

# 9. 右下リボン
fill_rect((640, 895, 970, 975), bg_color=(244, 114, 114, 255), radius=12)
d = ImageDraw.Draw(im)
d.text((805, 924), "「買わない決断」こそ", font=font(20), fill="white", stroke_width=2, stroke_fill="#991B1B", anchor="mm")
d.text((805, 954), "自由を取り戻す最大の武器！", font=font(20), fill="white", stroke_width=2, stroke_fill="#991B1B", anchor="mm")

out_path = r"C:\Users\kurro\.gemini\antigravity\brain\ddf0d915-c14e-4824-bb8a-3fe210f00490\haruka_trio_fresh_japanese.png"
im.convert("RGB").save(out_path, quality=95)
print("Saved 100% clean Japanese studio infographic to", out_path)
