import os
import sys

import pytest

from conftest import assert_bash_exec, assert_complete


class TestMake:
    @pytest.fixture
    def remove_extra_makefile(self, bash):
        yield
        # For some reason macos make doesn't actually create extra_makefile
        if sys.platform != "darwin":
            os.remove(f"{bash.cwd}/make/extra_makefile")

    @pytest.mark.complete("make -f Ma", cwd="make")
    def test_1(self, completion):
        assert completion == "kefile"

    @pytest.mark.complete("make .", cwd="make", require_cmd=True)
    def test_2(self, bash, completion, remove_extra_makefile):
        """Hidden targets."""
        assert completion == ".cache/ .test_passes".split()

    @pytest.mark.complete("make .cache/", cwd="make", require_cmd=True)
    def test_3(self, bash, completion, remove_extra_makefile):
        assert completion == ".cache/1 .cache/2".split()

    @pytest.mark.complete("make ", cwd="shared/empty_dir")
    def test_4(self, completion):
        assert not completion

    @pytest.mark.complete("make -j ")
    def test_5(self, completion):
        assert completion

    @pytest.mark.complete("make ", cwd="make", require_cmd=True)
    def test_6(self, bash, completion, remove_extra_makefile):
        assert completion == "all clean extra_makefile install sample".split()

    @pytest.mark.complete("make .cache/.", cwd="make", require_cmd=True)
    def test_7(self, bash, completion, remove_extra_makefile):
        assert completion == ".cache/.1 .cache/.2".split()

    @pytest.mark.complete("make -C make ", require_cmd=True)
    def test_8(self, bash, completion, remove_extra_makefile):
        assert completion == "all clean extra_makefile install sample".split()

    @pytest.mark.complete("make -nC make ", require_cmd=True)
    def test_8n(self, bash, completion, remove_extra_makefile):
        assert completion == "all clean extra_makefile install sample".split()

    @pytest.mark.complete("make -", require_cmd=True)
    def test_9(self, completion):
        assert completion


@pytest.mark.bashcomp(require_cmd=True, cwd="make/test2")
class TestMake2:
    def test_github_issue_544_1(self, bash):
        completion = assert_complete(bash, "make ab")
        assert completion == "c/xyz"

    def test_github_issue_544_2(self, bash):
        completion = assert_complete(bash, "make 1")
        assert completion == "23/"

    def test_github_issue_544_3(self, bash):
        completion = assert_complete(bash, "make 123/")
        assert completion == ["123/xaa", "123/xbb"]

    def test_github_issue_544_4(self, bash):
        completion = assert_complete(bash, "make 123/xa")
        assert completion == "a"

    def test_subdir_1(self, bash):
        completion = assert_complete(bash, "make sub1")
        assert completion == "test/bar/"

    def test_subdir_2(self, bash):
        completion = assert_complete(bash, "make sub2")
        assert completion == "test/bar/alpha"

    def test_subdir_3(self, bash):
        completion = assert_complete(bash, "make sub3")
        assert completion == "test/"

    def test_subdir_4(self, bash):
        completion = assert_complete(bash, "make sub4")
        assert completion == "sub4test/bar/ sub4test2/foo/gamma".split()


@pytest.mark.bashcomp(cmd="make", require_cmd=True, cwd="make/test3")
class TestMake3:
    """Targets whose plain name is also the prefix of other targets.

    Completion models target names as filesystem paths and collapses shared
    prefixes to `dir/'.  But a `/' in a target name is not necessarily a
    directory boundary: when a plain, runnable target is also the prefix of
    `/'-suffixed siblings (`MyProgram' with `MyProgram/fast', `install' with
    `install/local'), the plain form must still be offered, not dropped in favor
    of only the suffixed ones.
    """

    def test_all_targets(self, bash):
        """Both plain and `/'-suffixed forms are offered together."""
        completion = assert_complete(bash, "make ")
        assert completion == [
            "MyProgram",
            "MyProgram/fast",
            "all",
            "clean",
            "clean/fast",
            "install",
            "install/",
        ]

    def test_single_child_keeps_plain(self, bash):
        """`MyProgram' (single `/fast' child) keeps its plain form."""
        completion = assert_complete(bash, "make My")
        assert completion == ["MyProgram", "MyProgram/fast"]

    def test_single_child_drill_in(self, bash):
        completion = assert_complete(bash, "make MyProgram/")
        assert completion == "fast"

    def test_multi_child_keeps_plain(self, bash):
        """`install' (multiple children) is offered alongside `install/'."""
        completion = assert_complete(bash, "make install")
        assert completion == ["install", "install/"]

    def test_multi_child_drill_in(self, bash):
        completion = assert_complete(bash, "make install/")
        assert completion == ["install/local", "install/strip"]

    def test_clean_keeps_plain(self, bash):
        """A second single-child case: `clean' is kept next to `clean/fast'."""
        completion = assert_complete(bash, "make clean")
        assert completion == ["clean", "clean/fast"]


