import logging

from business_rules.validators import BaseValidator

logger = logging.getLogger(__name__)


class ExampleValidators(BaseValidator):
    def __init__(self, basket):
        self.basket = basket

    def items(self, operator, value):
        logger.debug('operator={}, value={}'.format(operator, value))
        # TODO validation logic
        return True

    def current_month(self, operator, value):
        logger.debug('operator={}, value={}'.format(operator, value))
        # TODO validation logic
        return True

    def current_month_boolean(self, operator, value):
        logger.debug('operator={}, value={}'.format(operator, value))
        return True

    def current_year_boolean(self, operator, value):
        logger.debug('operator={}, value={}'.format(operator, value))
        return True
