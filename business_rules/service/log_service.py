import logging


class LogService(object):
    def __init__(self):
        super(LogService, self).__init__()
        self.logger = logging.getLogger(__name__)

    def _fetch_public_properties(self, obj):
        return [name for name in dir(obj) if not name.startswith('_')]

    def log_rule(self, rule, conditions_met, action_triggered, defined_variables):
        variables_public_props = self._fetch_public_properties(defined_variables)

        self.logger.info('rule={} - conditions = {} - actions = {} - defined_variables = {}'.format(rule,
                                                                                                    conditions_met,
                                                                                                    action_triggered,
                                                                                                    variables_public_props))
