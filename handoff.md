# 交接：sarcopenia-clinic

## ⏯️ 目前做到哪

**目前 v0.2.5**。2026-08-09 這輪只動 `education.html` 的列印樣式（見下方
「### 2026-08-09 改了什麼」），沒碰篩檢判定邏輯。

在此之前核心工具停在 v0.2.4。2026-08-05 這天陸續加了：
衛教測驗分享頁 `quiz.html`（海報＋Wordwall 測驗嵌入）、**現場競賽版**（`compete.html`
轉址頁＋`tools/reset-competition.py` 一鍵重置排行榜工具，細節見下方「🔗 Wordwall
測驗－現場競賽版」）、給同事的連結彙整表 `quiz-links.docx`（真超連結格式，方便複製轉傳）。
2026-07-30 把三個版本號統一（`education.html` 原本一路停在 v0.1.0）。
在此之前：2026-07-29 在醫院那台（X108521）修掉一個會讓現場誤判「工具壞掉」的 bug，
依門診實際需求擴充判定流程，補上真正的離線能力；回到家裡這台後修復代號的日期字首預設，
並接上 Google 表單。

- **線上版**：https://philia81301-commits.github.io/sarcopenia-clinic/
- **衛教頁（QR 指向處）**：https://philia81301-commits.github.io/sarcopenia-clinic/education.html
- **衛教測驗分享頁（練習版）**：https://philia81301-commits.github.io/sarcopenia-clinic/quiz.html
- **衛教測驗現場競賽版（QR code 掃碼用，固定網址）**：
  https://philia81301-commits.github.io/sarcopenia-clinic/compete.html
- **連結彙整表（給同事）**：`quiz-links.docx`（repo 根目錄，含超連結＋重置步驟）
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

### 2026-08-05（傍晚）再改一輪——字體仍不一致 + Q5 內容調整

潘醫師實測後回報「字體大小仍不一」，代表上面第 1 點只砍離群值不夠。這次改法不同：
**把全部 40 個答案選項一次重新拉齊**，目標同一題內部落差 ≤3–4 字、全部題目落在
6–11 字區間（不是只砍長的，太短的也補長），教訓已記進
`~/.claude/projects/.../memory/wordwall-quiz-style-elderly.md`。

同時處理 **Q5 內容修改**：正確答案「蒸蛋、絞肉都可以」→「蒸蛋、豆腐都可以」
（潘醫師指定刪絞肉改豆腐，豆腐對牙口不好的長輩來說也更貼題）。

**已用 `/tc/embed` 實際截圖 Q1 驗證**：四個選項現在同一字級，改善明顯。
這輪只動 Wordwall 內容本身，`quiz.html` 的 iframe 網址／主題／檸檬黃樣式都沒再變。

### 2026-07-30 改了什麼（版本號同步）

**只有版本號，功能與內容一字未動。** 三處統一到 **0.2.4（2026-07-30）**：
`sw.js` 的 `VERSION`、`index.html` 的 `APP_VERSION`、`education.html` 頁尾的硬編字串。

- **為什麼要 bump 而不是把 education 標成 0.2.3**：`sw.js` 的 `PRECACHE` 有快取
  `education.html`，不動 `VERSION` 的話已「加到主畫面」的裝置不會拿到新版。
- 根因是 `agents.md` 的部署段只寫「同步**兩個**版本號」，漏了 `education.html`
  ——它是硬編、沒有 JS 會漏改。已改成三個並做成表格，`sw.js` 與 `index.html` 的註解也補上。
- **已用本機 http 伺服器驗過**：三處都顯示 0.2.4、Service Worker 狀態「可離線使用」、Console 無錯誤。

### 2026-08-06 做了什麼（現場試跑排查：資料靜默消失事件）

**沒動程式碼，純營運面排查與修復。** 社區工作站試跑當天，工作人員回報「App 顯示送出
成功、待補送 0，但回應試算表完全沒有新資料」。追查到根因是 **Google 表單被移進了
Google Drive 垃圾桶**（這是第二次發生同一件事），`formResponse` 端點會 302 導向
`.../closedform`，但 `index.html` 的 `send()` 用 `fetch(..., {mode:"no-cors"})` 送出，
瀏覽器看不到實際回應內容，只要請求送得出去就判定成功、把紀錄從本機佇列移除——
**這是目前架構的已知盲點，不只是這次的偶發事件**，見下方「⚠️ 注意事項」。

