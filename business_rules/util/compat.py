from __future__ import absolute_import, unicode_literals

import sys
from collections import namedtuple

PY2 = sys.version_info[0] == 2

# Taken from https://github.com/HypothesisWorks/hypothesis/pull/625/files#diff-e84a85b835af44101e1986c47ba39630R264
if PY2:
    FullArgSpec = namedtuple('FullArgSpec', 'args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations')

    def getfullargspec(func):
        import inspect
        args, varargs, varkw, defaults = inspect.getargspec(func)
        return FullArgSpec(args, varargs, varkw, defaults, [], None, {})
else:
    from inspect import getfullargspec

    if sys.version_info[:2] == (3, 5):
        # silence deprecation warnings on Python 3.5
        # (un-deprecated in 3.6 to allow single-source 2/3 code like this)
        def silence_warnings(func):
            import warnings
            import functools

            @functools.wraps(func)
            def inner(*args, **kwargs):
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore', DeprecationWarning)
                    return func(*args, **kwargs)
            return inner

        getfullargspec = silence_warnings(getfullargspec)
