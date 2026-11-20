from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

INTRODUCTIONS = {
    "科学的な適職_投稿セット.md": "今回ご紹介したいのは、鈴木祐さんの『新版 科学的な適職』です。",
    "君だけの人生_投稿セット.md": "今回ご紹介したいのは、伊藤羊一さんの『君は、君だけの人生を歩め』です。",
    "自分軸習慣_投稿セット.md": "今回ご紹介したいのは、一番ケ瀬瑶子さんの『「やるべきこと」に追われない 自分軸習慣』です。",
    "それって必要_投稿セット.md": "今回ご紹介したいのは、筆子さんの『それって、必要？』です。",
    "引き算思考_投稿セット.md": "今回ご紹介したいのは、ミニマリストTakeruさんの『人生は「引き算」で軽くなる』です。",
}


def update_section(text: str, heading: str, intro: str) -> str:
    pattern = rf"(^## {re.escape(heading)}\s*$\n)\s*(?:今回(?:ご)?紹介(?:する本|したいの)は、[^\n]+です。\s*)?"
    return re.sub(pattern, rf"\1\n{intro}\n\n", text, count=1, flags=re.MULTILINE)


for filename, intro in INTRODUCTIONS.items():
    path = ROOT / "outputs" / filename
    text = path.read_text(encoding="utf-8")
    text = update_section(text, "長文投稿", intro)
    text = update_section(text, "約500文字投稿", intro)
    path.write_text(text, encoding="utf-8")
    print(filename)
