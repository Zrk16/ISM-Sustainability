from flask import Flask, request, jsonify
import requests

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def home():
    return app.send_static_file('Home page.html')

@app.route('/<path:filename>')
def serve_file(filename):
    return app.send_static_file(filename)

@app.route('/api/chat', methods=['POST'])
def chat():
    msg = request.json['message']

    r = requests.post(
        "https://integrate.api.nvidia.com/v1/chat/completions",
        headers={"Authorization": "Bearer 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", "Content-Type": "application/json"},
        json={
            "model": "meta/llama-3.1-8b-instruct",
            "messages": [
                {"role": "system", "content": "You are ISM's sustainability chatbot. Keep answers short."},
                {"role": "user", "content": msg}
            ]
        }
    )

    answer = r.json()['choices'][0]['message']['content']
    return jsonify({'reply': answer})

app.run(port=5000, debug=True)
