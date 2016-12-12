import logging
from .fields import FIELD_NO_INPUT
from business_rules.service.log_service import LogService
from business_rules.validators import BaseValidator

logger = logging.getLogger(__name__)


def run_all(rule_list,
            defined_variables,
            defined_actions,
            defined_validators=BaseValidator(),
            stop_on_first_trigger=False,
            log_service=None):
    log_service = LogService() if log_service is None else log_service
    rule_was_triggered = False
    for rule in rule_list:
        result = run(rule, defined_variables, defined_actions, defined_validators, log_service)
        if result:
            rule_was_triggered = True
            if stop_on_first_trigger:
                return True
    return rule_was_triggered


def run(rule, defined_variables, defined_actions, defined_validators, log_service):
    conditions, actions = rule['conditions'], rule['actions']
    rule_triggered, matches = check_conditions_recursively(conditions, defined_variables)
    if rule_triggered:
        do_actions(actions, defined_actions, defined_validators, defined_variables, matches, rule, log_service)
        return True
    return False


def check_conditions_recursively(conditions, defined_variables):
    """

    :param conditions:
    :param defined_variables:
    :param matches:
    :return: tuple with result of condition check and list of checked conditions with each individual result.
    """
    keys = list(conditions.keys())
    if keys == ['all']:
        assert len(conditions['all']) >= 1
        matches = []
        for condition in conditions['all']:
            check_condition_result, matches_results = check_conditions_recursively(condition, defined_variables)
            matches.extend(matches_results)
            if not check_condition_result:
                return False, matches
        return True, matches

    elif keys == ['any']:
        assert len(conditions['any']) >= 1
        matches = []
        for condition in conditions['any']:
            check_condition_result, matches_results = check_conditions_recursively(condition, defined_variables)
            matches.extend(matches_results)
            if check_condition_result:
                return True, matches
        return False, matches

    else:
        # help prevent errors - any and all can only be in the condition dict
        # if they're the only item
        assert not ('any' in keys or 'all' in keys)
        result = check_condition(conditions, defined_variables)
        return result[0], [result]



def check_condition(condition, defined_variables):
    """ Checks a single rule condition - the condition will be made up of
    variables, values, and the comparison operator. The defined_variables
    object must have a variable defined for any variables in this condition.
    """
    name, op, value = condition['name'], condition['operator'], condition['value']
    operator_type = _get_variable_value(defined_variables, name)
    return _do_operator_comparison(operator_type, op, value), name, op, value


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


def do_actions(actions, defined_actions, defined_validators, defined_variables, payload, rule, log_service):
    def action_fallback(*args, **kwargs):
        raise AssertionError("Action {0} is not defined in class {1}" \
                             .format(method_name, defined_actions.__class__.__name__))

    # Execute validators, if all False, then not execute actions for rule
    valid = [
        getattr(
            defined_validators,
            condition_result[1],
            defined_validators.validator_fallback(condition_result[1]),
        )(condition_result[2], condition_result[3])
        for condition_result in payload if condition_result[0]
        ]
    if not any(valid):
        logger.info('Rule already executed: {rule}'.format(rule=rule))
        return

    for action in actions:
        method_name = action['name']
        params = action.get('params') or {}

        try:
            method = getattr(defined_actions, method_name, action_fallback)
            method(**params)

            log_service.log_rule(rule, payload, action, defined_variables)
        except AssertionError as e:
            # TODO: Log also using log_service?
            logger.error("AssertionError: {exception}".format(exception=e))
        except Exception as e:
            # TODO: Log also using log_service?
            logger.error("Exception: {exception}".format(exception=e))
