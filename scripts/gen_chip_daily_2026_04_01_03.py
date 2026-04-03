#!/usr/bin/env python3
"""Generate chip daily image for 2026-04-01~03"""

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
                "台積電美國擴廠震撼彈！最多建12座亞利桑那廠、4座封裝廠",
                "美國科技媒體HotHardware報導，台積電正評估在亞利桑那州最多建立12座晶圓廠及4座先進封裝廠，規模遠超目前已宣布的計畫。此舉被解讀為台積電回應特朗普政府關稅施壓與美國製造業回流政策的重大戰略轉向，若成真將是半導體史上最大單一投資案。",
                "HotHardware · Reuters · 4/3"
            ),
            (
                "晶片股全面崩跌：特朗普暗示強化軍事關稅，美超微、輝達、英特爾齊挫",
                "特朗普總統暗示將進一步強化對半導體的軍事安全關稅，消息一出引發美光、美超微、輝達、英特爾、台積電ADR等晶片股全面下殺。市場擔憂新一輪關稅衝擊將壓縮晶片廠獲利空間，科技股回調幅度創近期新高。",
                "Stocktwits · Yahoo財經 · 4/3"
            ),
        ]
    },
    {
        "tag": "💾 記憶體戰場",
        "color": (30, 100, 180),
        "items": [
            (
                "輝達砸20億美元入股Marvell！NVLink Fusion晶片聯盟成形",
                "輝達宣布向Marvell投資20億美元，雙方將透過NVLink Fusion技術深化AI晶片互連合作。此舉被視為輝達打造自有晶片生態系的關鍵一步，Marvell股價聞訊飆漲逾20%，AI網路晶片賽道競爭格局加速重塑。",
                "WSJ · Bloomberg · Reuters · 3/31"
            ),
            (
                "韓國FuriosaAI發表推理AI晶片，正面挑戰輝達",
                "韓國新創FuriosaAI發表最新推理AI晶片，聲稱在特定場景效能超越輝達H100，直接向輝達推理晶片地位發起挑戰。此舉引發市場高度關注，業界認為AI推理晶片市場正逐漸走向多元競爭格局，輝達一枝獨秀的局面或將改變。",
                "The Korea Herald · 4/2"
            ),
        ]
    },
    {
        "tag": "🌏 地緣政治",
        "color": (140, 60, 0),
        "items": [
            (
                "中國晶片廠搶佔本土市場！輝達中國份額跌破六成",
                "路透社報導，中國本土晶片廠商正快速搶佔市場，輝達在中國AI晶片市場佔有率已跌破60%，中國廠商合計拿下近半壁江山。華為昇騰、寒武紀等中資晶片商加速出貨，美國出口管制的「替代效應」正在加速顯現。",
                "Reuters · Tom's Hardware · 4/1"
            ),
            (
                "DeepSeek新AI模型將成華為大勝利？西方媒體解析地緣科技博弈",
                "The Information報導，DeepSeek即將發布的新一代AI模型在訓練與推理上對硬體需求更低，被認為將大幅受益於華為昇騰晶片，形成「DeepSeek+華為」的中國AI硬體閉環，進一步削弱輝達在中國市場的地位。",
                "The Information · 4/3"
            ),
        ]
    },
    {
        "tag": "🏭 產業動態",
        "color": GOLD,
        "items": [
            (
                "台積電日本熊本廠升級3奈米！2028年量產，印太晶片版圖重組",
                "台積電確認計畫於2028年在日本熊本廠啟動3奈米晶片量產，路透社與外媒紛紛報導此一里程碑。熊本廠升級不僅是技術突破，更被《外交家》雜誌解讀為安全導向的印太供應鏈重組戰略，具有深遠的地緣政治意義。",
                "Reuters · The Diplomat · 4/1~3"
            ),
            (
                "三星衝刺1奈米2030年量產、矽光子封裝搶先台積電",
                "三星宣布雙管齊下：一方面設定2030年量產1奈米製程的目標，另一方面計劃2028年量產矽光子互連元件，企圖藉由chiplet技術與光互連雙重突破追趕台積電。台積電2028年產能已告滿，三星正借此視窗積極搶單。",
                "Digitimes · businesskorea · 3/31"
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
d.text((50, y+6), "📅 2026年4月1日～3日  半導體三日報", font=df, fill=(252, 248, 238))
src_txt = "HotHardware · Reuters · WSJ · The Diplomat · Stocktwits"
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
footer = "🤖 晶片日報  ·  半導體與AI晶片情報  ·  由 OpenClaw 自動生成  ·  2026-04-03"
bb = d.textbbox((0, 0), footer, font=ff)
d.text(((W - (bb[2]-bb[0])) // 2, y), footer, font=ff, fill=(120, 110, 90))

# ── Save ──────────────────────────────────────────────────────────────────────
out = "/workspace/chip_daily_2026_04_01_03.png"
img.save(out, "PNG", optimize=True)
print(f"Saved: {out}  ({W}x{H}px)")
