import os
from pathlib import Path
from PIL import Image

ROOT = Path(r"C:\Users\kurro\.gemini\antigravity\scratch\haru-post-tool-ai-handoff-20261121")
BRAIN = Path(r"C:\Users\kurro\.gemini\antigravity\brain\37b73ff8-3d00-4627-bc53-b533c97e2644")

p_studio = BRAIN / "fukusute_6_habits_infographic_1795311698433.jpg"
p_personal = BRAIN / "fukusute_6_habits_infographic_v2_1795311700281.jpg"

im_studio = Image.open(p_studio)
im_personal = Image.open(p_personal)

out_studio = ROOT / "outputs" / "服捨て_ダンススタジオ用.png"
out_personal = ROOT / "outputs" / "服捨て_個人アカウント用.png"

im_studio.resize((1254, 1254), Image.LANCZOS).save(out_studio, format="PNG")
im_personal.resize((1254, 1254), Image.LANCZOS).save(out_personal, format="PNG")

print(f"Saved Studio Infographic: {out_studio} ({out_studio.stat().st_size} bytes)")
print(f"Saved Personal Infographic: {out_personal} ({out_personal.stat().st_size} bytes)")
