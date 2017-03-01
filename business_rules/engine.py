import inspect
import logging

import utils
from business_rules.models import ConditionResult
from business_rules.validators import BaseValidator
from util import method_type
from .fields import FIELD_NO_INPUT

logger = logging.getLogger(__name__)


def run_all(rule_list,
            defined_variables,
            defined_actions,
            defined_validators=BaseValidator(),
            stop_on_first_trigger=False,
            ):

    rule_was_triggered = False
    for rule in rule_list:
        result = run(rule, defined_variables, defined_actions, defined_validators)
        if result:
            rule_was_triggered = True
            if stop_on_first_trigger:
                return True
    return rule_was_triggered


def run(rule, defined_variables, defined_actions, defined_validators):
    conditions, actions = rule['conditions'], rule['actions']
    rule_triggered, checked_conditions_results = check_conditions_recursively(conditions, defined_variables, rule)
    if rule_triggered:
        do_actions(actions, defined_actions, defined_validators, defined_variables, checked_conditions_results, rule)
        return True
    return False


def check_conditions_recursively(conditions, defined_variables, rule):
    """

    :param conditions:  Conditions to be checked
    :param defined_variables: BaseVariables instance to get variables values to check Conditions
    :param rule: Original rule where Conditions and Actions are defined
    :return: tuple with result of condition check and list of checked conditions with each individual result.

            (condition_result, [(condition1_result), (condition2_result)]

            condition1_result = (condition_result, variable name, condition operator, condition value, condition params)
    """
    keys = list(conditions.keys())
    if keys == ['all']:
        assert len(conditions['all']) >= 1
        matches = []
        for condition in conditions['all']:
            check_condition_result, matches_results = check_conditions_recursively(condition, defined_variables, rule)
            matches.extend(matches_results)
            if not check_condition_result:
                return False, []
        return True, matches

    elif keys == ['any']:
        assert len(conditions['any']) >= 1
        for condition in conditions['any']:
            check_condition_result, matches_results = check_conditions_recursively(condition, defined_variables, rule)
            if check_condition_result:
                return True, matches_results
        return False, []

    else:
        # help prevent errors - any and all can only be in the condition dict
        # if they're the only item
        assert not ('any' in keys or 'all' in keys)
        result = check_condition(conditions, defined_variables, rule)
        return result[0], [result]


def check_condition(condition, defined_variables, rule):
    """
    Checks a single rule condition - the condition will be made up of
    variables, values, and the comparison operator. The defined_variables
    object must have a variable defined for any variables in this condition.

    :param condition:
    :param defined_variables:
    :param rule:
    :return: business_rules.models.ConditionResult

        .. code-block::
        (
            result of condition: bool,
            condition name: str,
            condition operator: str,
            condition value: ?,
            condition params: {}
        )
    """
    name, op, value = condition['name'], condition['operator'], condition['value']
    params = condition.get('params', {})
    operator_type = _get_variable_value(defined_variables, name, params, rule)
    return ConditionResult(result=_do_operator_comparison(operator_type, op, value), name=name, operator=op,
                           value=value, parameters=params)


def _get_variable_value(defined_variables, name, params, rule):
    """
    Call the function provided on the defined_variables object with the
    given name (raise exception if that doesn't exist) and casts it to the
    specified type.

    Returns an instance of operators.BaseType
    :param defined_variables:
    :param name:
    :param params:
    :return: Instance of operators.BaseType
    """

    method = getattr(defined_variables, name, None)

    if method is None:
        raise AssertionError("Variable {0} is not defined in class {1}".format(
            name, defined_variables.__class__.__name__))

    utils.check_params_valid_for_method(method, params, method_type.METHOD_TYPE_VARIABLE)

    method_params = _build_variable_parameters(method, params, rule)
    variable_value = method(**method_params)
    return method.field_type(variable_value)


def _do_operator_comparison(operator_type, operator_name, comparison_value):
    """
    Finds the method on the given operator_type and compares it to the
    given comparison_value.

    operator_type should be an instance of operators.BaseType
    comparison_value is whatever python type to compare to
    returns a bool
    :param operator_type:
    :param operator_name:
    :param comparison_value:
    :return:
    """

    def fallback(*args, **kwargs):
        raise AssertionError("Operator {0} does not exist for type {1}".format(
            operator_name, operator_type.__class__.__name__))

    method = getattr(operator_type, operator_name, fallback)
    if getattr(method, 'input_type', '') == FIELD_NO_INPUT:
        return method()
    return method(comparison_value)


def do_actions(actions, defined_actions, defined_validators, defined_variables, checked_conditions_results, rule):
    """

    :param actions:             List of actions objects to be executed (defined in library)
                                Example:

                                .. code-block:: json

                                    {
                                        "name": "action name",
                                        "params": {
                                            "param1": value
                                        }
                                    }
    :param defined_actions:     Class with function that implement the logic for each possible action defined in
                                'actions' parameter
    :param defined_validators:
    :param defined_variables:
    :param checked_conditions_results:
    :param rule:                Rule that is beign executed
    :return: None
    """

    # Get only conditions when result was TRUE
    successful_conditions = filter(lambda x: x[0], checked_conditions_results)

    # Execute validators, if all False, then not execute actions for rule
    valid = [
        getattr(
            defined_validators,
            condition_result[1],
            defined_validators.validator_fallback(condition_result[1]),
        )(condition_result[2], condition_result[3])
        for condition_result in successful_conditions
        ]

    for action in actions:
        method_name = action['name']
        params = action.get('params') or {}

        method = getattr(defined_actions, method_name, None)

        if not method:
            raise AssertionError("Action {0} is not defined in class {1}" \
                                 .format(method_name, defined_actions.__class__.__name__))

        if method.bypass_validator or any(valid):
            utils.check_params_valid_for_method(method, params, method_type.METHOD_TYPE_ACTION)

            method_params = _build_action_parameters(method, params, rule, successful_conditions)
            method(**method_params)


def _build_action_parameters(method, parameters, rule, conditions):
    """
    Adds extra parameters to the parameters defined for the method
    :param method:
    :param parameters:
    :param rule:
    :param conditions:
    :return:
    """
    extra_parameters = {
        'rule': rule,
        'conditions': conditions
    }

    return _build_parameters(method, parameters, extra_parameters)


def _build_variable_parameters(method, parameters, rule):
    """
    Adds extra parameters to the Variable's method parameters
    :param method:
    :param parameters:
    :param rule:
    :return:
    """
    extra_parameters = {
        'rule': rule,
    }

    return _build_parameters(method, parameters, extra_parameters)


def _build_parameters(method, parameters, extra_parameters):
    if inspect.getargspec(method).keywords is not None:
        method_params = extra_parameters
    else:
        method_params = {}

    method_params.update(parameters)

    return method_params
