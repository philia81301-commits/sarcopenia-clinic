# 交接：sarcopenia-clinic

## ⏯️ 目前做到哪

**核心工具仍是 v0.2.4**（版本號本次沒動，原因見下）。2026-08-05 新增衛教測驗分享頁
`quiz.html`（海報＋Wordwall 測驗嵌入），並在 `index.html` 結果頁加一個非強制連結入口。
2026-07-30 把三個版本號統一（`education.html` 原本一路停在 v0.1.0）。
在此之前：2026-07-29 在醫院那台（X108521）修掉一個會讓現場誤判「工具壞掉」的 bug，
依門診實際需求擴充判定流程，補上真正的離線能力；回到家裡這台後修復代號的日期字首預設，
並接上 Google 表單。

- **線上版**：https://philia81301-commits.github.io/sarcopenia-clinic/
- **衛教頁（QR 指向處）**：https://philia81301-commits.github.io/sarcopenia-clinic/education.html
- **衛教測驗分享頁（新）**：https://philia81301-commits.github.io/sarcopenia-clinic/quiz.html
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

### 2026-08-05 改了什麼

**新增衛教測驗分享頁，不動核心篩檢工具的判定邏輯。**

1. **Wordwall 測驗**：建立「肌少症衛教小測驗」（10 題選擇題），主題換成 Indigo（原
   Classic 主題花俏、對長輩不易讀），已設為 **Public**（任何人拿連結免登入可玩）。
   詳見下方「🔗 Wordwall 測驗」。
2. **順手修掉 wordwall 技能的 bug**：Wordwall 網站改版後範本卡片選擇器失效，
   已在 `~/.claude/skills/wordwall/wordwall.py` 補上新選擇器並驗證通過。
   **這是第三方 repo（`mathruffian-dot/wordwall-cli`），修好後還沒推送**——
   見下方「⚠️ 注意事項」。
3. **NotebookLM 生成衛教海報**：`images/sarcopenia-quiz-poster.jpg`，主題「肌少症衛教」，
   活潑插畫風格。**AI 生圖內嵌的文字有 9 處是亂碼**（看起來像中文字但拼不成正確詞，
   例如「若鵜檢戁鬗」應為「若懷疑異常」），逐一比對衛教頁原文後用去背填色＋重繪文字修正。
   **這是 NotebookLM infographic 功能的已知限制，不是這次特例**——日後用同工具再生成
   類似素材，務必逐字核對，不能只看排版順眼就發出去。
4. **`quiz.html`**：海報＋Wordwall 測驗 iframe 嵌入＋連回 `education.html` 的按鈕。
   刻意做成獨立頁面，**不進 `sw.js` 的 PRECACHE、不影響離線功能**——反正 Wordwall
   iframe 本來就需要網路，跟著要求離線沒有意義。
5. **`index.html` 結果頁**加一個「→ 要不要一起做完衛教測驗？」連結按鈕，跟 QR code
   共用顯示條件（`screen_negative` 時隱藏），**非強制**——人潮多時可以只做篩檢跳過測驗。
6. **本機驗證**：`python -m http.server 8765` 起本機伺服器，實際跑過一次篩檢流程到
   出現陽性結果，截圖確認連結按鈕位置與樣式正常、Wordwall iframe 正確載入 Indigo 主題。

### 2026-08-05（下午）改了什麼——Wordwall 測驗調整

潘醫師實際玩過一輪後回報四個問題，全部處理：

1. **選項字體大小不一**：Wordwall 是每題自動把最長的選項縮字，題與題之間字級才會跳動。
   逐題比對衛教原文，把 11 個過長的答案選項縮短拉齊（例如「錯，吃夠蛋白質＋規律出力可以
   練回來」→「錯，吃夠蛋白質能練回來」），縮小題與題之間的字級落差。
2. **英文字改中文、START 改開始**：Wordwall 有 `/tc/`（繁體中文）網址前綴，
   `https://wordwall.net/tc/embed/...` 會讓整個播放器介面（開始、一系列多選題。點擊正確
   答案繼續。）變成中文，不用改內容，換內嵌網址就好。`quiz.html` 已改用這個網址。
3. **黑底改檸檬黃**：Wordwall 主題從 Indigo 換成 Clouds，**題目畫面**變成亮藍色雲朵風。
   但**進場前的黑底封面卡片是 Wordwall 播放器固定樣式，任何主題都是黑的，改不掉**——
   這是平台限制，不是沒設定好。折衷做法：`quiz.html` 的測驗卡片外圍背景改成潘醫師指定
   的檸檬黃 `#FFF450`，把黑色封面「包」在指定色裡。
