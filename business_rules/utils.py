from decimal import Decimal, Inexact, Context
from datetime import datetime, tzinfo
import re
import inspect
import numpy as np
from dateutil.parser import parse
import pytz

iso_8601_regex = re.compile("^\d{4}(-\d\d(-\d\d(T\d\d:\d\d(:\d\d)?(\.\d+)?(([+-]\d\d:\d\d)|Z)?)?)?)?$")

def fn_name_to_pretty_label(name):
    return ' '.join([w.title() for w in name.split('_')])

def export_rule_data(variables, actions):
    """ export_rule_data is used to export all information about the
    variables, actions, and operators to the client. This will return a
    dictionary with three keys:
    - variables: a list of all available variables along with their label, type and options
    - actions: a list of all actions along with their label and params
    - variable_type_operators: a dictionary of all field_types -> list of available operators
    """
    from . import operators
    actions_data = actions.get_all_actions()
    variables_data = variables.get_all_variables()
    variable_type_operators = {}
    for variable_class in inspect.getmembers(operators, lambda x: getattr(x, 'export_in_rule_data', False)):
        variable_type = variable_class[1] # getmembers returns (name, value)
        variable_type_operators[variable_type.name] = variable_type.get_all_operators()

    return {"variables": variables_data,
            "actions": actions_data,
            "variable_type_operators": variable_type_operators}

def float_to_decimal(f):
    """
    Convert a floating point number to a Decimal with
    no loss of information. Intended for Python 2.6 where
    casting float to Decimal does not work.
    """
    n, d = f.as_integer_ratio()
    numerator, denominator = Decimal(n), Decimal(d)
    ctx = Context(prec=60)
    result = ctx.divide(numerator, denominator)
    while ctx.flags[Inexact]:
        ctx.flags[Inexact] = False
        ctx.prec *= 2
        result = ctx.divide(numerator, denominator)
    return result

def is_valid_date(date_string: str) -> bool:
    return bool(iso_8601_regex.match(date_string))

def get_year(date_string: str):
    timestamp = get_date(date_string)
    return timestamp.year

def get_month(date_string: str):
    timestamp = get_date(date_string)
    return timestamp.month

def get_day(date_string: str):
    timestamp = get_date(date_string)
    return timestamp.day

def get_hour(date_string: str):
    timestamp = get_date(date_string)
    return timestamp.hour

def get_minute(date_string: str):
    timestamp = get_date(date_string)
    return timestamp.minute

def get_second(date_string: str):
    timestamp = get_date(date_string)
    return timestamp.second

def get_microsecond(date_string: str):
    timestamp = get_date(date_string)
    return timestamp.microsecond

def get_date_component(component: str, date_string: str):
    component_func_map = {
        "year": get_year,
        "month": get_month,
        "day": get_day,
        "hour": get_hour,
        "minute": get_minute,
        "microsecond": get_microsecond,
        "second": get_second
    }
    component_function = component_func_map.get(component)
    if component_function:
        return component_function(date_string)
    else:
        return get_date(date_string)

def get_date(date_string: str):
    """
    Returns a utc timestamp for comparison
    """
    date = parse(date_string)
    utc = pytz.UTC
    if date.tzinfo is not None and date.tzinfo.utcoffset(date) is not None:
        # timezone aware
        return date.astimezone(utc)
    else:
        return utc.localize(date)

def is_complete_date(date_string: str) -> bool:
    try:
        datetime.fromisoformat(date_string)
    except:
        try:
            datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        except:
            return False
        return True
    return True

def get_dict_key_val(dict_to_get: dict, key):
    return dict_to_get.get(key)

vectorized_is_complete_date = np.vectorize(is_complete_date)
vectorized_date_component = np.vectorize(get_date_component)
vectorized_is_valid = np.vectorize(is_valid_date)
vectorized_get_dict_key = np.vectorize(get_dict_key_val)
vectorized_len = np.vectorize(len)
