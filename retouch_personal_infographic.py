from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

p_pers = Path(r"C:\Users\kurro\.gemini\antigravity\scratch\haru-post-tool-ai-handoff-20261121\outputs\服捨て_個人アカウント用.png")
im = Image.open(p_pers).convert("RGBA")

# Card background is pale ivory / white, let's sample around bbox
# Card 01 text: [155, 519, 493, 565]
# Card 06 text: [748, 901, 1065, 945]

draw = ImageDraw.Draw(im)

# Clean card 01 text area
bg_color_01 = (255, 253, 248, 255) # Ivory card color
draw.rectangle((152, 518, 495, 566), fill=bg_color_01)

# Clean card 06 text area
bg_color_06 = (255, 253, 248, 255)
draw.rectangle((745, 900, 1065, 945), fill=bg_color_06)

font_path = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
font_01 = ImageFont.truetype(font_path, 21)
font_06 = ImageFont.truetype(font_path, 21)

# Draw clean text with crisp red/brown tone matching the original
text_color_01 = (180, 50, 45, 255) # warm dark red/brown
draw.text((155, 526), "「いま喜ばせる服」だけ残す！", font=font_01, fill=text_color_01)

text_color_06 = (60, 50, 50, 255) # dark text
draw.text((748, 908), "服を減らしても魅力は奪われない", font=font_06, fill=text_color_06)

im.convert("RGB").save(p_pers, quality=95)
print("Personal Infographic retouched cleanly!")
