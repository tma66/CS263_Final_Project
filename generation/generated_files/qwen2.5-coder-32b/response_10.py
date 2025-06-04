from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data store
data_store = [
    {"id": 1, "name": "Alice", "age": 30},
    {"id": 2, "name": "Bob", "age": 25},
    {"id": 3, "name": "Charlie", "age": 35}
]

@app.route('/query', methods=['POST'])
def query_records():
    filter_criteria = request.json
    filtered_results = [record for record in data_store if all(record.get(key) == value for key, value in filter_criteria.items())]
    return jsonify(filtered_results)

if __name__ == '__main__':
    app.run(debug=True)