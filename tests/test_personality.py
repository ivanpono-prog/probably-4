from personality import (
    hostility_level,
    should_confirm,
    should_delay,
    should_become_gentleman,
)


def test_hostility_progression():
    assert hostility_level(0) == 1
    assert hostility_level(2) == 1
    assert hostility_level(3) == 2
    assert hostility_level(6) == 2
    assert hostility_level(7) == 3


def test_no_early_confirmations():
    for _ in range(100):
        assert should_confirm(0) is False


def test_no_early_delays():
    for _ in range(100):
        assert should_delay(0) is False


def test_gentleman_unavailable_before_five():
    for count in range(5):
        assert should_become_gentleman(count) is False
