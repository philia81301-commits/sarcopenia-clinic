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
| `docs/google-form-fields.md` | Google 表單欄位對照表與建表注意事項 |
| `tools/make-qr.py` | 重新產生並嵌入衛教頁 QR（只有網址變更時才需要跑） |
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
- [ ] 建立 Google 表單並填入 `FORM_ID` 與 `ENTRY`（**未完成前不可正式收案**）
- [ ] 手機實掃 QR 驗證
- [ ] 替換 SARC-F 為指定的已驗證中文版並補引用出處
- [ ] 骨鬆專案入口頁互放連結

## 部署

公開 repo ＋ GitHub Pages，root 的 `index.html`。改檔 → commit → push，Pages 約 1–2 分鐘重建。
**GitHub 為 canonical**，repo 放在 `C:\projects\`，不要放進 OneDrive（`.git` 會產生衝突複本）。
醫院電腦沒有 `G:`，流程不依賴 Google Drive。

## 本機預覽

```
python -m http.server 8765 --directory C:\projects\sarcopenia-clinic
```

直接雙擊開 `index.html` 也可以（無外部相依），但用 http 比較接近實際部署環境。
