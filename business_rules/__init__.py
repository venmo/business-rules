__version__ = '1.0.10'

import logging
from .engine import run_all
from .utils import export_rule_data

# Appease pyflakes by "using" these exports
assert run_all
assert export_rule_data

logging.getLogger("business_rules").addHandler(logging.NullHandler())
