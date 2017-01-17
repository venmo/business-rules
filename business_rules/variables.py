import inspect

import utils
from .operators import (
    BaseType,
    NumericType,
    StringType,
    BooleanType,
    SelectType,
    SelectMultipleType,
    DateTimeType,
    TimeType,
)
from .utils import fn_name_to_pretty_label


class BaseVariables(object):
    """
    Classes that hold a collection of variables to use with the rules
    engine should inherit from this.
    """

    @classmethod
    def get_all_variables(cls):
        methods = inspect.getmembers(cls)
        return [{
                    'name': m[0],
                    'label': m[1].label,
                    'field_type': m[1].field_type.name,
                    'options': m[1].options,
                    'params': m[1].params
                } for m in methods if getattr(m[1], 'is_rule_variable', False)]


def rule_variable(field_type, label=None, options=None, params=None):
    """
    Decorator to make a function into a rule variable
    :param field_type:
    :param label:
    :param options:
    :param params:
    :param inject_rule:
    :return:
    """
    options = options or []
    params = params or []

    def wrapper(func):
        if not (type(field_type) == type and issubclass(field_type, BaseType)):
            raise AssertionError("{0} is not instance of BaseType in" \
                                 " rule_variable field_type".format(field_type))

        params_wrapper = utils.params_dict_to_list(params)

        _validate_variable_parameters(func, params_wrapper)

        func.params = params
        func.field_type = field_type
        func.is_rule_variable = True
        func.label = label or fn_name_to_pretty_label(func.__name__)
        func.options = options

        return func

    return wrapper


def _rule_variable_wrapper(field_type, label, params=None):
    if callable(label):
        # Decorator is being called with no args, label is actually the decorated func
        return rule_variable(field_type, params=params)(label)

    return rule_variable(field_type, label=label, params=params)


def numeric_rule_variable(label=None, params=None):
    """
    Decorator to make a function into a numeric rule variable.

    NOTE: add **kwargs argument to receive Rule as parameters

    :param label: Label for Variable
    :param params: Parameters expected by the Variable function
    :return: Decorator function wrapper
    """
    return _rule_variable_wrapper(NumericType, label, params=params)


def string_rule_variable(label=None, params=None):
    """
    Decorator to make a function into a string rule variable.

    NOTE: add **kwargs argument to receive Rule as parameters

    :param label: Label for Variable
    :param params: Parameters expected by the Variable function
    :return: Decorator function wrapper
    """
    return _rule_variable_wrapper(StringType, label, params=params)


def boolean_rule_variable(label=None, params=None):
    """
    Decorator to make a function into a boolean rule variable.

    NOTE: add **kwargs argument to receive Rule as parameters

    :param label: Label for Variable
    :param params: Parameters expected by the Variable function
    :return: Decorator function wrapper
    """
    return _rule_variable_wrapper(BooleanType, label, params=params)


def select_rule_variable(label=None, options=None, params=None):
    """
    Decorator to make a function into a select rule variable.

    NOTE: add **kwargs argument to receive Rule as parameters

    :param label: Label for Variable
    :param options:
    :param params: Parameters expected by the Variable function
    :return: Decorator function wrapper
    """
    return rule_variable(SelectType, label=label, options=options, params=params)


def select_multiple_rule_variable(label=None, options=None, params=None):
    """
    Decorator to make a function into a select multiple rule variable.

    NOTE: add **kwargs argument to receive Rule as parameters

    :param label: Label for Variable
    :param options:
    :param params: Parameters expected by the Variable function
    :return: Decorator function wrapper
    """
    return rule_variable(SelectMultipleType, label=label, options=options, params=params)


def datetime_rule_variable(label=None, params=None):
    """
    Decorator to make a function into a datetime rule variable.

    NOTE: add **kwargs argument to receive Rule as parameters

    :param label:
    :param params:
    :return: Decorator function wrapper for DateTime values
    """

    return _rule_variable_wrapper(field_type=DateTimeType, label=label, params=params)


def time_rule_variable(label=None, params=None):
    """
    Decorator to make a function into a Time rule variable.

    NOTE: add **kwargs argument to receive Rule as parameters

    :param label:
    :param params:
    :return: Decorator function wrapper for Time values
    """

    return _rule_variable_wrapper(field_type=TimeType, label=label, params=params)


def _validate_variable_parameters(func, params):
    """
    Verifies that the parameters specified are actual parameters for the
    function `func`, and that the field types are FIELD_* types in fields.
    :param func:
    :param params:
    :return:
    """
    valid_fields = utils.get_valid_fields()

    if params is not None:
        for param in params:
            param_name, field_type = param['name'], param['field_type']

            if param_name not in func.__code__.co_varnames:
                raise AssertionError("Unknown parameter name {0} specified for variable {1}".format(
                    param_name, func.__name__))

            if field_type not in valid_fields:
                raise AssertionError("Unknown field type {0} specified for variable {1} param {2}".format(
                    field_type, func.__name__, param_name))
