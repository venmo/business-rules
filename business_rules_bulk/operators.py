import inspect
import re
from functools import wraps
from .six import string_types, integer_types

from .fields import (FIELD_TEXT, FIELD_NUMERIC, FIELD_NO_INPUT,
                     FIELD_SELECT, FIELD_SELECT_MULTIPLE)
from .utils import fn_name_to_pretty_label, float_to_decimal, get_difference
from decimal import Decimal, Inexact, Context
import variables


class BaseType(object):
    def __init__(self, value):
        self.value = self._assert_valid_value_and_cast(value)

    def _assert_valid_value_and_cast(self, value):
        raise NotImplemented()

    @classmethod
    def get_all_operators(cls):
        methods = inspect.getmembers(cls)
        return [{'name': m[0],
                 'label': m[1].label,
                 'input_type': m[1].input_type}
                for m in methods if getattr(m[1], 'is_operator', False)]


def export_type(cls):
    """ Decorator to expose the given class to business_rules.export_rule_data. """
    cls.export_in_rule_data = True
    return cls


def type_operator(input_type, label=None,
                  assert_type_for_arguments=True):
    """ Decorator to make a function into a type operator.

    - assert_type_for_arguments - if True this patches the operator function
      so that arguments passed to it will have _assert_valid_value_and_cast
      called on them to make type errors explicit.
    """

    def wrapper(func):
        func.is_operator = True
        func.label = label \
                     or fn_name_to_pretty_label(func.__name__)
        func.input_type = input_type

        @wraps(func)
        def inner(self, *args, **kwargs):
            if assert_type_for_arguments:
                args = [self._assert_valid_value_and_cast(arg) for arg in args]
                kwargs = dict((k, self._assert_valid_value_and_cast(v))
                              for k, v in kwargs.items())
            return func(self, *args, **kwargs)

        return inner

    return wrapper


