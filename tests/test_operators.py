from pandas.core.frame import DataFrame
from business_rules.operators import (DataframeType, StringType,
                                      NumericType, BooleanType, SelectType,
                                      SelectMultipleType, GenericType)

from . import TestCase
from decimal import Decimal
import sys
import pandas

class StringOperatorTests(TestCase):

    def test_operator_decorator(self):
        self.assertTrue(StringType("foo").equal_to.is_operator)

    def test_string_equal_to(self):
        self.assertTrue(StringType("foo").equal_to("foo"))
        self.assertFalse(StringType("foo").equal_to("Foo"))

    def test_string_not_equal_to(self):
        self.assertTrue(StringType("foo").not_equal_to("Foo"))
        self.assertTrue(StringType("foo").not_equal_to("boo"))
        self.assertFalse(StringType("foo").not_equal_to("foo"))

    def test_string_equal_to_case_insensitive(self):
        self.assertTrue(StringType("foo").equal_to_case_insensitive("FOo"))
        self.assertTrue(StringType("foo").equal_to_case_insensitive("foo"))
        self.assertFalse(StringType("foo").equal_to_case_insensitive("blah"))

    def test_string_starts_with(self):
        self.assertTrue(StringType("hello").starts_with("he"))
        self.assertFalse(StringType("hello").starts_with("hey"))
        self.assertFalse(StringType("hello").starts_with("He"))

    def test_string_ends_with(self):
        self.assertTrue(StringType("hello").ends_with("lo"))
        self.assertFalse(StringType("hello").ends_with("boom"))
        self.assertFalse(StringType("hello").ends_with("Lo"))

    def test_string_contains(self):
        self.assertTrue(StringType("hello").contains("ell"))
        self.assertTrue(StringType("hello").contains("he"))
        self.assertTrue(StringType("hello").contains("lo"))
        self.assertFalse(StringType("hello").contains("asdf"))
        self.assertFalse(StringType("hello").contains("ElL"))

    def test_string_matches_regex(self):
        self.assertTrue(StringType("hello").matches_regex(r"^h"))
        self.assertFalse(StringType("hello").matches_regex(r"^sh"))

    def test_non_empty(self):
        self.assertTrue(StringType("hello").non_empty())
        self.assertFalse(StringType("").non_empty())
        self.assertFalse(StringType(None).non_empty())


class NumericOperatorTests(TestCase):

    def test_instantiate(self):
        err_string = "foo is not a valid numeric type"
        with self.assertRaisesRegexp(AssertionError, err_string):
            NumericType("foo")

    def test_numeric_type_validates_and_casts_decimal(self):
        ten_dec = Decimal(10)
        ten_int = 10
        ten_float = 10.0
        if sys.version_info[0] == 2:
            ten_long = long(10)
        else:
            ten_long = int(10) # long and int are same in python3
        ten_var_dec = NumericType(ten_dec) # this should not throw an exception
        ten_var_int = NumericType(ten_int)
        ten_var_float = NumericType(ten_float)
        ten_var_long = NumericType(ten_long)
        self.assertTrue(isinstance(ten_var_dec.value, Decimal))
        self.assertTrue(isinstance(ten_var_int.value, Decimal))
        self.assertTrue(isinstance(ten_var_float.value, Decimal))
        self.assertTrue(isinstance(ten_var_long.value, Decimal))

    def test_numeric_equal_to(self):
        self.assertTrue(NumericType(10).equal_to(10))
        self.assertTrue(NumericType(10).equal_to(10.0))
        self.assertTrue(NumericType(10).equal_to(10.000001))
        self.assertTrue(NumericType(10.000001).equal_to(10))
        self.assertTrue(NumericType(Decimal('10.0')).equal_to(10))
        self.assertTrue(NumericType(10).equal_to(Decimal('10.0')))
        self.assertFalse(NumericType(10).equal_to(10.00001))
        self.assertFalse(NumericType(10).equal_to(11))

    def test_numeric_not_equal_to(self):
        self.assertTrue(NumericType(10).not_equal_to(10.00001))
        self.assertTrue(NumericType(10).not_equal_to(11))
        self.assertTrue(NumericType(Decimal('10.0')).not_equal_to(Decimal('10.1')))

        self.assertFalse(NumericType(10).not_equal_to(10))
        self.assertFalse(NumericType(10).not_equal_to(10.0))
        self.assertFalse(NumericType(Decimal('10.0')).not_equal_to(Decimal('10.0')))

    def test_other_value_not_numeric(self):
        error_string = "10 is not a valid numeric type"
        with self.assertRaisesRegexp(AssertionError, error_string):
            NumericType(10).equal_to("10")

    def test_numeric_greater_than(self):
        self.assertTrue(NumericType(10).greater_than(1))
        self.assertFalse(NumericType(10).greater_than(11))
        self.assertTrue(NumericType(10.1).greater_than(10))
        self.assertFalse(NumericType(10.000001).greater_than(10))
        self.assertTrue(NumericType(10.000002).greater_than(10))

    def test_numeric_greater_than_or_equal_to(self):
        self.assertTrue(NumericType(10).greater_than_or_equal_to(1))
        self.assertFalse(NumericType(10).greater_than_or_equal_to(11))
        self.assertTrue(NumericType(10.1).greater_than_or_equal_to(10))
        self.assertTrue(NumericType(10.000001).greater_than_or_equal_to(10))
        self.assertTrue(NumericType(10.000002).greater_than_or_equal_to(10))
        self.assertTrue(NumericType(10).greater_than_or_equal_to(10))

    def test_numeric_less_than(self):
        self.assertTrue(NumericType(1).less_than(10))
        self.assertFalse(NumericType(11).less_than(10))
        self.assertTrue(NumericType(10).less_than(10.1))
        self.assertFalse(NumericType(10).less_than(10.000001))
        self.assertTrue(NumericType(10).less_than(10.000002))

    def test_numeric_less_than_or_equal_to(self):
        self.assertTrue(NumericType(1).less_than_or_equal_to(10))
        self.assertFalse(NumericType(11).less_than_or_equal_to(10))
        self.assertTrue(NumericType(10).less_than_or_equal_to(10.1))
        self.assertTrue(NumericType(10).less_than_or_equal_to(10.000001))
        self.assertTrue(NumericType(10).less_than_or_equal_to(10.000002))
        self.assertTrue(NumericType(10).less_than_or_equal_to(10))


class BooleanOperatorTests(TestCase):

    def test_instantiate(self):
        err_string = "foo is not a valid boolean type"
        with self.assertRaisesRegexp(AssertionError, err_string):
            BooleanType("foo")
        err_string = "None is not a valid boolean type"
        with self.assertRaisesRegexp(AssertionError, err_string):
            BooleanType(None)

    def test_boolean_is_true_and_is_false(self):
        self.assertTrue(BooleanType(True).is_true())
        self.assertFalse(BooleanType(True).is_false())
        self.assertFalse(BooleanType(False).is_true())
        self.assertTrue(BooleanType(False).is_false())


