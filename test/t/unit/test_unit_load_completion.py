import pytest

from conftest import assert_bash_exec, bash_env_saved


@pytest.mark.bashcomp(cmd=None, cwd="_comp_load")
class TestLoadCompletion:
    def test_cmd_path_1(self, bash):
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

    def test_cmd_path_2(self, bash):
        with bash_env_saved(bash) as bash_env:
            bash_env.write_variable("PATH", "$PWD/bin:$PATH", quote=False)
            output = assert_bash_exec(
                bash, "_comp_load cmd1", want_output=True
            )
            assert output.strip() == "cmd1: sourced from prefix1"
            output = assert_bash_exec(
                bash, "_comp_load cmd2", want_output=True
            )
            assert output.strip() == "cmd2: sourced from prefix1"
