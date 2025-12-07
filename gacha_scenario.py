import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

GACHA_URL = "https://stg.croissant.buzz/gacha/XOkAY2E3"


def run_gacha_scenario(draw_count: int = 3) -> bool:
    """
    ガチャE2Eシナリオを1本実行する。
    成功したら True、どこかで失敗したら False を返す。
    """
    success = False

    with sync_playwright() as p:
        # CI環境（GitHub Actions）では headless=True、ローカルでは False
        is_ci = os.getenv("CI") == "true"
        browser = p.chromium.launch(headless=is_ci)
        page = browser.new_page()

        try:
            print(f"\n=== ガチャシナリオ開始：{draw_count} 回 ===")

            # ① ページアクセス
            print("① ガチャページにアクセス")
            try:
                page.goto(GACHA_URL, wait_until="domcontentloaded", timeout=15000)
                print("   → ページ遷移完了")
            except PlaywrightTimeoutError:
                print("❌ ページ読み込みがタイムアウトしました")
                return False

            # ② 「ガチャを回す」ボタンをクリック
            print("② 「ガチャを回す」ボタンをクリック")
            page.get_by_text("ガチャを回す", exact=True).click()

            # ③ 抽選回数を選択
            print(f"③ 抽選回数 {draw_count} を選択")
            page.get_by_text(str(draw_count), exact=True).click()

            # ④ 「スタート」ボタンをクリック
            print("④ スタートボタンをクリック")
            page.get_by_text("スタート").click()

            # ⑤ カード表示待ち
            print("⑤ カード表示待ち")
            try:
                cards = page.get_by_alt_text("ガチャ結果")
                cards.first.wait_for(timeout=10000)
            except PlaywrightTimeoutError:
                print("❌ カードが表示されませんでした（タイムアウト）")
                return False

            # ⑥ カードを順番にめくる（1枚のカードを draw_count 回タップする想定）
            visible_card = cards.first
            print("⑥ カードを順番にめくります")

            for i in range(draw_count):
                print(f"   → {i+1}回目のタップ")
                visible_card.click()
                page.wait_for_timeout(800)

            # ⑦ 結果画面への遷移待ち
            print("⑦ 結果画面への遷移待ち")
            page.wait_for_timeout(3000)

            # ⑧ 結果画面の文言チェック
            print("⑧ 結果画面の文言チェック")
            body_text = page.text_content("body") or ""
            if "結果" in body_text:
                print("✅ テスト成功っぽい：結果画面に遷移しています")
                success = True
            else:
                print("⚠ 『結果』という文言が見つかりませんでした")
                success = False

            # ⑨ スクリーンショット保存
            screenshot_name = f"gacha_result_{draw_count}.png"
            page.screenshot(path=screenshot_name, full_page=True)
            print(f"📷 スクリーンショット保存: {screenshot_name}")

            return success

        finally:
            browser.close()


if __name__ == "__main__":
    # 手動確認用
    run_gacha_scenario(3)
