import inspect

from . import fields
from .utils import fn_name_to_pretty_label


class BaseActions(object):
    """ Classes that hold a collection of actions to use with the rules
    engine should inherit from this.
    """
    @classmethod
    def get_all_actions(cls):
        methods = inspect.getmembers(cls)
        return [{'name': m[0],
                 'label': m[1].label,
                 'params': m[1].params
                } for m in methods if getattr(m[1], 'is_rule_action', False)]

def _validate_action_parameters(func, params):
    """ Verifies that the parameters specified are actual parameters for the
    function `func`, and that the field types are FIELD_* types in fields.
    """
    if params is not None:
        # Verify field name is valid
        valid_fields = [getattr(fields, f) for f in dir(fields) \
                if f.startswith("FIELD_")]
        for param in params:
            param_name, field_type = param['name'], param['fieldType']
            if param_name not in func.__code__.co_varnames:
                raise AssertionError("Unknown parameter name {0} specified for"\
                        " action {1}".format(
                        param_name, func.__name__))

            if field_type not in valid_fields:
                raise AssertionError("Unknown field type {0} specified for"\
                        " action {1} param {2}".format(
                        field_type, func.__name__, param_name))

def rule_action(label=None, params=None):
    """ Decorator to make a function into a rule action
    """
    def wrapper(func):
        params_ = params
        if isinstance(params, dict):
            params_ = [dict(label=fn_name_to_pretty_label(name),
                           name=name,
                           fieldType=field_type) \
                      for name, field_type in params.items()]
        _validate_action_parameters(func, params_)
        func.is_rule_action = True
        func.label = label \
                or fn_name_to_pretty_label(func.__name__)
        func.params = params_
        return func
    return wrapper