class SelectOperatorTests(TestCase):

    def test_contains(self):
        self.assertTrue(SelectType([1, 2]).contains(2))
        self.assertFalse(SelectType([1, 2]).contains(3))
        self.assertTrue(SelectType([1, 2, "a"]).contains("A"))

    def test_does_not_contain(self):
        self.assertTrue(SelectType([1, 2]).does_not_contain(3))
        self.assertFalse(SelectType([1, 2]).does_not_contain(2))
        self.assertFalse(SelectType([1, 2, "a"]).does_not_contain("A"))


class SelectMultipleOperatorTests(TestCase):

    def test_contains_all(self):
        self.assertTrue(SelectMultipleType([1, 2]).
                        contains_all([2, 1]))
        self.assertFalse(SelectMultipleType([1, 2]).
                         contains_all([2, 3]))
        self.assertTrue(SelectMultipleType([1, 2, "a"]).
                        contains_all([2, 1, "A"]))

    def test_is_contained_by(self):
        self.assertTrue(SelectMultipleType([1, 2]).
                        is_contained_by([2, 1, 3]))
        self.assertFalse(SelectMultipleType([1, 2]).
                         is_contained_by([2, 3, 4]))
        self.assertTrue(SelectMultipleType([1, 2, "a"]).
                        is_contained_by([2, 1, "A"]))

    def test_shares_at_least_one_element_with(self):
        self.assertTrue(SelectMultipleType([1, 2]).
                        shares_at_least_one_element_with([2, 3]))
        self.assertFalse(SelectMultipleType([1, 2]).
                         shares_at_least_one_element_with([4, 3]))
        self.assertTrue(SelectMultipleType([1, 2, "a"]).
                        shares_at_least_one_element_with([4, "A"]))

    def test_shares_exactly_one_element_with(self):
        self.assertTrue(SelectMultipleType([1, 2]).
                        shares_exactly_one_element_with([2, 3]))
        self.assertFalse(SelectMultipleType([1, 2]).
                         shares_exactly_one_element_with([4, 3]))
        self.assertTrue(SelectMultipleType([1, 2, "a"]).
                        shares_exactly_one_element_with([4, "A"]))
        self.assertFalse(SelectMultipleType([1, 2, 3]).
                         shares_exactly_one_element_with([2, 3, "a"]))

    def test_shares_no_elements_with(self):
        self.assertTrue(SelectMultipleType([1, 2]).
                        shares_no_elements_with([4, 3]))
        self.assertFalse(SelectMultipleType([1, 2]).
                         shares_no_elements_with([2, 3]))
        self.assertFalse(SelectMultipleType([1, 2, "a"]).
                         shares_no_elements_with([4, "A"]))

