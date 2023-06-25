__version__ = '1.1.2'

from .engine import run_all
from .engine import run_all_with_results
from .utils import export_rule_data

# Appease pyflakes by "using" these exports
assert run_all
assert run_all_with_results
assert export_rule_data
