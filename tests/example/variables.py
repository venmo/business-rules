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
