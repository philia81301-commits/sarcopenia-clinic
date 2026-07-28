"""產生衛教頁的固定 QR code，並直接嵌入 index.html。

用法（在 repo 根目錄）：
    python tools/make-qr.py

會做兩件事：
1. 產生 tools/qr-education.svg（保留一份原始檔）
2. 把 index.html 中 <!-- QR:BEGIN --> 與 <!-- QR:END --> 之間的內容換成該 SVG

網址改變時（換 repo 名、換自訂網域）改下面的 URL 再重跑一次。
執行後的網頁本身沒有任何外部相依，這個腳本只在維護時用得到。
"""

import re
from pathlib import Path

import qrcode
from qrcode.image.svg import SvgPathImage

URL = "https://philia81301-commits.github.io/sarcopenia-clinic/education.html"

ROOT = Path(__file__).resolve().parent.parent
SVG_PATH = ROOT / "tools" / "qr-education.svg"
INDEX = ROOT / "index.html"

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=2,
)
qr.add_data(URL)
qr.make(fit=True)
svg = qr.make_image(image_factory=SvgPathImage).to_string(encoding="unicode")

# 去掉固定的 mm 尺寸，改由 CSS 控制大小；補白底避免深色模式掃不到
svg = re.sub(r'\s(width|height)="[^"]*"', "", svg, count=2)
side = qr.modules_count + qr.border * 2
svg = svg.replace(
    ">", f'><rect width="{side}" height="{side}" fill="#ffffff"/>', 1
)

SVG_PATH.write_text(svg, encoding="utf-8")

html = INDEX.read_text(encoding="utf-8")
new_html, n = re.subn(
    r"(<!-- QR:BEGIN -->).*?(<!-- QR:END -->)",
    lambda m: m.group(1) + "\n    " + svg + "\n    " + m.group(2),
    html,
    flags=re.S,
)
if n != 1:
    raise SystemExit(f"index.html 找不到唯一的 QR 標記區塊（找到 {n} 個），沒有寫入。")

INDEX.write_text(new_html, encoding="utf-8")
print(f"已嵌入 QR（{URL}），index.html 更新完成。")
