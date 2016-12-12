class BaseValidator(object):
    def validator_fallback(self, condition_name):
        def fallback(operator, value):
            return True

        return fallback
