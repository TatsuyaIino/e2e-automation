# summarize_results.py
import xml.etree.ElementTree as ET
import os
import re


def main() -> None:
    tests = failures = errors = skipped = 0
    all_tests: list[str] = []
    failed_tests: list[str] = []

    if not os.path.exists("report.xml"):
        # pytest 自体が動かなかったなど
        _write_env(0, 0, 0, 0, [], [])
        return

    tree = ET.parse("report.xml")
    root = tree.getroot()

    # <testsuite> と <testsuites> 両対応
    if root.tag == "testsuite":
        suites = [root]
    elif root.tag == "testsuites":
        suites = list(root)
    else:
        suites = []

    for suite in suites:
        tests += int(suite.attrib.get("tests", 0))
        failures += int(suite.attrib.get("failures", 0))
        errors += int(suite.attrib.get("errors", 0))
        skipped += int(suite.attrib.get("skipped", 0))

        for case in suite.iter("testcase"):
            name = case.attrib.get("name", "")

            # 例: test_gacha_scenario[10] → 抽選10回
            m = re.search(r"\[(\d+)\]", name)
            if m:
                draw = m.group(1)
                human_name = f"抽選{draw}回"
            else:
                human_name = name

            all_tests.append(human_name)

            has_problem = case.find("failure") is not None or case.find("error") is not None
            if has_problem:
                failed_tests.append(human_name)

    passed_tests = [t for t in all_tests if t not in failed_tests]
    _write_env(
        total=tests,
        passed=len(passed_tests),
        failed=len(failed_tests),
        skipped=skipped,
        passed_tests=passed_tests,
        failed_tests=failed_tests,
    )


def _write_env(
    total: int,
    passed: int,
    failed: int,
    skipped: int,
    passed_tests: list[str],
    failed_tests: list[str],
) -> None:
    """
    GITHUB_ENV に集計結果を書き込む。
    テスト一覧は Slack 用に「・抽選1回\\n・抽選3回...」形式で保存。
    """
    def format_list(items: list[str]) -> str:
        if not items:
            return "なし"
        # \n は後段の Slack 通知用に「\\n」（バックスラッシュ+n）として渡す
        return "\\n".join(f"・{x}" for x in items)

    env_path = os.environ.get("GITHUB_ENV")
    if not env_path:
        return

    with open(env_path, "a") as f:
        f.write(f"TEST_TOTAL={total}\n")
        f.write(f"TEST_PASSED={passed}\n")
        f.write(f"TEST_FAILED={failed}\n")
        f.write(f"TEST_SKIPPED={skipped}\n")
        f.write("PASSED_TESTS=" + format_list(passed_tests) + "\n")
        f.write("FAILED_TESTS=" + format_list(failed_tests) + "\n")


if __name__ == "__main__":
    main()
