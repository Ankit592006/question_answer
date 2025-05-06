from flask import Flask, request, jsonify
from flask_cors import CORS
from model import get_answer

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '').strip()

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    answer = get_answer(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    # Run the Flask app on localhost port 5000
    app.run(host='127.0.0.1', port=5000, debug=True)
