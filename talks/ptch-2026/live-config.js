/* ============================================================
   現場互動設定檔（簡報端 index.html 與觀眾作答頁 live.html 共用）
   ------------------------------------------------------------
   Firebase 專案沿用「肥胖醫學會 AI 演講」那一個（obesity-ai-firebase），
   只換集合名稱。⚠️ 新集合要先在 Firestore 安全性規則加上白名單，
   規則片段見同目錄 firestore-rules-snippet.txt；沒加之前簡報會顯示
   「互動未啟用」，其餘頁面照常播放。
   ============================================================ */
window.TALK_LIVE = {
  firebaseConfig: {
    apiKey:            "AIzaSyBXXCQ5x0iWicUfe47U5LTgz3_83MrDNB4",
    authDomain:        "obesity-ai-firebase.firebaseapp.com",
    projectId:         "obesity-ai-firebase",
    storageBucket:     "obesity-ai-firebase.firebasestorage.app",
    messagingSenderId: "343364935435",
    appId:             "1:343364935435:web:ce3e80555052f4f3c1cc0e"
  },

  /* 本場專屬集合名稱，避免與其他場次資料混用。改名要同步改安全性規則。 */
  wordcloudCollection: 'ptch_sarcopenia_2026_wordcloud',
  pollCollection:      'ptch_sarcopenia_2026_poll',

  /* 第 2 頁投票選項。id 只能是 a/b/c/d（安全性規則有白名單）。 */
  pollQuestion: '您的門診現在怎麼處理肌少症？',
  pollOptions: [
    { id: 'a', label: '沒有特別篩，遇到再說' },
    { id: 'b', label: '會問跌倒、走路慢，但沒有固定量表' },
    { id: 'c', label: '有做 SARC-F 或握力，但後續轉介不固定' },
    { id: 'd', label: '有完整流程：篩檢、判定、轉介、追蹤' }
  ],

  /* 第 26 頁文字雲題目 */
  wordcloudQuestion: '回去之後，您會先改門診的哪一件事？',

  /* 觀眾作答頁網址（第 2 頁 QR 指向這裡） */
  audienceUrl: 'https://philia81301-commits.github.io/sarcopenia-clinic/talks/ptch-2026/live.html',

  /* 每支手機文字雲最多送出幾則（擋洗版，存 localStorage，非強制） */
  wordcloudMaxPerDevice: 3
};

window.TALK_LIVE.isConfigured = function () {
  var k = window.TALK_LIVE.firebaseConfig.apiKey;
  return typeof k === 'string' && k.indexOf('PASTE_') !== 0 && k.length > 10;
};
