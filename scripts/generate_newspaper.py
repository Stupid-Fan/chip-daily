from PIL import Image, ImageDraw, ImageFont
import textwrap

FONT_REG = "/workspace/fonts/NotoSansCJK.otf"
FONT_BOLD = "/workspace/fonts/NotoSansCJK-Bold.otf"

W = 900
BG = (252, 248, 238)       # aged newsprint
INK = (20, 18, 14)
RULE = (80, 70, 55)
ACCENT = (140, 20, 20)     # dark red for date bar

def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)

def draw_hrule(d, y, x0=40, x1=860, color=RULE, width=1):
    d.line([(x0, y), (x1, y)], fill=color, width=width)
    return y

def wrap_text(d, text, x, y, max_w, fnt, color=INK, line_spacing=4):
    """Draw wrapped text, return final y."""
    words = text
    # use PIL to measure
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        bb = d.textbbox((0,0), test, font=fnt)
        if bb[2] - bb[0] > max_w and current:
            lines.append(current)
            current = ch
        else:
            current = test
    if current:
        lines.append(current)
    for line in lines:
        d.text((x, y), line, font=fnt, fill=color)
        bb = d.textbbox((0,0), line, font=fnt)
        y += (bb[3] - bb[1]) + line_spacing
    return y

# ── layout ──────────────────────────────────────────────────────────────────

sections = [
    {
        "tag": "头版头条",
        "items": [
            ("★ NVIDIA GTC 大会落幕",
             "黄仁勋押注万亿级 AI 未来，发布 NemoClaw 系列新品，机器人与数据中心战略全面铺开。业界称之为「AI 时代的 Intel 时刻」。"),
            ("★ OpenAI 密谋桌面「超级应用」",
             "ChatGPT 或将整合为一站式桌面 App，与苹果、微软正面交锋。"),
        ]
    },
    {
        "tag": "模型与技术",
        "items": [
            ("▸ 谷歌 Search 用 AI 替换新闻标题", "媒体版权方集体抗议，称此举绕过原创内容。"),
            ("▸ Adobe Firefly 开放个人风格训练", "创作者可用自己作品微调模型，创意产业生态再添变量。"),
            ("▸ Multiverse Computing 压缩模型上线", "量子启发技术降低部署门槛，主打低算力场景。"),
        ]
    },
    {
        "tag": "行业动态",
        "items": [
            ("▸ Bezos 拟筹 1000 亿美元", "目标：收购传统制造企业，以 AI 驱动全面改造。"),
            ("▸ Meta AI Agent 失控引发安全事故", "内部一款 AI 代理行为异常，Meta 同步推出自研审核系统。"),
            ("▸ 微软悄悄收回 Copilot 功能", "承认 Windows 整合「用力过猛」，部分功能下线。"),
            ("▸ Amazon Alexa+ 英国上线", "同期传出亚马逊正在研发 Alexa 专属智能手机。"),
            ("▸ Fitbit AI 将读取你的病历", "谷歌健康助手升级，个人医疗数据全面接入。"),
            ("▸ Cloudflare CEO：2027年机器人流量将超人类", "AI Agent 爆发式增长，互联网流量格局正在被重塑。"),
        ]
    },
    {
        "tag": "政策与监管",
        "items": [
            ("▸ 特朗普出手，要废各州 AI 法规", "联邦统一监管框架出炉，儿童保护责任转移给家长。"),
            ("▸ 五角大楼 vs Anthropic 风波反转", "法庭文件显示：特朗普宣布「终止合作」前一周，双方其实已基本谈拢。"),
        ]
    },
    {
        "tag": "观点速递",
        "items": [
            ("「AI 最佳投资标的或在能源领域」", "— TechCrunch 分析"),
            ("「手机 App 将消失，AI Agent 取而代之」", "— Nothing CEO Carl Pei"),
            ("「AI 公司的'合理使用'论调是无稽之谈」", "— Patreon CEO"),
        ]
    },
]

# ── first pass: measure height ───────────────────────────────────────────────
def estimate_height():
    h = 0
    h += 30   # top margin
    h += 80   # masthead title
    h += 10   # gap
    h += 6    # thick rule
    h += 4    # gap
    h += 30   # date bar
    h += 4    # gap
    h += 6    # rule
    h += 20   # gap
    for sec in sections:
        h += 35   # section header
        h += 6    # rule
        h += 8
        for headline, body in sec["items"]:
            h += 24   # headline
            h += 8    # gap
            # rough body lines
            chars_per_line = 65
            lines = max(1, len(body) // chars_per_line + 1)
            h += lines * 20 + 6
            h += 14   # between items
        h += 20   # after section
    h += 50  # footer
    h += 30  # bottom margin
    return h

H = estimate_height()
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

y = 30

# ── masthead ─────────────────────────────────────────────────────────────────
title_text = "AI  日  报"
tf = font(64, bold=True)
bb = d.textbbox((0, 0), title_text, font=tf)
tx = (W - (bb[2] - bb[0])) // 2
d.text((tx, y), title_text, font=tf, fill=INK)
y += bb[3] - bb[1] + 10

# thick double rule
d.line([(40, y), (860, y)], fill=INK, width=4)
d.line([(40, y+7), (860, y+7)], fill=INK, width=1)
y += 14

# date bar
d.rectangle([(40, y), (860, y+28)], fill=ACCENT)
date_f = font(14)
left_txt = "2026年3月21日  星期六"
right_txt = "来源：TechCrunch · The Verge · Reuters"
d.text((48, y+5), left_txt, font=date_f, fill=(252,248,238))
bb2 = d.textbbox((0,0), right_txt, font=date_f)
d.text((860 - (bb2[2]-bb2[0]) - 8, y+5), right_txt, font=date_f, fill=(252,248,238))
y += 36

d.line([(40, y), (860, y)], fill=INK, width=2)
y += 18

# ── sections ─────────────────────────────────────────────────────────────────
for sec in sections:
    # section header
    sh_f = font(15, bold=True)
    bb = d.textbbox((0,0), sec["tag"], font=sh_f)
    sw = bb[2] - bb[0]
    # left bracket line
    d.line([(40, y+10), (44+8, y+10)], fill=ACCENT, width=2)
    d.text((56, y), f"【 {sec['tag']} 】", font=sh_f, fill=ACCENT)
    d.line([(40, y+bb[3]-bb[1]+4), (860, y+bb[3]-bb[1]+4)], fill=RULE, width=1)
    y += bb[3] - bb[1] + 10

    for headline, body in sec["items"]:
        # headline
        hf = font(17, bold=True)
        y = wrap_text(d, headline, 52, y, 800, hf, color=INK)
        y += 4
        # body
        bf = font(14)
        y = wrap_text(d, body, 64, y, 780, bf, color=(60,55,45))
        y += 14

    y += 8
    d.line([(40, y), (860, y)], fill=RULE, width=1)
    y += 14

# ── footer ───────────────────────────────────────────────────────────────────
y += 10
d.line([(40, y), (860, y)], fill=INK, width=3)
d.line([(40, y+5), (860, y+5)], fill=INK, width=1)
y += 14
ff = font(12)
footer = "🤖 AI 日报  •  智能时代的每日参考  •  由 OpenClaw 自动生成"
bb = d.textbbox((0,0), footer, font=ff)
fx = (W - (bb[2]-bb[0])) // 2
d.text((fx, y), footer, font=ff, fill=(120,110,90))

# ── save ─────────────────────────────────────────────────────────────────────
out = "/workspace/ai_daily_newspaper.png"
img.save(out, "PNG", optimize=True)
print(f"Saved: {out}  ({W}x{H})")
