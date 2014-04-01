business-rules
==============

As your codebase and business grow, eventually everyone needs a way to run business logic.
TODO: Finish this up.

## Usage

### Define Your Set of variables and actions
TODO: write later

```python
class ProductVariables(BaseVariables):

    def __init__(self, product):
        self.product = product

    @numeric_rule_variable
    def current_inventory(self):
        return self.product.current_inventory

    @numeric_rule_variable(description='Days until expiration')
    def expiration_days(self)
        last_order = self.product.orders[-1]
        return (last_order.expiration_date - datetime.date.today()).days

    @string_rule_variable(cache_result=False)
    def current_month(self):
        return datetime.datetime.now().strftime("%B")

    @select_rule_variable
    def goes_well_with(self):
        return products.related_products
```

```python
class ProductActions(BaseActions):

    def __init__(self, product):
        self.product = product

    @rule_action(field_type=TEXT_FIELD)
    def put_on_sale(self, sale_percentage):
        self.product.price = (1.0 - sale_percentage) * self.product.price
        self.product.save()

    @rule_action(field_type=TEXT_FIELD)
    def order_more(self, number_to_order):
        ProductOrder.objects.create(product_id=self.product.id,
                                    quantity=number_to_order)
```

### Build a Set of Rules
A good front-end library that we modeled this after can be found [here](https://github.com/chrisjpowers/business-rules).

This models a set of rules in the following format:

```python
rules = [
# expiration_days < 5 AND current_inventory > 20
{ "conditions": { "all": [
      { "name": "expiration_days",
        "operator": "less_than",
        "value": "5",
      },
      { "name": "current_inventory",
        "operator": "greater_than",
        "value": "20",
      },
  ]},
  "actions": [
      { "name": "put_on_sale",
        "fields": [{"name": "sale_percentage", "value": 0.25}],
      },
  ],
},

# current_inventory < 5 OR (current_month = "December" AND current_inventory < 20)
{ "conditions": { "any": [
      { "name": "current_inventory",
        "operator": "less_than",
        "value": 5,
      },
    ]},
      { "all": [
        {  "name": "current_month",
          "operator": "equals",
          "value": "December",
        },
        { "name": "goes_well_with",
          "operator": "contains_one_of",
          "value": ["eggnog", "sugar cookies"],
        }
      ]},
  },
  "actions": [
    { "name": "order_more",
      "fields":[{"name":"number_to_order", "value": 40}]}
  ],
}]
```

### Run your rules

```python
import BusinessRules
for product in Products.objects.all():
    product_variables = ProductVariables(product)
    product_actions = ProductActions(product)
    for rule in rules:
        BusinessRules.run(rule, product_variables, product_actions)

from business_rules import run_all
for product in Products.objects.all():
    run_all(rules=rules,
            variables=ProductVariables(product),
            actions=ProductActions(product),
            stop_on_first_trigger=True
           )
```

## API

Rule variable definitions:

@numeric_rule_variable - the decorated function returns a numeric type - an integer, fixed-point decimal or float
  Operators:

    * equal_to
    * greater_than
    * less_than
    * greater_than_or_equal_to
    * less_than_or_equal_to

NB: For numerics, `equal_to` will cast to a float and then do an almost equal comparison (with epsilon = 0.000001).  So basically everything is a float.

@string_rule_variable
  Operators:

    * equal_to
    * starts_with
    * ends_with
    * contains
    * matches_regex
    * non_empty

@select_rule_variable - the decorated function returns a 
  Operators:

    * contains
    * does_not_contain

@select_multiple_rule_variable - a set of items
  Operators:

    * contains_one_of
    * contains_all
    * does_not_contain
    * containts_at_least_one_of?

@boolean_rule_variable - True/False
  Operators:

    * is


## Contributing

Open up a pull request, making sure to add tests for any new functionality. To set up the dev environment (assuming you're using [virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvwrapper)):

```bash
$ mkvirtualenv business-rules
$ pip install -r dev-requirements.txt
$ nosetests
```
