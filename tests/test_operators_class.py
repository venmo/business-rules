from unittest import TestCase

from mock import MagicMock

from business_rules.operators import BaseType, type_operator


class OperatorsClassTests(TestCase):
    """Test methods on classes that inherit from BaseType."""

    def test_base_has_no_operators(self):
        self.assertEqual(len(BaseType.get_all_operators()), 0)

    def test_get_all_operators(self):
        """Returns a dictionary listing all the operators on the class
        that can be called on that type, with some data about them.
        """

        class SomeType(BaseType):
            @type_operator(input_type='text')
            def some_operator(self):
                return True

            def not_an_operator(self):
                return 'yo yo'

        operators = SomeType.get_all_operators()
        self.assertEqual(len(operators), 1)
        some_operator = operators[0]
        self.assertEqual(some_operator['name'], 'some_operator')
        self.assertEqual(some_operator['label'], 'Some Operator')
        self.assertEqual(some_operator['input_type'], 'text')

    def test_operator_decorator_casts_argument(self):
        """Any operator that has the @type_operator decorator
        should call _assert_valid_value_and_cast on the parameter.
        """

        class SomeType(BaseType):
            def __init__(self, value):
                self.value = value

            _assert_valid_value_and_cast = MagicMock()

            @type_operator('text')
            def some_operator(self, other_param):
                pass

            @type_operator('text', assert_type_for_arguments=False)
            def other_operator(self, other_param):
                pass

        # casts with positional args
        some_type = SomeType('val')
        some_type.some_operator('foo')  # positional
        some_type._assert_valid_value_and_cast.assert_called_once_with('foo')

        # casts with keyword args
        some_type._assert_valid_value_and_cast.reset_mock()
        some_type.some_operator(other_param='foo2')  # keyword
        some_type._assert_valid_value_and_cast.assert_called_once_with('foo2')

        # does not cast if that argument is set
        some_type._assert_valid_value_and_cast.reset_mock()
        some_type.other_operator('blah')
        some_type.other_operator(other_param='blah')
        self.assertEqual(some_type._assert_valid_value_and_cast.call_count, 0)
