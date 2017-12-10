import pytest

from business_rules import fields
from business_rules import utils
from business_rules.fields import FIELD_DATETIME, FIELD_TIME
from tests import actions, variables
from tests.test_integration import SomeVariables, SomeActions


def test_fn_name_to_pretty_label():
    name = 'action_function_name'

    pretty_label = utils.fn_name_to_pretty_label(name)

    assert pretty_label != name
    assert pretty_label == 'Action Function Name'


def test_fn_name_to_pretty_label_with_no_underscores():
    name = 'Action Function Name'

    pretty_label = utils.fn_name_to_pretty_label(name)

    assert pretty_label == name


def test_fn_name_to_pretty_label_with_different_cases():
    name = 'actiON_FUNCTION_nAMe'

    pretty_label = utils.fn_name_to_pretty_label(name)

    assert pretty_label != name
    assert pretty_label == 'Action Function Name'


def test_get_valid_fields():
    valid_fields = utils.get_valid_fields()

    assert len(valid_fields) == 7


def test_params_dict_to_list_when_params_none():
    result = utils.params_dict_to_list(None)

    assert result == []


def test_export_rule_data():
    """
    Tests that export_rule_data has the three expected keys in the right format.
    """
    all_data = utils.export_rule_data(SomeVariables(), SomeActions())

    assert all_data.get("actions") == [
        {
            "name": "action_with_no_params",
            "label": "Action With No Params",
            "params": None
        },
        {
            "name": "some_action",
            "label": "Some Action",
            "params": [
                {
                    'fieldType': 'numeric',
                    'label': 'Foo',
                    'name': 'foo'
                }
            ]
        },
        {
            "name": "some_other_action",
            "label": "woohoo",
            "params": [
                {
                    'fieldType': 'text',
                    'label': 'Bar',
                    'name': 'bar'
                }
            ]
        },
        {
            "name": "some_select_action",
            "label": "Some Select Action",
            "params": [
                {
                    'fieldType': fields.FIELD_SELECT,
                    'name': 'baz',
                    'label': 'Baz',
                    'options': [
                         {'label': 'Chose Me', 'name': 'chose_me'},
                         {'label': 'Or Me', 'name': 'or_me'}
                     ]
                }
            ]
        }
    ]

    assert all_data.get("variables") == [
        {
            "name": "foo",
            "label": "Foo",
            "field_type": "string",
            "options": [],
            "params": [],
            "public": True
        },
        {
            'name': 'private_string_variable',
            'label': 'Private String Variable',
            'field_type': 'string',
            'options': [],
            'params': [],
            'public': False
        },
        {
            'name': 'rule_received',
            'label': 'Rule Received',
            'field_type': 'boolean',
            'options': [],
            'params': [],
            "public": True
        },
        {
            'name': 'string_variable_with_options',
            'label': 'StringLabel',
            'field_type': 'string',
            'options': ['one', 'two', 'three'],
            'params': [],
            "public": True
        },
        {
            "name": "ten",
            "label": "Diez",
            "field_type": "numeric",
            "options": [],
            "params": [],
            "public": True
        },
        {
            'name': 'true_bool',
            'label': 'True Bool',
            'field_type': 'boolean',
            'options': [],
            "params": [],
            "public": True
        },
        {
            'name': 'x_plus_one',
            'label': 'X Plus One',
            'field_type': 'numeric',
            'options': [],
            'params': [
                {'field_type': 'numeric', 'name': 'x', 'label': 'X'}
            ],
            "public": True
        }
    ]

    assert all_data.get("variable_type_operators") == {
        'boolean': [{'input_type': 'none',
                     'label': 'Is False',
                     'name': 'is_false'},
                    {'input_type': 'none',
                     'label': 'Is True',
                     'name': 'is_true'}],
        'datetime': [
            {
                'input_type': FIELD_DATETIME,
                'label': 'After Than',
                'name': 'after_than'
            },
            {
                'input_type': FIELD_DATETIME,
                'label': 'After Than Or Equal To',
                'name': 'after_than_or_equal_to'
            },
            {
                'input_type': FIELD_DATETIME,
                'label': 'Before Than',
                'name': 'before_than'
            },
            {
                'input_type': FIELD_DATETIME,
                'label': 'Before Than Or Equal To',
                'name': 'before_than_or_equal_to'
            },
            {
                'input_type': FIELD_DATETIME,
                'label': 'Equal To',
                'name': 'equal_to'
            },
        ],
        'numeric': [{'input_type': 'numeric',
                     'label': 'Equal To',
                     'name': 'equal_to'},
                    {'input_type': 'numeric', 'label': 'Greater Than',
                     'name': 'greater_than'},
                    {'input_type': 'numeric',
                     'label': 'Greater Than Or Equal To',
                     'name': 'greater_than_or_equal_to'},
                    {'input_type': 'numeric', 'label': 'Less Than',
                     'name': 'less_than'},
                    {'input_type': 'numeric',
                     'label': 'Less Than Or Equal To',
                     'name': 'less_than_or_equal_to'}],
        'select': [{'input_type': 'select', 'label': 'Contains',
                    'name': 'contains'},
                   {'input_type': 'select',
                    'label': 'Does Not Contain',
                    'name': 'does_not_contain'}],
        'select_multiple': [{'input_type': 'select_multiple',
                             'label': 'Contains All',
                             'name': 'contains_all'},
                            {'input_type': 'select_multiple',
                             'label': 'Is Contained By',
                             'name': 'is_contained_by'},
                            {'input_type': 'select_multiple',
                             'label': 'Shares At Least One Element With',
                             'name': 'shares_at_least_one_element_with'},
                            {'input_type': 'select_multiple',
                             'label': 'Shares Exactly One Element With',
                             'name': 'shares_exactly_one_element_with'},
                            {'input_type': 'select_multiple',
                             'label': 'Shares No Elements With',
                             'name': 'shares_no_elements_with'}],
        'string': [{'input_type': 'text', 'label': 'Contains',
                    'name': 'contains'},
                   {'input_type': 'text', 'label': 'Ends With',
                    'name': 'ends_with'},
                   {'input_type': 'text', 'label': 'Equal To',
                    'name': 'equal_to'},
                   {'input_type': 'text',
                    'label': 'Equal To (case insensitive)',
                    'name': 'equal_to_case_insensitive'},
                   {'input_type': 'text', 'label': 'Matches Regex',
                    'name': 'matches_regex'},
                   {'input_type': 'none', 'label': 'Non Empty',
                    'name': 'non_empty'},
                   {'input_type': 'text', 'label': 'Starts With',
                    'name': 'starts_with'}],
        'time': [
            {
                'input_type': FIELD_TIME,
                'label': 'After Than',
                'name': 'after_than'
            },
            {
                'input_type': FIELD_TIME,
                'label': 'After Than Or Equal To',
                'name': 'after_than_or_equal_to'
            },
            {
                'input_type': FIELD_TIME,
                'label': 'Before Than',
                'name': 'before_than'
            },
            {
                'input_type': FIELD_TIME,
                'label': 'Before Than Or Equal To',
                'name': 'before_than_or_equal_to'
            },
            {
                'input_type': FIELD_TIME,
                'label': 'Equal To',
                'name': 'equal_to'
            },
        ],
    }


