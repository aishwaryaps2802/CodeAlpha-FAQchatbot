# chatbot.py — FAQ Matching Logic
# Uses TF-IDF + Cosine Similarity to find best answer

import json
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data (run once)
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

# ── Load FAQs ──────────────────────────────────────
def load_faqs(filepath='faqs.json'):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data['faqs']

# ── Clean & Preprocess Text ────────────────────────
def preprocess(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize
    tokens = nltk.word_tokenize(text)
    # Remove stopwords (a, the, is, etc.)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# ── Find Best Matching FAQ ─────────────────────────
def get_best_answer(user_question, faqs, threshold=0.2):
    # Preprocess user question
    cleaned_question = preprocess(user_question)

    # Get all FAQ questions
    faq_questions = [preprocess(faq['question']) for faq in faqs]

    # Add user question at the end for comparison
    all_texts = faq_questions + [cleaned_question]

    # Convert to TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Calculate cosine similarity of user Q with all FAQ Qs
    user_vector   = tfidf_matrix[-1]
    faq_vectors   = tfidf_matrix[:-1]
    similarities  = cosine_similarity(user_vector, faq_vectors).flatten()

    # Find the best match
    best_index = similarities.argmax()
    best_score = similarities[best_index]

    print(f"Best match score: {best_score:.2f}")  # for debugging

    if best_score >= threshold:
        return faqs[best_index]['answer']
    else:
        return "Sorry, I could not find an answer to your question. Please contact support."

# ── Test in Terminal ───────────────────────────────
if __name__ == '__main__':
    faqs = load_faqs()
    print("FAQ Chatbot ready! Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        answer = get_best_answer(user_input, faqs)
        print(f"Bot: {answer}\n")