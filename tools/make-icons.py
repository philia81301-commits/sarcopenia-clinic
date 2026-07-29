"""產生 PWA 圖示（可重複執行，結果固定）。

用法：python tools/make-icons.py
輸出：icon-192.png、icon-512.png、icon-512-maskable.png（放在 repo 根目錄）

maskable 版留了較大留白，Android 把圖示裁成圓形時「肌」字才不會被切到。
字型用微軟正黑體粗體；換電腦若沒有該字型，改 FONT 常數即可。
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ACCENT = (31, 111, 139)      # 與 index.html 的 --accent 同色
WHITE = (255, 255, 255)
FONT = r"C:\Windows\Fonts\msjhbd.ttc"
GLYPH = "肌"


def make(size: int, out: str, pad_ratio: float = 0.0) -> None:
    """畫一張圖示。pad_ratio 是四周留白佔邊長的比例（maskable 用）。"""
    # 先用 4 倍解析度畫再縮小，圓角和字邊才不會有鋸齒
    scale = 4
    big = size * scale
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    pad = int(big * pad_ratio)
    box = [pad, pad, big - pad - 1, big - pad - 1]
    radius = int((big - 2 * pad) * 0.22)
    d.rounded_rectangle(box, radius=radius, fill=ACCENT)

    inner = big - 2 * pad
    font = ImageFont.truetype(FONT, int(inner * 0.58))
    # 用實際字形邊界置中，不要靠 anchor 猜，中文字上下留白不對稱
    l, t, r, b = d.textbbox((0, 0), GLYPH, font=font)
    d.text((pad + (inner - (r - l)) / 2 - l,
            pad + (inner - (b - t)) / 2 - t),
           GLYPH, font=font, fill=WHITE)

    img.resize((size, size), Image.LANCZOS).save(ROOT / out)
    print(f"已產生 {out}（{size}×{size}）")


if __name__ == "__main__":
    make(192, "icon-192.png")
    make(512, "icon-512.png")
    make(512, "icon-512-maskable.png", pad_ratio=0.14)
