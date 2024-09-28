# Comprehensive Research API

This FastAPI application provides a comprehensive research endpoint that generates theories, fetches related papers from arXiv, provides Google search results, and can extract content from URLs based on a given query.

## Setup

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