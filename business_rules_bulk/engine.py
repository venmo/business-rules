from .fields import FIELD_NO_INPUT


def run_all(rule_list, defined_variables, defined_actions, stop_on_first_trigger=False):
    values_satisfying_rules = values_not_satisfying_rules = []
    for rule in rule_list:
        values_satisfying_rules, values_not_satisfying_rules = run(rule, defined_variables, defined_actions)
        if are_rules_executed(values_satisfying_rules):
            if stop_on_first_trigger:
                return values_satisfying_rules, values_not_satisfying_rules

    return values_satisfying_rules, values_not_satisfying_rules


def run(rule, defined_variables, defined_actions):
    conditions, actions = rule['conditions'], rule['actions']
    values_satisfying_rules, values_not_satisfying_rules = check_conditions_recursively(conditions, defined_variables)
    if are_rules_executed(values_satisfying_rules):
        do_actions(actions, defined_actions, values_satisfying_rules)
    return values_satisfying_rules, values_not_satisfying_rules


def check_conditions_recursively(conditions, defined_variables):
    keys = list(conditions.keys())
    if keys == ['all']:
        assert len(conditions['all']) >= 1

        for condition in conditions['all']:
            values_satisfying_rules, values_not_satisfying_rules = check_conditions_recursively(condition,
                                                                                                defined_variables)
        return values_satisfying_rules, values_not_satisfying_rules

    elif keys == ['any']:
        assert len(conditions['any']) >= 1
        for condition in conditions['any']:
            values_satisfying_rules, values_not_satisfying_rules = check_conditions_recursively(condition,
                                                                                                defined_variables)

            return values_satisfying_rules, values_not_satisfying_rules
    else:
        # help prevent errors - any and all can only be in the condition dict
        # if they're the only item
        assert not ('any' in keys or 'all' in keys)
        return check_condition(conditions, defined_variables)


def check_condition(condition, defined_variables):
    """
    Checks a single rule condition - the condition will be made up of
    variables, values, and the comparison operator. The defined_variables
    object must have a variable defined for any variables in this condition.
    """
    name, op, value = condition['name'], condition['operator'], condition['value']
    operator_type = _get_variable_value(defined_variables, name)
    return _do_operator_comparison(operator_type, op, value)


def _get_variable_value(defined_variables, name):
    """ Call the function provided on the defined_variables object with the
    given name (raise exception if that doesn't exist) and casts it to the
    specified type.

    Returns an instance of operators.BaseType
    """

    def fallback(*args, **kwargs):
        raise AssertionError("Variable {0} is not defined in class {1}".format(
            name, defined_variables.__class__.__name__))

    method = getattr(defined_variables, name, fallback)
    val = method()
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


def do_actions(actions, defined_actions, values_satisfying_rules):
    for action in actions:
        method_name = action['name']

        def fallback(*args, **kwargs):
            raise AssertionError("Action {0} is not defined in class {1}"
                                 .format(method_name, defined_actions.__class__.__name__))

        params = action.get('params') or {}
        method = getattr(defined_actions, method_name, fallback)
        method(values_satisfying_rules, **params)


def are_rules_executed(values):
    """

    :param values:
    :return:
    """
    return len(values) > 0
