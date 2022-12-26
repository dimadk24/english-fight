from common.list_utils import count_times


class TestCountTimes:
    def test_returns_zero_when_empty_list(self):
        assert count_times([], lambda x: x) == 0

    def test_returns_zero_when_zero_matches(self):
        assert count_times([1, 2, 3], lambda x: False) == 0

    def test_returns_one_when_one_match(self):
        assert count_times([1, 2, 3], lambda x: x == 1) == 1

    def test_returns_2_when_2_matches(self):
        assert count_times([1, 2, 3], lambda x: x < 3) == 2

    def test_returns_len_when_all_match(self):
        assert count_times([1, 2, 3, 5, ''], lambda x: True) == 5
