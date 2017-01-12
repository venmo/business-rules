class BaseActionManager(object):
    def __init__(self, audit_service, rule, conditions_met, action_triggered, defined_variables):
        super(BaseActionManager, self).__init__()
        self._result = None
        self.audit_service = audit_service
        self.rule = rule
        self.conditions_met = conditions_met
        self.action_triggered = action_triggered
        self.defined_variables = defined_variables

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, new_value):
        self._result = new_value
