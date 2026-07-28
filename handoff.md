# 交接：sarcopenia-clinic

最後更新：**2026-07-29**（家用電腦）

## 現在做到哪

第一版 `index.html` 與 `education.html` 已完成並在本機瀏覽器實測通過：

- 兩段式流程（SARC-CalF 初篩 → AWGS 2019）四種判定分支都驗過
- 五次起坐計時器可用，秒數會寫回欄位
- 送出後表單清空、流水號進位、統計頁數字正確（`1／2` 這種 n<10 的顯示方式）
- 重新整理不會吃掉流水號，也不會殘留上一位的資料
- 場域（門診／社區）欄位已加入，未選會被擋下，統計頁分開列
- 衛教頁 QR 已用 `tools/make-qr.py` 產生並內嵌，無外部相依
- Console 無錯誤

## 下一步（依順序）

1. **建 GitHub repo `sarcopenia-clinic`（公開）並開 Pages** —— 尚未建立。
   建好後確認 `https://philia81301-commits.github.io/sarcopenia-clinic/` 可開，
   並實際用手機掃一次結果頁的 QR，確認連得到 `education.html`。
2. **建 Google 表單**，依 `docs/google-form-fields.md` 建 11 個簡答題，
   把 formId 與各 `entry.xxx` 填進 `index.html` 最上方的 `FORM_ID` 與 `ENTRY`。
   填好後頁面上方的「上線前待辦」提示會自動消失。送一筆測試資料確認欄位對得上。
3. **替換 SARC-F 中文題目** —— 目前是暫用措辭。請指定要引用的已驗證中文版，
   替換後在頁尾補上引用出處。
4. 在骨鬆專案的入口頁加一條連到這個工具的連結（兩邊互放）。

## 待決事項

- 衛教頁的運動處方要不要加圖示或示範照片？目前是純文字條列。
- ~~現場即時統計是否要跨裝置合計~~ → **2026-07-29 定案：不合計**。維持「只送不讀」，
  現場各台看自己的數字，全場合計以 Google 回應試算表為準。日後若真的需要現場全場數字，
  建議走 Apps Script 只回傳彙總數（總數／陽性數），不要開明細讀取口。

## 環境備忘

- repo 在 `C:\projects\sarcopenia-clinic`，**不要搬進 OneDrive**。
- 醫院電腦：有 Claude Code 與 GitHub，沒有 `G:`。開工先 `git pull`，收工更新本檔後 push。
- 本機預覽：`python -m http.server 8765 --directory C:\projects\sarcopenia-clinic`