class DataframeOperatorTests(TestCase):
    def test_exists(self):
        df = pandas.DataFrame.from_dict({
            "var1": [1,2,4],
            "var2": [3,5,6],
        })
        self.assertTrue(DataframeType(df).exists({"target": "var1"}))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).exists({"target": "--r1"}))
        self.assertFalse(DataframeType(df).exists({"target": "invalid"}))

    def test_not_exists(self):
        df = pandas.DataFrame.from_dict({
            "var1": [1,2,4],
            "var2": [3,5,6]
        })
        self.assertTrue(DataframeType(df).not_exists({"target": "invalid"}))
        self.assertFalse(DataframeType(df).not_exists({"target": "var1"}))
        self.assertFalse(DataframeType(df, column_prefix_map={"--": "va"}).not_exists({"target": "--r1"}))

    def test_equal_to(self):
        df = pandas.DataFrame.from_dict({
            "var1": [1,2,4],
            "var2": [3,5,6],
            "var3": [1,3,8]
        })
        self.assertTrue(DataframeType(df).equal_to({
            "target": "var1",
            "comparator": 2
        }))
        self.assertTrue(DataframeType(df).equal_to({
            "target": "var1",
            "comparator": "var3"
        }))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).equal_to({
            "target": "--r1",
            "comparator": "--r3"
        }))
        self.assertFalse(DataframeType(df).equal_to({
            "target": "var1",
            "comparator": "var2"
        }))
        self.assertFalse(DataframeType(df).equal_to({
            "target": "var1",
            "comparator": 20
        }))

    def test_not_equal_to(self):
        df = pandas.DataFrame.from_dict({
            "var1": [1,2,4],
            "var2": [3,5,6],
            "var3": [1,3,8],
            "var4": [1,2,4]
        })
        self.assertFalse(DataframeType(df).not_equal_to({
            "target": "var1",
            "comparator": "var4"
        }))
        self.assertTrue(DataframeType(df).not_equal_to({
            "target": "var1",
            "comparator": "var2"
        }))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).not_equal_to({
            "target": "--r1",
            "comparator": "--r2"
        }))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).not_equal_to({
            "target": "--r1",
            "comparator": 20
        }))

    def test_equal_to_case_insensitive(self):
        df = pandas.DataFrame.from_dict({
            "var1": ["word", "new", "val"],
            "var2": ["WORD", "test", "VAL"],
            "var3": ["LET", "GO", "read"]
        })
        self.assertTrue(DataframeType(df).equal_to_case_insensitive({
            "target": "var1",
            "comparator": "NEW"
        }))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).equal_to_case_insensitive({
            "target": "--r1",
            "comparator": "--r2"
        }))
        self.assertTrue(DataframeType(df).equal_to_case_insensitive({
            "target": "var1",
            "comparator": "var2"
        }))
        self.assertFalse(DataframeType(df).equal_to({
            "target": "var1",
            "comparator": "var3"
        }))

    def test_not_equal_to_case_insensitive(self):
        df = pandas.DataFrame.from_dict({
            "var1": ["word", "new", "val"],
            "var2": ["WORD", "test", "VAL"],
            "var3": ["LET", "GO", "read"],
            "var4": ["WORD", "NEW", "VAL"]
        })
        self.assertFalse(DataframeType(df).not_equal_to_case_insensitive({
            "target": "var1",
            "comparator": "var4"
        }))
        self.assertTrue(DataframeType(df).not_equal_to_case_insensitive({
            "target": "var1",
            "comparator": "var2"
        }))

    def test_less_than(self):
        df = pandas.DataFrame.from_dict({
            "var1": [1,2,4],
            "var2": [3,5,6],
            "var3": [1,3,8],
            "var4": [1,2,4]
        })
        self.assertFalse(DataframeType(df).less_than({
            "target": "var1",
            "comparator": "var4"
        }))
        self.assertTrue(DataframeType(df).less_than({
            "target": "var1",
            "comparator": "var3"
        }))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).less_than({
            "target": "--r1",
            "comparator": "var3"
        }))
        self.assertFalse(DataframeType(df).less_than({
            "target": "var2",
            "comparator": 2
        }))
        self.assertTrue(DataframeType(df).less_than({
            "target": "var1",
            "comparator": 3
        }))

    def test_less_than_or_equal_to(self):
        df = pandas.DataFrame.from_dict({
            "var1": [1,2,4],
            "var2": [3,5,6],
            "var3": [1,3,8],
            "var4": [1,2,4]
        })
        self.assertTrue(DataframeType(df).less_than_or_equal_to({
            "target": "var1",
            "comparator": "var4"
        }))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).less_than_or_equal_to({
            "target": "--r1",
            "comparator": "var4"
        }))
        self.assertFalse(DataframeType(df).less_than_or_equal_to({
            "target": "var2",
            "comparator": "var1"
        }))
        self.assertFalse(DataframeType(df).less_than_or_equal_to({
            "target": "var2",
            "comparator": 2
        }))
        self.assertTrue(DataframeType(df).less_than_or_equal_to({
            "target": "var2",
            "comparator": "var3"
        }))

    def test_greater_than(self):
        df = pandas.DataFrame.from_dict({
            "var1": [1,2,4],
            "var2": [3,5,6],
            "var3": [1,3,8],
            "var4": [1,2,4]
        })
        self.assertFalse(DataframeType(df).greater_than({
            "target": "var1",
            "comparator": "var4"
        }))
        self.assertFalse(DataframeType(df).greater_than({
            "target": "var1",
            "comparator": "var3"
        }))
        self.assertFalse(DataframeType(df, column_prefix_map={"--": "va"}).greater_than({
            "target": "var1",
            "comparator": "--r3"
        }))
        self.assertTrue(DataframeType(df).greater_than({
            "target": "var2",
            "comparator": 2
        }))
        self.assertFalse(DataframeType(df).greater_than({
            "target": "var1",
            "comparator": 5000
        }))

    def test_greater_than_or_equal_to(self):
        df = pandas.DataFrame.from_dict({
            "var1": [1,2,4],
            "var2": [3,5,6],
            "var3": [1,3,8],
            "var4": [1,2,4]
        })
        self.assertTrue(DataframeType(df).greater_than_or_equal_to({
            "target": "var1",
            "comparator": "var4"
        }))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).greater_than_or_equal_to({
            "target": "var1",
            "comparator": "--r4"
        }))
        self.assertTrue(DataframeType(df).greater_than_or_equal_to({
            "target": "var2",
            "comparator": "var3"
        }))
        self.assertTrue(DataframeType(df).greater_than_or_equal_to({
            "target": "var2",
            "comparator": 2
        }))

    def test_contains(self):
        df = pandas.DataFrame.from_dict({
            "var1": [1,2,4],
            "var2": [3,5,6],
            "var3": [1,3,8],
            "var4": [1,2,4]
        })
        self.assertTrue(DataframeType(df).contains({
            "target": "var1",
            "comparator": 2
        }))
        self.assertTrue(DataframeType(df).contains({
            "target": "var1",
            "comparator": "var3"
        }))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).contains({
            "target": "var1",
            "comparator": "--r3"
        }))
        self.assertFalse(DataframeType(df).contains({
            "target": "var1",
            "comparator": "var2"
        }))

    def test_does_not_contain(self):
        df = pandas.DataFrame.from_dict({
            "var1": [1,2,4],
            "var2": [3,5,6],
            "var3": [1,3,8],
            "var4": [1,2,4]
        })
        self.assertTrue(DataframeType(df).does_not_contain({
            "target": "var1",
            "comparator": 5
        }))
        self.assertFalse(DataframeType(df).does_not_contain({
            "target": "var1",
            "comparator": "var3"
        }))
        self.assertFalse(DataframeType(df, column_prefix_map={"--": "va"}).does_not_contain({
            "target": "var1",
            "comparator": "--r3"
        }))
        self.assertTrue(DataframeType(df).does_not_contain({
            "target": "var1",
            "comparator": "var2"
        }))

    def test_contains_case_insensitive(self):
        df = pandas.DataFrame.from_dict({
            "var1": ["pikachu", "charmander", "squirtle"],
            "var2": ["PIKACHU", "CHARIZARD", "BULBASAUR"],
            "var3": ["POKEMON", "CHARIZARD", "BULBASAUR"],
        })
        self.assertTrue(DataframeType(df).contains_case_insensitive({
            "target": "var1",
            "comparator": "PIKACHU"
        }))
        self.assertTrue(DataframeType(df).contains_case_insensitive({
            "target": "var1",
            "comparator": "var2"
        }))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).contains_case_insensitive({
            "target": "var1",
            "comparator": "var2"
        }))
        self.assertFalse(DataframeType(df).contains_case_insensitive({
            "target": "var1",
            "comparator": "var3"
        }))

    def test_does_not_contain_case_insensitive(self):
        df = pandas.DataFrame.from_dict({
            "var1": ["pikachu", "charmander", "squirtle"],
            "var2": ["PIKACHU", "CHARIZARD", "BULBASAUR"],
            "var3": ["pikachu", "charizard", "bulbasaur"],
        })
        self.assertTrue(DataframeType(df).does_not_contain_case_insensitive({
            "target": "var1",
            "comparator": "IVYSAUR"
        }))
        self.assertFalse(DataframeType(df).does_not_contain_case_insensitive({
            "target": "var3",
            "comparator": "var2"
        }))

    def test_is_contained_by(self):
        df = pandas.DataFrame.from_dict({
            "var1": [1,2,4],
            "var2": [3,5,6],
            "var3": [1,3,8],
            "var4": [1,2,4]
        })
        self.assertTrue(DataframeType(df).is_contained_by({
            "target": "var1",
            "comparator": [4,5,6]
        }))
        self.assertTrue(DataframeType(df).is_contained_by({
            "target": "var1",
            "comparator": "var3"
        }))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).is_contained_by({
            "target": "var1",
            "comparator": "--r3"
        }))
        self.assertFalse(DataframeType(df).is_contained_by({
            "target": "var1",
            "comparator": [9, 10, 11]
        }))
        self.assertFalse(DataframeType(df).is_contained_by({
            "target": "var1",
            "comparator": "var2"
        }))

    def test_is_not_contained_by(self):
        df = pandas.DataFrame.from_dict({
            "var1": [1,2,4],
            "var2": [3,5,6],
            "var3": [1,3,8],
            "var4": [1,2,4]
        })
        self.assertTrue(DataframeType(df).is_not_contained_by({
            "target": "var1",
            "comparator": "var3"
        }))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).is_not_contained_by({
            "target": "var1",
            "comparator": "--r3"
        }))
        self.assertTrue(DataframeType(df).is_not_contained_by({
            "target": "var1",
            "comparator": [9, 10, 11]
        }))
        self.assertFalse(DataframeType(df).is_not_contained_by({
            "target": "var1",
            "comparator": "var1"
        }))

    def test_is_contained_by_case_insensitive(self):
        df = pandas.DataFrame.from_dict({
            "var1": ["WORD", "test"],
            "var2": ["word", "TEST"],
            "var3": ["another", "item"]
        })
        self.assertTrue(DataframeType(df).is_contained_by_case_insensitive({
            "target": "var1",
            "comparator": ["word", "TEST"]
        }))
        self.assertTrue(DataframeType(df).is_contained_by_case_insensitive({
            "target": "var1",
            "comparator": "var1"
        }))
        self.assertFalse(DataframeType(df).is_contained_by_case_insensitive({
            "target": "var1",
            "comparator": "var3"
        }))
        self.assertFalse(DataframeType(df, column_prefix_map={"--": "va"}).is_contained_by_case_insensitive({
            "target": "var1",
            "comparator": "--r3"
        }))

    def test_is_not_contained_by_case_insensitive(self):
        df = pandas.DataFrame.from_dict({
            "var1": ["WORD", "test"],
            "var2": ["word", "TEST"],
            "var3": ["another", "item"]
        })
        self.assertFalse(DataframeType(df).is_not_contained_by_case_insensitive({
            "target": "var1",
            "comparator": ["word", "TEST"]
        }))
        self.assertTrue(DataframeType(df).is_not_contained_by_case_insensitive({
            "target": "var1",
            "comparator": "var3"
        }))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).is_not_contained_by_case_insensitive({
            "target": "var1",
            "comparator": "--r3"
        }))

    def test_prefix_matches_regex(self):
        df = pandas.DataFrame.from_dict({
            "var1": ["WORD", "test"],
            "var2": ["word", "TEST"],
            "var3": ["another", "item"]
        })
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).prefix_matches_regex({
            "target": "--r2",
            "comparator": "w.*",
            "prefix": 2
        }))
        self.assertFalse(DataframeType(df).prefix_matches_regex({
            "target": "var2",
            "comparator": "[0-9].*",
            "prefix": 2
        }))

    def test_suffix_matches_regex(self):
        df = pandas.DataFrame.from_dict({
            "var1": ["WORD", "test"],
            "var2": ["word", "TEST"],
            "var3": ["another", "item"]
        })
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).suffix_matches_regex({
            "target": "--r1",
            "comparator": "es.*",
            "suffix": 3
        }))
        self.assertFalse(DataframeType(df).suffix_matches_regex({
            "target": "var1",
            "comparator": "[0-9].*",
            "suffix": 3
        }))

    def test_not_prefix_matches_suffix(self):
        df = pandas.DataFrame.from_dict({
            "var1": ["WORD", "test"],
            "var2": ["word", "TEST"],
            "var3": ["another", "item"]
        })
        self.assertFalse(DataframeType(df, column_prefix_map={"--": "va"}).not_prefix_matches_regex({
            "target": "--r1",
            "comparator": ".*",
            "prefix": 2
        }))
        self.assertTrue(DataframeType(df).not_prefix_matches_regex({
            "target": "var2",
            "comparator": "[0-9].*",
            "prefix": 2
        }))

    def test_not_suffix_matches_regex(self):
        df = pandas.DataFrame.from_dict({
            "var1": ["WORD", "test"],
            "var2": ["word", "TEST"],
            "var3": ["another", "item"]
        })
        self.assertFalse(DataframeType(df).not_suffix_matches_regex({
            "target": "var1",
            "comparator": ".*",
            "suffix": 3
        }))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).not_suffix_matches_regex({
            "target": "--r1",
            "comparator": "[0-9].*",
            "suffix": 3
        }))

    def test_matches_suffix(self):
        df = pandas.DataFrame.from_dict({
            "var1": ["WORD", "test"],
            "var2": ["word", "TEST"],
            "var3": ["another", "item"]
        })
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).matches_regex({
            "target": "--r1",
            "comparator": ".*",
        }))
        self.assertFalse(DataframeType(df).matches_regex({
            "target": "var2",
            "comparator": "[0-9].*",
        }))

    def test_not_matches_regex(self):
        df = pandas.DataFrame.from_dict({
            "var1": ["WORD", "test"],
            "var2": ["word", "TEST"],
            "var3": ["another", "item"]
        })
        self.assertFalse(DataframeType(df).not_matches_regex({
            "target": "var1",
            "comparator": ".*",
        }))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).not_matches_regex({
            "target": "--r1",
            "comparator": "[0-9].*",
        }))

    def test_starts_with(self):
        df = pandas.DataFrame.from_dict({
            "var1": ["WORD", "test"],
            "var2": ["word", "TEST"],
            "var3": ["another", "item"]
        })
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).starts_with({
            "target": "--r1",
            "comparator": "WO",
        }))
        self.assertFalse(DataframeType(df).starts_with({
            "target": "var2",
            "comparator": "ABC",
        }))

    def test_ends_with(self):
        df = pandas.DataFrame.from_dict({
            "var1": ["WORD", "test"],
            "var2": ["word", "TEST"],
            "var3": ["another", "item"]
        })
        self.assertFalse(DataframeType(df, column_prefix_map={"--": "va"}).ends_with({
            "target": "--r1",
            "comparator": "abc",
        }))
        self.assertTrue(DataframeType(df).ends_with({
            "target": "var1",
            "comparator": "est",
        }))

    def test_has_equal_length(self):
        df = pandas.DataFrame.from_dict(
            {
                "var_1": ['test', 'value']
            }
        )
        df_operator = DataframeType(df, column_prefix_map={"--": "va"})
        result = df_operator.has_equal_length({"target": "--r_1", "comparator": 4})
        self.assertTrue(result)

    def test_has_not_equal_length(self):
        df = pandas.DataFrame.from_dict(
            {
                "var_1": ['test', 'value']
            }
        )
        df_operator = DataframeType(df, column_prefix_map={"--": "va"})
        result = df_operator.has_not_equal_length({"target": "--r_1", "comparator": 4})
        self.assertTrue(result)

    def test_longer_than(self):
        df = pandas.DataFrame.from_dict(
            {
                "var_1": ['test', 'value']
            }
        )
        df_operator = DataframeType(df, column_prefix_map={"--": "va"})
        self.assertTrue(df_operator.longer_than({"target": "--r_1", "comparator": 3}))

    def test_longer_than_or_equal_to(self):
        df = pandas.DataFrame.from_dict(
            {
                "var_1": ['test', 'alex']
            }
        )
        df_operator = DataframeType(df, column_prefix_map={"--": "va"})
        self.assertTrue(df_operator.longer_than_or_equal_to({"target": "--r_1", "comparator": 3}))
        self.assertTrue(df_operator.longer_than_or_equal_to({"target": "var_1", "comparator": 4}))

    def test_shorter_than(self):
        df = pandas.DataFrame.from_dict(
            {
                "var_1": ['test', 'val']
            }
        )
        df_operator = DataframeType(df, column_prefix_map={"--": "va"})
        self.assertTrue(df_operator.shorter_than({"target": "--r_1", "comparator": 5}))

    def test_shorter_than_or_equal_to(self):
        df = pandas.DataFrame.from_dict(
            {
                "var_1": ['test', 'alex']
            }
        )
        df_operator = DataframeType(df, column_prefix_map={"--": "va"})
        self.assertTrue(df_operator.shorter_than_or_equal_to({"target": "--r_1", "comparator": 5}))
        self.assertTrue(df_operator.shorter_than_or_equal_to({"target": "var_1", "comparator": 4}))

    def test_contains_all(self):
        df = pandas.DataFrame.from_dict(
            {
                "var1": ['test', 'value', 'word'],
                "var2": ["test", "value", "test"]
            }
        )
        self.assertTrue(DataframeType(df).contains_all({
            "target": "var1",
            "comparator": "var2",
        }))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).contains_all({
            "target": "--r1",
            "comparator": "--r2",
        }))
        self.assertFalse(DataframeType(df).contains_all({
            "target": "var2",
            "comparator": "var1",
        }))
        self.assertTrue(DataframeType(df).contains_all({
            "target": "var2",
            "comparator": ["test", "value"],
        }))

    def test_not_contains_all(self):
        df = pandas.DataFrame.from_dict(
            {
                "var1": ['test', 'value', 'word'],
                "var2": ["test", "value", "test"]
            }
        )
        self.assertTrue(DataframeType(df).contains_all({
            "target": "var1",
            "comparator": "var2",
        }))
        self.assertFalse(DataframeType(df).contains_all({
            "target": "var2",
            "comparator": "var1",
        }))
        self.assertTrue(DataframeType(df).contains_all({
            "target": "var2",
            "comparator": ["test", "value"],
        }))

    def test_invalid_date(self):
        df = pandas.DataFrame.from_dict(
            {
                "var1": ['2021', '2021', '2021', '2021', '2099'],
                "var2": ["2099", "2022", "2034", "90999", "20999"],
                "var3": ["1997-07", "1997-07-16", "1997-07-16T19:20:30.45+01:00", "1997-07-16T19:20:30+01:00", "1997-07-16T19:20+01:00"], 
            }
        )
        self.assertFalse(DataframeType(df, column_prefix_map={"--": "va"}).invalid_date({"target": "--r1"}))
        self.assertFalse(DataframeType(df).invalid_date({"target": "var3"}))
        self.assertTrue(DataframeType(df).invalid_date({"target": "var2"}))
    
    def test_date_equal_to(self):
        df = pandas.DataFrame.from_dict(
            {
                "var1": ['2021', '2021', '2021', '2021', '2021'],
                "var2": ["2099", "2022", "2034", "90999", "20999"],
                "var3": ["1997-07", "1997-07-16", "1997-07-16T19:20:30.45+01:00", "1997-07-16T19:20:30+01:00", "1997-07-16T19:20+01:00"],
                "var4": ["1997-07", "1997-07-16", "1997-07-16T19:20:30.45+01:00", "1997-07-16T19:20:30+01:00", "1997-07-16T19:20+01:00"],
                "var5": ["1997-08", "1997-08-16", "1997-08-16T19:20:30.45+01:00", "1997-08-16T19:20:30+01:00", "1997-08-16T19:20+01:00"],
                "var6": ["1998-08", "1998-08-11", "1998-08-17T20:21:31.46+01:00", "1998-08-17T20:21:31+01:00", "1998-08-17T20:21+01:00"]
            }
        )
        self.assertTrue(DataframeType(df).date_equal_to({"target": "var1", "comparator": '2021'}))
        self.assertTrue(DataframeType(df).date_equal_to({"target": "var3", "comparator": "1997-07-16T19:20:30.45+01:00"}))
        self.assertTrue(DataframeType(df).date_equal_to({"target": "var3", "comparator": "var4"}))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "va"}).date_equal_to({"target": "--r3", "comparator": "--r4", "date_component": "year"}))
        self.assertTrue(DataframeType(df).date_equal_to({"target": "var3", "comparator": "var5", "date_component": "hour"}))
        self.assertTrue(DataframeType(df).date_equal_to({"target": "var3", "comparator": "var5", "date_component": "minute"}))
        self.assertTrue(DataframeType(df).date_equal_to({"target": "var3", "comparator": "var5", "date_component": "second"}))
        self.assertTrue(DataframeType(df).date_equal_to({"target": "var3", "comparator": "var5", "date_component": "microsecond"}))
        self.assertTrue(DataframeType(df).date_equal_to({"target": "var3", "comparator": "var5", "date_component": "year"}))
        self.assertFalse(DataframeType(df).date_equal_to({"target": "var3", "comparator": "var5", "date_component": "month"}))
        self.assertFalse(DataframeType(df).date_equal_to({"target": "var3", "comparator": "var6", "date_component": "year"}))
        self.assertFalse(DataframeType(df).date_equal_to({"target": "var3", "comparator": "var6", "date_component": "month"}))
    
    def test_date_not_equal_to(self):
        df = pandas.DataFrame.from_dict(
            {
                "var1": ['2021', '2021', '2021', '2021', '2021'],
                "var2": ["2099", "2022", "2034", "90999", "20999"],
                "var3": ["1997-07", "1997-07-16", "1997-07-16T19:20:30.45+01:00", "1997-07-16T19:20:30+01:00", "1997-07-16T19:20+01:00"],
                "var4": ["1997-07", "1997-07-16", "1997-07-16T19:20:30.45+01:00", "1997-07-16T19:20:30+01:00", "1997-07-16T19:20+01:00"],
                "var5": ["1997-08", "1997-08-16", "1997-08-16T19:20:30.45+01:00", "1997-08-16T19:20:30+01:00", "1997-08-16T19:20+01:00"],
                "var6": ["1998-08", "1998-08-11", "1998-08-17T20:21:31.46+01:00", "1998-08-17T20:21:31+01:00", "1998-08-17T20:21+01:00"]
            }
        )
        self.assertTrue(DataframeType(df).date_not_equal_to({"target": "var1", "comparator": '2022'}))
        self.assertTrue(DataframeType(df).date_not_equal_to({"target": "var3", "comparator": "1998-07-16T19:20:30.45+01:00"}))
        self.assertFalse(DataframeType(df).date_not_equal_to({"target": "var3", "comparator": "var4"}))
        self.assertFalse(DataframeType(df).date_not_equal_to({"target": "var3", "comparator": "var4", "date_component": "year"}))
        self.assertTrue(DataframeType(df).date_not_equal_to({"target": "var3", "comparator": "var6", "date_component": "hour"}))
        self.assertTrue(DataframeType(df).date_not_equal_to({"target": "var3", "comparator": "var6", "date_component": "minute"}))
        self.assertTrue(DataframeType(df).date_not_equal_to({"target": "var3", "comparator": "var6", "date_component": "second"}))
        self.assertTrue(DataframeType(df).date_not_equal_to({"target": "var3", "comparator": "var6", "date_component": "microsecond"}))
        self.assertTrue(DataframeType(df).date_not_equal_to({"target": "var3", "comparator": "var6", "date_component": "year"}))
        self.assertTrue(DataframeType(df).date_not_equal_to({"target": "var3", "comparator": "var6", "date_component": "month"}))
        self.assertFalse(DataframeType(df).date_not_equal_to({"target": "var3", "comparator": "var5", "date_component": "year"}))
        self.assertTrue(DataframeType(df).date_not_equal_to({"target": "var3", "comparator": "var5", "date_component": "month"}))
        self.assertFalse(DataframeType(df).date_not_equal_to({"target": "var3", "comparator": "var5", "date_component": "day"}))
        self.assertFalse(DataframeType(df).date_not_equal_to({"target": "var3", "comparator": "var5", "date_component": "hour"}))
        self.assertFalse(DataframeType(df).date_not_equal_to({"target": "var3", "comparator": "var5", "date_component": "second"}))
        self.assertFalse(DataframeType(df).date_not_equal_to({"target": "var3", "comparator": "var5", "date_component": "microsecond"}))
    
    def test_date_less_than(self):
        df = pandas.DataFrame.from_dict(
            {
                "var1": ['2021', '2021', '2021', '2021', '2021'],
                "var2": ["2099", "2022", "2034", "90999", "20999"],
                "var3": ["1997-07", "1997-07-16", "1997-07-16T19:20:30.45+01:00", "1997-07-16T19:20:30+01:00", "1997-07-16T19:20+01:00"],
                "var4": ["1997-07", "1997-07-16", "1997-07-16T19:20:30.45+01:00", "1997-07-16T19:20:30+01:00", "1997-07-16T19:20+01:00"],
                "var5": ["1997-08", "1997-08-16", "1997-08-16T19:20:30.45+01:00", "1997-08-16T19:20:30+01:00", "1997-08-16T19:20+01:00"],
                "var6": ["1998-08", "1998-08-11", "1998-08-17T20:21:31.46+01:00", "1998-08-17T20:21:31+01:00", "1998-08-17T20:21+01:00"]
            }
        )
        self.assertTrue(DataframeType(df).date_less_than({"target": "var1", "comparator": '2022'}))
        self.assertTrue(DataframeType(df).date_less_than({"target": "var3", "comparator": "1998-07-16T19:20:30.45+01:00"}))
        self.assertFalse(DataframeType(df).date_less_than({"target": "var3", "comparator": "var4"}))
        self.assertFalse(DataframeType(df).date_less_than({"target": "var3", "comparator": "var4", "date_component": "year"}))
        self.assertTrue(DataframeType(df).date_less_than({"target": "var3", "comparator": "var6", "date_component": "hour"}))

    def test_date_greater_than(self):
        df = pandas.DataFrame.from_dict(
            {
                "var1": ['2021', '2021', '2021', '2021', '2021'],
                "var2": ["2099", "2022", "2034", "90999", "20999"],
                "var3": ["1997-07", "1997-07-16", "1997-07-16T19:20:30.45+01:00", "1997-07-16T19:20:30+01:00", "1997-07-16T19:20+01:00"],
                "var4": ["1997-07", "1997-07-16", "1997-07-16T19:20:30.45+01:00", "1997-07-16T19:20:30+01:00", "1997-07-16T19:20+01:00"],
                "var5": ["1997-08", "1997-08-16", "1997-08-16T19:20:30.45+01:00", "1997-08-16T19:20:30+01:00", "1997-08-16T19:20+01:00"],
                "var6": ["1998-08", "1998-08-11", "1998-08-17T20:21:31.46+01:00", "1998-08-17T20:21:31+01:00", "1998-08-17T20:21+01:00"]
            }
        )
        self.assertTrue(DataframeType(df).date_greater_than({"target": "var1", "comparator": '2020'}))
        self.assertTrue(DataframeType(df).date_greater_than({"target": "var3", "comparator": "1996-07-16T19:20:30.45+01:00"}))
        self.assertFalse(DataframeType(df).date_greater_than({"target": "var3", "comparator": "var4"}))
        self.assertFalse(DataframeType(df).date_greater_than({"target": "var3", "comparator": "var4", "date_component": "year"}))
        self.assertTrue(DataframeType(df).date_greater_than({"target": "var6", "comparator": "var3", "date_component": "hour"}))
    
    def test_date_greater_than_or_equal_to(self):
        df = pandas.DataFrame.from_dict(
            {
                "var1": ['2021', '2021', '2021', '2021', '2021'],
                "var2": ["2099", "2022", "2034", "90999", "20999"],
                "var3": ["1997-07", "1997-07-16", "1997-07-16T19:20:30.45+01:00", "1997-07-16T19:20:30+01:00", "1997-07-16T19:20+01:00"],
                "var4": ["1997-07", "1997-07-16", "1997-07-16T19:20:30.45+01:00", "1997-07-16T19:20:30+01:00", "1997-07-16T19:20+01:00"],
                "var5": ["1997-08", "1997-08-16", "1997-08-16T19:20:30.45+01:00", "1997-08-16T19:20:30+01:00", "1997-08-16T19:20+01:00"],
                "var6": ["1998-08", "1998-08-11", "1998-08-17T20:21:31.46+01:00", "1998-08-17T20:21:31+01:00", "1998-08-17T20:21+01:00"]
            }
        )
        self.assertTrue(DataframeType(df).date_greater_than_or_equal_to({"target": "var1", "comparator": '2020'}))
        self.assertFalse(DataframeType(df).date_greater_than_or_equal_to({"target": "var1", "comparator": '2023'}))
        self.assertTrue(DataframeType(df).date_greater_than_or_equal_to({"target": "var3", "comparator": "1996-07-16T19:20:30.45+01:00"}))
        self.assertTrue(DataframeType(df).date_greater_than_or_equal_to({"target": "var3", "comparator": "var4"}))
        self.assertTrue(DataframeType(df).date_greater_than_or_equal_to({"target": "var3", "comparator": "var4", "date_component": "year"}))
        self.assertTrue(DataframeType(df).date_greater_than_or_equal_to({"target": "var6", "comparator": "var3", "date_component": "hour"}))
    
    def test_date_less_than_or_equal_to(self):
        df = pandas.DataFrame.from_dict(
            {
                "var1": ['2021', '2021', '2021', '2021', '2021'],
                "var2": ["2099", "2022", "2034", "90999", "20999"],
                "var3": ["1997-07", "1997-07-16", "1997-07-16T19:20:30.45+01:00", "1997-07-16T19:20:30+01:00", "1997-07-16T19:20+01:00"],
                "var4": ["1997-07", "1997-07-16", "1997-07-16T19:20:30.45+01:00", "1997-07-16T19:20:30+01:00", "1997-07-16T19:20+01:00"],
                "var5": ["1997-08", "1997-08-16", "1997-08-16T19:20:30.45+01:00", "1997-08-16T19:20:30+01:00", "1997-08-16T19:20+01:00"],
                "var6": ["1998-08", "1998-08-11", "1998-08-17T20:21:31.46+01:00", "1998-08-17T20:21:31+01:00", "1998-08-17T20:21+01:00"]
            }
        )
        self.assertTrue(DataframeType(df).date_less_than_or_equal_to({"target": "var1", "comparator": '2022'}))
        self.assertFalse(DataframeType(df).date_less_than_or_equal_to({"target": "var1", "comparator": '2020'}))
        self.assertTrue(DataframeType(df).date_less_than_or_equal_to({"target": "var3", "comparator": "1998-07-16T19:20:30.45+01:00"}))
        self.assertTrue(DataframeType(df).date_less_than_or_equal_to({"target": "var3", "comparator": "var4"}))
        self.assertTrue(DataframeType(df).date_less_than_or_equal_to({"target": "var3", "comparator": "var4", "date_component": "year"}))
        self.assertTrue(DataframeType(df).date_less_than_or_equal_to({"target": "var6", "comparator": "var3", "date_component": "hour"}))
        
    def test_is_complete_date(self):
        df = pandas.DataFrame.from_dict(
            {
                "var1": [ '2021', '2021', '2099'],
                "var2": [ "1997-07-16", "1997-07-16T19:20:30+01:00", "1997-07-16T19:20+01:00"], 
            }
        )
        self.assertTrue(DataframeType(df).is_incomplete_date({"target" : "var1"}))
        self.assertFalse(DataframeType(df).is_incomplete_date({"target" : "var2"}))

    def test_is_unique_set(self):
        df = pandas.DataFrame.from_dict( {"ARM": ["PLACEBO", "PLACEBO", "A", "A"], "TAE": [1,1,1,2], "LAE": [1,2,1,2], "ARF": [1,2,3,4]})
        self.assertTrue(DataframeType(df).is_unique_set({"target" : "ARM", "comparator": "LAE"}))
        self.assertTrue(DataframeType(df).is_unique_set({"target" : "ARM", "comparator": ["LAE"]}))
        self.assertFalse(DataframeType(df).is_unique_set({"target" : "ARM", "comparator": ["TAE"]}))
        self.assertFalse(DataframeType(df).is_unique_set({"target" : "ARM", "comparator": "TAE"}))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "AR"}).is_unique_set({"target" : "--M", "comparator": "--F"}))
        self.assertTrue(DataframeType(df, column_prefix_map={"--": "AR"}).is_unique_set({"target" : "--M", "comparator": ["--F"]}))

    def test_is_not_unique_set(self):
        df = pandas.DataFrame.from_dict( {"ARM": ["PLACEBO", "PLACEBO", "A", "A"], "TAE": [1,1,1,2], "LAE": [1,2,1,2], "ARF": [1,2,3,4]})
        self.assertFalse(DataframeType(df).is_not_unique_set({"target" : "ARM", "comparator": "LAE"}))
        self.assertFalse(DataframeType(df).is_not_unique_set({"target" : "ARM", "comparator": ["LAE"]}))
        self.assertTrue(DataframeType(df).is_not_unique_set({"target" : "ARM", "comparator": ["TAE"]}))
        self.assertTrue(DataframeType(df).is_not_unique_set({"target" : "ARM", "comparator": "TAE"}))
        self.assertFalse(DataframeType(df, column_prefix_map={"--": "AR"}).is_not_unique_set({"target" : "--M", "comparator": "--F"}))
        self.assertFalse(DataframeType(df, column_prefix_map={"--": "AR"}).is_not_unique_set({"target" : "--M", "comparator": ["--F"]}))

    def test_is_unique_relationship(self):
        """
        Test validates one-to-one relationship against a dataset.
        One-to-one means that a pir of columns can be duplicated
        but its integrity should not be violated.
        """
        one_to_one_related_df = pandas.DataFrame.from_dict(
            {
                "STUDYID": [1, 2, 3, 1, 2],
                "STUDYDESC": ["Russia", "USA", "China", "Russia", "USA", ],
            }
        )
        self.assertTrue(
            DataframeType(one_to_one_related_df).is_unique_relationship(
                {"target": "STUDYID", "comparator": "STUDYDESC"}
            )
        )
        self.assertTrue(
            DataframeType(one_to_one_related_df, column_prefix_map={"--": "STUDY"}).is_unique_relationship(
                {"target": "--ID", "comparator": "--DESC"}
            )
        )

        df_violates_one_to_one = pandas.DataFrame.from_dict(
            {
                "TESTID": [1, 2, 1, 3],
                "TESTNAME": ["Functional", "Stress", "Functional", "Stress", ],
            }
        )
        self.assertFalse(DataframeType(df_violates_one_to_one).is_unique_relationship(
            {"target": "TESTID", "comparator": "TESTNAME"})
        )

    def test_is_not_unique_relationship(self):
        """
        Test validates one-to-one relationship against a dataset.
        One-to-one means that a pir of columns can be duplicated
        but its integrity should not be violated.
        """
        valid_df = pandas.DataFrame.from_dict(
            {
                "VISITNUM": [1, 2, 1, 3],
                "VISIT": ["Consulting", "Surgery", "Consulting", "Treatment", ],
            }
        )
        self.assertFalse(DataframeType(valid_df).is_not_unique_relationship(
            {"target": "VISITNUM", "comparator": "VISIT"})
        )

        valid_df_1 = pandas.DataFrame.from_dict(
            {
                "VISIT": ["Consulting", "Surgery", "Consulting", "Treatment", ],
                "VISITDESC": [
                    "Doctor Consultation", "Heart Surgery", "Doctor Consultation", "Long Lasting Treatment",
                ],
            }
        )
        self.assertFalse(DataframeType(valid_df_1).is_not_unique_relationship(
            {"target": "VISIT", "comparator": "VISITDESC"})
        )

        df_violates_one_to_one = pandas.DataFrame.from_dict(
            {
                "VISITNUM": [1, 2, 1, 3],
                "VISIT": ["Consulting", "Surgery", "Consulting", "Consulting", ],
            }
        )
        self.assertTrue(DataframeType(df_violates_one_to_one).is_not_unique_relationship(
            {"target": "VISITNUM", "comparator": "VISIT"})
        )

        df_violates_one_to_one_1 = pandas.DataFrame.from_dict(
            {
                "VISIT": ["Consulting", "Surgery", "Consulting", "Treatment", ],
                "VISITDESC": ["Doctor Consultation", "Heart Surgery", "Heart Surgery", "Long Lasting Treatment", ],
            }
        )
        self.assertTrue(DataframeType(df_violates_one_to_one_1).is_not_unique_relationship(
            {"target": "VISIT", "comparator": "VISITDESC"})
        )
        self.assertTrue(DataframeType(df_violates_one_to_one_1, column_prefix_map={"--": "VI"}).is_not_unique_relationship(
            {"target": "--SIT", "comparator": "--SITDESC"})
        )


