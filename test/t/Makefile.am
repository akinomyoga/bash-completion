SUBDIRS = unit

EXTRA_DIST = \
	conftest.py \
	test_fio.py \
	test_man.py \
	test_pgrep.py \
	test_ps.py \
	test_pylint.py \
	test_ss.py \
	test_ssh_keygen.py \
	test_ssh_keyscan.py \
	test_tox.py \
	test_tshark.py

all:

PYTEST = @PYTEST@

check-local:
	ABS_TOP_BUILDDIR="$(abs_top_builddir)" \
		$(PYTEST) $(PYTESTFLAGS) $(srcdir)

clean-local:
	$(RM) -R __pycache__