4. **海報標題被裁切**：`images/sarcopenia-quiz-poster.jpg` 的標題「存肌力、享健康：
   您的肌少症生活指南」原本字級偏大，在手機預覽視窗容易被截掉一截。已在原始 PNG 上
   去背重繪縮小字級（約縮到 70%），重新輸出 JPG 更新進 repo。

**已用本機 http 伺服器＋無頭瀏覽器截圖驗證**：Wordwall 中文介面、Clouds 主題實際題目畫面、
`quiz.html` 頁面排版（含檸檬黃卡片、縮小後的海報標題）都截圖確認過。

### 2026-07-30 改了什麼（版本號同步）

**只有版本號，功能與內容一字未動。** 三處統一到 **0.2.4（2026-07-30）**：
`sw.js` 的 `VERSION`、`index.html` 的 `APP_VERSION`、`education.html` 頁尾的硬編字串。

- **為什麼要 bump 而不是把 education 標成 0.2.3**：`sw.js` 的 `PRECACHE` 有快取
  `education.html`，不動 `VERSION` 的話已「加到主畫面」的裝置不會拿到新版。
- 根因是 `agents.md` 的部署段只寫「同步**兩個**版本號」，漏了 `education.html`
  ——它是硬編、沒有 JS 會漏改。已改成三個並做成表格，`sw.js` 與 `index.html` 的註解也補上。
- **已用本機 http 伺服器驗過**：三處都顯示 0.2.4、Service Worker 狀態「可離線使用」、Console 無錯誤。

## 🚦 目前狀態

**可運行。判定功能完整，資料採「純本機」模式。**

已實測通過（本機 http 伺服器實跑，不是只讀程式碼）：五種判定分支、初篩陰性加測、
五次起坐留空的部分評估、性別切點交叉驗證（同一組數字換性別會得到不同判定）、
兩項都空與「填了沒按計算」的擋下、送出後清空與流水號進位、
**關掉伺服器後仍能載入並完成判定**、Console 無錯誤。

**評估結果已連上 Google 表單**（2026-07-29 接上並實測通過，見下方「🔗 Google 表單」）。
送出即進回應試算表，那份試算表就是將來統計分析的資料來源。
沒網路時紀錄先存本機佇列，回到有網路按「一鍵補送」。

**衛教測驗頁已上線**（2026-08-05，見下方「🔗 Wordwall 測驗」），本機驗證過連結與嵌入
正常，尚未在真實手機上實測（`file:///` 或本機伺服器測的都是桌機瀏覽器）。

> 「匯出 CSV 備份」現在是**備援**，不是唯一出路。但長時間離線作業、或裝置要換／要清瀏覽器
> 資料之前，仍請先按一次匯出——本機佇列裡沒送出的紀錄清掉就沒了。

## ➡️ 下一步

1. **在真實平板上驗離線**：連網開一次 →「加到主畫面」→ 關 WiFi → 重開。
   （桌機已驗過，平板未驗。）
2. **用手機實際掃一次結果頁的 QR**，確認連得到衛教頁。尚未實際掃描驗證。
   > 衛教 QR **已經存在、不需重產**：`tools/qr-education.svg`（原始檔）＋ `index.html`
   > 內嵌的同一份 inline SVG。指向的網址沒變過，改版本號不影響它。
3. **替換 SARC-F 中文題目** —— 目前是暫用措辭，頁尾已誠實標註。
4. 骨鬆專案入口頁加一條連到本工具的連結（要動另一個 repo）。
5. **用手機實際玩一次 `quiz.html`**，確認海報圖與 Wordwall iframe 在手機瀏覽器排版正常、
   標題縮小後不再被截、檸檬黃卡片與黑底封面的視覺對比可以接受
   （目前只驗過桌機瀏覽器＋無頭瀏覽器截圖）。
6. `wordwall.py` 的選擇器修正還沒推送到 `mathruffian-dot/wordwall-cli`，見「⚠️ 注意事項」。

## 🔗 Wordwall 測驗（2026-08-05 建立，同日下午調整）

「肌少症衛教小測驗」，10 題選擇題，主題 **Clouds**（原 Indigo，2026-08-05 下午換），
**已設為 Public**（免登入可玩），介面走中文（`/tc/` 路徑）。

