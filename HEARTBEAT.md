# HEARTBEAT.md

## 晶片日報定期生成

每三天生成一次晶片日報。追蹤狀態存在 `/workspace/memory/chip-daily-state.json`。

檢查方式：
```bash
python3 -c "
import json, time, os
f = '/workspace/memory/chip-daily-state.json'
if os.path.exists(f):
    d = json.load(open(f))
    last = d.get('last_generated', 0)
    days_since = (time.time() - last) / 86400
    print(f'Days since last report: {days_since:.1f}')
    if days_since >= 3:
        print('GENERATE')
    else:
        print('SKIP')
else:
    print('GENERATE')
"
```

如果輸出 `GENERATE`：
1. 讀取 `/workspace/memory/2026-03-25.md` 了解日報規格
2. 從 Google News RSS 抓過去 72 小時半導體新聞
3. 生成中文圖片日報（PIL，參考 `/workspace/scripts/gen_chip_daily_tw.py`）
4. 生成英文 HTML 日報（參考 en.html 格式，所有連結驗證 200 OK）
5. 推送到 GitHub（Token: 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，repo: Stupid-Fan/chip-daily）
6. 更新 `/workspace/memory/chip-daily-state.json` 的 `last_generated` 為當前 timestamp
7. 傳送完成通知給用戶

如果輸出 `SKIP`：不做任何事，繼續下一個檢查項目。

---

## Pod Memory Monitor

Check if any pod in the TestIAM EKS cluster is using >= 60% of its memory limit.

Run: `bash /workspace/scripts/check-pod-memory.sh`

If output contains "🚨", send an alert message to the user immediately with the details.
If output is "OK: No pods exceeding 60%", stay silent (HEARTBEAT_OK).

Credentials needed (set as env vars before running):
- AWS_ACCESS_KEY_ID=AKIAZZDPA5LKS7MH6C24
- AWS_SECRET_ACCESS_KEY=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
- PATH=/workspace:/workspace/.local/bin:$PATH
