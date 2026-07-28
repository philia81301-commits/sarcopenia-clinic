# 肌少症篩檢紀錄工具

門診與社區篩檢站都適用的肌少症篩檢工具。單頁 HTML、無外部相依、可離線使用。

**線上使用：** https://philia81301-commits.github.io/sarcopenia-clinic/
**衛教頁（可直接給受檢者）：** https://philia81301-commits.github.io/sarcopenia-clinic/education.html

## 這個工具做什麼

兩段式流程：

1. **初篩** —— SARC-F 問卷加小腿圍（SARC-CalF）。SARC-F ≥ 4 或 SARC-CalF ≥ 11 為陽性。
2. **判定** —— 初篩陽性者續做 **AWGS 2019**：握力、五次起坐、小腿圍，分出「肌少症可能」、
   「疑似肌少症」與「疑似嚴重肌少症」。

判定為陽性時，畫面會出現一個 QR code，受檢者用手機掃描即可看到運動與蛋白質衛教內容。
該頁面不含任何個人資料。

## 現場使用注意

- **每台裝置開工前先選一個不同的工作站代碼（A–H）**，否則多台裝置會產生相同的受檢者代號。
- **姓名記在紙本對照表**，不要輸入工具。系統只送出代號、場域、出生年、性別與測量值。
- 小腿圍請照畫面上的量測提示做，不同人量出來的數字才能互相比較。
- 沒有網路也可以照常填寫，紀錄會存在裝置本機，回到有網路的地方按「一鍵補送」。

## 限制

小腿圍只是肌肉量的**代理指標**，本工具不能用於確診。確定診斷需在醫療院所以 DXA 或 BIA
測量肌肉量。所有結果文字皆標示為「疑似」，並提示轉介。

工具內不寫死健保給付條文，請以就診當時的公告為準。

## 開發

| 檔案 | 用途 |
|---|---|
| `index.html` | 主工具 |
| `education.html` | 靜態衛教頁 |
| `docs/google-form-fields.md` | Google 表單欄位對照表 |
| `tools/make-qr.py` | 重新產生並嵌入衛教頁 QR（只有網址變更時需要） |
| `agents.md` / `handoff.md` | 專案藍圖與進度交接 |
| `rdq/` | 需求規格卡 |

本機預覽：

```
python -m http.server 8765 --directory .
```

## 授權

© 2026 潘湘如　·　[CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.zh-hant)

製作：潘湘如醫師｜家醫科。介面與程式實作由 Claude 協助。
問題回報請開 [Issue](https://github.com/philia81301-commits/sarcopenia-clinic/issues)。
