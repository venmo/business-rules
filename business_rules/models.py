from __future__ import absolute_import
from collections import namedtuple

ConditionResult = namedtuple('ConditionResult', ['result', 'name', 'operator', 'value', 'parameters'])
