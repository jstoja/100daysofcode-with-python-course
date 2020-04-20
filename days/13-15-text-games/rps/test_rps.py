import pytest

import rps


@pytest.mark.parametrize("name", ["player1", "player2"])
def test_print_header(capfd, name):
    rps.print_header(name)
    out, _ = capfd.readouterr()
    assert name in out


@pytest.fixture(params=[
    rps.Roll("rock", ["scissors"], ["paper"]),
    rps.Roll("paper", ["rock"], ["scissors"]),
    rps.Roll("scissors", ["paper"], ["rock"]),
])
def Pick1(request):
    return request.param

@pytest.fixture(params=[
    rps.Roll("rock", ["scissors"], ["paper"]),
    rps.Roll("paper", ["rock"], ["scissors"]),
    rps.Roll("scissors", ["paper"], ["rock"]),
])
def Pick2(request):
    return request.param


class TestRoll:
    def test_can_defeat(self, Pick1, Pick2):
        assert Pick1.can_defeat(Pick2)
