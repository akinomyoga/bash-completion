import pytest


class TestIp:
    @pytest.mark.complete("ip addr show type ", require_cmd=True)
    def test_addr_type(self, completion):
        assert "bridge" in completion
