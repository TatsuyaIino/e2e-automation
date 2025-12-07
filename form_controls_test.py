from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # ① チェックボックスを操作
        page.goto("https://the-internet.herokuapp.com/checkboxes")

        # 最初のチェックボックスを ON にする
        first_checkbox = page.locator("input[type='checkbox']").nth(0)
        first_checkbox.check()

        is_checked = first_checkbox.is_checked()
        print("1つ目のチェックボックス ON？:", is_checked)

        if is_checked:
            print("✅ チェックボックス操作 成功")
        else:
            print("❌ チェックボックス操作 失敗")

        # ② ドロップダウンを操作
        page.goto("https://the-internet.herokuapp.com/dropdown")

        # value="2" の選択肢を選ぶ
        page.select_option("#dropdown", "2")

        # 現在選択されている value を取得
        selected_value = page.locator("#dropdown").input_value()
        print("選択された値:", selected_value)

        if selected_value == "2":
            print("✅ ドロップダウン選択 成功")
        else:
            print("❌ ドロップダウン選択 失敗")

        # ③ 結果ページのスクリーンショットを保存
        page.screenshot(path="form_controls_result.png", full_page=True)
        print("📷 スクリーンショット保存: form_controls_result.png")

        page.wait_for_timeout(2000)
        browser.close()

if __name__ == "__main__":
    main()
