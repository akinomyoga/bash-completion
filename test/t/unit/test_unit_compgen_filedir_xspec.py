import pytest

from conftest import assert_bash_exec, assert_complete, prepare_fixture_dir


@pytest.mark.bashcomp(cmd=None, ignore_env=r"^\+COMPREPLY=|^[-+]_comp_xspecs=")
class TestUnitFiledirXspec:
    @pytest.fixture(scope="class")
    def functions(self, request, bash):
        assert_bash_exec(
            bash,
            "_comp_xspecs[xspec1]='!*.txt'; "
            "_comp_xspecs[xspec2]=; "
            "_comp_xspecs[xspec4]='*.txt'; "
            "complete -F _filedir_xspec xspec{1..4}",
        )

    @pytest.fixture
    def fixture_dir(self, request, bash):
        ret, _, _ = prepare_fixture_dir(
            request,
            files=["a.txt", "b.TXT", "c.dat", "d.bin"],
            dirs=[],
        )
        return ret

    def test_1(self, bash, functions, fixture_dir):
        """Test the pattern for an extension"""
        completion = assert_complete(bash, "xspec1 ", cwd=fixture_dir)
        assert completion == sorted("a.txt b.TXT".split())

    def test_2(self, bash, functions, fixture_dir):
        """Test an empty _comp_xspecs entry"""
        completion = assert_complete(bash, "xspec2 ", cwd=fixture_dir)
        assert completion == sorted("a.txt b.TXT c.dat d.bin".split())

    def test_3(self, bash, functions, fixture_dir):
        """Test an unset _comp_xspecs entry"""
        completion = assert_complete(bash, "xspec3 ", cwd=fixture_dir)
        assert completion == sorted("a.txt b.TXT c.dat d.bin".split())

    def test_4(self, bash, functions, fixture_dir):
        """Test an exclusion pattern"""
        completion = assert_complete(bash, "xspec4 ", cwd=fixture_dir)
        assert completion == sorted("c.dat d.bin".split())