- 排查方式：直接用 curl 對 `formUrl()` 帶 `ENTRY` 對應欄位送測試資料，看 response
  header 的 `Location` 是否為 `.../closedform`（未接受回應）；正常應為 200 無重導向。
- 復原表單（移出垃圾桶）後用同樣方式送測試資料驗證，確認 200、且測試代號
  （`20260806-DIAG003/004`）真的進了回應試算表，判定修復成功。
- 表單「回覆」分頁計數與試算表列數曾經對不上（垃圾桶期間卡住 1-2 筆未同步的回覆），
  但確認當天是測試日、沒有真實受檢者，不影響正式資料。
- **根因追到底**：表單被誤刪是因為潘醫師「整理雲端空間」時裸放在 Drive 根目錄的檔案
  容易被連坐清掉（已發生兩次）。已把表單、回應試算表、連同減重門診的「減重評估表」
  一起搬進新建的 Drive 資料夾「**門診工具-正式運作中**」並加星號，之後整理空間時
  跳過這個資料夾即可。**移動資料夾不影響檔案 ID／網址／entry 編號**，工具與分析
  流程完全不受影響，已用 API 驗證搬移後四個檔案的 `parentId` 都正確指向新資料夾。
- 這個坑與排查方法、資料夾慣例已記進使用者全域 memory
  （`sarcopenia-clinic-project.md`、`clinic-tool-project-recipe.md`），下次遇到
  「App 顯示成功但資料沒進試算表」可以直接先查表單狀態，不用重跑一輪排查。

### 2026-08-09 改了什麼（衛教頁列印樣式，v0.2.5）

`education.html` 原本**完全沒有 `@media print`**，等於直接把螢幕版印出來。新增列印區塊：

1. **`@page{size:210mm 279.4mm;margin:10mm 15mm 12mm}`** —— A4 與 Letter 的交集
   （寬取 A4、高取 Letter）。醫院影印機紙匣有時放 Letter，寫 `size:A4` 會被裁掉底部、
   寫 `size:Letter` 又會在 A4 上裁掉左右，只有取交集兩邊都安全。**不要改回單一紙張。**
2. **深色模式的 CSS 變數在列印時強制覆蓋回淺色**——本頁有 `prefers-color-scheme:dark`，
   用深色手機列印會整片黑底。
3. **`.big` 由深色底反白字改成淺底黑字**——列印預設不印背景，原本那段會整段看不見。
4. 卡片、表格、頁尾加 `break-inside:avoid`，避免被切成兩頁。
5. 為了收在雙面兩頁，**只壓間距、行高降到 1.5（下限），字級一個字都沒動**（讀者多為 50 歲以上）。
6. 版本號三處同步：`sw.js` 的 `VERSION`、`index.html` 的 `APP_VERSION`、本頁頁尾 → **0.2.5**。

**量測方式（不是目測）**：本機 http 起 server，把 print 媒體查詢切成生效、版面寬度鎖在
列印可用寬度 180mm，實際量每個區塊高度。結果：內容總高 **440.8mm**、最高的不可拆單位
**114.8mm**。一頁可用高度關掉瀏覽器頁首頁尾是 257.4mm、開著只剩 233.4mm ——
**關掉是雙面兩頁，開著會變三頁（不會被裁，只是多一張紙）**。

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

**衛教頁可以印了**（2026-08-09，v0.2.5）。只驗到「排版量測」這一層，
**還沒真的送進影印機印一張出來**。

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
7. **真人拿手機掃一次現場競賽版 QR code**（`images/quiz-competition-qr.png`），確認
   跳轉到 `compete.html` 再轉址進 Wordwall 全程順暢——目前只驗過 curl／桌機瀏覽器。
8. 醫院電腦（如 X108521）如果要現場執行 `reset-competition.ps1`，要先在那台電腦裝
   Python＋Playwright 並重新走一次 Wordwall 登入（`chrome-login`→`grab-session`），
   細節見 `agents.md` 路線圖。
9. Wordwall「我的結果」清一下這次開發測試留下的幾份「肌少症衛教小測驗－現場競賽版 …」
   測試課業（不影響現在運作，純粹整理用，見「🔗 Wordwall 測驗－現場競賽版」段落）。
