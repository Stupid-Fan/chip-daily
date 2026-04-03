#!/usr/bin/env python3
"""Generate chip daily image for 3/25-3/28 2026"""

from PIL import Image, ImageDraw, ImageFont
import textwrap

FONT_REG  = "/workspace/fonts/NotoSansCJK.otf"
FONT_BOLD = "/workspace/fonts/NotoSansCJK-Bold.otf"

W   = 960
BG  = (252, 248, 238)
INK = (20, 18, 14)
RULE_COLOR = (80, 70, 55)
ACCENT = (180, 20, 20)
GOLD   = (160, 120, 0)

def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)

def wrap_draw(d, text, x, y, max_w, fnt, color=INK, line_gap=5):
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        bb = d.textbbox((0, 0), test, font=fnt)
        if bb[2] - bb[0] > max_w and current:
            lines.append(current)
            current = ch
        else:
            current = test
    if current:
        lines.append(current)
    for line in lines:
        d.text((x, y), line, font=fnt, fill=color)
        bb = d.textbbox((0, 0), line, font=fnt)
        y += (bb[3] - bb[1]) + line_gap
    return y

# ── News content ──────────────────────────────────────────────────────────────

sections = [
    {
        "tag": "🔴 頭版頭條",
        "color": ACCENT,
        "items": [
            (
                "Arm 發表首款 AI 資料中心晶片：搶進兆元半導體市場，年營收上看150億美元",
                "Arm 正式宣布推出首款自有品牌 AI 資料中心 CPU 晶片，股價隨即飆漲，市場預估此舉將使 Arm 年營收衝上 150 億美元規模。分析師指出，Arm 此舉直接挑戰 Intel、AMD 在資料中心的霸主地位，也強化其在 AI 半導體兆元商機中的戰略卡位。",
                "經濟日報 · 科技島 · 3/27"
            ),
            (
                "美國會推《晶片安全法》：阻斷 AI 晶片走私中國，衝擊全球半導體版圖",
                "美國眾議院委員會推進《晶片安全法》，明確授權政府阻斷 AI 晶片非法流向中國。法案通過後將強化出口管制執法，商傳媒分析此舉恐引發全球半導體供應鏈重組，台灣 AI 伺服器廠商合規壓力同步升高。",
                "商傳媒 · IndexBox · 3/27"
            ),
        ]
    },
    {
        "tag": "💾 記憶體戰場",
        "color": (30, 100, 180),
        "items": [
            (
                "Google TurboQuant 震撼記憶體股：分析師逆勢喊「逢低買進」",
                "Google 發布 TurboQuant 量化壓縮技術，市場擔憂 HBM 記憶體需求可能受衝擊，帶動記憶體概念股短線重挫。然而多位分析師指出，AI 長期推論需求仍強勁，建議趁回調逢低布局，SK Hynix 等 HBM 龍頭受惠預期依然不變。",
                "South China Morning Post · 3/26"
            ),
            (
                "SK 海力士赴美上市：籌資擴產 AI 記憶體，搶攻 HBM 全球龍頭地位",
                "SK 海力士正式向美國提交上市申請，擬借助美股市場籌集資金，用於擴大 AI 晶片所需 HBM 高頻寬記憶體產能。日經亞洲報導，此舉顯示記憶體廠商對 AI 算力長週期需求信心強烈，也反映韓美半導體合作深化趨勢。",
                "Nikkei Asia · 3/25"
            ),
        ]
    },
    {
        "tag": "🌏 地緣政治",
        "color": (140, 60, 0),
        "items": [
            (
                "防堵 AI 晶片外流：美國新立法強化管制，台灣 AI 伺服器供應鏈首當其衝",
                "美國多項立法持續收緊 AI 晶片出口管制。DIGITIMES 與商周分析指出，台灣 AI 伺服器業者在轉口貿易合規審查上面臨更嚴格要求，鴻海、廣達、緯創等主要代工廠均需建立更完整的端到端溯源機制以符合新規。",
                "商傳媒 · DIGITIMES · 3/27"
            ),
            (
                "中國成熟製程晶片 2028 年將占全球 42%：AI 熱潮加速本土擴產",
                "TechNews 科技新報引述最新研究，在 AI 算力需求帶動下，中國大陸積極擴張成熟製程（28nm+）產能，預估 2028 年市占率將達 42%，形成對歐美日台晶片廠商的長期競爭壓力，半導體設備出口管制的政策效果備受考驗。",
                "TechNews · PChome · 3/26"
            ),
        ]
    },
    {
        "tag": "🏭 產業動態",
        "color": GOLD,
        "items": [
            (
                "日月光攜手楠梓電合建廠房：擴大 AI 先進封測產能，搶抓 CoWoS 訂單",
                "TechNews 科技新報報導，日月光投控與楠梓電子簽署合作備忘錄，雙方將合建廠房、共同擴大 AI 晶片先進封測產能。此舉被視為日月光積極搶進台積電 CoWoS 先進封裝生態系、強化 AI 供應鏈地位的重要布局。",
                "TechNews 科技新報 · 3/26"
            ),
            (
                "阿里巴巴發布 AI 代理專用晶片：自研能力大躍進，應對算力瓶頸",
                "科技島報導，阿里巴巴正式推出針對 AI Agent（代理）任務優化的自研晶片，強調可顯著降低大型語言模型推論成本並提升效率。此舉凸顯中國科技巨頭在美國出口管制壓力下加速晶片自給自足的戰略意圖。",
                "科技島 · 3/25"
            ),
            (
                "AI 狂潮重塑半導體業：全球市值前 25 大企業中，半導體股攻佔 7 席",
                "經濟日報深度分析，輝達帶動的 AI 晶片浪潮已根本改變全球股市生態。目前全球市值前 25 大企業中有 7 席由半導體公司把持，創下歷史記錄，顯示資本市場對 AI 算力長期需求的高度信心，台積電、輝達、博通等均名列其中。",
                "經濟日報 · 3/26"
            ),
        ]
    },
]

