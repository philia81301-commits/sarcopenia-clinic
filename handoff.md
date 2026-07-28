# 交接：sarcopenia-clinic

## ⏯️ 目前做到哪

第一版完成並**已上線 GitHub Pages**。當天從零開始：跑 RDQ 需求訪談 → 產出規格卡 →
實作兩段式篩檢工具與衛教頁 → 瀏覽器實測 → 建 repo、開 Pages。

- **線上版**：https://philia81301-commits.github.io/sarcopenia-clinic/
- **衛教頁（QR 指向處）**：https://philia81301-commits.github.io/sarcopenia-clinic/education.html
- **repo**：https://github.com/philia81301-commits/sarcopenia-clinic （公開，main 的 root）
- **需求規格卡**：`rdq/RDQ-spec-sarcopenia-screening-20260729.md`（`status: confirmed`、`revisions: 2`）

## 🚦 目前狀態

**可運行，但還不能正式收案。**

已實測通過：四種判定分支、五次起坐計時器、送出後清空與流水號進位、統計頁 n<10 顯示分子分母、
重新整理不殘留也不跳號、工作站代碼防撞號、場域未選會被擋、Console 無錯誤。

**做一半的是資料上傳**：`index.html` 的 `FORM_ID` 與 `ENTRY` 都還是空字串，
所以送出的紀錄**只會存在各台裝置的本機佇列，不會進雲端**。清瀏覽器資料就沒了。
要先試跑的話，每次收工務必按「匯出 CSV 備份」。

## ➡️ 下一步

1. **建 Google 表單**，依 `docs/google-form-fields.md` 建 11 個簡答題（**全部不要設必填**，
   初篩陰性者的握力與五次起坐是空值），把 formId 與各 `entry.xxx` 填進 `index.html` 最上方。
   填好後頁面上方的「上線前待辦」提示會自動消失。務必送一筆測試資料確認欄位對得上。
2. **用手機實際掃一次結果頁的 QR**，確認連得到衛教頁。QR 是用該網址產生的，但尚未實際掃描驗證。
3. **替換 SARC-F 中文題目** —— 目前是暫用措辭，頁尾已誠實標註。指定要引用的已驗證中文版後替換並補出處。
4. 骨鬆專案入口頁加一條連到本工具的連結（要動另一個 repo）。

## ⚠️ 注意事項

- **多台裝置同時作業時，每台開工前要各選一個不同的工作站代碼（A–H）**，
  代號格式 `YYYYMMDD-<工作站><流水號>`。沒選就不給代號也送不出去。紙本對照表建議照工作站分開。
- **統整靠 Google 表單回應試算表**，各台送出的紀錄自動彙整成一份，不需要有人去收 CSV。
  CSV 匯出只是斷網備援，檔案會落在各台裝置自己的下載資料夾。
- **現場即時統計刻意不跨裝置合計**（2026-07-29 定案，維持「只送不讀」架構）。
  日後若真需要現場全場數字，走 Apps Script 只回傳彙總數，不要開明細讀取口。
- 改動前先讀規格卡的「❌ 排除項」，那些是刻意不做的：不做步速、不上傳姓名電話、
  不做列印版衛教卡、不從雲端讀回。
- 本專案**未建立 Obsidian 筆記**（未經 project-init，agents.md 未登記 vault 路徑）。
- 本機 repo 在 `C:\projects\sarcopenia-clinic`，**不要搬進 OneDrive**。
  醫院電腦需自行 `git clone`，開工先 `git pull`。
- 醫院端若要用 RDQ 技能，需另外 clone：
  `git clone https://github.com/mathruffian-dot/rdq-skill.git $env:USERPROFILE\.claude\skills\rdq`

## 🕐 最後更新

2026-07-29　·　阿克（Claude Code）@ DESKTOP-LVSV9Q5　·　Git push：✅ 已推（`e6bf2e5`）
