import pandas as pd
import json

class DataTransformationPipeline:
    def __init__(self):
        self.data = None

    def load_data(self, file_path):
        if file_path.endswith('.csv'):
            self.data = pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            self.data = pd.read_json(file_path)
        else:
            raise ValueError("Unsupported file format")

    def apply_transformation_rules(self, rules):
        if isinstance(rules, str):
            rules = json.loads(rules)

        for rule in rules:
            action = rule['action']
            column = rule.get('column')
            value = rule.get('value')

            if action == 'drop':
                self.data.drop(columns=[column], inplace=True)
            elif action == 'fillna':
                self.data[column].fillna(value, inplace=True)
            elif action == 'replace':
                self.data[column] = self.data[column].replace(rule['old_value'], value)
            elif action == 'apply_function':
                func_name = rule['function']
                if func_name == 'str.lower':
                    self.data[column] = self.data[column].astype(str).str.lower()
                elif func_name == 'round':
                    self.data[column] = self.data[column].round(value)

    def get_transformed_data(self):
        return self.data

# Example usage:
pipeline = DataTransformationPipeline()
pipeline.load_data('data.csv')
transformation_rules = '[{"action": "drop", "column": "unnecessary_column"}, {"action": "fillna", "column": "missing_values_column", "value": 0}]'
pipeline.apply_transformation_rules(transformation_rules)
print(pipeline.get_transformed_data())