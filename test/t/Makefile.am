SUBDIRS = unit

EXTRA_DIST = \
	conftest.py \
	test_xfreerdp.py

all:

PYTEST = @PYTEST@

# Some tests require completions/ symlinks to be in place, which would be a
# chore to achieve in the build dir with VPATH builds (well not the symlinks,
# but the "main" files they target), e.g. "make distcheck". Therefore we test
# the installed tree instead, which isn't a bad idea in the first place.
installcheck-local:
	ABS_TOP_BUILDDIR="$(abs_top_builddir)" \
	BASH_COMPLETION_TEST_BASH_COMPLETION="$(DESTDIR)/$(pkgdatadir)/bash_completion" \
		$(PYTEST) $(PYTESTFLAGS) $(srcdir)

clean-local:
	$(RM) -R __pycache__
