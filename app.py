# app.py — Flask Web Server for Chat UI
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

from flask import Flask, request, jsonify, render_template
from chatbot import load_faqs, get_best_answer

app = Flask(__name__)
faqs = load_faqs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data            = request.get_json()
    user_question   = data.get('question', '')
    answer          = get_best_answer(user_question, faqs)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)