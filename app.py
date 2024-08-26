from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import json
import os

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

STACK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stack.json')

def load_stack():
    if os.path.exists(STACK_FILE):
        try:
            with open(STACK_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []
    return []

def save_stack():
    with open(STACK_FILE, 'w') as f:
        json.dump(stack, f)

stack = load_stack()

@app.route('/stack', methods=['POST'])
def add_to_stack():
    element = request.json.get('element')
    if element is not None:
        try:
            stack.append(float(element))
            save_stack()
            return {"stack": stack}, 201
        except ValueError:
            return {"error": "Invalid element provided. Must be a number."}, 400
    return {"error": "No element provided"}, 400

@app.route('/stack', methods=['GET'])
def get_stack():
    return {"stack": stack}

@app.route('/stack', methods=['DELETE'])
def clear_stack():
    stack.clear()
    save_stack()
    return {"message": "Stack cleared"}, 200

@app.route('/stack/add', methods=['POST'])
def add():
    if len(stack) < 2:
        return {"error": "Not enough elements in stack"}, 400
    b = stack.pop()
    a = stack.pop()
    result = a + b
    stack.append(result)
    save_stack()
    return {"result": result, "stack": stack}

@app.route('/stack/subtract', methods=['POST'])
def subtract():
    if len(stack) < 2:
        return {"error": "Not enough elements in stack"}, 400
    b = stack.pop()
    a = stack.pop()
    result = a - b
    stack.append(result)
    save_stack()
    return {"result": result, "stack": stack}

@app.route('/stack/multiply', methods=['POST'])
def multiply():
    if len(stack) < 2:
        return {"error": "Not enough elements in stack"}, 400
    b = stack.pop()
    a = stack.pop()
    result = a * b
    stack.append(result)
    save_stack()
    return {"result": result, "stack": stack}

@app.route('/stack/divide', methods=['POST'])
def divide():
    if len(stack) < 2:
        return {"error": "Not enough elements in stack"}, 400
    b = stack.pop()
    a = stack.pop()
    if b == 0:
        return {"error": "Division by zero"}, 400
    result = a / b
    stack.append(result)
    save_stack()
    return {"result": result, "stack": stack}

if __name__ == '__main__':
    app.run(debug=True)
