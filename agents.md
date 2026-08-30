# sarcopenia-clinic｜專案藍圖

肌少症篩檢紀錄工具。**門診與社區**兩種場域都用，以 SARC-CalF 初篩 → AWGS 2019 判定。

需求來源：[`rdq/RDQ-spec-sarcopenia-screening-20260729.md`](rdq/RDQ-spec-sarcopenia-screening-20260729.md)（`status: confirmed`）。
**改動前先讀那份規格卡**，特別是「❌ 排除項」——那些是刻意不做的，不要自作主張加回來。

## 檔案

| 檔案 | 用途 |
|---|---|
| `README.md` | 公開 repo 首頁：用途、現場注意事項、限制與授權 |
| `index.html` | 主工具（單頁、原生 JS、無外部相依、可離線） |
| `education.html` | 靜態衛教頁，QR code 指向這裡，**不含任何個人資料** |
| `quiz.html` | 衛教測驗分享頁：海報圖＋Wordwall 測驗嵌入＋連回 education.html，**獨立頁面、不影響篩檢流程** |
| `compete.html` | 現場競賽版轉址頁，QR code 固定指向這裡；內容轉址到當輪 Wordwall `/play/` 連結 |
| `tools/reset-competition.py`／`.ps1` | 一鍵重置現場競賽排行榜：建新課業＋換 `compete.html` 轉址目標＋push，見 handoff.md |
| `quiz-links.docx` | 給同事的連結彙整表（真超連結格式，方便複製轉傳），內容跟 handoff.md 保持一致，需要時手動更新 |
| `images/sarcopenia-quiz-poster.jpg` | 衛教海報（NotebookLM 生成，已人工修正 AI 生圖亂碼文字，見 handoff.md） |
| `sw.js` | Service Worker。網頁 network-first、其餘 cache-first |
| `manifest.webmanifest` | PWA 設定 |
| `icon-*.png` | PWA 圖示（`tools/make-icons.py` 產生） |
| `docs/google-form-fields.md` | Google 表單欄位對照表與建表注意事項 |
| `tools/make-qr.py` | 重新產生並嵌入衛教頁 QR（只有網址變更時才需要跑） |
| `tools/make-icons.py` | 重新產生 PWA 圖示 |
| `tools/create-google-form.gs` | Apps Script：一鍵建立表單與回應試算表，並印出 `FORM_ID`／`ENTRY` |
| `rdq/` | RDQ 需求規格卡 |

## 臨床與資料守則（不可違反）

1. **性別編碼 `0 = 女`、`1 = 男`**。介面顯示中文，送出時才轉碼。分析前用平均身高交叉驗證。
2. **n < 10 的組別不呈現百分比**，只列分子分母。統計頁已內建這個規則。
3. **不上傳姓名、電話、出生月日**。只送代號、出生年、性別與測量值。
4. **表單載入時強制清空**，防止殘留上一位受檢者的資料。
5. **多台裝置同時作業時，每台要各選一個工作站代碼（A–H）**，代號格式
   `YYYYMMDD-<工作站><流水號>`。沒有這個字母，兩台裝置會產生一樣的代號。
6. 小腿圍只是肌肉量的**代理指標**，結果文字一律寫「疑似」，並提示轉介 DXA／BIA 確認。
7. 給付條文不寫死，只註明核對當期公告。
8. **初篩陰性也要開放加測握力／五次起坐**（選填）。SARC-F 敏感度有限，初篩陰性不等於
   沒有肌少症；加測才發現低下的個案要在結果卡標註「以實測為準」。不要把這條「簡化」掉。
9. **少測一項就不是完整判定**。五次起坐留空時不得宣稱「肌力與體能均未達切點」，
   要標為部分評估並寫明無法排除嚴重肌少症。沒測到的項目在明細寫「未測」，不可留白。
10. **判定用的切點要顯示在數字旁邊**（男女不同），現場才能當場核對、事後才能回查。

## 切點（AWGS 2019）

| 項目 | 男 | 女 |
|---|---|---|
| 握力 | < 28 kg | < 18 kg |
| 五次起坐 | ≥ 12 秒 | ≥ 12 秒 |
| 小腿圍 | < 34 cm | < 33 cm |

初篩陽性：SARC-F ≥ 4 或 SARC-CalF ≥ 11。

## 路線圖

- [x] RDQ 需求訪談與規格卡（`status: confirmed`）
- [x] 主工具 `index.html`：兩段式判定、計時器、離線佇列、本機當日統計
- [x] 靜態衛教頁 `education.html` 與固定 QR
- [x] 場域（門診／社區）與工作站代碼（A–H，防多台撞號）
- [x] 建立公開 repo 並開啟 GitHub Pages
- [x] 修正初篩陽性按鈕「按了沒反應」（只靠 smooth 捲動當回饋，捲動失效就全無變化）
- [x] 初篩陰性開放加測（選填）、五次起坐改選填並標示部分評估
- [x] 判定切點顯示在數字旁；未測項目明寫「未測」
- [x] PWA 離線（`sw.js` + manifest + 圖示）、版本顯示與更新提示
- [x] PWA 離線的操作說明改寫進 README，**不放在工具首頁**
      （2026-07-29 試過放首頁，現場判斷太複雜而移除；要再加請先確認會不會擋住流程）
- [ ] 手機實掃 QR 驗證
- [ ] 替換 SARC-F 為指定的已驗證中文版並補引用出處
- [ ] 骨鬆專案入口頁互放連結
- [x] **接 Google 表單**（2026-07-29，已端到端驗證，含性別編碼交叉驗證）。
      回應試算表即統計分析的資料來源，連結見 `handoff.md`。
