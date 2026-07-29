# 交接：sarcopenia-clinic

## ⏯️ 目前做到哪

**v0.2.2**。2026-07-29 在醫院那台（X108521）修掉一個會讓現場誤判「工具壞掉」的 bug，
依門診實際需求擴充判定流程，補上真正的離線能力；回到家裡這台後修復代號的日期字首預設，
並確定**暫不接 Google 表單**。

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
8. **v0.2.2**：加入工作站代碼後，未選工作站時代號欄變成全空，失去原本一載入就看得到
   日期字首的行為。現在一律先填 `20260729-`，選好工作站才補上流水號；只有字首時送出會被擋。

## 🚦 目前狀態

**可運行。判定功能完整，資料採「純本機」模式。**

已實測通過（本機 http 伺服器實跑，不是只讀程式碼）：五種判定分支、初篩陰性加測、
五次起坐留空的部分評估、性別切點交叉驗證（同一組數字換性別會得到不同判定）、
兩項都空與「填了沒按計算」的擋下、送出後清空與流水號進位、
**關掉伺服器後仍能載入並完成判定**、Console 無錯誤。

**評估結果目前沒有連到任何 Google 表單。** `index.html` 的 `FORM_ID` 與 `ENTRY`
都是空字串，送出的紀錄**只存在各台裝置的 localStorage**，「一鍵補送」也會直接回報無法補送。
這是 2026-07-29 的決定，不是待辦（見下方「🔮 未來視使用情形再決定」）。

> **因此每天收工必須在每一台裝置按「匯出 CSV 備份」。**
> 清瀏覽器資料、換裝置、裝置遺失都會讓當日紀錄消失，沒有第二份。

## ➡️ 下一步

1. **在真實平板上驗離線**：連網開一次 →「加到主畫面」→ 關 WiFi → 重開。
   （桌機已驗過，平板未驗。）
2. **用手機實際掃一次結果頁的 QR**，確認連得到衛教頁。尚未實際掃描驗證。
3. **替換 SARC-F 中文題目** —— 目前是暫用措辭，頁尾已誠實標註。
4. 骨鬆專案入口頁加一條連到本工具的連結（要動另一個 repo）。

## 🔗 接 Google 表單（進行中）

決定**要接**，作為將來統計分析的資料來源。做法已備妥 `tools/create-google-form.gs`：
到 script.google.com 新增專案 → 貼上該檔內容 → 執行 `createSarcopeniaForm` → 授權 →
看執行紀錄，把印出來的 `FORM_ID` 與 `ENTRY` 兩段貼回 `index.html` 最上方。
腳本會一併建好回應試算表並連結，題目全部簡答、全部非必填。

**要用個人 Google 帳號跑**（Workspace 帳號可能限制僅組織內可填，平板會靜默送不出去）。
接上後頁面上方的「上線前待辦」提示會自動消失，務必實際送一筆測試資料確認回應表有進資料。
程式的送出與補送邏輯早就寫好，填完兩個常數即生效，不需要改其他地方。

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

2026-07-29　·　阿克（Claude Code）@ DESKTOP-LVSV9Q5（家）　·　v0.2.2　·　Git push：✅ 已推（`efbab93`）

前一筆：2026-07-29 @ X108521（醫院）· v0.2.1 · `95db796`
