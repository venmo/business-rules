import datetime
import logging

from business_rules import run_all
from tests.example.actions import ExampleActions
from tests.example.basket import Item, Basket
from tests.example.validators import ExampleValidators
from tests.example.variables import ExampleVariables

logging.basicConfig(level=logging.DEBUG)

rules = [
    {
        "conditions": {
            "all": [
                {
                    "name": "items",
                    "operator": "contains",
                    "value": 1,
                },
                {
                    "name": "current_month",
                    "operator": "equal_to",
                    "value": "January",
                },
                {
                    "name": "item_count",
                    "operator": "greater_than",
                    "value": 1,
                },
                {
                    "name": "rule_variable",
                    "operator": "is_true",
                    "value": "True",
                },
                {
                    "name": "today",
                    "operator": "after_than_or_equal_to",
                    "value": "2017-01-16",
                }
            ]
        },
        "actions": [
            {
                "name": "log",
                "params": {
                    "message": "All criteria met!",
                }
            }
        ]
    }
]

hot_drink = Item(code=1, name='Hot Drink', line_number=1, quantity=1)
pastry = Item(code=2, name='Pastry', line_number=2, quantity=1)
basket = Basket(id=0, items=[hot_drink, pastry])
run_all(
    rule_list=rules,
    defined_variables=ExampleVariables(basket),
    defined_actions=ExampleActions(basket),
    defined_validators=ExampleValidators(basket),
)