# ── Estimate height ───────────────────────────────────────────────────────────
def estimate_h():
    h = 40   # top margin
    h += 90  # masthead
    h += 14  # double rule
    h += 36  # date bar
    h += 14  # rule
    h += 16  # gap
    for sec in sections:
        h += 38  # section header
        h += 10
        for title, body, src in sec["items"]:
            # title: ~17px per line, ~50 chars/line
            title_lines = max(1, len(title) // 22 + 1)
            h += title_lines * 22 + 6
            body_lines = max(1, len(body) // 45 + 1)
            h += body_lines * 19 + 4
            src_h = 20
            h += src_h + 18  # item gap
        h += 20  # section gap
    h += 60  # footer
    return h

H = estimate_h()
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

y = 40

# ── Masthead ──────────────────────────────────────────────────────────────────
title_text = "晶  片  日  報"
tf = font(62, bold=True)
bb = d.textbbox((0, 0), title_text, font=tf)
tx = (W - (bb[2] - bb[0])) // 2
d.text((tx, y), title_text, font=tf, fill=INK)
sub_f = font(13)
sub_text = "Semiconductor & AI Chip Intelligence  ·  Taiwan Edition"
bb2 = d.textbbox((0, 0), sub_text, font=sub_f)
d.text(((W - (bb2[2] - bb2[0])) // 2, y + bb[3] - bb[1] + 4), sub_text, font=sub_f, fill=(120, 110, 90))
y += bb[3] - bb[1] + 22

# double rule
d.line([(40, y), (W-40, y)], fill=INK, width=4)
d.line([(40, y+7), (W-40, y+7)], fill=INK, width=1)
y += 14

# date bar
d.rectangle([(40, y), (W-40, y+28)], fill=ACCENT)
df = font(13)
d.text((50, y+6), "📅 2026年3月25日～28日  半導體週報", font=df, fill=(252, 248, 238))
src_txt = "經濟日報 · 商傳媒 · TechNews · DIGITIMES · 科技島"
bb3 = d.textbbox((0, 0), src_txt, font=df)
d.text((W-40 - (bb3[2]-bb3[0]) - 8, y+6), src_txt, font=df, fill=(252, 230, 180))
y += 36

d.line([(40, y), (W-40, y)], fill=INK, width=2)
y += 18

# ── Sections ──────────────────────────────────────────────────────────────────
for sec in sections:
    sec_color = sec["color"]

    # Section header
    sh_f = font(15, bold=True)
    d.rectangle([(40, y), (W-40, y+28)], fill=sec_color)
    bb = d.textbbox((0, 0), f"  {sec['tag']}  ", font=sh_f)
    d.text((52, y+5), f"  {sec['tag']}", font=sh_f, fill=(255, 255, 255))
    y += 34

    for title, body, src in sec["items"]:
        # Title
        tf2 = font(17, bold=True)
        y = wrap_draw(d, title, 52, y, W-100, tf2, color=INK, line_gap=4)
        y += 5

        # Body
        bf = font(13)
        y = wrap_draw(d, body, 60, y, W-110, bf, color=(60, 55, 45), line_gap=4)
        y += 4

        # Source
        sf = font(11)
        d.text((60, y), f"▸ {src}", font=sf, fill=(150, 130, 80))
        y += 18

        # Item divider
        d.line([(52, y), (W-52, y)], fill=(220, 210, 190), width=1)
        y += 10

    y += 14
    d.line([(40, y), (W-40, y)], fill=RULE_COLOR, width=1)
    y += 16

# ── Footer ────────────────────────────────────────────────────────────────────
y += 8
d.line([(40, y), (W-40, y)], fill=INK, width=3)
d.line([(40, y+5), (W-40, y+5)], fill=INK, width=1)
y += 16
ff = font(12)
footer = "🤖 晶片日報  ·  半導體與AI晶片情報  ·  由 OpenClaw 自動生成  ·  2026-03-28"
bb = d.textbbox((0, 0), footer, font=ff)
d.text(((W - (bb[2]-bb[0])) // 2, y), footer, font=ff, fill=(120, 110, 90))

# ── Save ──────────────────────────────────────────────────────────────────────
out = "/workspace/chip_daily_2026_03_28.png"
img.save(out, "PNG", optimize=True)
print(f"Saved: {out}  ({W}x{H}px)")
