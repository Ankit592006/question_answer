from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from model import extract_text_from_file

app = Flask(__name__)
CORS(app)

# Create uploads folder if not exists
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text and store globally in model.py
        extract_text_from_file(file_path)

        print(f"✅ File '{filename}' uploaded and processed successfully.")
        return jsonify({'message': 'File uploaded and processed'})
    except Exception as e:
        print(f"❌ Error uploading file: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '').strip()

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Import here to avoid circular imports
    from model import document_content

    # Optional: Limit context size for better performance
    MAX_CONTEXT_LENGTH = 1000
    short_context = document_content[:MAX_CONTEXT_LENGTH]

    # Build prompt
    prompt = f"""
You are an educational assistant. Use the following context to answer the question accurately.

Context:
{short_context}

Question:
{question}

Answer:
"""

    print("🧠 Prompt sent to LLM:")
    print(prompt)

    try:
        # Get answer from LLM
        from model import llm
        answer = llm(prompt).strip()
        print("🤖 Answer received:", answer)

        return jsonify({'answer': answer})
    except Exception as e:
        print("❌ LLM Error:", str(e))
        return jsonify({'error': 'Failed to generate answer'}), 500

if __name__ == '__main__':
    print("🚀 Starting EduBot backend on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)
