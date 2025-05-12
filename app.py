from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import os

print(">>> Flask app started execution")

app = Flask(__name__)
CORS(app)

# Load dataset and model at startup, but not embeddings
print(">>> Loading dataset...")
movies_df = pd.read_csv('movies.csv')
movies_df['overview'] = movies_df['overview'].fillna('')
movies_df['genres'] = movies_df['genres'].fillna('')
movies_df['vote_average'] = pd.to_numeric(movies_df['vote_average'], errors='coerce').fillna(0)
movies_df['vote_count'] = pd.to_numeric(movies_df['vote_count'], errors='coerce').fillna(0)

print(">>> Loading transformer model...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

@app.route("/")
def index():
    return jsonify({"message": "EasyFilm backend is running!"})

@app.route("/recommend", methods=["POST"])
def recommend_movies():
    data = request.json
    user_input = data.get("input", "")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Compute embedding for user input
    input_embedding = model.encode(user_input)

    # Build embeddings on the fly
    def build_text_embedding(row):
        text = f"{row['overview']} Genres: {row['genres']}"
        return model.encode(text)

    print(">>> Generating embeddings...")
    movies_df["embedding"] = movies_df.apply(build_text_embedding, axis=1).tolist()

    similarities = cosine_similarity([input_embedding], list(movies_df["embedding"]))[0]
    top_indices = np.argsort(similarities)[::-1][:10]

    recommendations = movies_df.iloc[top_indices][["title", "overview", "genres"]].to_dict(orient="records")
    return jsonify(recommendations)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)










