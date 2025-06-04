import json
from typing import Dict, List

class RecordService:
    def __init__(self):
        self.records = [
            {"id": 1, "name": "John", "age": 25},
            {"id": 2, "name": "Jane", "age": 30},
            {"id": 3, "name": "Bob", "age": 35}
        ]

    def query(self, filter_criteria: str) -> List[Dict]:
        try:
            filter_criteria = json.loads(filter_criteria)
        except json.JSONDecodeError:
            return []
        
        results = self.records
        for field, value in filter_criteria.items():
            if isinstance(value, dict):
                sub_results = [result for result in results if all(result.get(key) == val for key, val in value.items())]
                results = sub_results
            else:
                results = [result for result in results if result.get(field) == value]

        return results

if __name__ == "__main__":
    service = RecordService()
    filter_criteria = '{"age": {"gt": 30}}'
    print(service.query(filter_criteria))