@export_type
class StringType(BaseType):
    name = "string"

    def _assert_valid_value_and_cast(self, value):
        """
        :param value: 2 possible values is expected here as Input.
            1. The value which the user provide while defining the rule.
            2. The values of the in form of VariableWrapper instances

        :return:
        Will check the value passed and will return AssertionError if value is not a valid numeric type.
        """
        value = value or ""
        if not isinstance(value, string_types) and not isinstance(value, variables.VariableValuesWrapper):
            raise AssertionError("{0} is not a valid string type.".
                                 format(value))

        if isinstance(value, variables.VariableValuesWrapper):
            for single_value in value.instances:
                if single_value[value.variable] and not isinstance(single_value[value.variable], string_types):
                    raise AssertionError("{0} is not a valid string type.".
                                         format(single_value[value.variable]))
        return value

    @type_operator(FIELD_TEXT)
    def equal_to(self, other_string):
        """

        :param other_string: The value we specified while we created a rule.

        Eg. If a contact's first_name is "abc" and we define a rule for a list that,
         Rule : "First Name equal_to xyz".
         Then the value "xyz" of the rule is what other_string parameter will refer to.

        :return:
        values_satisfying_equal_to :list of instances which satisfy the equal_to condition against other_string
        values_not_satisfying_equal_to : list of instances which DOES NOT satisfy the equal_to condition against
        other_string

        """
        values_satisfying_equal_to = filter(
            lambda single_instance: single_instance[self.value.variable] == other_string if
            single_instance[self.value.variable] else False, self.value.instances)
        values_not_satisfying_equal_to = get_difference(self.value.instances, values_satisfying_equal_to)
        return values_satisfying_equal_to, values_not_satisfying_equal_to

    @type_operator(FIELD_TEXT, label="Equal To (case insensitive)")
    def equal_to_case_insensitive(self, other_string):
        """
        :param other_string: The value we specified while we created a rule.

        Eg. If a contact's first_name is "abc" and we define a rule for a list that,
         Rule : "First Name equal_to_case_insensitive xyz".
         Then the value "xyz" of the rule is what other_string parameter will refer to.

        :return:
        values_satisfying_equal_to_case_sensitive :list of instances which satisfy the equal_to_case_insensitive
        condition against other_string

        values_not_satisfying_equal_to_case_sensitive : list of instances which DOES NOT satisfy the
        equal_to_case_insensitive condition against other_string
        """
        values_satisfying_equal_to_case_sensitive = filter(
            lambda single_instance: single_instance[self.value.variable].lower() == other_string.lower() if
            single_instance[self.value.variable] else False, self.value.instances)

        values_not_satisfying_equal_to_case_sensitive = get_difference(
            self.value.instances, values_satisfying_equal_to_case_sensitive)
        return values_satisfying_equal_to_case_sensitive, values_not_satisfying_equal_to_case_sensitive

    @type_operator(FIELD_TEXT)
    def starts_with(self, other_string):
        """
        :param other_string: The value we specified while we created a rule.

        Eg. If a contact's first_name is "abc" and we define a rule for a list that,
         Rule : "First Name starts_with xyz".
         Then the value "xyz" of the rule is what other_string parameter will refer to.

        :return:
        values_satisfying_starts_with :list of instances which satisfy the starts_with condition against other_string

        values_not_satisfying_starts_with : list of instances which DOES NOT satisfy the starts_with
        condition against other_string
        """
        values_satisfying_starts_with = filter(
            lambda single_instance: single_instance[self.value.variable].startswith(other_string) if
            single_instance[self.value.variable] else False, self.value.instances)

        values_not_satisfying_starts_with = get_difference(self.value.instances, values_satisfying_starts_with)
        return values_satisfying_starts_with, values_not_satisfying_starts_with

    @type_operator(FIELD_TEXT)
    def ends_with(self, other_string):
        """
        :param other_string: The value we specified while we created a rule.

        Eg. If a contact's first_name is "abc" and we define a rule for a list that,
         Rule : "First Name ends_with xyz".
         Then the value "xyz" of the rule is what other_string parameter will refer to.

        :return:
        values_satisfying_ends_with :list of instances which satisfy the ends_with condition against other_string

        values_not_satisfying_ends_with : list of instances which DOES NOT satisfy the ends_with
        condition against other_string
        """
        values_satisfying_ends_with = filter(
            lambda single_instance: single_instance[self.value.variable].endswith(other_string) if
            single_instance[self.value.variable] else False, self.value.instances)

        values_not_satisfying_ends_with = get_difference(self.value.instances, values_satisfying_ends_with)
        return values_satisfying_ends_with, values_not_satisfying_ends_with

    @type_operator(FIELD_TEXT)
    def contains(self, other_string):
        """
        :param other_string: The value we specified while we created a rule.

        Eg. If a contact's first_name is "abc" and we define a rule for a list that,
         Rule : "First Name contains xyz".
         Then the value "xyz" of the rule is what other_string parameter will refer to.

        :return:
        values_satisfying_contains :list of instances which satisfy the contains condition against other_string

        values_not_satisfying_contains : list of instances which DOES NOT satisfy the contains
        condition against other_string
        """
        values_satisfying_contains = filter(
            lambda single_instance: other_string in single_instance[self.value.variable] if
            single_instance[self.value.variable] else False, self.value.instances)

        values_not_satisfying_contains = get_difference(self.value.instances, values_satisfying_contains)
        return values_satisfying_contains, values_not_satisfying_contains

        # return other_string in self.value

    @type_operator(FIELD_TEXT)
    def matches_regex(self, regex):
        """
        :param regex: The value we specified while we created a rule.

        Eg. If a contact's first_name is "abc" and we define a rule for a list that,
         Rule : "First Name regex %e".
         Then the value "%e" of the rule is what other_string parameter will refer to.

        :return:
        values_satisfying_contains :list of instances which satisfy the matches_regex condition against other_string

        values_not_satisfying_contains : list of instances which DOES NOT satisfy the matches_regex
        condition against other_string
        """
        values_satisfying_regex = filter(
            lambda single_instance: re.search(regex, single_instance[self.value.variable]) if
            single_instance[self.value.variable] else False, self.value.instances)

        values_not_satisfying_regex = get_difference(self.value.instances, values_satisfying_regex)
        return values_satisfying_regex, values_not_satisfying_regex

    @type_operator(FIELD_NO_INPUT)
    def non_empty(self):
        """
        :return:
        values_satisfying_non_empty :list of instances which satisfy the non_empty condition against other_string

        values_not_satisfying_non_empty : list of instances which DOES NOT satisfy the non_empty
        condition against other_string
        """
        values_satisfying_non_empty = filter(
            lambda single_instance: bool(single_instance[self.value.variable]) if
            single_instance[self.value.variable] else False, self.value.instances)

        values_not_satisfying_non_empty = get_difference(self.value.instances, values_satisfying_non_empty)
        return values_satisfying_non_empty, values_not_satisfying_non_empty


