import inspect
from functools import wraps
from .utils import fn_name_to_pretty_label
from .operators import (BaseType,
                        NumericType,
                        StringType,
                        BooleanType,
                        SelectType,
                        SelectMultipleType,
                        GenericType,
                        DataframeType)

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


def rule_variable(field_type, label=None, options=None):
    """ Decorator to make a function into a rule variable
    """
    options = options or []
    def wrapper(func):
        if not (type(field_type) == type and issubclass(field_type, BaseType)):
            raise AssertionError("{0} is not instance of BaseType in"\
                    " rule_variable field_type".format(field_type))
        func.field_type = field_type
        func.is_rule_variable = True
        func.label = label \
                or fn_name_to_pretty_label(func.__name__)
        func.options = options
        return func
    return wrapper


def _rule_variable_wrapper(field_type, label):
    if callable(label):
        # Decorator is being called with no args, label is actually the decorated func
        return rule_variable(field_type)(label)
    return rule_variable(field_type, label=label)

def numeric_rule_variable(label=None):
    return _rule_variable_wrapper(NumericType, label)

def string_rule_variable(label=None):
    return _rule_variable_wrapper(StringType, label)

def boolean_rule_variable(label=None):
    return _rule_variable_wrapper(BooleanType, label)

def select_rule_variable(label=None, options=None):
    return rule_variable(SelectType, label=label, options=options)

def select_multiple_rule_variable(label=None, options=None):
    return rule_variable(SelectMultipleType, label=label, options=options)

def generic_rule_variable(label=None, options=None):
    return rule_variable(GenericType, label=label, options=options)

def dataframe_rule_variable(label=None, options=None):
    return rule_variable(DataframeType, label=label, options=options)
