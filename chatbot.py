import json
import nltk
import string
import os
import math
from collections import Counter

nltk.download('punkt',     quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def load_faqs():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, 'faqs.json')
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"Loaded {len(data['faqs'])} FAQs successfully")
        return data['faqs']
    except Exception as e:
        print(f"Error loading FAQs: {str(e)}")
        return []

def preprocess(text):
    try:
        text       = text.lower()
        text       = text.translate(
                         str.maketrans('', '', string.punctuation)
                     )
        tokens     = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        tokens     = [w for w in tokens if w not in stop_words]
        return tokens
    except Exception as e:
        print(f"Preprocess error: {str(e)}")
        return text.lower().split()

def cosine_similarity(vec1, vec2):
    try:
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator    = sum(vec1[x] * vec2[x] for x in intersection)
        sum1         = sum(v**2 for v in vec1.values())
        sum2         = sum(v**2 for v in vec2.values())
        denominator  = math.sqrt(sum1) * math.sqrt(sum2)
        if denominator == 0:
            return 0
        return numerator / denominator
    except:
        return 0

def text_to_vector(tokens):
    return Counter(tokens)

def get_best_answer(user_question, faqs, threshold=0.1):
    try:
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

        print(f"Best score: {best_score}")
        return best_answer
    except Exception as e:
        print(f"Answer error: {str(e)}")
        return "Sorry, something went wrong. Please try again."
