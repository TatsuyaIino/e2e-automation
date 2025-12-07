from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 練習用ログインページ
        page.goto("https://the-internet.herokuapp.com/login")

        # ID(ユーザー名)を入力
        page.fill("#username", "tomsmith")

        # パスワードを入力
        page.fill("#password", "SuperSecretPassword!")

        # ログインボタンをクリック
        page.click("button[type='submit']")

        # 遷移を待つ
        page.wait_for_timeout(2000)

        # 成功メッセージが出たかチェック
        success = page.locator(".flash.success").inner_text()

        print("ログイン結果:", success)

        if "You logged into a secure area!" in success:
            print("✅ テスト成功：ログインできました")
        else:
            print("❌ テスト失敗：ログイン失敗")

        browser.close()

if __name__ == "__main__":
    main()
