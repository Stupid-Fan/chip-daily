#!/usr/bin/env python3
"""Generate chip daily image for 2026-05-04~06"""

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
                "馬斯克擬砸1190億美元建晶圓廠：SpaceX豪賭AI晶片自主製造",
                "SpaceX計劃投入高達1190億美元在美國本土興建晶圓廠，目標生產Starlink及Dojo AI晶片。馬斯克從未有晶圓代工經驗，此舉震驚半導體業界，被視為對台積電、三星及英特爾代工的重大挑戰，也引發對其執行可行性的廣泛質疑。",
                "The Register · 2026-05-06"
            ),
            (
                "DRAM短缺衝擊AMD全年展望：記憶體漲價拖累PC出貨預測下修",
                "AMD警告全球DRAM供應持續吃緊，記憶體成本大幅攀升將直接壓縮PC出貨量，全年業績展望面臨下修壓力。此消息與AI伺服器記憶體需求暴增互為呼應，HBM缺貨與DRAM漲價形成雙重壓力。",
                "The Register · 2026-05-06"
            ),
        ]
    },
    {
        "tag": "💾 記憶體 / AI晶片",
        "color": (30, 100, 180),
        "items": [
            (
                "GPU租用者面臨「矽片彩票」：雲端算力效能差異高達3倍",
                "IEEE Spectrum深度報告揭露，雲端GPU租用市場存在嚴重效能差異——同一型號GPU在不同供應商或甚至同一供應商不同時段，實際運算效能可差達3倍，AI新創公司算力成本估算因此大幅失準。",
                "IEEE Spectrum · 2026-05-05"
            ),
            (
                "稀疏AI硬體突破：零值加速技術可望讓AI晶片功耗砍半",
                "IEEE Spectrum報導，新型稀疏化運算硬體架構能跳過神經網路中大量接近零的數值，在不損失精度的前提下大幅減少實際計算量，有望使下一代AI推理晶片效能提升2倍、功耗減少50%。",
                "IEEE Spectrum · 2026-05-04"
            ),
        ]
    },
    {
        "tag": "🌏 地緣博弈",
        "color": (140, 60, 0),
        "items": [
            (
                "2026 Q1全球半導體銷售急速成長，AI需求推升市場創新高",
                "業界數據顯示2026年第一季全球半導體銷售金額大幅成長，AI伺服器晶片、先進記憶體及高效能運算需求持續旺盛，台灣、韓國主要晶圓廠訂單滿載，全年展望樂觀。",
                "Semiconductor Digest · 2026-05-05"
            ),
            (
                "輝達與康寧攜手：光纖網路基礎設施支撐美國AI算力擴張",
                "輝達宣布與康寧（Corning）簽署長期戰略合作協議，共同強化美國AI資料中心光纖網路基礎設施。康寧負責供應新一代低損耗光纖，支援輝達NVLink及Infiniband高頻寬互聯，確保美國AI製造供應鏈本土化。",
                "Semiconductor Digest · 2026-05-05"
            ),
        ]
    },
    {
        "tag": "🏭 產業動態",
        "color": GOLD,
        "items": [
            (
                "Arm AGI CPU通過西門子硬體驗證，代理AI應用規模部署在望",
                "西門子EDA完成對Arm最新AGI（人工通用智慧）CPU設計的硬體輔助功能驗證，確認其可支援大規模代理AI工作負載。此次驗證被視為Arm在資料中心CPU市場挑戰x86架構的重要里程碑。",
                "Semiconductor Digest · 2026-05-06"
            ),
            (
                "應用材料收購先進封裝設備商NEXX，強化CoWoS製程布局",
                "應用材料（Applied Materials）宣布收購NEXX System，一家專注於先進封裝電鍍設備的廠商。此舉將強化應用材料在CoWoS、SoIC等3D封裝製程的設備競爭力，直接受益於台積電與英特爾的封裝擴產計畫。",
                "Semiconductor Digest · 2026-05-05"
            ),
            (
                "GlobalFoundries推SCALE共封裝光學模組，搶進AI資料中心互聯市場",
                "GlobalFoundries（格芯）發表SCALE共封裝光學（CPO）模組解決方案，整合矽光子技術於AI資料中心交換器，可大幅降低高速互聯能耗。此舉標誌格芯正積極從傳統特殊製程轉型，搶攻AI基礎設施市場。",
                "Semiconductor Digest · 2026-05-05"
            ),
            (
                "FPGA晶片獲IEEE里程碑認證：可重寫硬體革命50週年紀念",
                "IEEE授予FPGA晶片技術里程碑獎章，紀念可重寫硬體架構問世近50週年。FPGA技術如今已廣泛應用於AI加速、5G通訊及自動駕駛，Altera（英特爾旗下）、Xilinx（AMD旗下）及Lattice等廠商持續推動技術進化。",
                "IEEE Spectrum · 2026-05-04"
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
d.text((50, y+6), "📅 2026年5月4日～6日  半導體三日報", font=df, fill=(252, 248, 238))
src_txt = "The Register · Semiconductor Digest · IEEE Spectrum"
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
footer = "🤖 晶片日報  ·  半導體與AI晶片情報  ·  由 OpenClaw 自動生成  ·  2026-05-06"
bb = d.textbbox((0, 0), footer, font=ff)
d.text(((W - (bb[2]-bb[0])) // 2, y), footer, font=ff, fill=(120, 110, 90))

# ── Save ──────────────────────────────────────────────────────────────────────
out = "/workspace/chip_daily_2026_05_04_06.png"
img.save(out, "PNG", optimize=True)
print(f"Saved: {out}  ({W}x{H}px)")
