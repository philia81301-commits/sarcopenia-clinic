# 交接：sarcopenia-clinic

## ⏯️ 目前做到哪

**v0.2.1**。今天（2026-07-29）在醫院這台修掉一個會讓現場誤判「工具壞掉」的 bug，
依門診實際需求擴充判定流程，補上真正的離線能力。

- **線上版**：https://philia81301-commits.github.io/sarcopenia-clinic/
- **衛教頁（QR 指向處）**：https://philia81301-commits.github.io/sarcopenia-clinic/education.html
- **repo**：https://github.com/philia81301-commits/sarcopenia-clinic （公開，main 的 root）
- **需求規格卡**：`rdq/RDQ-spec-sarcopenia-screening-20260729.md`（`status: confirmed`）

### 今天改了什麼

1. **修掉「按了沒反應」**（原始回報的 bug）——初篩陽性時原本只解除隱藏第 3 段卡片，
   再靠 `scrollIntoView({behavior:"smooth"})` 把人捲下去，**本身不顯示任何判定文字**。
   實測 smooth 捲動會靜悄悄失效（scrollY 停在 0），畫面於是一個字都沒變。
   現在初篩結果一律當場寫出，捲動只是加分；新增 `goTo()`，400ms 內沒捲到就直接跳。
2. **初篩陰性也能加測**（選填）。SARC-F 敏感度有限，原本這些人連握力都沒量就被放掉。
3. **五次起坐改選填**。留空標為「部分評估」，明講無法排除嚴重肌少症；未測項目寫「未測」。
4. **切點顯示在數字旁**（男女不同）。小腿圍原本畫面上完全沒標切點。
5. **防呆**：握力／五次起坐輸入值與目前判定不一致時擋下送出。
6. **PWA 離線**：`sw.js`、`manifest.webmanifest`、3 個圖示、`tools/make-icons.py`。
7. ~~首頁使用說明~~ ——**已於 v0.2.1 移除**（現場判斷太複雜）。離線操作說明改放 README。

## 🚦 目前狀態

**可運行，但仍不能正式收案。**

已實測通過（本機 http 伺服器實跑，不是只讀程式碼）：五種判定分支、初篩陰性加測、
五次起坐留空的部分評估、性別切點交叉驗證（同一組數字換性別會得到不同判定）、
兩項都空與「填了沒按計算」的擋下、送出後清空與流水號進位、
**關掉伺服器後仍能載入並完成判定**、Console 無錯誤。

**做一半的仍是資料上傳**：`index.html` 的 `FORM_ID` 與 `ENTRY` 還是空字串，
送出的紀錄**只存在各台裝置的本機佇列**。要試跑的話，每次收工務必按「匯出 CSV 備份」。

## ➡️ 下一步

1. **建 Google 表單**，依 `docs/google-form-fields.md` 建 11 個簡答題（**全部不要設必填**，
   初篩陰性與未測五次起坐者會是空值），把 formId 與各 `entry.xxx` 填進 `index.html` 最上方。
   填好後頁面上方的「上線前待辦」提示會自動消失。務必送一筆測試資料確認欄位對得上。
2. **在真實平板上驗離線**：連網開一次 →「加到主畫面」→ 關 WiFi → 重開。
   （桌機已驗過，平板未驗。）
3. **用手機實際掃一次結果頁的 QR**，確認連得到衛教頁。尚未實際掃描驗證。
4. **替換 SARC-F 中文題目** —— 目前是暫用措辭，頁尾已誠實標註。
5. 骨鬆專案入口頁加一條連到本工具的連結（要動另一個 repo）。

## ⚠️ 注意事項

- **改版務必同步 `sw.js` 的 `VERSION` 與 `index.html` 的 `APP_VERSION`**，
  否則既有裝置上的圖示、manifest 不會更新。網頁本身是 network-first，連得上網就拿最新版。
- **從沒連網開過的裝置離線打不開**；`file://` 直接開啟時 Service Worker 不會註冊，
  頁尾會顯示「不支援（此頁未透過網址開啟）」。要驗離線就得走 http。
- **病人掃衛教 QR 需要他自己手機的網路**，離線功能保護不到。
- **首頁使用說明已被判定太複雜而移除**，要再加回去前先確認會不會擋住現場流程。
- **多台裝置同時作業時，每台開工前各選一個不同的工作站代碼（A–H）**。
- **現場即時統計刻意不跨裝置合計**（2026-07-29 定案，維持「只送不讀」架構）。
- 改動前先讀規格卡的「❌ 排除項」。另見 `agents.md` 臨床守則第 8–10 條
  （陰性加測／部分評估／切點顯示），那三條是今天踩出來的，不要簡化掉。
- 本專案**未建立 Obsidian 筆記**（未經 project-init，`agents.md` 未登記 vault 路徑），
  本次收工的 L3 詳細紀錄因此未寫。要補的話先跑 project-init 登記 vault 路徑。
- 本機 repo 在 `C:\projects\sarcopenia-clinic`，**不要搬進 OneDrive**。
- **RDQ 技能不在 chezmoi 納管範圍**，每台電腦要各自 clone：
  `git clone https://github.com/mathruffian-dot/rdq-skill.git $env:USERPROFILE\.claude\skills\rdq`
  醫院這台（X108521）今天已補裝。`chezmoi update` 不會帶進來。

## 🔁 下次在家裡筆電接手

今天在**醫院電腦 X108521** 收工，下次在**家裡筆電**繼續。
**開工第一件事：`git pull`**，否則會蓋掉今天的成果。

```
cd C:\projects\sarcopenia-clinic
git pull
```

家裡那台若還沒 clone 過：

```
git clone https://github.com/philia81301-commits/sarcopenia-clinic.git C:\projects\sarcopenia-clinic
```

## 🕐 最後更新

2026-07-29　·　阿克（Claude Code）@ X108521（醫院）　·　v0.2.1　·　Git push：待推
