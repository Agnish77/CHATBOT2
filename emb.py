import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import faiss
import json

# Step 1: Scrape data from the website
def scrape_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Customize this part based on the website structure
        courses = soup.find_all('div', class_='course-card-title')  # Adjust class name if needed
        if not courses:
            raise ValueError("No courses found on the website.")
        
        data = [course.text.strip() for course in courses]
        return data
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return []
    except ValueError as e:
        print(f"Error processing the content: {e}")
        return []

# Step 2: Generate embeddings using Sentence Transformers
def create_embeddings(data):
    if not data:
        raise ValueError("No data available to generate embeddings.")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(data, show_progress_bar=True)
    return embeddings

# Step 3: Store embeddings in FAISS
def store_embeddings(data, embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)  # L2 distance
    index.add(embeddings)
    
    # Save the index and metadata for reuse
    faiss.write_index(index, "courses_index.faiss")
    with open("courses_metadata.json", "w") as f:
        json.dump(data, f)

# Step 4: Load FAISS index and metadata
def load_index():
    if not os.path.exists("courses_index.faiss"):
        return None, None
    
    index = faiss.read_index("courses_index.faiss")
    with open("courses_metadata.json", "r") as f:
        metadata = json.load(f)
    
    return index, metadata

# Step 5: Query FAISS for the closest match
def query_index(query, index, metadata):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k=1)  # Find the closest match
    
    closest_index = indices[0][0]
    return metadata[closest_index], distances[0][0]

# Step 6: Create Flask RESTful API
app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("query", "")
    if not user_query:
        return jsonify({"error": "Query is required"}), 400
    
    index, metadata = load_index()
    
    if index is None or metadata is None:
        return jsonify({"error": "Embeddings not found. Please regenerate embeddings."}), 500
    
    response, distance = query_index(user_query, index, metadata)
    
    return jsonify({"response": response, "distance": distance})

if __name__ == "__main__":
    # Ensure the embeddings are created only once
    if not os.path.exists("courses_index.faiss"):
        url = "https://brainlox.com/courses/category/technical"
        data = scrape_data(url)
        
        if data:
            embeddings = create_embeddings(data)
            store_embeddings(data, embeddings)
        else:
            print("Failed to scrape data. Exiting.")
            exit(1)
    
    app.run(debug=True)

