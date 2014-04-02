import inspect
from .utils import fn_name_to_pretty_description


class BaseActions(object):
    """ Classes that hold a collection of actions to use with the rules
    engine should inherit from this.
    """
    @classmethod
    def get_all_actions(cls):
        methods = inspect.getmembers(cls, predicate=inspect.ismethod)
        return [{'name': m[0],
                 'description': m[1].description
                } for m in methods if getattr(m[1], 'is_rule_action', False)]

def rule_action(description=None):
    """ Decorator to make a function into a rule action
    """
    def wrapper(func):
        func.is_rule_action = True
        func.description = description \
                or fn_name_to_pretty_description(func.__name__)
        return func
    return wrapper
