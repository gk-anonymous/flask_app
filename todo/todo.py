from flask import Flask, jsonify, request ,render_template
app = Flask(__name__)

# Sample data
items = [
    {"id": 1, "name": "item1", "description": "This is item1"},
    {"id": 2, "name": "item2", "description": "This is item2"}
]


@app.route('/frontend')
def frontend():
    return render_template('index.html')

# GET: Retrieve all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# GET: Retrieve a specific item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)

# POST: Create a new item
@app.route('/items', methods=['POST'])
def create_item():
    if not request.json or 'name' not in request.json or 'description' not in request.json:
        return jsonify({"error": "Invalid input"}), 400

    new_item = {
        "id": items[-1]["id"] + 1 if items else 1,
        "name": request.json['name'],
        "description": request.json['description']
    }
    items.append(new_item)
    return jsonify(new_item), 201

# PUT: Update an existing item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.json
    item['name'] = data.get('name', item['name'])
    item['description'] = data.get('description', item['description'])
    return jsonify(item)

# DELETE: Remove an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    items = [item for item in items if item['id'] != item_id]
    return jsonify({"message": "Item deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
