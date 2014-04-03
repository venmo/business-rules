import inspect

from . import fields
from .utils import fn_name_to_pretty_description


class BaseActions(object):
    """ Classes that hold a collection of actions to use with the rules
    engine should inherit from this.
    """
    @classmethod
    def get_all_actions(cls):
        methods = inspect.getmembers(cls)
        return [{'name': m[0],
                 'description': m[1].description,
                 'params': m[1].params
                } for m in methods if getattr(m[1], 'is_rule_action', False)]

def rule_action(description=None, params=None):
    """ Decorator to make a function into a rule action
    """
    def wrapper(func):
        # Verify field name is valid
        valid_fields = [getattr(fields, f) for f in dir(fields) \
                if f.startswith("FIELD_")]
        for param_name, field_type in params.items():
            if field_type not in valid_fields:
                raise AssertionError("Unknown field type {0} specified for"\
                        " action {1} param {2}".format(
                        field_type, func.__name__, param_name))

        func.is_rule_action = True
        func.description = description \
                or fn_name_to_pretty_description(func.__name__)
        func.params = params
        return func
    return wrapper
