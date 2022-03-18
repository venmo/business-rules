from unittest import TestCase

# Allow us to use Python 3's `assertRaisesRegex` to avoid "DeprecationWarning: Please use assertRaisesRegex instead."
if not hasattr(TestCase, 'assertRaisesRegex'):
    TestCase.assertRaisesRegex = TestCase.assertRaisesRegexp