10. `wordwall.py` 的 `assign` timing bug 已丟背景任務建議（`task_63bbac40`），還沒處理。
11. **實際印一張衛教頁出來看**（A4 紙匣、Letter 紙匣各一次），確認沒被裁。
    列印視窗要**取消勾選「頁首及頁尾」**、邊界選「預設」不要選「無」；
    開著頁首頁尾會變三頁。

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

## 🔗 Wordwall 測驗－現場競賽版（2026-08-05 建立，同日再改成可重置架構）

同一份「肌少症衛教小測驗」（10 題不變），另外用 Wordwall 的「課業分配」開課業給現場
多人競賽用，掃 QR code 進去打暱稱作答，玩完看排行榜。

**QR code 不是直接指向 Wordwall，而是指向 `compete.html`（固定網址）**，
`compete.html` 裡面才是真正的 Wordwall `/play/` 連結，用 meta refresh＋JS 立刻轉址。
這樣設計是因為 Wordwall 沒有「清空排行榜但保留同一個連結」的功能，唯一的重置方式是
建一份全新的課業（會拿到新的 `/play/` 連結）——讓 QR code 固定指向 `compete.html`，
每次重置只要換 `compete.html` 裡面轉址的目標，印出來的 QR code 就永遠不用換。

- QR code 圖檔：`images/quiz-competition-qr.png`，指向
  `https://philia81301-commits.github.io/sarcopenia-clinic/compete.html`。
- **一鍵重置**：雙擊 `tools/reset-competition.ps1`（或 `python tools/reset-competition.py`）。
  會建一份新課業（乾淨排行榜、暱稱登入、不能重新作答、結束不顯示答案）、把
  `compete.html` 裡的轉址目標換成新連結、`git commit + push`，最後印出這輪的
  Wordwall 結果頁網址（活動結束後打開看排行榜、公布前五名）。
  **push 後 GitHub Pages 大約要等 30-60 秒才生效**，不要卡在活動開始前最後幾秒才跑。
  舊的課業不會被刪除，留在 Wordwall「我的結果」當上一輪的存檔。
- 目前 Wordwall「我的結果」底下已經有幾份「肌少症衛教小測驗－現場競賽版 …」的
  測試課業（含最早那份 `assignment_id: 55048369`，排行榜第一名有一筆測試資料
  「nn」9/10分），都是這次開發跟測試 `reset-competition.py` 留下的，不是真的參賽紀錄，
  之後想整理可以直接去 Wordwall 網站手動刪除，不影響 `compete.html` 現在指向的那份。

**`wordwall.py` 有一個已知 timing bug（還沒修進上游）**：`assign` 指令送出設定後只
固定等 1200ms 就去抓 `/play/` 連結，但「課業設置」對話框有時還在轉圈圈，導致抓不到
連結、指令回報失敗（exit code 3），**但作業其實已經在 Wordwall 那邊建立成功**——遇到
這個失敗訊息不能直接重跑 `assign`，會建出重複的作業，要先用 `results list` 確認。
`tools/reset-competition.py` 用自己的輪詢＋`/myresults` 保險路徑繞開了這個問題，
已丟一個背景任務建議去修 `wordwall.py` 本身（`task_63bbac40`），還沒處理。

## 🔗 Google 表單（已接上，2026-07-29）

用 `tools/create-google-form.gs` 建的，`FORM_ID` 與 11 個 `entry.xxx` 已填進 `index.html` 最上方。

- 表單編輯：https://docs.google.com/forms/d/1PU792zBD1c9CMvfjKcisUZvGA1WbYe8l1M0YDpd8DJc/edit
- **回應試算表（統計分析的資料來源）**：
  https://docs.google.com/spreadsheets/d/1-OSC6jePQB5-FkQkD3iE4HY6Z8Ye2gzuHdNwNBYoL7c/edit
- **2026-08-06 起：兩個檔案都搬進 Drive 資料夾「門診工具-正式運作中」**（原本裸放
  根目錄，被誤刪兩次才搬家），網址與 `entry` 編號不變，見下方「⚠️ 注意事項」。

**已端到端驗證**：從工具送出一筆 → 回應試算表 12 欄全部對位，
性別交叉驗證通過（介面選「女」→ 試算表存 `0`）。測試列的代號是 `TEST-請刪除`。

