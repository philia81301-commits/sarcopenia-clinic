#!/usr/bin/env python3
"""
產生離線用的中文字型子集（供 index.html 內嵌／本地載入）。

為什麼需要這支腳本：
  Noto Sans TC / Serif TC 完整檔各 12MB / 17MB，直接帶著跑不切實際；
  但 Google Fonts CDN 的分割子集缺全形標點（，／：）與羅馬數字（Ⅰ Ⅱ Ⅲ），
  用了會滿頁豆腐字。所以自己從完整 variable font 切。

何時要重跑：
  **改動 index.html 的文字內容之後**（新增了原本沒有的字）。
  腳本會自動比對並在缺字時警告。

用法：
  python build_fonts.py
輸出：
  fonts/NotoSansTC-subset.woff2
  fonts/NotoSerifTC-subset.woff2
"""
import re
import sys
import urllib.request
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

HERE = Path(__file__).parent
HTML = HERE / "index.html"
FONTS = HERE / "fonts"

GF = "https://raw.githubusercontent.com/google/fonts/main/ofl"
SOURCES = [
    ("NotoSansTC-VF.ttf", "NotoSansTC-subset.woff2",
     f"{GF}/notosanstc/NotoSansTC%5Bwght%5D.ttf"),
    ("NotoSerifTC-VF.ttf", "NotoSerifTC-subset.woff2",
     f"{GF}/notoseriftc/NotoSerifTC%5Bwght%5D.ttf"),
]


def ensure_source(path: Path, url: str) -> None:
    """來源 VF 檔共 27MB、不進 git，缺少時自動下載（換電腦後首次執行會用到）。"""
    if path.exists():
        return
    print(f"下載來源字型 {path.name} …（約 10–17 MB）")
    FONTS.mkdir(exist_ok=True)
    urllib.request.urlretrieve(url, path)


def chars_used_in_html() -> set:
    """抓 index.html 內所有會被排版的字元（排除 script/style 內容與標籤本身）。"""
    html = HTML.read_text(encoding="utf-8")
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    return {c for c in body if c.isprintable() and not c.isspace()}


def big5_common() -> set:
    """
    Big5 常用字區（0xA440–0xC67E，約 5400 字）當安全邊際：
    日後補內容時多半不會再撞到缺字，不必每次都重跑這支腳本。
    """
    out = set()
    for hi in range(0xA4, 0xC7):
        for lo in list(range(0x40, 0x7F)) + list(range(0xA1, 0xFF)):
            try:
                out.add(bytes([hi, lo]).decode("big5"))
            except UnicodeDecodeError:
                pass
    return out


def main() -> int:
    used = chars_used_in_html()
    target = used | big5_common()

    total_missing = {}
    for src_name, out_name, url in SOURCES:
        src = FONTS / src_name
        ensure_source(src, url)

        cov = {chr(c) for c in TTFont(src).getBestCmap()}
        # 只有「簡報實際用到卻不存在於字型」才算問題；Big5 補集缺字無所謂
        missing = used - cov
        if missing:
            total_missing[src_name] = missing

        keep = "".join(sorted(target & cov))
        args = [
            str(src),
            f"--text={keep}",
            "--output-file=" + str(FONTS / out_name),
            "--flavor=woff2",
            "--layout-features=*",
            "--no-hinting",
            "--desubroutinize",
            # variable font：保留完整字重軸，一個檔案供 400/500/700/900 共用
            "--drop-tables+=DSIG",
        ]
        subset.main(args)
        size = (FONTS / out_name).stat().st_size
        print(f"{out_name}: {size/1024/1024:.2f} MB（{len(keep)} 字元）")

    if total_missing:
        print("\n[警告] 以下字元簡報有用到，但字型檔沒有，會顯示為豆腐字：")
        for f, m in total_missing.items():
            print(f"  {f}: {''.join(sorted(m))}")
        return 2

    print("\n完成，未發現缺字。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
