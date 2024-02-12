import pytest


class TestWho:
    @pytest.mark.complete(
        "who --", require_cmd=True, xfail="! who --help 2>&1 | grep -qe --"
    )
    def test_1(self, bash, completion):
        assert completion
