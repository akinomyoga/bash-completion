import pytest
from conftest import assert_bash_exec


class TestWho:
    @pytest.mark.complete(
        "who --", require_cmd=True, xfail="! who --help &>/dev/null"
    )
    def test_1(self, bash, completion):
        assert_bash_exec(bash, "who --help")
        assert completion
