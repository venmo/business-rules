import logging

from business_rules.actions import *
from business_rules.fields import *

logger = logging.getLogger(__name__)


class ExampleActions(BaseActions):
    def __init__(self, basket):
        self.basket = basket

    @rule_action(params={
        "stamps": FIELD_NUMERIC
    })
    def award_stamps(self, stamps):
        logger.info('Awarding {} stamps to basket id: {}'.format(
            stamps,
            self.basket.id,
        ))
        pass
