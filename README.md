# Comprehensive Research API

This FastAPI application provides a comprehensive research endpoint that generates theories, fetches related papers from arXiv, provides Google search results, and can extract content from URLs based on a given query.

## Features
1. URL Content Extraction: Extracts and cleans text from a given URL.
2. Keyword Extraction: Identifies the most relevant keywords from the text.
3. heory Generation: Generates a brief theory or explanation based on the extracted keywords using a language model.
4. ArXiv Paper Search: Fetches related academic papers from arXiv.
5. Google Search Results: Retrieves related search results from Google.

## Setup
Feel free to contribute to this project by opening issues or submitting pull requests. For major changes, please open an issue first to discuss what you would like to change.
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` file with your GEMINI_API_KEY and OPENAI_API_KEY
4. Run the application: `uvicorn app.main:app --reload`

## Usage

Send a POST request to `/research` with a JSON body:

```json
{
  "query": "Your research query or URL here"
}

