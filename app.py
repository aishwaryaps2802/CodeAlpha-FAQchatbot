import os
import nltk

nltk.download('punkt',     quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

from flask import Flask, request, jsonify
from chatbot import load_faqs, get_best_answer

app  = Flask(__name__)
faqs = load_faqs()

@app.route('/')
def index():
    return open(os.path.join(os.path.dirname(__file__), 'index.html')).read()

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data          = request.get_json()
        user_question = data.get('question', '')
        if not user_question:
            return jsonify({'answer': 'Please type a question.'})
        answer = get_best_answer(user_question, faqs)
        return jsonify({'answer': answer})
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({'answer': 'Sorry, something went wrong.'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
