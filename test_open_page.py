from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # ブラウザ起動（headless=False で画面を表示）
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # ページを開く
        page.goto("https://example.com")
        print("ページタイトル:", page.title())

        # 少し待ってから閉じる
        page.wait_for_timeout(2000)
        browser.close()

if __name__ == "__main__":
    main()