@export_type
class NumericType(BaseType):
    EPSILON = Decimal('0.000001')

    name = "numeric"

    @staticmethod
    def _assert_valid_value_and_cast(value):
        """
        :param value: 2 possible values is expected here as Input.
            1. The value which the user provide while defining the rule.
            2. The values of the in form of VariableWrapper instances

        :return:
          Will check the value passed and will return :
            Decimal(value) if the value is a valid number.
                            OR
            AssertionError if value is not a valid numeric type.

        """

        def _get_numeric_value(inner_value):
            if isinstance(inner_value, float):
                # In python 2.6, casting float to Decimal doesn't work
                return float_to_decimal(inner_value)
            if isinstance(inner_value, integer_types):
                return Decimal(inner_value)
            if isinstance(value, Decimal):
                return inner_value
            else:
                return AssertionError("{0} is not a valid numeric type".format(inner_value))

        # Considering the both type of values getting as Input
        if not isinstance(value, variables.VariableValuesWrapper):
            _get_numeric_value(value)

        elif isinstance(value, variables.VariableValuesWrapper):
            for single_value in value.instances:
                _get_numeric_value(single_value[value.variable])

        return value

    @type_operator(FIELD_NUMERIC)
    def equal_to(self, other_numeric):
        """

        :param other_numeric: The value we specified while we created a rule.

        Eg. If a contact's age is 50 and we define a rule for a list that,
         Rule : "Age equal_to 20".
         Then the value "20" of the rule is what other_numeric parameter will refer to.

         As per above example :
         other_numeric : 20
         self.value : VariableValuesWrapper type object consisting of variable and instances.
         Value of the each instance will be compared to other_numeric for equal_to operator.

        :return :
        values_satisfying_equal_to :list of instances which satisfy the equal_to condition against other_numeric
        values_not_satisfying_equal_to : list of instances which DOES NOT satisfy the equal_to condition against
        other_numeric

        In case if any of self.value.instances is null, that value will be added in values_not_satisfying_equal_to
        """
        values_satisfying_equal_to = filter(
            lambda single_instance: abs(single_instance[self.value.variable] - other_numeric) <= self.EPSILON,
            self.value.instances)

        values_not_satisfying_equal_to = get_difference(self.value.instances, values_satisfying_equal_to)
        return values_satisfying_equal_to, values_not_satisfying_equal_to

    @type_operator(FIELD_NUMERIC)
    def greater_than(self, other_numeric):
        """

        :param other_numeric: The value we specified while we created a rule.

        Eg. If a contact's age is 50 and we define a rule for a list that,
         Rule : "Age greater_than 20".
         Then the value "20" of the rule is what other_numeric parameter will refer to.

         As per above example :
         other_numeric : 20
         self.value : VariableValuesWrapper type object consisting of variable and instances
         Value of the each instance will be compared to other_numeric for greater_than operator.

        :return :
        values_satisfying_greater_than :list of instances which satisfy the greater_than condition against other_numeric
        values_not_satisfying_greater_than : list of instances which DOES NOT satisfy the greater_than condition against
        other_numeric
        """
        values_satisfying_greater_than = filter(
            lambda single_instance: (single_instance[self.value.variable] - other_numeric) > self.EPSILON,
            self.value.instances)

        values_not_satisfying_greater_than = get_difference(self.value.instances, values_satisfying_greater_than)
        return values_satisfying_greater_than, values_not_satisfying_greater_than

    @type_operator(FIELD_NUMERIC)
    def greater_than_or_equal_to(self, other_numeric):
        """

        :param other_numeric: The value we specified while we created a rule.

        Eg. If a contact's age is 50 and we define a rule for a list that,
         Rule : "Age greater_than_or_equal_to 20".
         Then the value "20" of the rule is what other_numeric parameter will refer to.

         As per above example :
         other_numeric : 20
         self.value : VariableValuesWrapper type object consisting of variable and instances
        Value of the each instance will be compared to other_numeric for greater_than_or_equal_to operator.
        :return :
        values_satisfying_greater_than_equal_to :list of instances which satisfy the greater_than_or_equal_to condition
        against other_numeric

        values_not_satisfying_greater_than_equal_to : list of instances which DOES NOT satisfy the greater_than_or_equal_
        to condition against other_numeric
        """
        values_satisfying_greater_than_equal_to = filter(
            lambda single_instance: self.greater_than(other_numeric) or self.equal_to(other_numeric),
            self.value.instances)

        values_not_satisfying_greater_than_equal_to = get_difference(
            self.value.instances, values_satisfying_greater_than_equal_to)

        return values_satisfying_greater_than_equal_to, values_not_satisfying_greater_than_equal_to

    @type_operator(FIELD_NUMERIC)
    def less_than(self, other_numeric):
        """

        :param other_numeric: The value we specified while we created a rule.

        Eg. If a contact's age is 50 and we define a rule for a list that,
         Rule : "Age less_than 20".
         Then the value "20" of the rule is what other_numeric parameter will refer to.

         As per above example :
         other_numeric : 20
         self.value : VariableValuesWrapper type object consisting of variable and instances
        Value of the each instance will be compared to other_numeric for less_than operator.

        :return :
        values_satisfying_less_than :list of instances which satisfy the less_than condition against other_numeric
        values_not_satisfying_less_than : list of instances which DOES NOT satisfy the less_than condition against
        other_numeric

        """
        values_satisfying_less_than = filter(
            lambda single_instance: (other_numeric - self.value) > self.EPSILON, self.value.instances)

        values_not_satisfying_less_than = get_difference(self.value.instances, values_satisfying_less_than)
        return values_satisfying_less_than, values_not_satisfying_less_than

    @type_operator(FIELD_NUMERIC)
    def less_than_or_equal_to(self, other_numeric):
        """

        :param other_numeric: The value we specified while we created a rule.

        Eg. If a contact's age is 50 and we define a rule for a list that,
         Rule : "Age less_than_or_equal_to 20".
         Then the value "20" of the rule is what other_numeric parameter will refer to.
        Value of the each instance will be compared to other_numeric for greater_than operator.

         As per above example :
         other_numeric : 20
         self.value : VariableValuesWrapper type object consisting of variable and instances
        Value of the each instance will be compared to other_numeric for less_than_or_equal_to operator.

        :return :
        values_satisfying_less_than_equal_to :list of instances which satisfy the less_than_or_equal_to
        condition against other_numeric

        values_not_satisfying_less_than_equal_to : list of instances which DOES NOT satisfy the less_than_or_equal_to
         condition against other_numeric

        In case if any of self.value.instances is null, that value will be added in
        values_not_satisfying_less_than_equal_to.
        """
        values_satisfying_less_than_equal_to = filter(
            lambda single_instance: self.less_than(other_numeric) or self.equal_to(other_numeric), self.value.instances)

        values_not_satisfying_less_than_equal_to = get_difference(
            self.value.instances, values_satisfying_less_than_equal_to)

        return values_satisfying_less_than_equal_to, values_not_satisfying_less_than_equal_to


