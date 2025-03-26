import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_similar_question(input_question):
    questions_json = {}

    with open("data/questions.json", "r") as f:
        questions_json = json.load(f)

    question_keys = list(questions_json.keys())
    question_descriptions = [questions_json[key]["description"] for key in question_keys]
    question_files = [questions_json[key]["files"] for key in question_keys]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(question_descriptions)

    input_question_vector = vectorizer.transform([input_question])
    cosine_similarities = cosine_similarity(input_question_vector, tfidf_matrix).flatten()
    most_similar_question_index = np.argmax(cosine_similarities)

    most_similar_question = question_keys[most_similar_question_index]
    most_similar_question_description = question_descriptions[most_similar_question_index]

    # **Manual Rule to Differentiate "apache_log_requests" and "apache_log_downloads"**
    if most_similar_question in ["apache_log_requests", "apache_log_downloads"]:
        if "top data consumer" in input_question or "bytes downloaded" in input_question or "bandwidth" in input_question:
            most_similar_question = "apache_log_downloads"
        if "successful GET requests" in input_question or "peak hours" in input_question:
            most_similar_question = "apache_log_requests"
        
    return (most_similar_question, most_similar_question_description, question_files[most_similar_question_index])


# Example usage
if __name__ == "__main__":
    question, description, files = find_similar_question("i want to create a HTTP request with uv?")
    print(question, description, files)