import datetime

from business_rules.variables import *


class ExampleVariables(BaseVariables):
    def __init__(self, basket):
        self.basket = basket

    @select_rule_variable()
    def items(self):
        return self.basket.product_codes

    @string_rule_variable()
    def current_month(self):
        return datetime.datetime.now().strftime("%B")

    @numeric_rule_variable()
    def item_count(self):
        return len(self.basket.product_codes)

    @boolean_rule_variable()
    def rule_variable(self, **kwargs):
        rule = kwargs.get('rule')
        return True

    @datetime_rule_variable()
    def today(self):
        return datetime.date.today()
