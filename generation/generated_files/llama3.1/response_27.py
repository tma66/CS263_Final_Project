import pandas as pd
import json
from typing import List, Dict

class TransformationPipeline:
    def __init__(self):
        self.rules = []

    def load_rules(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as f:
                rules = json.load(f)
                for rule in rules['rules']:
                    self.add_rule(rule)
        except Exception as e:
            print(f"Error loading rules: {str(e)}")

    def add_rule(self, rule: Dict) -> None:
        if isinstance(rule, dict):
            self.rules.append(rule)

    def transform_data(self, data: pd.DataFrame) -> pd.DataFrame:
        transformed_data = data.copy()
        for rule in self.rules:
            column_name = rule['column']
            operation = rule['operation']
            value = rule.get('value')
            if operation == 'rename':
                transformed_data.rename(columns={column_name: rule['new_name']}, inplace=True)
            elif operation == 'drop':
                transformed_data.drop(column_name, axis=1, inplace=True)
            elif operation == 'replace':
                transformed_data[column_name] = transformed_data[column_name].str.replace(value, rule['replacement'])
            elif operation == 'cast':
                if value:
                    transformed_data[column_name] = pd.to_numeric(transformed_data[column_name], downcast=value)
                else:
                    transformed_data[column_name] = pd.to_numeric(transformed_data[column_name])
        return transformed_data

class RuleManager:
    def __init__(self):
        self.pipeline = TransformationPipeline()

    def load_rules(self, file_path: str) -> None:
        self.pipeline.load_rules(file_path)

    def add_rule(self, rule: Dict) -> None:
        self.pipeline.add_rule(rule)

    def transform_data(self, data: pd.DataFrame) -> pd.DataFrame:
        return self.pipeline.transform_data(data)

# Example usage
rule_manager = RuleManager()
data = pd.DataFrame({
    'Name': ['John', 'Anna'],
    'Age': [28, 24]
})

rules = {
    "rules": [
        {"column": "Age", "operation": "cast", "value": None},
        {"column": "Name", "operation": "replace", "value": "John", "replacement": "*"}
    ]
}

rule_manager.load_rules(json.dumps(rules))
transformed_data = rule_manager.transform_data(data)
print(transformed_data)