- 活動頁：https://wordwall.net/resource/117017138/肌少症衛教小測驗
- 內嵌（`quiz.html` 用的就是這組，**注意含 `/tc/` 且 `themeId=46`**）：
  `https://wordwall.net/tc/embed/b01e95a1a20d4c91a9f0a1545d307ef8?themeId=46&templateId=5&fontStackId=0`

改題目或換主題請登入 `philia81301@gmail.com` 到 Wordwall 編輯，`quiz.html` 的 iframe
網址不會變（除非重新建立活動）。**若之後又手動換主題，記得 embed 網址的 `themeId` 要
跟著改，兩邊會脫鉤**（Wordwall 編輯頁換主題不會自動更新既有的內嵌程式碼）。

**已知平台限制**：測驗開始前的封面卡片（Logo＋「開始」按鈕那頁）固定是黑底，
Wordwall 所有主題都一樣，無法透過主題或設定改掉；「Options」下的進階設定（含可能的
自訂色彩）鎖在付費訂閱，免費帳號點了會被「Subscription required」擋住。

## 🔗 Google 表單（已接上，2026-07-29）

用 `tools/create-google-form.gs` 建的，`FORM_ID` 與 11 個 `entry.xxx` 已填進 `index.html` 最上方。

- 表單編輯：https://docs.google.com/forms/d/1PU792zBD1c9CMvfjKcisUZvGA1WbYe8l1M0YDpd8DJc/edit
- **回應試算表（統計分析的資料來源）**：
  https://docs.google.com/spreadsheets/d/1-OSC6jePQB5-FkQkD3iE4HY6Z8Ye2gzuHdNwNBYoL7c/edit

**已端到端驗證**：從工具送出一筆 → 回應試算表 12 欄全部對位，
性別交叉驗證通過（介面選「女」→ 試算表存 `0`）。測試列的代號是 `TEST-請刪除`。

日後要改題目：**不要動題目順序或刪題重建**，`entry` 編號會變，改了要重跑腳本並更新
`index.html`。只改題目文字不影響 `entry` 編號。

## ⚠️ 注意事項

- **`wordwall.py` 的選擇器修正還沒推送**：Wordwall 網站改版讓範本卡片選擇器失效，
  已在本機 `~/.claude/skills/wordwall/wordwall.py` 修好並驗證通過，但這是**第三方 repo**
  （`mathruffian-dot/wordwall-cli`，不是潘醫師的），還沒 commit + push，也還沒問過要不要
  推送／開 PR。下次用 wordwall 技能前確認一下這個修正還在，或詢問是否要推送上游。
- **NotebookLM infographic 的內嵌文字不可信任**：這次生的海報有 9 處文字是亂碼
  （字型看起來正常，但拼不成正確詞），已逐字核對修正。日後用 NotebookLM 生同類素材，
  **生完一定要放大檢查每一段文字**，不要只看排版順眼。
- **改版務必同步三個版本號**：`sw.js` 的 `VERSION`、`index.html` 的 `APP_VERSION`、
  **`education.html` 頁尾的硬編 `v?.?.?`**（第三項最容易漏，2026-07-30 就是這樣不同步的）。
  否則既有裝置上的圖示、manifest、衛教頁不會更新。網頁本身是 network-first，連得上網就拿最新版。
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

## 🔁 跨電腦接手

2026-07-30 在**家裡筆電 DESKTOP-LVSV9Q5** 收工。
**開工第一件事：`git pull`**，否則會蓋掉上次的成果。

```
cd C:\projects\sarcopenia-clinic
git pull
```

家裡那台若還沒 clone 過：

```
git clone https://github.com/philia81301-commits/sarcopenia-clinic.git C:\projects\sarcopenia-clinic
```

## 🕐 最後更新

2026-08-05（下午）　·　阿克（Claude Code, Sonnet 5）@ DESKTOP-LVSV9Q5（家）　·　**v0.2.4**（核心工具版本未變）　·　Git push：待回填

前一筆：2026-08-05（上午）@ DESKTOP-LVSV9Q5（家）· v0.2.4 · `9bf3730`
再前一筆：2026-07-30 @ DESKTOP-LVSV9Q5（家）· v0.2.4 · `1cc9882`

> L3 Obsidian：本專案**未建立**筆記（未經 project-init、`agents.md` 未登記 vault 路徑），
> 因此本次同樣沒有 L3 紀錄。要補的話先跑 project-init。
