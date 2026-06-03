import json
import nltk
import string
import os
import math
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

from nltk.corpus import stopwords

def load_faqs():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, 'faqs.json')
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data['faqs']

def preprocess(text):
    text       = text.lower()
    text       = text.translate(str.maketrans('', '', string.punctuation))
    tokens     = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens     = [w for w in tokens if w not in stop_words]
    return tokens

def cosine_similarity(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator    = sum(vec1[x] * vec2[x] for x in intersection)
    sum1         = sum(v**2 for v in vec1.values())
    sum2         = sum(v**2 for v in vec2.values())
    denominator  = math.sqrt(sum1) * math.sqrt(sum2)
    if denominator == 0:
        return 0
    return numerator / denominator

def text_to_vector(tokens):
    return Counter(tokens)

def get_best_answer(user_question, faqs, threshold=0.1):
    user_tokens = preprocess(user_question)
    user_vector = text_to_vector(user_tokens)
    best_score  = 0
    best_answer = "Sorry, I could not find an answer. Please contact support."

    for faq in faqs:
        faq_tokens = preprocess(faq['question'])
        faq_vector = text_to_vector(faq_tokens)
        score      = cosine_similarity(user_vector, faq_vector)
        if score > best_score:
            best_score  = score
            best_answer = faq['answer']

    return best_answer
