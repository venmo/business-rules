from business_rules import variables


class TestVariables(variables.BaseVariables):

    @variables.boolean_rule_variable()
    def bool_variable(self):
        return True

    @variables.string_rule_variable()
    def str_variable(self):
        return 'test'

    @variables.select_multiple_rule_variable()
    def select_multiple_variable(self):
        return [1, 2, 3]

    @variables.numeric_rule_variable()
    def numeric_variable(self):
        return 1

    @variables.datetime_rule_variable()
    def datetime_variable(self):
        return datetime.now()

    @variables.time_rule_variable()
    def time_variable(self):
        return time.time()

    @variables.select_rule_variable()
    def select_variable(self):
        return [1, 2, 3]