@export_type
class BooleanType(BaseType):
    name = "boolean"

    def _assert_valid_value_and_cast(self, value):
        """
        :param value: 2 possible values is expected here as Input.
            1. The value which the user provide while defining the rule.
            2. The values of the in form of VariableWrapper instances

        :return:
        Will check the value passed and will return AssertionError if value is not a valid boolean type.

        """
        if not isinstance(value, variables.VariableValuesWrapper):
            if type(value) != bool:
                raise AssertionError("{0} is not a valid boolean type.".format(value))

        if isinstance(value, variables.VariableValuesWrapper):
            for single_value in value.instances:
                if type(single_value[value.variable]) != bool:
                    raise AssertionError("{0} is not a valid boolean type.".format(
                        single_value[value.variable]))
        return value

    @type_operator(FIELD_NO_INPUT)
    def is_true(self):
        """
        :return:
        values_satisfying_is_true :list of instances which satisfy the is_true condition

        values_not_satisfying_is_true : list of instances which DOES NOT satisfy the is_true condition
        """
        values_satisfying_is_true = filter(
            lambda single_instance: single_instance[self.value.variable] if
            single_instance[self.value.variable] else False, self.value.instances)

        values_not_satisfying_is_true = get_difference(self.value.instances, values_satisfying_is_true)
        return values_satisfying_is_true, values_not_satisfying_is_true

    @type_operator(FIELD_NO_INPUT)
    def is_false(self):
        """
        :return:
        values_satisfying_is_false :list of instances which satisfy the is_false condition

        values_not_satisfying_is_false : list of instances which DOES NOT satisfy the is_false condition
        """
        values_satisfying_is_false = filter(
            lambda single_instance: not single_instance[self.value.variable] if
            single_instance[self.value.variable] else False, self.value.instances)

        values_not_satisfying_equal_to = get_difference(self.value.instances, values_satisfying_is_false)
        return values_satisfying_is_false, values_not_satisfying_equal_to


