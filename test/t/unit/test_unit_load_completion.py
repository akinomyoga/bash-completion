import pytest
import os

from conftest import assert_bash_exec, bash_env_saved, prepare_fixture_dir


@pytest.mark.bashcomp(cmd=None, cwd="_comp_load")
class TestLoadCompletion:
    @pytest.fixture
    def fixture_dir(self, request, bash):
        tmpdir, _, _ = prepare_fixture_dir(request, files=[], dirs=[])
        assert_bash_exec(bash, "cp -R %s/* %s/" % (os.getcwd(), tmpdir))
        assert_bash_exec(bash, "mkdir -p %s/bin" % tmpdir)
        assert_bash_exec(
            bash, "ln -sf ../prefix1/bin/cmd1 %s/bin/cmd1" % tmpdir
        )
        assert_bash_exec(
            bash, "ln -sf ../prefix1/sbin/cmd2 %s/bin/cmd2" % tmpdir
        )
        return str(tmpdir)

    def test_cmd_path_1(self, bash, fixture_dir):
        with bash_env_saved(bash) as bash_env:
            bash_env.chdir(fixture_dir)
            assert_bash_exec(bash, "complete -r cmd1 || :", want_output=None)
            output = assert_bash_exec(
                bash, "_comp_load prefix1/bin/cmd1", want_output=True
            )
            assert output.strip() == "cmd1: sourced from prefix1"
            output = assert_bash_exec(
                bash, 'complete -p "$PWD/prefix1/bin/cmd1"', want_output=True
            )
            assert "/prefix1/bin/cmd1" in output
            assert_bash_exec(bash, "! complete -p cmd1", want_output=None)
            output = assert_bash_exec(
                bash, "_comp_load prefix1/sbin/cmd2", want_output=True
            )
            assert output.strip() == "cmd2: sourced from prefix1"
            output = assert_bash_exec(
                bash, "_comp_load bin/cmd1", want_output=True
            )
            assert output.strip() == "cmd1: sourced from prefix1"
            output = assert_bash_exec(
                bash, "_comp_load bin/cmd2", want_output=True
            )
            assert output.strip() == "cmd2: sourced from prefix1"

    def test_cmd_path_2(self, bash, fixture_dir):
        with bash_env_saved(bash) as bash_env:
            bash_env.chdir(fixture_dir)
            bash_env.write_variable("PATH", "$PWD/bin:$PATH", quote=False)
            output = assert_bash_exec(
                bash, "_comp_load cmd1", want_output=True
            )
            assert output.strip() == "cmd1: sourced from prefix1"
            output = assert_bash_exec(
                bash, "_comp_load cmd2", want_output=True
            )
            assert output.strip() == "cmd2: sourced from prefix1"
