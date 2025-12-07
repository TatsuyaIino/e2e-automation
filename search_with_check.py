from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # ① Wikipediaを開く
        page.goto("https://www.wikipedia.org")

        # ② 検索ボックスに入力
        keyword = "Playwright Python"
        page.fill("input[name='search']", keyword)

        # ③ 検索ボタンをクリック
        page.click("button[type='submit']")

        # ④ 結果が出るまで少し待つ
        page.wait_for_timeout(2000)

        # ⑤ ページタイトルに Playwright が含まれているかチェック
        title = page.title()
        print("ページタイトル:", title)

        if "Playwright" in title:
            print("✅ テスト成功：タイトルに 'Playwright' が含まれています")
        else:
            print("❌ テスト失敗：タイトルに 'Playwright' が含まれていません")

        page.wait_for_timeout(2000)
        browser.close()

if __name__ == "__main__":
    main()
