"""每場肌少症衛教小測驗現場競賽開始前，一鍵重置排行榜。

用法（在 repo 根目錄，或直接跑 tools/reset-competition.ps1）：
    python tools/reset-competition.py

會做四件事：
1. 用 Wordwall 建立一份新的課業（乾淨排行榜、暱稱登入、不能重玩、結束不顯示答案）。
   舊的那份不會刪除，留在 Wordwall「我的結果」裡當作上一輪的存檔，不會遺失資料。
2. 把新課業的學生 /play/ 連結寫進 compete.html（QR code 掃到的固定網址本身不變，
   只有裡面轉址的目標換掉）。
3. git commit + push，讓 GitHub Pages 更新。
4. 印出這輪的 Wordwall 結果頁網址，活動快結束時打開來看排行榜、公布前五名。

**執行後大約要等 30-60 秒 GitHub Pages 才會真的生效**，不要在活動開始前最後幾秒才跑。
需要先跑過 wordwall 技能的登入設定（見 ~/.claude/skills/wordwall 的
`python wordwall.py doctor --login`）。
"""

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

WORDWALL_DIR = Path.home() / ".claude" / "skills" / "wordwall"
sys.path.insert(0, str(WORDWALL_DIR))

try:
    import wordwall as ww  # noqa: E402  複用既有的登入/選擇器邏輯，不重寫一份
except ImportError:
    sys.exit(f"找不到 {WORDWALL_DIR}\\wordwall.py，這支腳本要跟 wordwall 技能裝在同一台電腦上跑。")

RESOURCE_URL = "https://wordwall.net/resource/117017138/肌少症衛教小測驗"
REPO = Path(__file__).resolve().parent.parent
COMPETE_HTML = REPO / "compete.html"


def find_play_link(page) -> str | None:
    values = page.locator("input").evaluate_all(
        "els => els.map(e => e.value || '').filter(Boolean)")
    hrefs = page.locator("a").evaluate_all(
        "els => els.map(e => e.href || '').filter(Boolean)")
    body = page.locator("body").inner_text()
    candidates = values + hrefs + re.findall(
        r"https?://(?:www\.)?wordwall\.net/play/[^\s\"'<>]+", body)
    for v in candidates:
        if re.match(r"^https?://(?:www\.)?wordwall\.net/play/", v):
            return v
    return None


def create_assignment(title: str) -> tuple[str, str]:
    """開一份新課業，回傳 (play_link, results_url)。"""
    sync_playwright = ww._need_playwright()
    with sync_playwright() as p:
        browser, ctx = ww._context(p, headless=True)
        page = ctx.new_page()
        if not ww._verify_logged_in(page):
            browser.close()
            sys.exit("Wordwall 登入已失效，先跑一次 `python wordwall.py doctor --login`。")

        try:
            page.goto(RESOURCE_URL, wait_until="networkidle")
            page.locator(".js-assignment-button:visible").first.click()
            title_field = page.locator(".js-results-title")
            title_field.wait_for(state="visible", timeout=15000)

            page.locator("#register_name").click()
            page.locator("#deadline_none").click()
            ww._set_checkbox(page, "#gameover_review", False)      # 結束不顯示答案
            ww._set_checkbox(page, "#gameover_leaderboard", True)  # 開排行榜
            ww._set_checkbox(page, "#gameover_restart", False)     # 不能重玩
            title_field.fill(title)

            page.locator(".js-next-start").click()

            # 耐心輪詢取代固定 sleep，避開已知的抓連結逾時 bug
            link = None
            for _ in range(20):
                page.wait_for_timeout(500)
                link = find_play_link(page)
                if link:
                    break

            # 不論上面輪詢有沒有抓到連結，都回 /myresults 用標題找到這份作業的
            # 專屬結果頁——這一步同時是「保險路徑」，也用來取得真正的結果頁網址
            # （而不是仍停在資源頁的網址），活動結束後就是打開這個網址看排行榜。
            page.goto(f"{ww.BASE}/myresults", wait_until="networkidle")
            items = page.locator("a.js-result-item")
            target_href = None
            for i in range(items.count()):
                item = items.nth(i)
                name = item.locator(".js-item-name").inner_text().strip()
                if name == title:
                    target_href = item.get_attribute("href")
                    break
            if not target_href:
                if link:
                    sys.exit(f"作業已建立、連結也抓到了（{link}），但在 /myresults 對不到"
                             f"「{title}」這個標題去確認結果頁網址，去 Wordwall 網站手動確認一下。")
                sys.exit(f"作業可能已建立，但在 /myresults 找不到「{title}」，"
                         f"去 Wordwall 網站手動確認。")

            results_url = target_href if target_href.startswith("http") else f"{ww.BASE}{target_href}"

            if not link:
                page.goto(results_url, wait_until="networkidle")
                page.wait_for_timeout(1500)
                link = find_play_link(page)
                if not link:
                    sys.exit(f"作業已建立（{results_url}），但連結還是撈不到，去上面網址手動複製。")

            return link, results_url
        except SystemExit:
            raise
        except Exception as e:  # noqa
            ww._dump_debug(page, "reset_competition_fail")
            sys.exit(f"建立作業失敗，原始錯誤：{e}")
        finally:
            browser.close()


def update_compete_html(play_link: str) -> None:
    html = COMPETE_HTML.read_text(encoding="utf-8")

    html, n1 = re.subn(
        r'(<!-- PLAY_URL:BEGIN -->\n<meta http-equiv="refresh" content="0; url=)[^"]*(">)',
        lambda m: m.group(1) + play_link + m.group(2),
        html,
    )
    html, n2 = re.subn(
        r'(<!-- PLAY_HREF:BEGIN --><a class="go-link" id="go" href=")[^"]*(">)',
        lambda m: m.group(1) + play_link + m.group(2),
        html,
    )
    if n1 != 1 or n2 != 1:
        sys.exit("compete.html 裡的標記找不到或不只一個，沒有寫入，"
                 "檢查一下檔案有沒有被手動改過標記註解。")

    COMPETE_HTML.write_text(html, encoding="utf-8")


def git_publish(round_title: str) -> None:
    subprocess.run(["git", "add", "compete.html"], cwd=REPO, check=True)
    result = subprocess.run(
        ["git", "commit", "-m", f"重置現場競賽排行榜：{round_title}"],
        cwd=REPO, capture_output=True, text=True,
    )
    if result.returncode != 0 and "nothing to commit" not in result.stdout:
        print(result.stdout, result.stderr)
        sys.exit("git commit 失敗，看上面訊息。")
    subprocess.run(["git", "push"], cwd=REPO, check=True)


def main():
    round_title = f"肌少症衛教小測驗－現場競賽版 {datetime.now():%Y-%m-%d %H:%M}"
    print(f"建立新一輪作業：{round_title}")
    play_link, results_url = create_assignment(round_title)
    print(f"拿到連結：{play_link}")

    update_compete_html(play_link)
    print("compete.html 已更新。")

    git_publish(round_title)
    print("已 push，GitHub Pages 大約 30-60 秒後生效。")

    print()
    print("=" * 50)
    print("QR code 不用換，掃到的還是同一張。")
    print(f"這輪結果頁（活動結束後打開看排行榜、公布前五名）：\n{results_url}")
    print("=" * 50)


if __name__ == "__main__":
    main()
