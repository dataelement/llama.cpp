from flask import Flask, request
import requests
import threading
import json

class ThreadSafeRoundRobin:
    def __init__(self, items):
        self.items = items
        self.index = 0
        self.lock = threading.Lock()

    def next(self):
        with self.lock:
            if not self.items:
                return None
            item = self.items[self.index % len(self.items)]
            self.index += 1
        return item


config = json.load(open('/opt/proxy.json'))
round_robin_map = {}
for key, server in config.items():
    round_robin_map[key] = ThreadSafeRoundRobin(server)


GLOBAL_TOKEN = "Bearer ELEM8x3V7C2n0Q5y"

def impl_call(data):
    api_key = "your_openai_api_key"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    model = data['model']
    internal_url = round_robin_map.get(model).next()
    response = requests.post(internal_url, json=data, headers=headers).json()
    return response


app = Flask(__name__)


@app.route('/v1/chat/completions', methods=['POST'])
def completions():
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return {'message': 'Authorization header is missing'}, 400

    if not auth_header.startswith('Bearer '):
        return {'message': 'Invalid Authorization header'}, 400
    
    if auth_header != GLOBAL_TOKEN:
        return {'message': 'Invalid token'}, 403

    data = request.json
    model = data.get('model')
    if model in ['qwen1.5-110b-chat', 'command-r-plus-104b']:
        return impl_call(data)
    else:
        return {'message': 'model not found'}, 404


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=12600)