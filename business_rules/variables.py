import inspect
from functools import wraps
from .utils import fn_name_to_pretty_label
from .operators import (BaseType,
                        NumericType,
                        StringType,
                        BooleanType,
                        SelectType,
                        SelectMultipleType)

class BaseVariables(object):
    """ Classes that hold a collection of variables to use with the rules
    engine should inherit from this.
    """
    @classmethod
    def get_all_variables(cls):
        methods = inspect.getmembers(cls)
        return [{'name': m[0],
                 'label': m[1].label,
                 'field_type': m[1].field_type.name,
                 'options': m[1].options,
                } for m in methods if getattr(m[1], 'is_rule_variable', False)]


def rule_variable(field_type, label=None, options=None, cache_result=True):
    """ Decorator to make a function into a rule variable
    """
    options = options or []
    def wrapper(func):
        if not (type(field_type) == type and issubclass(field_type, BaseType)):
            raise AssertionError("{0} is not instance of BaseType in"\
                    " rule_variable field_type".format(field_type))
        func.field_type = field_type
        if cache_result:
            func = _memoize_return_values(func)
        func.is_rule_variable = True
        func.label = label \
                or fn_name_to_pretty_label(func.__name__)
        func.options = options
        return func
    return wrapper

def numeric_rule_variable(label=None):
    return rule_variable(NumericType, label=label)

def string_rule_variable(label=None):
    return rule_variable(StringType, label=label)

def boolean_rule_variable(label=None):
    return rule_variable(BooleanType, label=label)

def select_rule_variable(label=None, options=None):
    return rule_variable(SelectType, label=label, options=options)

def select_multiple_rule_variable(label=None, options=None):
    return rule_variable(SelectMultipleType, label=label, options=options)

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
