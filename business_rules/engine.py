from .fields import FIELD_NO_INPUT

def run_all(rule_list,
            defined_variables,
            defined_actions,
            stop_on_first_trigger=False):

    rule_was_triggered = False
    for rule in rule_list:
        result = run(rule, defined_variables, defined_actions)
        if result:
            rule_was_triggered = True
            if stop_on_first_trigger:
                return True
    return rule_was_triggered

def run(rule, defined_variables, defined_actions):
    conditions, actions = rule['conditions'], rule['actions']
    rule_triggered = check_conditions_recursively(conditions, defined_variables)
    if rule_triggered:
        do_actions(actions, defined_actions)
        return True
    return False


def check_conditions_recursively(conditions, defined_variables):
    keys = list(conditions.keys())
    if keys == ['all']:
        assert len(conditions['all']) >= 1
        for condition in conditions['all']:
            if not check_conditions_recursively(condition, defined_variables):
                return False
        return True

    elif keys == ['any']:
        assert len(conditions['any']) >= 1
        for condition in conditions['any']:
            if check_conditions_recursively(condition, defined_variables):
                return True
        return False

    else:
        # help prevent errors - any and all can only be in the condition dict
        # if they're the only item
        assert not ('any' in keys or 'all' in keys)
        return check_condition(conditions, defined_variables)

def check_condition(condition, defined_variables):
    """ Checks a single rule condition - the condition will be made up of
    variables, values, and the comparison operator. The defined_variables
    object must have a variable defined for any variables in this condition.
    """
    name, op, value = condition['name'], condition['operator'], condition['value']
    params = condition.get('params') or {}
    operator_type = _get_variable_value(defined_variables, name, params)
    return _do_operator_comparison(operator_type, op, value)

def _get_variable_value(defined_variables, name, params):
    """ Call the function provided on the defined_variables object with the
    given name (raise exception if that doesn't exist) and casts it to the
    specified type.

    Returns an instance of operators.BaseType
    """
    method = getattr(defined_variables, name, None)
    if not method:
        raise AssertionError("Variable {0} is not defined in class {1}".format(
                name, defined_variables.__class__.__name__))
    _check_params_valid_for_method(method, params, 'variable')
    val = method(**params)
    return method.field_type(val)

def _do_operator_comparison(operator_type, operator_name, comparison_value):
    """ Finds the method on the given operator_type and compares it to the
    given comparison_value.

    operator_type should be an instance of operators.BaseType
    comparison_value is whatever python type to compare to
    returns a bool
    """
    def fallback(*args, **kwargs):
        raise AssertionError("Operator {0} does not exist for type {1}".format(
            operator_name, operator_type.__class__.__name__))
    method = getattr(operator_type, operator_name, fallback)
    if getattr(method, 'input_type', '') == FIELD_NO_INPUT:
        return method()
    return method(comparison_value)


def do_actions(actions, defined_actions):
    for action in actions:
        method_name = action['name']
        params = action.get('params') or {}
        method = getattr(defined_actions, method_name, None)
        if not method:
            raise AssertionError("Action {0} is not defined in class {1}"\
                    .format(method_name, defined_actions.__class__.__name__))
        _check_params_valid_for_method(method, params, 'action')
        method(**params)

def _check_params_valid_for_method(method, given_params, method_type):
    """ Verifies that the given parameters match the names of those defined in
    the variable or action decorator. Raise an error if one of the sets contains
    a parameter that the other does not.
    """
    defined_params = [param.get('name') for param in getattr(method, 'params', []) if param.get('name')]
    missing_params = set(defined_params).difference(given_params)
    if missing_params:
        raise AssertionError("Missing parameters {0} for {1} {2}"\
                .format(', '.join(missing_params), method_type, method.__name__))

    invalid_params = set(given_params).difference(defined_params)
    if invalid_params:
        raise AssertionError("Invalid parameters {0} for {1} {2}"\
                .format(', '.join(invalid_params), method_type, method.__name__))
