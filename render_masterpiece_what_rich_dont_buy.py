import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(r"C:\Users\kurro\.gemini\antigravity\scratch\haru-post-tool-ai-handoff-20261121")
OUT = ROOT / "outputs"

FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"
FONT_M = r"C:\Windows\Fonts\BIZ-UDMinchoM.ttc"


def get_font(size, bold=True, mincho=False):
    if mincho:
        return ImageFont.truetype(FONT_M, size)
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def draw_stroked_text(
    draw, xy, text, size, fill, stroke_fill="white", stroke_width=3, bold=True, mincho=False, anchor="mm", align="center", spacing=4
):
    f = get_font(size, bold=bold, mincho=mincho)
    draw.multiline_text(
        xy, text, font=f, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill, anchor=anchor, align=align, spacing=spacing
    )


CARDS_CONFIG = [
    {
        "num": "01",
        "title": "立派すぎる葬儀",
        "badge_color": (201, 42, 42),
        "sub": "世間体や見栄を排除！",
        "sub_bg": (255, 235, 235),
        "sub_fg": "#C92A2A",
        "body": "・過剰な祭壇・生前墓地はNG\n・シンプルな家族葬で十分\n・事前相談で適正プラン決定",
        "icon": ROOT / "icon_rule_1.png",
    },
    {
        "num": "02",
        "title": "大手新築一戸建て",
        "badge_color": (43, 138, 62),
        "sub": "買った瞬間に2割下落！",
        "sub_bg": (235, 251, 238),
        "sub_fg": "#2B8A3E",
        "body": "・莫大なCM費・ブランド料回避\n・35年ローン地獄を抜け出す\n・価値の落ちない中古や賃貸",
        "icon": ROOT / "icon_rule_2.png",
    },
    {
        "num": "03",
        "title": "高額情報教材",
        "badge_color": (25, 113, 194),
        "sub": "不安につけ込む商材NG！",
        "sub_bg": (231, 245, 255),
        "sub_fg": "#1971C2",
        "body": "・高額教材を買っても稼げない\n・不安の解消はお金で買えない\n・千円の良書と本業の実務",
        "icon": ROOT / "icon_rule_3.png",
    },
    {
        "num": "04",
        "title": "孤独を埋める消費",
        "badge_color": (134, 46, 156),
        "sub": "夜の街・過剰課金をゼロに",
        "sub_bg": (243, 217, 250),
        "sub_fg": "#862E9C",
        "body": "・他人の承認はお金で買えない\n・買った関係は虚無しか残らない\n・本当の仲間と豊かな時間",
        "icon": ROOT / "icon_rule_4.png",
    },
    {
        "num": "05",
        "title": "不要な民間保険",
        "badge_color": (217, 72, 15),
        "sub": "不安任せの特約は即解約！",
        "sub_bg": (255, 232, 204),
        "sub_fg": "#D9480F",
        "body": "・高額療養費制度があるから安心\n・自己負担上限を理解して防衛\n・浮いた固定費を投資へ回す",
        "icon": ROOT / "icon_rule_5.png",
    },
    {
        "num": "06",
        "title": "搾取宝くじ",
        "badge_color": (194, 37, 92),
        "sub": "還元率46%の愚か者の税金",
        "sub_bg": (255, 222, 235),
        "sub_fg": "#C2255C",
        "body": "・胴元が半分抜く超搾取ゲーム\n・期待値マイナスに1円も出さない\n・新NISAでインデックス投資",
        "icon": ROOT / "icon_rule_6.png",
    },
]