日後要改題目：**不要動題目順序或刪題重建**，`entry` 編號會變，改了要重跑腳本並更新
`index.html`。只改題目文字不影響 `entry` 編號。

## ⚠️ 注意事項

- **改版務必同步三個版本號**：`sw.js` 的 `VERSION`、`index.html` 的 `APP_VERSION`、
  `education.html` 頁尾（目前皆 **0.2.5**）。頁尾那個沒有 JS 會漏改。
- **`education.html` 的 `@page` 是 `210mm 279.4mm`（A4∩Letter 交集），不要改回單一紙張**。
  另外**任何掛 `page-break-inside:avoid` 的區塊都不能高於可用頁高**（開著瀏覽器頁首頁尾時
  只剩約 233mm），超過的話瀏覽器只會忽略它、斷點反而失控（骨鬆專案的衛教單張踩過）。
  改完版面要實際量高度，別憑看起來順眼。要省空間的順序：先動間距 → 再動行高（1.5 是下限）
  → **絕不動字級**。
- **App 無法分辨「送出成功」與「Google 表單拒收」，這是架構性盲點**（2026-08-06 踩到，
  已是第二次因此掉資料）。`send()` 用 `fetch(..., {mode:"no-cors"})`，瀏覽器看不到真實
  回應內容，只要請求送得出去（有網路）就判定成功、清掉本機佇列——即使表單被移進垃圾桶、
  關閉接受回應、或 entry 編號對不上，UI 都會顯示「送出成功」，CSV 備援也不會觸發
  （因為佇列本來就被清空了）。**排查口訣**：遇到「App 說成功、試算表沒資料」，先用 curl
  直接打 `formUrl()`（`https://docs.google.com/forms/d/e/{FORM_ID}/formResponse`）帶
  `ENTRY` 對應欄位，看 response header 的 `Location` 是否為 `.../closedform`
  （代表表單未接受回應，通常是被移進垃圾桶或手動關閉），正常應為 200 無重導向。
  這個限制目前**沒有修**（no-cors 是瀏覽器對跨網域請求的安全限制，繞不過去），只能靠
  排查口訣加速定位，不要照一般順序（先查離線、查 entry 編號）一步步查。
- **表單與回應試算表已搬進 Drive「門診工具-正式運作中」資料夾**（2026-08-06，見上方
  「🔗 Google 表單」），原因是裸放根目錄容易在「整理雲端空間」時被連坐刪除（已發生兩次）。
  之後新建的門診工具表單／試算表，記得也搬進這個資料夾。
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
- **`.gitignore` 加了 `~$*`**：開 `quiz-links.docx` 時 Word 會在旁邊留一個
  `~$quiz-links.docx` 鎖定暫存檔，git 會抓到當成未追蹤檔案，已加規則排除，不用手動忽略。
- **Wordwall 登入狀態（`~/.wordwall/state.json`）不跟著 repo 走**，每台電腦要各自
  `chrome-login`→`grab-session` 登入一次，這是刻意的帳號安全設計，沒有共用的辦法。

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

2026-08-09　·　阿克（Claude Code, Opus 5）@ DESKTOP-LVSV9Q5（家）　·　**v0.2.5**（衛教頁補上列印樣式，未動判定邏輯）　·　Git push：✅ 已推（`124a8b2` 工具改動、`0d3c054` 文件）

> 本次一併補交 2026-08-06 那輪留在工作區、標記「待推」的 `agents.md`／`handoff.md`
> 更新（Google 表單垃圾桶事件的排查紀錄）——它們與本次的修改在同一個檔案裡，分不開。

前一筆：2026-08-06 @ DESKTOP-LVSV9Q5（家）· v0.2.4（營運面排查與修復，沒動程式碼）· 文件當時未推
再前一筆：2026-08-05（晚）@ DESKTOP-LVSV9Q5（家）· v0.2.4（加現場競賽版＋交接文件）· `578a57e`
再前一筆：2026-08-05（傍晚，現場競賽版架構建立＋首次重置測試）@ DESKTOP-LVSV9Q5（家）· `b4d212b`（另有 `a53d06d`）

> L3 Obsidian：本專案**未建立**筆記（未經 project-init、`agents.md` 未登記 vault 路徑），
> 因此本次同樣沒有 L3 紀錄。要補的話先跑 project-init。
