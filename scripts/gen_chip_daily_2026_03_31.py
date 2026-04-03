#!/usr/bin/env python3
"""Generate chip daily image for 2026-03-29~31"""

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
                "台積電AI晶片產能陷瓶頸 博通示警恐衝擊2026年供應",
                "博通（Broadcom）警告，台積電先進製程產能瓶頸可能嚴重衝擊2026年AI晶片供應。台積電CoWoS先進封裝與3nm/2nm製程產能持續吃緊，多家AI廠商爭搶排單，博通、Google等大客戶預計受到最直接影響，業界呼籲台積電加速擴產時程。",
                "tw.stock.yahoo.com · 3/26"
            ),
            (
                "Arm 發表首款晶片 搶進全球 AI 半導體兆元商機",
                "Arm 正式發表旗下首款自有品牌晶片，直接切入資料中心AI運算市場，挑戰英特爾與AMD的x86主導地位。此舉被視為Arm從IP授權商轉型為晶片設計商的重大戰略跨越，並搭上全球AI半導體超兆元商機的快車，引發市場高度關注。",
                "經濟日報 · 3/27"
            ),
        ]
    },
    {
        "tag": "💾 記憶體戰場",
        "color": (30, 100, 180),
        "items": [
            (
                "記憶體漲價潮蔓延！外媒：半導體價格全面漲",
                "外媒報導，全球記憶體漲價潮持續蔓延，NAND Flash與DRAM報價雙雙走揚，帶動整體半導體價格全面上漲。AI伺服器需求大增加上產能受限，供需失衡局面恐延續至2026年底，台灣記憶體供應商與下游組裝廠同步受惠。",
                "MSN · 3/30"
            ),
            (
                "全球先進記憶體廠樂了！JEDEC 這項決定將影響 AI 記憶體布局",
                "JEDEC 最新標準決定將深遠影響全球AI記憶體的技術布局，HBM與LPDDR5X等規格明確化，有助三星、SK海力士、美光加速量產節奏。業界普遍認為此決定有利於先進記憶體廠商搶佔未來AI訓練與推理晶片的記憶體訂單。",
                "TechNews 科技新報 · 3/30"
            ),
            (
                "記憶體僅需1/6？谷歌AI新演算法引發存儲股降溫",
                "谷歌發表突破性AI演算法，聲稱可將模型推理所需記憶體降低至原本的1/6，消息一出引發HBM與DRAM相關個股大幅回落。但多數分析師認為短期衝擊有限，長期AI算力需求仍撐起記憶體多頭格局，逢低布局機會浮現。",
                "日經中文網 · 3/30"
            ),
        ]
    },
    {
        "tag": "🌏 地緣政治",
        "color": (140, 60, 0),
        "items": [
            (
                "暴漲557%更勝黃金！戰略重要金屬「鎢」受地緣政治影響 供應鏈極度吃緊",
                "鎢（Tungsten）價格年內暴漲557%，超越黃金漲幅，成為最受矚目的戰略金屬。鎢是半導體製程中不可或缺的材料，主要產地集中於中國，地緣政治緊張使全球供應鏈高度吃緊，台灣、美國、日本等晶片製造重鎮正積極尋求替代來源與戰略儲備。",
                "倡議家 · 3/20"
            ),
            (
                "三星預定 2028 年量產矽光子元件 欲彎道超車台積電",
                "三星宣布計畫於2028年量產矽光子（Silicon Photonics）元件，意圖藉由光互連技術在先進封裝領域實現彎道超車，直接挑戰台積電的CoWoS與SoIC主導地位。矽光子被視為下一代AI晶片互連的關鍵技術，市場競爭日趨白熱化。",
                "TechNews 科技新報 · 3/30"
            ),
        ]
    },
    {
        "tag": "🏭 產業動態",
        "color": GOLD,
        "items": [
            (
                "魏哲家談機器人：核心還是半導體，95%AI晶片由台積電製造",
                "台積電董事長魏哲家出席論壇時指出，機器人時代核心仍在半導體，目前全球約95%的先進AI晶片由台積電製造。魏哲家強調，台積電將持續加大先進製程研發投入，並看好機器人AI市場在未來五年內帶來的龐大晶片需求。",
                "工商時報 · 3/22"
            ),
            (
                "AI熱潮引發記憶體短缺！三星與SK海力士加碼投資中國晶圓廠",
                "AI應用需求爆發引發全球記憶體短缺，三星與SK海力士宣布加碼投資在中國的晶圓廠產能，以應對龐大的本地市場需求。此舉在中美科技博弈背景下引發外界高度關注，業界擔憂美方出口管制政策可能進一步收緊，影響韓廠在中國的擴產計畫。",
                "CTWANT · 3/29"
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
d.text((50, y+6), "📅 2026年3月29日～31日  半導體三日報", font=df, fill=(252, 248, 238))
src_txt = "工商時報 · TechNews · Yahoo財經 · MSN · 日經中文網"
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
footer = "🤖 晶片日報  ·  半導體與AI晶片情報  ·  由 OpenClaw 自動生成  ·  2026-03-31"
bb = d.textbbox((0, 0), footer, font=ff)
d.text(((W - (bb[2]-bb[0])) // 2, y), footer, font=ff, fill=(120, 110, 90))

# ── Save ──────────────────────────────────────────────────────────────────────
out = "/workspace/chip_daily_2026_03_29_31.png"
img.save(out, "PNG", optimize=True)
print(f"Saved: {out}  ({W}x{H}px)")
