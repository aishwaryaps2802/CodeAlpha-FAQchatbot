import json
import nltk
import string
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

from nltk.corpus import stopwords

def load_faqs():
    base_dir  = os.path.dirname(os.path.abspath(__file__))
    filepath  = os.path.join(base_dir, 'faqs.json')
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data['faqs']

def preprocess(text):
    text   = text.lower()
    text   = text.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if w not in stop_words]
    return ' '.join(tokens)

def get_best_answer(user_question, faqs, threshold=0.2):
    cleaned       = preprocess(user_question)
    faq_questions = [preprocess(f['question']) for f in faqs]
    all_texts     = faq_questions + [cleaned]

    vectorizer   = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    user_vector  = tfidf_matrix[-1]
    faq_vectors  = tfidf_matrix[:-1]
    similarities = cosine_similarity(user_vector, faq_vectors).flatten()

    best_index = similarities.argmax()
    best_score = similarities[best_index]

    if best_score >= threshold:
        return faqs[best_index]['answer']
    else:
        return "Sorry, I could not find an answer. Please contact support."