@pytest.mark.bashcomp(cmd="make", require_cmd=True)
class TestMakeOptions:
    """Plain-and-prefix targets are still both offered when the makefile or its
    directory is selected via -f/-C.

    Run from the fixtures root so the -C/-f paths are relative to it.
    """

    def test_directory_option(self, bash):
        completion = assert_complete(bash, "make -C make/test3 install")
        assert completion == ["install", "install/"]

    def test_file_option(self, bash):
        completion = assert_complete(
            bash, "make -f make/test3/Makefile install"
        )
        assert completion == ["install", "install/"]


@pytest.mark.bashcomp(cmd="make", require_cmd=True, cwd="make/test4")
class TestMake4:
    """Edge cases of completing target names that contain `/'."""

    def test_all_targets(self, bash):
        completion = assert_complete(bash, "make ")
        assert completion == ["a/", "a/b", "dir/", "foo/bar"]

    def test_nested_real_prefix(self, bash):
        """`a/b' is a target *and* a prefix of `a/b/c': offer `a/' and `a/b'."""
        completion = assert_complete(bash, "make a")
        assert completion == ["a/", "a/b"]

    def test_nested_real_prefix_drill(self, bash):
        """Plain `a/b' survives alongside the deeper `a/b/c'."""
        completion = assert_complete(bash, "make a/b")
        assert completion == ["a/b", "a/b/c"]

    def test_non_target_prefix_collapses(self, bash):
        """`dir' is not a target, so it collapses to `dir/' (no plain `dir')."""
        completion = assert_complete(bash, "make dir")
        assert completion == "/"
        # Collapsed `dir/' must not get a trailing space (nospace is set).
        assert completion.endswith("/")

    def test_trailing_slash_target_limitation(self, bash):
        """Known limitation: a literal `foo/' target is not surfaced, but no
        spurious plain `foo' is invented either (so `foo' completes straight to
        the `foo/bar' leaf)."""
        completion = assert_complete(bash, "make foo")
        assert completion == "/bar"


@pytest.mark.bashcomp(cmd="make", require_cmd=True, cwd="make/test3")
class TestMakeNospace:
    """A plain target and its `dir/' prefix coexist, so nospace must be decided
    by scanning every candidate, not just the first.

    `install/' is a prefix to drill into and needs `compopt -o nospace' so no
    space is appended; plain `install' does not.  compopt is all-or-nothing for
    the whole completion, and the two share an unspecified order in COMPREPLY,
    so nospace has to be requested whenever *any* candidate ends in `/'.  The
    completion result strips trailing whitespace and so cannot show this, so
    drive the completion directly with a shadowed `compopt' that records the
    request.
    """

    def test_nospace_requested_when_any_candidate_is_a_prefix(self, bash):
        assert_bash_exec(bash, "_comp_load -- make", want_output=None)
        # Shadowing compopt both records the `-o nospace' request and lets us
        # call the completion outside a real completion (where the builtin would
        # otherwise error).
        assert_bash_exec(
            bash,
            "compopt() { local a; for a; do [[ $a == nospace ]] && _ns=1; "
            "done; }",
            want_output=None,
        )
        try:
            # Emulate readline completing `make install<TAB>'.
            out = assert_bash_exec(
                bash,
                "COMP_LINE='make install' COMP_POINT=12 "
                "COMP_WORDS=(make install) COMP_CWORD=1 _ns=; "
                "_comp_cmd_make make install make; "
                'printf "%s\\t%s\\n" "$_ns" "${COMPREPLY[*]}"',
                want_output=True,
            ).strip()
        finally:
            assert_bash_exec(
                bash,
                "unset -f compopt; unset -v _ns COMP_LINE COMP_POINT "
                "COMP_WORDS COMP_CWORD COMPREPLY",
                want_output=None,
            )

        nospace, _, reply = out.partition("\t")
        # The scenario really is the mixed one: plain target and drill-in prefix.
        assert reply.split() == ["install", "install/"]
        # ...so nospace must have been requested (for the `install/' prefix).
        assert nospace == "1"
