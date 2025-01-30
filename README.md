# CHATBOT-FLASK API



This repository contains a Flask-based RESTful API that recommends courses based on user queries. It uses web scraping, natural language embeddings, and the FAISS library to provide accurate and efficient recommendations.

## Features

- **Web Scraping:** Scrapes course data from a specified website.
- **Embedding Generation:** Uses the Sentence Transformers library to generate sentence embeddings.
- **Efficient Search:** Leverages FAISS for fast similarity searches.
- **RESTful API:** Provides a simple `/chat` endpoint to query courses.

---

## Installation

### Prerequisites

- Python 3.7 or higher
- Virtual environment (optional but recommended)

### Clone the Repository


git clone https://github.com/your-username/course-recommendation-api.git
cd course-recommendation-api


### Install Dependencies

Create a virtual environment and install the required libraries:

python -m venv env

source env/bin/activate  # For Windows: env\Scripts\activate

pip install -r requirements.txt

Note: Add the requirements.txt file with dependencies:

Flask

requests

beautifulsoup4

sentence-transformers

faiss-cpu

## Usage

Run the API

To start the Flask server:

Ensure Scraping Target is Correct:

Verify the target URL in the script (https://brainlox.com/courses/category/technical) is correct and the class name for the course titles matches the website structure.

Run the Script:

python app.py

API Endpoint:

Access the /chat endpoint via POST request. Default port is 5000.

## Endpoints

/chat [POST]

Accepts a user query and returns the closest matching course.

Request

json

{
  "query": "machine learning courses"
}
Response
json

{
  "response": "Introduction to Machine Learning",
  "distance": 0.42
}

## Workflow

Web Scraping:

Scrapes course titles from the specified website.

Embedding Generation:

Converts scraped data into sentence embeddings using SentenceTransformer.

Embedding Storage:

Stores the embeddings and metadata using FAISS for future use.

Query Matching:

Matches user queries to the closest course title using FAISS.

API Interaction:

Exposes an API for external clients to query recommendations.

## File Structure

app.py: Main script containing all functionalities.

courses_index.faiss: Stored FAISS index file for embeddings.

courses_metadata.json: Metadata (course titles) file.

requirements.txt: Python dependencies.

## Customization

Target Website

Update the url in the script to scrape data from a different website. Ensure the class name for the course titles is updated accordingly.



url = "https://new-website.com/courses"

courses = soup.find_all('div', class_='new-course-class')

## Troubleshooting

No Data Found:

Ensure the target website's structure matches the scraping logic.

FAISS Index Not Found:

Regenerate embeddings by running the script once. Ensure the courses_index.faiss and courses_metadata.json files are created.

Model Compatibility:

Ensure you are using the all-MiniLM-L6-v2 model from Sentence Transformers.
