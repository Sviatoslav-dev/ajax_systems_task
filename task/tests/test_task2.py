import pytest

from task2 import cordinates


@pytest.mark.parametrize('given_dd, expected_ddm', [(-180, "180^0W"),
                                                    (-180.0, "180^0W"),
                                                    (-13.912, "13^54.72W"),
                                                    (0, "0^0E"),
                                                    (180.0, "180^0E"),
                                                    (180, "180^0E"),
                                                    (170.0323, "170^1.938E")])
def test_cordinates(given_dd, expected_ddm):
    assert cordinates(given_dd) == expected_ddm