class GenericOperatorTests(TestCase):
    def test_shares_no_elements_with(self):
        self.assertTrue(GenericType([1, 2]).
                        shares_no_elements_with([4, 3]))
        self.assertFalse(GenericType([1, 2]).
                         shares_no_elements_with([2, 3]))
        self.assertFalse(GenericType([1, 2, "a"]).
                         shares_no_elements_with([4, "A"]))
                    
    def test_contains(self):
        self.assertTrue(GenericType([1, 2]).contains(2))
        self.assertFalse(GenericType([1, 2]).contains(3))
        self.assertTrue(GenericType([1, 2, "a"]).contains("a"))

    def test_does_not_contain(self):
        self.assertTrue(GenericType([1, 2]).does_not_contain(3))
        self.assertFalse(GenericType([1, 2]).does_not_contain(2))
        self.assertFalse(GenericType([1, 2, "a"]).does_not_contain("A"))
    
    def test_boolean_is_true_and_is_false(self):
        self.assertTrue(GenericType(True).is_true())
        self.assertFalse(GenericType(True).is_false())
        self.assertFalse(GenericType(False).is_true())
        self.assertTrue(GenericType(False).is_false())


    def test_numeric_equal_to(self):
        self.assertTrue(GenericType(10).equal_to(10))
        self.assertTrue(GenericType(10).equal_to(10.0))
        self.assertTrue(GenericType(10).equal_to(10.000001))
        self.assertTrue(GenericType(10.000001).equal_to(10))
        self.assertTrue(GenericType(Decimal('10.0')).equal_to(10))
        self.assertTrue(GenericType(10).equal_to(Decimal('10.0')))
        self.assertFalse(GenericType(10).equal_to(10.00001))
        self.assertFalse(GenericType(10).equal_to(11))

    def test_numeric_not_equal_to(self):
        self.assertFalse(GenericType(10).not_equal_to(10))
        self.assertFalse(GenericType(10).not_equal_to(10.0))
        self.assertFalse(GenericType(10).not_equal_to(10.000001))
        self.assertFalse(GenericType(10.000001).not_equal_to(10))
        self.assertFalse(GenericType(Decimal('10.0')).not_equal_to(10))
        self.assertFalse(GenericType(10).not_equal_to(Decimal('10.0')))
        self.assertTrue(GenericType(10).not_equal_to(10.00001))
        self.assertTrue(GenericType(10).not_equal_to(11))

    def test_numeric_greater_than(self):
        self.assertTrue(GenericType(10).greater_than(1))
        self.assertFalse(GenericType(10).greater_than(11))
        self.assertTrue(GenericType(10.1).greater_than(10))
        self.assertFalse(GenericType(10.000001).greater_than(10))
        self.assertTrue(GenericType(10.000002).greater_than(10))

    def test_numeric_greater_than_or_equal_to(self):
        self.assertTrue(GenericType(10).greater_than_or_equal_to(1))
        self.assertFalse(GenericType(10).greater_than_or_equal_to(11))
        self.assertTrue(GenericType(10.1).greater_than_or_equal_to(10))
        self.assertTrue(GenericType(10.000001).greater_than_or_equal_to(10))
        self.assertTrue(GenericType(10.000002).greater_than_or_equal_to(10))
        self.assertTrue(GenericType(10).greater_than_or_equal_to(10))

    def test_numeric_less_than(self):
        self.assertTrue(GenericType(1).less_than(10))
        self.assertFalse(GenericType(11).less_than(10))
        self.assertTrue(GenericType(10).less_than(10.1))
        self.assertFalse(GenericType(10).less_than(10.000001))
        self.assertTrue(GenericType(10).less_than(10.000002))

    def test_numeric_less_than_or_equal_to(self):
        self.assertTrue(GenericType(1).less_than_or_equal_to(10))
        self.assertFalse(GenericType(11).less_than_or_equal_to(10))
        self.assertTrue(GenericType(10).less_than_or_equal_to(10.1))
        self.assertTrue(GenericType(10).less_than_or_equal_to(10.000001))
        self.assertTrue(GenericType(10).less_than_or_equal_to(10.000002))
        self.assertTrue(GenericType(10).less_than_or_equal_to(10))
    
    def test_string_equal_to(self):
        self.assertTrue(GenericType("foo").equal_to("foo"))
        self.assertFalse(GenericType("foo").equal_to("Foo"))

    def test_string_not_equal_to(self):
        self.assertTrue(GenericType("foo").not_equal_to("POKEMON"))
        self.assertFalse(GenericType("foo").not_equal_to("foo"))

    def test_string_equal_to_case_insensitive(self):
        self.assertTrue(GenericType("foo").equal_to_case_insensitive("FOo"))
        self.assertTrue(GenericType("foo").equal_to_case_insensitive("foo"))
        self.assertFalse(GenericType("foo").equal_to_case_insensitive("blah"))

    def test_string_starts_with(self):
        self.assertTrue(GenericType("hello").starts_with("he"))
        self.assertFalse(GenericType("hello").starts_with("hey"))
        self.assertFalse(GenericType("hello").starts_with("He"))

    def test_string_ends_with(self):
        self.assertTrue(GenericType("hello").ends_with("lo"))
        self.assertFalse(GenericType("hello").ends_with("boom"))
        self.assertFalse(GenericType("hello").ends_with("Lo"))

    def test_string_contains(self):
        self.assertTrue(GenericType("hello").contains("ell"))
        self.assertTrue(GenericType("hello").contains("he"))
        self.assertTrue(GenericType("hello").contains("lo"))
        self.assertFalse(GenericType("hello").contains("asdf"))
        self.assertFalse(GenericType("hello").contains("ElL"))

    def test_string_matches_regex(self):
        self.assertTrue(GenericType("hello").matches_regex(r"^h"))
        self.assertFalse(GenericType("hello").matches_regex(r"^sh"))

    def test_non_empty(self):
        self.assertTrue(GenericType("hello").non_empty())
        self.assertFalse(GenericType("").non_empty())
        self.assertFalse(GenericType(None).non_empty())

    def test_is_contained_by(self):
        self.assertTrue(GenericType("hello").is_contained_by(["hello", "world"]))
        self.assertFalse(GenericType("earth").is_contained_by(["hello", "world"]))

    def test_is_not_contained_by(self):
        self.assertTrue(GenericType("rat").is_not_contained_by(["moose", "chicken"]))
        self.assertFalse(GenericType("chicken").is_not_contained_by(["moose", "chicken"]))

    def test_exists(self):
        df = pandas.DataFrame.from_dict({
            "var1": [1,2,4],
            "var2": [3,5,6]
        })
        self.assertTrue(GenericType(df).exists({"target": "var1"}))
        self.assertFalse(GenericType(df).exists({"target": "invalid"}))

    def test_not_exists(self):
        df = pandas.DataFrame.from_dict({
            "var1": [1,2,4],
            "var2": [3,5,6]
        })
        self.assertTrue(GenericType(df).not_exists({"target": "invalid"}))
        self.assertFalse(GenericType(df).not_exists({"target": "var1"}))
