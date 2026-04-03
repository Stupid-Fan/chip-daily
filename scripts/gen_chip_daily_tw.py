#!/usr/bin/env python3
"""Generate chip daily image for 3/23-3/24 2026"""

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
                "美超微走私案擴大衝擊：美兩黨議員要求凍結輝達AI晶片出口許可",
                "美超微（Super Micro）高管涉嫌非法走私輝達AI晶片至中國事件持續延燒，美國兩黨議員聯手向商務部長施壓，要求暫停所有輝達AI晶片出口許可，防堵非法轉運漏洞。自由財經、Yahoo新聞均跟進報導，此事件引發市場對出口管制執法力道的重新評估。",
                "自由財經 · 信傳媒 · Yahoo新聞 · 3/24"
            ),
            (
                "Arm 聯手 Meta、OpenAI 挑戰 Intel、AMD：首款 AGI CPU 架構大解析",
                "工商時報獨家報導，Arm 正協同 Meta 與 OpenAI 共同開發專為 AGI 設計的 CPU 架構，效能設計與現有 x86 架構截然不同，被視為 Arm 進軍資料中心的重大戰略布局，Intel、AMD 面臨新一波威脅。",
                "工商時報 · 3/24"
            ),
        ]
    },
    {
        "tag": "💾 記憶體戰場",
        "color": (30, 100, 180),
        "items": [
            (
                "美光毛利率74.9%創10年新高！5年長約鎖定AI需求，記憶體盛世還能延續多久？",
                "財訊深度分析，美光最新財報毛利率達 74.9%，創下十年來最高紀錄。AI 訓練與推理對 HBM 高頻寬記憶體的旺盛需求推動業績爆發，多家 AI 巨擘更有意簽訂多年記憶體長約，台灣相關廠商南亞科、華邦電等同步受惠。",
                "財訊 · 經濟日報 · 3/23"
            ),
            (
                "美光財報後震盪：記憶體概念股分化，HBM 設備商悄悄接管戰場",
                "旺得富理財網報導，美光財報發布後市場出現「鬼轉」行情，晶豪科等部分個股吞跌停，但 HBM 設備供應商卻逆勢吸金，顯示市場資金正從傳統記憶體廠轉向上游設備端布局。",
                "旺得富理財網 · 3/24"
            ),
        ]
    },
    {
        "tag": "🌏 地緣政治",
        "color": (140, 60, 0),
        "items": [
            (
                "中國晶片攻堅14奈米：半導體業人士坦言7奈米還遠",
                "鉅亨網報導，全球晶片戰持續升溫，中國半導體業界人士坦言，目前正全力突破14奈米製程，7奈米仍是遠程目標，短期難以挑戰台積電先進製程優勢，出口管制效果仍在發揮。",
                "鉅亨網 · 3/24"
            ),
            (
                "美超微走私案延伸：台灣經濟部回應，AI伺服器非法轉運疑慮升溫",
                "MSN / 台媒報導，美超微涉嫌非法輸出輝達AI伺服器至中國一事，台灣經濟部正式回應，強調將嚴查轉口貿易合規性，業界擔憂後續管制將波及台灣AI伺服器供應鏈。",
                "MSN · DIGITIMES · 3/24"
            ),
        ]
    },
    {
        "tag": "🏭 產業動態",
        "color": GOLD,
        "items": [
            (
                "三星代工2026年罷工危機：景氣翻轉、規模擴三倍，比2024更棘手",
                "DIGITIMES 報導，三星半導體代工部門勞資糾紛再度浮現，2026年罷工規模預估為2024年的三倍，恰逢三星積極爭取輝達等客戶訂單的關鍵時刻，對2nm製程量產進度構成潛在風險。",
                "DIGITIMES · 3/24"
            ),
            (
                "台積電擴產帶動設備商志聖、辛耘需求升溫",
                "工商時報報導，台積電持續擴大先進製程產能，帶動本土設備廠志聖工業、辛耘企業訂單能見度顯著提升，業界預期相關設備商將持續受惠於台積電未來2~3年的資本支出擴張計畫。",
                "工商時報 · 3/24"
            ),
            (
                "台灣高校首座半導體封裝教學產線啟用：亞大攜手矽品培育AI晶片封測人才",
                "商周報導，亞洲大學與矽品精密合作，建置台灣高等教育史上第一座半導體封裝類產線教學基地，針對先進封裝與AI晶片封測需求培育實務人才，填補產學落差。",
                "商周 · 3/24"
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
d.text((50, y+6), "📅 2026年3月23日～24日  半導體雙日報", font=df, fill=(252, 248, 238))
src_txt = "工商時報 · 財訊 · 自由財經 · DIGITIMES · 鉅亨網"
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
footer = "🤖 晶片日報  ·  半導體與AI晶片情報  ·  由 OpenClaw 自動生成  ·  2026-03-24"
bb = d.textbbox((0, 0), footer, font=ff)
d.text(((W - (bb[2]-bb[0])) // 2, y), footer, font=ff, fill=(120, 110, 90))

# ── Save ──────────────────────────────────────────────────────────────────────
out = "/workspace/chip_daily_2026_03_23_24.png"
img.save(out, "PNG", optimize=True)
print(f"Saved: {out}  ({W}x{H}px)")
