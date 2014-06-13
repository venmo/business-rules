from decimal import Decimal, Inexact, Context

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
    actions_data = actions.get_all_actions()
    variables_data = variables.get_all_variables()
    variable_type_operators = {}
    from .operators import (StringType,
                            NumericType,
                            BooleanType,
                            SelectType,
                            SelectMultipleType)
    for variable_type in [StringType,
                          NumericType,
                          BooleanType,
                          SelectType,
                          SelectMultipleType]:
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

