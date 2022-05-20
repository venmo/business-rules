__version__ = '1.1.1'

from .engine import run
from .engine import run_all
from .utils import export_rule_data

# Appease pyflakes by "using" these exports
assert run
assert run_all
assert export_rule_data