- [x] **衛教頁內建闖關小遊戲**（2026-08-27，v0.2.6）——「存肌力五連闖」，遊戲放內容前面（遊戲先）、
      列印隱藏、深色模式維持亮色；與 Wordwall 測驗並存（用途不同）；五題經潘醫師審定通過。
      **改表單時不要動題目順序或刪題重建**，`entry` 編號會變。
- [x] **存肌接接樂**（2026-08-30，v0.2.7）——canvas 動作小遊戲，獨立頁 `存肌接接樂.html`，
      入口在 education.html 五連闖下方連結卡；知識卡九則取自 education.html 審定內容；
      不進 PRECACHE（比照 quiz.html）。遊戲呈現形式待潘醫師過目。
- [x] **Wordwall 衛教測驗**（2026-08-05 建立，同日下午調整）：`肌少症衛教小測驗`，
      10 題選擇題，**Clouds 主題**（原 Indigo）、中文介面（`/tc/` 路徑）、答案選項已拉齊字數。
      連結與嵌入細節見 `handoff.md`「🔗 Wordwall 測驗」。**測驗開始前的封面卡片固定黑底，
      任何主題都改不掉，是平台限制**。
- [x] **NotebookLM 衛教海報**（2026-08-05）：`images/sarcopenia-quiz-poster.jpg`。
      **AI 生圖的內嵌文字有 9 處亂碼，已人工去背填色重繪修正**——這是 NotebookLM infographic
      功能的已知限制，日後若重新生成同類海報，**務必逐字核對內嵌文字**，不要只看排版順不順眼。
      標題字級同日下午也縮小過一次，避免手機預覽視窗裁到字。
- [x] `quiz.html`：海報＋測驗嵌入的分享頁，`index.html` 結果頁加了一個非強制連結入口
      （人潮多時可略過，只做篩檢不做測驗）。
- [x] **現場競賽版**（2026-08-05）：`compete.html` 轉址頁＋`tools/reset-competition.py`
      一鍵重置排行榜工具，QR code（`images/quiz-competition-qr.png`）印出來後永久不用換。
      已端到端測試過（建課業→更新轉址→push→curl 驗證 GitHub Pages 生效）。
      **未驗證**：真人拿手機掃 QR code 實測。細節見 `handoff.md`「🔗 Wordwall 測驗－現場競賽版」。
- [ ] 醫院電腦（如 X108521）若要在現場執行重置，需另外裝 Wordwall CLI 登入狀態
      （`~/.wordwall/state.json` 不跟著 repo 走，每台電腦要各自登入一次）。
- [x] **排查並修復現場試跑「App 顯示送出成功、試算表沒資料」事件**（2026-08-06）：
      根因是 Google 表單被移進 Drive 垃圾桶（已第二次），`send()` 用 `no-cors` 送出讓
      App 無法辨別表單拒收，這是架構性盲點、**沒有修掉，只有排查口訣**。已復原表單、
      驗證修復，並把表單與回應試算表搬進 Drive「門診工具-正式運作中」資料夾防止再誤刪。
      沒動程式碼，細節與排查口訣見 `handoff.md`「⚠️ 注意事項」第一條。
- [x] **衛教頁補上列印樣式**（2026-08-09，v0.2.5）：`education.html` 原本完全沒有
      `@media print`，等於直接印螢幕版。新增列印區塊，`@page` 用 A4∩Letter 交集
      `210mm 279.4mm`；深色模式變數在列印時覆蓋回淺色（否則深色手機列印整片黑底）；
      `.big` 由深色底反白字改為淺底黑字（未勾「背景圖形」時原本整段看不見）。
      實測內容總高 440.8mm，**關掉瀏覽器頁首頁尾為雙面兩頁**。

## 部署

公開 repo ＋ GitHub Pages，root 的 `index.html`。改檔 → commit → push，Pages 約 1–2 分鐘重建。

**改版務必同步三個版本號**（2026-07-30 更正，原本只寫兩個）：

| # | 位置 | 形式 |
|---|---|---|
| 1 | `sw.js` 的 `VERSION` | 常數 |
| 2 | `index.html` 的 `APP_VERSION` | 常數，JS 填進頁尾 `#appVer` |
| 3 | `education.html` 頁尾的 `v?.?.?` | **硬編字串，沒有 JS，最容易漏改** |

第 3 項原本沒寫進這裡，結果 `education.html` 一路停在 v0.1.0，直到 2026-07-30 才發現並統一到 0.2.4。
沒改的話，既有裝置上 cache-first 的檔案（圖示、manifest）不會更新；`education.html` 也在 `PRECACHE` 裡。
網頁本身是 network-first，只要裝置連得上網就一定拿到最新版，這是刻意的取捨——
臨床工具最怕平板卡在舊版沒人發現。

**GitHub 為 canonical**，repo 放在 `C:\projects\`，不要放進 OneDrive（`.git` 會產生衝突複本）。
醫院電腦沒有 `G:`，流程不依賴 Google Drive。

## 本機預覽

```
python -m http.server 8765 --directory C:\projects\sarcopenia-clinic
```

直接雙擊開 `index.html` 也可以（無外部相依），但**以 `file://` 開啟時 Service Worker
不會註冊**，測不到離線與更新提示，頁尾會顯示「不支援（此頁未透過網址開啟）」。
要驗離線就得走 http。驗證方式：連著開一次讓 SW 裝好 → 關掉伺服器 → 重新整理，
頁面應該照常出現。
