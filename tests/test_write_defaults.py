# 3rd party
from coincidence.regressions import AdvancedFileRegressionFixture
from libgunshotmatch.method import Method

# this package
from gunshotmatch_method_writer import default_method_toml


def test_write_defaults(advanced_file_regression: AdvancedFileRegressionFixture):

	m = Method()
	# m.consolidate.name_filter = ["siloxy"]
	advanced_file_regression.check(default_method_toml(m))
