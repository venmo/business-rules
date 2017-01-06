import datetime

from business_rules.variables import *
from business_rules import fields


class ExampleVariables(BaseVariables):
    def __init__(self, basket):
        self.basket = basket

    @select_rule_variable()
    def items(self):
        return self.basket.product_codes

    @string_rule_variable()
    def current_month(self):
        return datetime.datetime.now().strftime("%B")

    @boolean_rule_variable(params={
        'month': fields.FIELD_TEXT
    })
    def current_month_boolean(self, month):
        return datetime.datetime.now().strftime("%B") == month

    @boolean_rule_variable(params=[{
        'name': 'year',
        'field_type': fields.FIELD_NUMERIC
    }])
    def current_year_boolean(self, year):
        return datetime.datetime.now().year == year

    @boolean_rule_variable(inject_rule=True)
    def rule_variable(self, rule):
        print("Inside Variable function 'rule_variable', rule={}".format(rule))
        return True
