# Targets whose plain name is also the prefix of another target, for the `make'
# target completion.  A `/' in a target name is not necessarily a directory
# boundary: here a plain, runnable target coexists with `/'-suffixed siblings.
# Both forms must be offered by completion, not collapsed away in favor of only
# the suffixed ones:
#
#   - single-child case: `MyProgram' alongside `MyProgram/fast'
#   - multi-child case:  `install' alongside `install/local' and `install/strip'

all: MyProgram

MyProgram MyProgram/fast:
	@echo $@

clean clean/fast:
	@echo $@

install install/local install/strip:
	@echo $@
