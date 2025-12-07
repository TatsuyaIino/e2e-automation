import pytest
from gacha_scenario import run_gacha_scenario

# 抽選回数のパターンテスト（最小 / 中間 / 最大 みたいなイメージ）
@pytest.mark.parametrize("draw_count", [1, 3, 10])
def test_gacha_scenario(draw_count):
    result = run_gacha_scenario(draw_count)
    assert result is True, f"ガチャ{draw_count}回のシナリオが失敗しました"