def render_infographic(is_studio=False):
    base_file = "1億円貯める方法_ダンススタジオ用.png" if is_studio else "1億円貯める方法_個人アカウント用.png"
    im = Image.open(OUT / base_file).convert("RGBA")

    # 1. RETOUCH TITLE PLATE
    # Precise bounding box to completely cover legacy text
    tx1 = 260 if is_studio else 230
    tx2 = 1040 if is_studio else 1025
    ty1 = 15
    ty2 = 345
    t_w = tx2 - tx1
    t_h = ty2 - ty1

    title_patch = Image.new("RGBA", (t_w, t_h), (0, 0, 0, 0))
    tp_draw = ImageDraw.Draw(title_patch)

    # Rich wooden parchment signboard
    tp_draw.rounded_rectangle((4, 4, t_w - 5, t_h - 5), 28, fill=(255, 250, 242, 255), outline=(195, 145, 45), width=5)
    tp_draw.rounded_rectangle((12, 12, t_w - 13, t_h - 13), 22, fill=(255, 253, 247, 255), outline=(245, 220, 140), width=2)
    im.alpha_composite(title_patch, (tx1, ty1))
    draw = ImageDraw.Draw(im)

    cx = (tx1 + tx2) // 2

    # Top red tag
    top_badge_text = "上位1%の養分にならない！生活防衛の鉄則" if is_studio else "上位1%の養分になるな！資本主義の生活防衛"
    draw_stroked_text(draw, (cx, ty1 + 48), top_badge_text, 25, "#B91C1C", stroke_fill="white", stroke_width=3, bold=True)

    # Main Big Title
    f_main = get_font(46, bold=True, mincho=True)
    seg1 = "金持ちが "
    seg2 = "「絶対買わない」"
    seg3 = " もの"
    w1 = f_main.getlength(seg1)
    w2 = f_main.getlength(seg2)
    w3 = f_main.getlength(seg3)
    total_w = w1 + w2 + w3
    start_x = cx - total_w / 2.0
    cy_main = ty1 + 106

    draw.text((start_x, cy_main), seg1, font=f_main, fill="#182638", stroke_width=6, stroke_fill="white", anchor="lm")
    draw.text((start_x + w1, cy_main), seg2, font=f_main, fill="#C92A2A", stroke_width=6, stroke_fill="white", anchor="lm")
    draw.text((start_x + w1 + w2, cy_main), seg3, font=f_main, fill="#182638", stroke_width=6, stroke_fill="white", anchor="lm")

    # Subtitle Ribbon
    draw_stroked_text(draw, (cx, ty1 + 172), "6つの黄金ルール", 40, "#D97706", stroke_fill="white", stroke_width=5, bold=True, mincho=True)

    # Bottom dark navy ribbon
    ribbon_box = (tx1 + 18, ty1 + 230, tx2 - 18, ty1 + 284)
    draw.rounded_rectangle(ribbon_box, 16, fill=(18, 35, 58), outline=(218, 165, 32), width=2)
    bottom_ribbon_text = "身軽さこそ最強のパフォーマンス！生活防衛＆身軽ライフ" if is_studio else "知っている人だけが得をする！資本主義の生活防衛ルート"
    draw_stroked_text(draw, (cx, ty1 + 257), bottom_ribbon_text, 20, "#FFDF73", stroke_fill="#12233A", stroke_width=1, bold=True)

    # 2. RENDER THE 6 CARDS
    # Continuous coverage to eliminate any gap line
    col_bounds = [(20, 420), (426, 826), (832, 1232)]

    f_title = get_font(24, bold=True)
    f_badge = get_font(20, bold=True)
    f_sub = get_font(17, bold=True)
    f_body = get_font(16, bold=True)

    for i, cfg in enumerate(CARDS_CONFIG):
        row = i // 3
        col = i % 3
        x1, x2 = col_bounds[col]
        # Row 0: y=346..742, Row 1: y=742..1024
        y1, y2 = (346, 742) if row == 0 else (742, 1024)
        w = x2 - x1
        h = y2 - y1

        patch = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        p_draw = ImageDraw.Draw(patch)

        # Parchment background fill with clean border
        p_draw.rounded_rectangle((0, 0, w - 1, h - 1), 20, fill=(255, 251, 242, 255), outline=(180, 140, 90), width=2)
        p_draw.rounded_rectangle((4, 4, w - 5, h - 5), 16, fill=(255, 253, 247, 255))

        # Badge
        badge_r = 20
        badge_cx, badge_cy = 32, 28
        p_draw.ellipse((badge_cx - badge_r, badge_cy - badge_r, badge_cx + badge_r, badge_cy + badge_r), fill=cfg["badge_color"])
        p_draw.text((badge_cx, badge_cy), cfg["num"], font=f_badge, fill="white", anchor="mm")

        # Title
        p_draw.text((62, badge_cy), cfg["title"], font=f_title, fill="#1A1A1A", anchor="lm")

        # Sub highlight
        p_draw.rounded_rectangle((10, 56, w - 10, 86), 8, fill=cfg["sub_bg"], outline=(230, 190, 190), width=1)
        p_draw.text((w // 2, 71), cfg["sub"], font=f_sub, fill=cfg["sub_fg"], anchor="mm")

        if row == 0:
            # Row 0: Body text in upper area
            p_draw.multiline_text((20, 98), cfg["body"], font=f_body, fill="#2B2B2B", spacing=6)

            # Icon centered at bottom
            if cfg["icon"].exists():
                icon = Image.open(cfg["icon"]).convert("RGBA")
                ratio = min(350 / icon.width, 185 / icon.height)
                icon_res = icon.resize((round(icon.width * ratio), round(icon.height * ratio)), Image.Resampling.LANCZOS)
                ix = (w - icon_res.width) // 2
                iy = h - icon_res.height - 10
                patch.alpha_composite(icon_res, (ix, iy))
        else:
            # Row 1: Left body text, Right icon
            p_draw.multiline_text((14, 98), cfg["body"], font=get_font(15, bold=True), fill="#2B2B2B", spacing=6)

            if cfg["icon"].exists():
                icon = Image.open(cfg["icon"]).convert("RGBA")
                ratio = min(180 / icon.width, 160 / icon.height)
                icon_res = icon.resize((round(icon.width * ratio), round(icon.height * ratio)), Image.Resampling.LANCZOS)
                ix = w - icon_res.width - 8
                iy = h - icon_res.height - 12
                patch.alpha_composite(icon_res, (ix, iy))

        im.alpha_composite(patch, (x1, y1))

    # 3. RETOUCH WOODEN BOARD (x: 65..415, y: 1070..1225)
    # Upper area (avoiding pen tip, covering '見直し' completely)
    wb_patch1 = Image.new("RGBA", (270 if is_studio else 285, 80), (255, 248, 235, 255))
    im.alpha_composite(wb_patch1, (65, 1070))
    # Bottom area extending to x=415 to cover '自動積立' completely
    wb_patch2 = Image.new("RGBA", (350, 80), (255, 248, 235, 255))
    im.alpha_composite(wb_patch2, (65, 1145))
    draw = ImageDraw.Draw(im)

    checklist_items = [
        "不要な民間保険を即解約",
        "固定費・不要サブスク削減",
        "新NISAで自動積立を設定",
    ]
    f_check = get_font(18, bold=True)
    f_cb = get_font(20, bold=True)
    for idx, item in enumerate(checklist_items):
        cy = 1104 + idx * 42
        draw.text((82, cy), "☑", font=f_cb, fill="#B91C1C", anchor="mm")
        draw.text((104, cy), item, font=f_check, fill="#1A1A1A", anchor="lm")

    # 4. RETOUCH CONCLUSION SCROLL
    # Left area under '結論' ribbon
    sc_patch1 = Image.new("RGBA", (110, 140), (255, 248, 235, 255))
    im.alpha_composite(sc_patch1, (460, 1085))

    # Right area extending to bankbook to cover entire text and '器。'
    sc_patch2 = Image.new("RGBA", (475, 170), (255, 248, 235, 255))
    im.alpha_composite(sc_patch2, (560, 1055))
    draw = ImageDraw.Draw(im)

    concl_text = (
        "「買わない決断」とはケチではなく、\n資本主義の理不尽な搾取から解放され、\n人生の主導権を取り戻す最大の武器。"
    )
    f_concl = get_font(22, bold=True, mincho=False)
    draw.multiline_text((495, 1146), concl_text, font=f_concl, fill="#681515", anchor="lm", spacing=8)

    # Save output
    out_name = "金持ちが絶対買わないもの_ダンススタジオ用.png" if is_studio else "金持ちが絶対買わないもの_個人アカウント用.png"
    out_path = OUT / out_name
    im.save(out_path, "PNG")
    print(f"Generated masterpiece infographic: {out_path}")


if __name__ == "__main__":
    render_infographic(is_studio=False)
    render_infographic(is_studio=True)
