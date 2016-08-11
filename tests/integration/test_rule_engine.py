from business_rules import run_all
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC, FIELD_CUSTOM
from business_rules.operators import export_type, BaseType, type_operator, CustomType
from business_rules.variables import BaseVariables, numeric_rule_variable, string_rule_variable, select_rule_variable, \
    custom_rule_variable
import datetime
from tests import TestCase


class Products(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    @staticmethod
    def top_holiday_items():
        return [10, 11, 12]

    def save(self):
        self.action_triggered = True;

class Orders(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)


class ProductVariables(BaseVariables):

    def __init__(self, product):
        self.product = product

    @numeric_rule_variable
    def current_inventory(self):
        return self.product.current_inventory

    @numeric_rule_variable(label='Days until expiration')
    def expiration_days(self):
        last_order = self.product.orders
        return (last_order['expiration_date'] - datetime.date.today()).days

    @string_rule_variable()
    def current_month(self):
        return datetime.datetime.now().strftime("%B")

    @select_rule_variable(options=Products.top_holiday_items())
    def goes_well_with(self):
        return self.product.related_product

    @custom_rule_variable()
    def tags(self):
        return self.product.tags


class ProductActions(BaseActions):

    def __init__(self, product):
        self.product = product

    @rule_action(params={"sale_percentage": FIELD_NUMERIC})
    def put_on_sale(self, sale_percentage):
        self.product.price = (1.0 - sale_percentage) * self.product.price
        self.product.save()

@export_type
class CustomOperator(CustomType):
    name = "user_defined"

    @type_operator(FIELD_CUSTOM)
    def equals(self, other_value):
        if self.value == other_value:
            return True
        else:
            return False


# create product args
args = {'current_inventory': 21,
        'related_product': 3,
        'orders': {'expiration_date': datetime.date.today()},
        'price': 1.24,
        'tags' :
            {
            'sector': ['Electronics', 'Sport'],
            'target_audience': 'Health Conscious',
            'dict': {'some': 'other'}
            },
        'action_triggered': False}

# create a product
product = Products(**args)


rules = [
# expiration_days < 5 AND current_inventory > 20
{ "conditions": { "all": [
      { "name": "expiration_days",
        "operator": "less_than",
        "value": 5,
      },
      { "name": "current_inventory",
        "operator": "greater_than",
        "value": 20,
      }
  ]},
  "actions": [
      { "name": "put_on_sale",
        "params": {"sale_percentage": 0.25},
      },
  ],
}]
rules_custom_operator = [
# expiration_days < 5 AND current_inventory > 20
{ "conditions": { "all": [
      { "name": "expiration_days",
        "operator": "less_than",
        "value": 5,
      },
      { "name": "current_inventory",
        "operator": "greater_than",
        "value": 20,
      },
      { "name": "tags",
        "operator": "equals",
        "value":
            {
            'sector': ['Electronics', 'Sport'],
            'target_audience': 'Health Conscious',
            'dict': {'some': 'other'}
            }
      }
  ]},
  "actions": [
      { "name": "put_on_sale",
        "params": {"sale_percentage": 0.25},
      },
  ],
}]

class IntegrationTests(TestCase):
    """Actual integration tests """

    def test_rule_engine(self):

        triggered = run_all(rule_list=rules,
                defined_variables=ProductVariables(product),
                defined_actions=ProductActions(product),
                stop_on_first_trigger=True
                )
        assert triggered == True
        assert product.action_triggered == True

    def test_rule_engine_custom_operator(self):

        triggered = run_all(rule_list=rules_custom_operator,
                defined_variables=ProductVariables(product),
                defined_actions=ProductActions(product),
                defined_operators=CustomOperator(CustomType),
                stop_on_first_trigger=True
                )
        assert triggered == True
        assert product.action_triggered == True