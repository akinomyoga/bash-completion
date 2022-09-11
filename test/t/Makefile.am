SUBDIRS = unit

EXTRA_DIST = \
	conftest.py \
	test_alias.py \
	test_apt_cache.py \
	test_cd.py

all:

PYTEST = @PYTEST@

check-local:
	ABS_TOP_BUILDDIR="$(abs_top_builddir)" \
		$(PYTEST) $(PYTESTFLAGS) $(srcdir)

clean-local:
	$(RM) -R __pycache__