@export_type
class SelectType(BaseType):
    name = "select"

    def _assert_valid_value_and_cast(self, value):
        """
        :param value: 2 possible values is expected here as Input.
            1. The value which the user provide while defining the rule.
            2. The values of the in form of VariableWrapper instances

        Checks whether the value passed here is a valid select type or not.
        If not valid it raises an AssertionError for invalid type of select type.
        """
        if not isinstance(value, variables.VariableValuesWrapper):
            if not hasattr(value, '__iter__'):
                raise AssertionError("{0} is not a valid select type".
                                     format(value))

        if isinstance(value, variables.VariableValuesWrapper):
            for single_value in value.instances:
                if not hasattr(single_value[value.variable], '__iter__'):
                    raise AssertionError("{0} is not a valid select type".
                                         format(single_value[value.variable]))

        return value

    @staticmethod
    def _case_insensitive_equal_to(value_from_list, other_value):
        if isinstance(value_from_list, string_types) and isinstance(other_value, string_types):
            return value_from_list.lower() == other_value.lower()
        else:
            return value_from_list == other_value

    @type_operator(FIELD_SELECT, assert_type_for_arguments=False)
    def contains(self, other_value):
        """

        :param other_value : The value we specified while we created a rule.

        Eg. If a contact's gender is Male and we define a rule for a list that,
         Rule : "Contact's gender  is_equal_to Female".
         Then the value "Female" of the rule is what other_value parameter will refer to.

         As per above example :
         other_numeric : "Female"
         self.value : VariableValuesWrapper type object consisting of variable and instances
        Value of the each instance will be compared to other_value for is_equal_to operator.

        :return :
        values_satisfying_contains :list of instances which satisfy the contains
        condition against other_value

        values_not_satisfying_contains : list of instances which DOES NOT satisfy the contains
         condition against other_value
        """

        def _check_contains(value):
            if isinstance(value, list):
                for single_value in value:
                    if self._case_insensitive_equal_to(single_value, other_value):
                        return True
                return False
            else:
                if self._case_insensitive_equal_to(value, other_value):
                    return True
                return False

        values_satisfying_contains = filter(
            lambda single_instance: _check_contains(single_instance[self.value.variable]) if
            single_instance[self.value.variable] else False, self.value.instances)

        values_not_satisfying_contains = get_difference(self.value.instances, values_satisfying_contains)
        return values_satisfying_contains, values_not_satisfying_contains

    @type_operator(FIELD_SELECT, assert_type_for_arguments=False)
    def does_not_contain(self, other_value):
        """

        :param other_value : The value we specified while we created a rule.

        Eg. If a contact's gender is Male and we define a rule for a list that,
         Rule : "Contact's gender  is_not_equal_to Female".
         Then the value "Female" of the rule is what other_value parameter will refer to.

         As per above example :
         other_numeric : "Female"
        self.value : VariableValuesWrapper type object consisting of variable and instances
        Value of the each instance will be compared to other_value for is_not_equal_to operator.

        :return :
        values_satisfying_does_not_contains :list of instances which satisfy the is_not_equal_to
        condition against other_value

        values_not_satisfying_does_not_contains : list of instances which DOES NOT satisfy the is_not_equal_to
         condition against other_value
        """

        def _check_does_not_contains(value):
            if isinstance(value, list):
                for single_value in value:
                    if self._case_insensitive_equal_to(single_value, other_value):
                        return False
            return True

        values_satisfying_does_not_contains = filter(
            lambda single_instance: _check_does_not_contains(single_instance[self.value.variable]) if
            single_instance[self.value.variable] else False, self.value.instances)

        values_not_satisfying_does_not_contains = get_difference(
            self.value.instances, values_satisfying_does_not_contains)
        return values_satisfying_does_not_contains, values_not_satisfying_does_not_contains


