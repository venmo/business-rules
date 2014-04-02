import inspect
from functools import wraps
from .utils import fn_name_to_pretty_description

TYPE_NUMERIC = 'numeric'
TYPE_STRING = 'string'

class BaseVariables(object):
    """ Classes that hold a collection of variables to use with the rules
    engine should inherit from this.
    """
    @classmethod
    def get_all_variables(cls):
        methods = inspect.getmembers(cls)
        return [{'name': m[0],
                 'description': m[1].description,
                 'return_type': m[1].return_type,
                 'options': m[1].options,
                } for m in methods if getattr(m[1], 'is_rule_variable', False)]


def rule_variable(return_type, description=None, options=None):
    """ Decorator to make a function into a rule variable
    """
    options = options or []
    def wrapper(func):
        func = _memoize_return_values(func)
        func.is_rule_variable = True
        func.description = description \
                or fn_name_to_pretty_description(func.__name__)
        func.return_type = return_type
        func.options = options
        return func
    return wrapper

def numeric_rule_variable(description=None):
    return rule_variable(TYPE_NUMERIC, description=description)

def string_rule_variable(description=None):
    return rule_variable(TYPE_STRING, description=description)

def _memoize_return_values(func):
    """ Simple memoization (cacheing) decorator, copied from
    http://code.activestate.com/recipes/577219-minimalistic-memoization/
    """
    cache= {}
    @wraps(func)
    def memf(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return memf
