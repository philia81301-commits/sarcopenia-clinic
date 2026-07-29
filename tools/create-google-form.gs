/**
 * 肌少症篩檢工具｜一鍵建立 Google 表單與回應試算表
 *
 * 做完三件事：
 *   1. 建立含 11 個簡答題、全部非必填的表單（欄位定義與 docs/google-form-fields.md 一致）
 *   2. 建立並連結回應試算表
 *   3. 印出 index.html 要用的 FORM_ID 與 ENTRY，可直接複製貼上
 *
 * 使用方式：
 *   1. 開 https://script.google.com/ → 新增專案
 *   2. 把這整個檔案的內容貼進去，取代原本的 myFunction
 *   3. 上方函式選 createSarcopeniaForm → 執行 → 第一次會要求授權，允許
 *   4. 執行完成後看「執行紀錄」，把印出來的兩段常數貼回 index.html
 *
 * 注意：
 *   - 用**個人 Google 帳號**執行，表單才會是「任何人皆可填寫、免登入」。
 *     公司或醫院的 Workspace 帳號可能預設限制組織內填寫，那樣現場平板會送不出去。
 *   - 這支程式可以重複執行，但每跑一次就會多一份表單，不要重複跑。
 */

function createSarcopeniaForm() {

  // [程式欄位, 表單題目]．順序即題目順序，與 docs/google-form-fields.md 對應
  var FIELDS = [
    ['site',      '受檢場域（clinic＝門診／community＝社區）'],
    ['code',      '受檢者代號（YYYYMMDD-工作站流水號）'],
    ['birthYear', '出生年（西元）'],
    ['gender',    '生理性別（0＝女／1＝男）'],
    ['falls',     '過去一年跌倒次數'],
    ['calf',      '小腿圍（公分）'],
    ['sarcf',     'SARC-F 分數'],
    ['stage1',    '初篩結果（positive／negative）'],
    ['grip',      '握力（公斤）'],
    ['sts',       '五次起坐（秒）'],
    ['result',    '判定結果']
  ];

  var form = FormApp.create('肌少症篩檢紀錄');
  form.setDescription(
    '由「肌少症篩檢紀錄工具」自動送出，請勿手動填寫。\n' +
    'https://philia81301-commits.github.io/sarcopenia-clinic/'
  );
  form.setCollectEmail(false);
  form.setLimitOneResponsePerUser(false);
  form.setAllowResponseEdits(false);
  form.setAcceptingResponses(true);

  // 建題：全部簡答、全部非必填
  // （初篩陰性者的握力／五次起坐、未測項目都會是空值，設必填會讓整筆被靜默拒收）
  var items = FIELDS.map(function (f) {
    var item = form.addTextItem().setTitle(f[1]).setRequired(false);
    return { key: f[0], item: item };
  });

  // 回應試算表
  var ss = SpreadsheetApp.create('肌少症篩檢紀錄（回覆）');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  // 用「假資料＝欄位名」產生預填連結，再依值反查 entry 編號
  // （不依賴參數順序，比較不會錯）
  var response = form.createResponse();
  items.forEach(function (o) {
    response = response.withItemResponse(o.item.createResponse(o.key));
  });
  var prefilled = response.toPrefilledUrl();

  var byValue = {};
  prefilled.split('?')[1].split('&').forEach(function (pair) {
    var kv = pair.split('=');
    if (kv[0].indexOf('entry.') === 0) byValue[decodeURIComponent(kv[1])] = kv[0];
  });

  // 取 formResponse 要用的長 ID（/forms/d/e/<這一段>/viewform）
  var published = form.getPublishedUrl();
  var m = published.match(/\/forms\/d\/e\/([^\/]+)\//);
  var formId = m ? m[1] : '（抓不到，請從發布網址 /forms/d/e/ 後面那段自行複製）';

  var missing = items.filter(function (o) { return !byValue[o.key]; })
                     .map(function (o) { return o.key; });

  var lines = [];
  lines.push('');
  lines.push('=========== 貼回 index.html 最上方 ===========');
  lines.push('const FORM_ID = "' + formId + '";');
  lines.push('const ENTRY = {');
  items.forEach(function (o, i) {
    lines.push('  ' + o.key + ':"' + (byValue[o.key] || '') + '"' +
               (i === items.length - 1 ? '' : ','));
  });
  lines.push('};');
  lines.push('============================================');
  lines.push('');
  lines.push('表單編輯網址：' + form.getEditUrl());
  lines.push('表單填寫網址：' + published);
  lines.push('回應試算表　：' + ss.getUrl());
  if (missing.length) {
    lines.push('');
    lines.push('⚠️ 有欄位沒抓到 entry 編號：' + missing.join('、') + '　請回報。');
  }

  Logger.log(lines.join('\n'));
  return lines.join('\n');
}