def test_validate_rule_data_success():
    valid_rule = {
        'conditions': {
            'all': [
                {
                    'name': 'bool_variable',
                    'operator': 'is_false',
                    'value': ''
                },
                {
                    'name': 'str_variable',
                    'operator': 'contains',
                    'value': 'test'
                },
                {
                    'name': 'select_multiple_variable',
                    'operator': 'contains_all',
                    'value': [1, 2, 3]
                },
                {
                    'name': 'numeric_variable',
                    'operator': 'equal_to',
                    'value': 1
                },
                {
                    'name': 'datetime_variable',
                    'operator': 'equal_to',
                    'value': '2016-01-01'
                },
                {
                    'name': 'time_variable',
                    'operator': 'equal_to',
                    'value': '10:00:00'
                },
                {
                    'name': 'select_variable',
                    'operator': 'contains',
                    'value': [1]
                }
            ]
        },
        'actions': [
            {
                'name': 'example_action',
                'params': {
                    'param': 1
                }
            }
        ]
    }
    utils.validate_rule_data(variables.TestVariables, actions.TestActions, valid_rule)


def test_validate_rule_data_nested_success():
    valid_rule = {
        'conditions': {
            'any': [
                {
                    'name': 'bool_variable',
                    'operator': 'is_false',
                    'value': ''
                },
                {
                    "all": [
                        {
                            'name': 'str_variable',
                            'operator': 'contains',
                            'value': 'test'
                        },
                        {
                            'name': 'select_multiple_variable',
                            'operator': 'contains_all',
                            'value': [1, 2, 3]
                        },
                    ]
                }
            ]
        },
        'actions': [
            {
                'name': 'example_action',
                'params': {
                    'param': 1
                }
            }
        ]
    }
    utils.validate_rule_data(variables.TestVariables, actions.TestActions, valid_rule)


def test_validate_rule_data_empty_dict():
    with pytest.raises(AssertionError):
        utils.validate_rule_data(variables.TestVariables, actions.TestActions, {})


