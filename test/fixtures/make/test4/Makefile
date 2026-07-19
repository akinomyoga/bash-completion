# Edge cases for make target completion `/'-handling.

# Nested real-prefix: `a/b' is both a runnable target and a path-prefix of
# `a/b/c'.  Completion must offer `a/' (drill-in) *and* plain `a/b'.
a/b a/b/c a/d:
	@echo $@

# Non-firing: `dir' is NOT itself a target, only a shared path prefix, so
# completion must still collapse to `dir/' and must not invent a plain `dir'.
dir/all dir/rule:
	@echo $@

# Known limitation: a target whose name literally ends in `/'.  The real `foo/'
# is not surfaced by completion, but no spurious plain `foo' is invented either.
foo/ foo/bar:
	@echo $@