@export_type
class SelectMultipleType(BaseType):
    name = "select_multiple"

    def _assert_valid_value_and_cast(self, value):
        """
        :param value: 2 possible values is expected here as Input.
            1. The value which the user provide while defining the rule.
            2. The values of the in form of VariableWrapper instances

        Checks whether the value passed here is a valid select_multiple type or not.
        If not valid it raises an AssertionError for invalid type of select type.
        """
        if not isinstance(value, variables.VariableValuesWrapper):
            if not hasattr(value, '__iter__'):
                raise AssertionError("{0} is not a valid select multiple type".
                                     format(value))

        if isinstance(value, variables.VariableValuesWrapper):
            for single_value in value.instances:

                if not hasattr(single_value[value.variable], '__iter__'):
                    raise AssertionError("{0} is not a valid select multiple type".
                                         format(single_value[value.variable]))

        return value

    @type_operator(FIELD_SELECT_MULTIPLE)
    def contains_all(self, other_value):
        """

        :param other_value : The value we specified while we created a rule.

        Eg. If a contact's tags are ["tag1", "tag2", "tag3", "tag4"] and we define a rule for a list that,
         Rule : "Contact's tags contains_all ["tag1", "tag2", "tag3"]".
         Then the value "["tag1", "tag2", "tag3"]" of the rule is what other_numeric parameter will refer to.

         As per above example :
         other_numeric : ["tag1", "tag2", "tag3"]
         self.value : VariableValuesWrapper type object consisting of variable and instances
        Value of the each instance will be compared to other_value for has_all_of operator.

        :return :
        values_satisfying_contains_all :list of instances which satisfy the contains_all
        condition against other_value

        values_not_satisfying_contains_all : list of instances which DOES NOT satisfy the contains_all
         condition against other_value

         Instance will be added to values_satisfying_contains_all :
            1) If a contact's tags are ["tag1", "tag2", "tag3", "tag4"] and we define a rule for a list that,
            Rule : "Contact's tags contains_all ["tag1", "tag2", "tag3"]".

         Instance will be added to values_not_satisfying_contains_all :
            1) If a contact's tags are ["tag1", "tag2", "tag3"] and we define a rule for a list that,
         Rule : "Contact's tags contains_all ["tag1", "tag2", "tag3", "tag4"].

        """
        values_satisfying_contains_all = []

        select = SelectType(self.value)
        for other_val in other_value:
            values_satisfying_contains_all = []
            values_satisfying_contains, values_not_satisfying_values_satisfying_contains = select.contains(other_val)
            if len(values_satisfying_contains) > 0:
                values_satisfying_contains_all += values_satisfying_contains

        values_not_satisfying_contains_all = get_difference(self.value.instances, values_satisfying_contains_all)
        return values_satisfying_contains_all, values_not_satisfying_contains_all

    @type_operator(FIELD_SELECT_MULTIPLE)
    def is_contained_by(self, other_value):
        """

        :param other_value : The value we specified while we created a rule.

        Eg.
        If a contact's tags are ["tag1", "tag2", "tag3", "tag4"] and we define a rule for a list that,
         Rule : "Contact's tags is_contained_by ["tag1", "tag2", "tag3"]".
         Then the value "["tag1", "tag2", "tag3"]" of the rule is what other_numeric parameter will refer to.

         As per above example :
         other_numeric : ["tag1", "tag2", "tag3"]
         self.value : VariableValuesWrapper type object consisting of variable and instances
        Value of the each instance will be compared to other_value for is_contained_by operator.

        :return :
        value_satisfying_is_contained_by :list of instances which satisfy the is_contained_by
        condition against other_value

        values_not_satisfying_is_contained_by : list of instances which DOES NOT satisfy the is_contained_by
         condition against other_value

        Instance will be added to value_satisfying_is_contained_by :
            1) If a contact's tags are ["tag1", "tag2", "tag3", "tag4"] and we define a rule for a list that,
            Rule : "Contact's tags is_contained_by ["tag1", "tag2", "tag3"]".

            2) If a contact's tags are ["tag1", "tag2", "tag3"] and we define a rule for a list that,
             Rule : "Contact's tags is_contained_by ["tag1", "tag2", "tag3", "tag4"].
        """

        def _check_is_contained_by(instance):
            all_values = instance
            if all_values:
                if len(all_values) > other_value:
                    return False
                else:
                    value_not_in_defined_rules = [single_element for single_element in all_values if
                                                  single_element not in other_value]
                    if len(value_not_in_defined_rules) > 0:
                        return False
                    else:
                        return True
            return False

        value_satisfying_is_contained_by = []
        for single_instance in self.value.instances:
            if _check_is_contained_by(single_instance[self.value.variable]):
                value_satisfying_is_contained_by.append(single_instance)

        values_not_satisfying_is_contained_by = get_difference(
            self.value.instances, value_satisfying_is_contained_by)

        return value_satisfying_is_contained_by, values_not_satisfying_is_contained_by

    @type_operator(FIELD_SELECT_MULTIPLE)
    def shares_at_least_one_element_with(self, other_value):
        """

        :param other_value : The value we specified while we created a rule.

        Eg.
        If a contact's tags are ["tag1", "tag2", "tag3", "tag4"] and we define a rule for a list that,
         Rule : "Contact's tags shares_at_least_one_element_with ["tag1", "tag2", "tag3"]".
         Then the value "["tag1", "tag2", "tag3"]" of the rule is what other_numeric parameter will refer to.

         As per above example :
         other_numeric : ["tag1", "tag2", "tag3"]
         self.value : VariableValuesWrapper type object consisting of variable and instances
        Value of the each instance will be compared to other_value for shares_at_least_one_element_with operator.

        :return :
        values_satisfying_has_at_least_one_of :list of instances which satisfy the shares_at_least_one_element_with
        condition against other_value

        values_not_satisfying_has_at_least_one_of : list of instances which DOES NOT satisfy the
        shares_at_least_one_element_with condition against other_value

        Instance will be added to values_satisfying_shares_at_least_one_element_with :
            1) If a contact's tags are ["tag1", "tag2", "tag3", "tag4"] and we define a rule for a list that,
             Rule : "Contact's tags shares_at_least_one_element_with ["tag1", "tag5", "tag6"]".

        Instance will be added to values_not_satisfying_shares_at_least_one_element_with :
            1) If a contact's tags are ["tag1", "tag2", "tag3"] and we define a rule for a list that,
             Rule : "Contact's tags shares_at_least_one_element_with ["tag5", "tag6"].

            2) In case if any value of self.value.instances is empty
        """
        select = SelectType(self.value)
        values_satisfying_shares_at_least_one_element_with = []

        for other_val in other_value:
            values_satisfying_equal_to, values_not_satisfying_equal_to = select.contains(other_val)
            if len(values_satisfying_equal_to) > 0:
                values_satisfying_shares_at_least_one_element_with += values_satisfying_equal_to
                break

        values_not_satisfying_shares_at_least_one_element_with = get_difference(
            self.value.instances, values_satisfying_shares_at_least_one_element_with)

        return \
            values_satisfying_shares_at_least_one_element_with, values_not_satisfying_shares_at_least_one_element_with

    @type_operator(FIELD_SELECT_MULTIPLE)
    def shares_exactly_one_element_with(self, other_value):
        """

        :param other_value : The value we specified while we created a rule.

        Eg.
        If a contact's tags are ["tag1", "tag2", "tag3", "tag4"] and we define a rule for a list that,
         Rule : "Contact's tags shares_exactly_one_element_with ["tag1", "tag2", "tag3"]".
         Then the value "["tag1", "tag2", "tag3"]" of the rule is what other_numeric parameter will refer to.

         As per above example :
         other_numeric : ["tag1", "tag2", "tag3"]
         self.value : VariableValuesWrapper type object consisting of variable and instances
        Value of the each instance will be compared to other_value for shares_exactly_one_element_with operator.

        :return :
        values_satisfying_shares_exactly_one_element_with :list of instances which satisfy the
        shares_exactly_one_element_with condition against other_value

        values_not_satisfying_shares_exactly_one_element_with : list of instances which DOES NOT satisfy the
        shares_exactly_one_element_with condition against other_value

        Instance will be added to values_satisfying_shares_exactly_one_element_with :
            1)If a contact's tags are ["tag1", "tag2", "tag3"] and we define a rule for a list that,
            Rule : "Contact's tags shares_exactly_one_element_with ["tag3", "tag6"].

        Instance will be added to values_not_satisfying_shares_exactly_one_element_with :
            1)If a contact's tags are ["tag1", "tag2", "tag3", "tag4"] and we define a rule for a list that,
             Rule : "Contact's tags shares_exactly_one_element_with ["tag1", "tag5", "tag6"]".

            2) In case if any value of self.value.instances is empty
        """
        list_of_duplicate_values = []
        all_values_satisfying_contains = []

        select = SelectType(self.value)

        for other_val in other_value:
            values_satisfying_equal_to, values_not_satisfying_equal_to = select.contains(other_val)
            list_of_duplicate_values += [i for i in all_values_satisfying_contains for j in values_satisfying_equal_to
                                         if i['id'] == j['id']]
            all_values_satisfying_contains += values_satisfying_equal_to

        values_satisfying_shares_exactly_one_element_with = []
        for single_value in all_values_satisfying_contains:
            if single_value not in list_of_duplicate_values:
                values_satisfying_shares_exactly_one_element_with.append(single_value)

        values_not_satisfying_shares_exactly_one_element_with = get_difference(
            self.value.instances, values_satisfying_shares_exactly_one_element_with)

        return values_satisfying_shares_exactly_one_element_with, values_not_satisfying_shares_exactly_one_element_with

    @type_operator(FIELD_SELECT_MULTIPLE)
    def shares_no_elements_with(self, other_value):
        """

        :param other_value : The value we specified while we created a rule.

        Eg.
        If a contact's tags are ["tag1", "tag2", "tag3", "tag4"] and we define a rule for a list that,
         Rule : "Contact's tags shares_no_elements_with ["tag1", "tag2", "tag3"]".
         Then the value "["tag1", "tag2", "tag3"]" of the rule is what other_numeric parameter will refer to.

         As per above example :
         other_numeric : ["tag1", "tag2", "tag3"]
         self.value : VariableValuesWrapper type object consisting of variable and instances
        Value of the each instance will be compared to other_value for shares_no_elements_with operator.

        :return :
        values_satisfying_shares_no_elements_with :list of instances which satisfy the shares_no_elements_with
        condition against other_value

        values_not_satisfying_shares_no_elements_with : list of instances which DOES NOT satisfy the
        shares_no_elements_with condition against other_value

        Instance will be added to values_satisfying_shares_no_elements_with :
            1) If a contact's tags are ["tag1", "tag2", "tag3", "tag4"] and we define a rule for a list that,
             Rule : "Contact's tags does_not_have_any_of ["tag8", "tag5", "tag6"]".

        Instance will be added to values_not_satisfying_shares_no_elements_with :
            1) If a contact's tags are ["tag1", "tag2", "tag3"] and we define a rule for a list that,
             Rule : "Contact's tags does_not_have_any_of ["tag3", "tag6"].

            2) In case if any value of self.value.instances is empty

         In case if self.value is empty, False will be returned.
        """
        select = SelectType(self.value)
        values_not_satisfying_shares_no_elements_with, values_satisfying_shares_no_elements_with = select.has_at_least_one_of(
            other_value)
        return values_satisfying_shares_no_elements_with, values_not_satisfying_shares_no_elements_with