def test_validate_rule_data_no_conditions():
    invalid_rule = {
        'actions': []
    }

    utils.validate_rule_data(variables.TestVariables, actions.TestActions, invalid_rule)


def test_validate_rule_data_no_actions():
    invalid_rule = {
        'conditions': {}
    }
    with pytest.raises(AssertionError):
        utils.validate_rule_data(variables.TestVariables, actions.TestActions, invalid_rule)


def test_validate_rule_data_unknown_action():
    invalid_rule = {
        'conditions': {},
        'actions': [
            {
                'name': 'unknown',
                'params': {}
            }
        ]
    }
    with pytest.raises(AssertionError):
        utils.validate_rule_data(variables.TestVariables, actions.TestActions, invalid_rule)


def test_validate_rule_data_missing_action_name():
    invalid_rule = {
        'conditions': {},
        'actions': [
            {
                'params': {}
            }
        ]
    }
    with pytest.raises(AssertionError):
        utils.validate_rule_data(variables.TestVariables, actions.TestActions, invalid_rule)


def test_validate_rule_data_unknown_condition_name():
    invalid_rule = {
        'conditions': {
            'any': [
                {
                    'name': 'unknown',
                    'operator': 'unknown',
                    'value': 'unknown'
                }
            ]
        },
        'actions': []
    }
    with pytest.raises(AssertionError):
        utils.validate_rule_data(variables.TestVariables, actions.TestActions, invalid_rule)


def test_validate_rule_data_unknown_condition_operator():
    invalid_rule = {
        'conditions': {
            'any': [
                {
                    'name': 'bool_variable',
                    'operator': 'unknown',
                    'value': ''
                }
            ]
        },
        'actions': []
    }
    with pytest.raises(AssertionError):
        utils.validate_rule_data(variables.TestVariables, actions.TestActions, invalid_rule)


def test_validate_rule_data_missing_condition_operator():
    invalid_rule = {
        'conditions': {
            'any': [
                {
                    'name': 'bool_variable',
                    'value': ''
                }
            ]
        },
        'actions': []
    }
    with pytest.raises(AssertionError):
        utils.validate_rule_data(variables.TestVariables, actions.TestActions, invalid_rule)


def test_validate_rule_data_bool_value_ignored():
    invalid_rule = {
        'conditions': {
            'any': [
                {
                    'name': 'bool_variable',
                    'operator': 'is_true',
                    'value': 'any value here'
                }
            ]
        },
        'actions': []
    }
    utils.validate_rule_data(variables.TestVariables, actions.TestActions, invalid_rule)


def test_validate_rule_data_bad_condition_value():
    invalid_rule = {
        'conditions': {
            'any': [
                {
                    'name': 'string_variable',
                    'operator': 'equal_to',
                    'value': 123
                }
            ]
        },
        'actions': []
    }
    with pytest.raises(AssertionError):
        utils.validate_rule_data(variables.TestVariables, actions.TestActions, invalid_rule)


def test_validate_rule_data_unknown_condition_key():
    invalid_rule = {
        'conditions': {
            'any': [
                {
                    'name': 'string_variable',
                    'operator': 'equal_to',
                    'value': 'test',
                    'unknown': 'unknown'
                }
            ]
        },
        'actions': []
    }
    with pytest.raises(AssertionError):
        utils.validate_rule_data(variables.TestVariables, actions.TestActions, invalid_rule)


def test_validate_rule_multiple_special_keys_in_condition():
    """ A rule cannot contain more than one 'any' or 'all' keys """
    invalid_rule = {
        'conditions': {
            'any': [
                {
                    'name': 'bool_variable',
                    'operator': 'is_false',
                    'value': ''
                }
            ],
            'all': [
                {
                    'name': 'bool_variable',
                    'operator': 'is_false',
                    'value': ''
                }
            ]
        },
        'actions': []
    }
    with pytest.raises(AssertionError):
        utils.validate_rule_data(variables.TestVariables, actions.TestActions, invalid_rule)


def test_validate_rule_actions_is_not_a_list():
    invalid_rule = {
        'conditions': {
            'any': [
                {
                    'name': 'bool_variable',
                    'operator': 'is_false',
                    'value': ''
                }
            ]
        },
        'actions': {}
    }
    with pytest.raises(AssertionError):
        utils.validate_rule_data(variables.TestVariables, actions.TestActions, invalid_rule)


def test_validate_rule_contions_is_not_a_dictionary():
    invalid_rule = {
        'conditions': [],
        'actions': {}
    }
    with pytest.raises(AssertionError):
        utils.validate_rule_data(variables.TestVariables, actions.TestActions, invalid_rule)
