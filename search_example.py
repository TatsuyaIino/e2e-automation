from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.wikipedia.org")

        # 入力フォームに文字を入力
        page.fill("input[name='search']", "Playwright Python")

        # 検索ボタンをクリック
        page.click("button[type='submit']")

        # 3秒待つ
        page.wait_for_timeout(3000)

        browser.close()

if __name__ == "__main__":
    main()
