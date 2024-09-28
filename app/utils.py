import requests
from bs4 import BeautifulSoup
import re
import nltk

# Ensure punkt_tab is downloaded


from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from urllib.parse import quote_plus, urlparse
import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
from app.config import client as groq_client

try:
    nltk.data.find('tokenizers/punkt_tab/english/')
except LookupError:
    nltk.download('punkt_tab')

def is_url(text):
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text
    except Exception as e:
        return f"Error extracting text from URL: {e}"

def extract_keywords(text, num_keywords=20):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
    word_freq = Counter(tokens)
    keywords = [word for word, _ in word_freq.most_common(num_keywords)]
    return keywords

def generate_theory(keywords):
    try:
        prompt = f"Generate a brief theory or explanation about the following topic: {keywords}"
        response = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates theories based on given keywords."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return {"error": f"Failed to generate content: {str(e)}"}

def get_arxiv_papers(query, max_papers=4):
    base_url = "http://export.arxiv.org/api/query?"
    search_query = quote_plus(query)
    url = f"{base_url}search_query=all:{search_query}&start=0&max_results={max_papers}"

    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Failed to fetch data from arXiv"}

    try:
        soup = BeautifulSoup(response.content, 'lxml-xml')  # Use 'lxml-xml' for XML parsing
    except Exception as e:
        return {"error": f"Error parsing XML: {e}"}

    papers = []
    for entry in soup.find_all('entry'):
        authors = entry.find_all('author')
        author_names = [author.find('name').string for author in authors if author.find('name')]
        
        title = entry.find('title')
        published = entry.find('published')
        summary = entry.find('summary')
        link = entry.find('id')

        paper = {
            "Title": title.string.strip() if title else "N/A",
            "Authors": ", ".join(author_names) if author_names else "N/A",
            "Published": published.string[:10] if published else "N/A",
            "Abstract": summary.string[:300] + "..." if summary and len(summary.string) > 300 else summary.string if summary else "N/A",
            "Link": link.string if link else "N/A"
        }
        papers.append(paper)

    return papers

def get_google_search_results(query, num_results=5):
    search_url = f"https://www.google.com/search?q={quote_plus(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    search_results = []
    for g in soup.find_all('div', class_='g')[:num_results]:
        anchor = g.find('a')
        if anchor:
            link = anchor['href']
            title = g.find('h3', class_='r')
            title = title.text if title else 'No title'
            snippet = g.find('div', class_='s')
            snippet = snippet.text if snippet else 'No snippet'
            search_results.append({
                "Title": title,
                "Link": link,
                "Snippet": snippet
            })
    
    return search_results

def comprehensive_research(input_text):
    if is_url(input_text):
        content = extract_text_from_url(input_text)
        if "Error extracting text from URL" in content:
            return {"error": content}
    else:
        content = input_text

    keywords = extract_keywords(content)
    query = " ".join(keywords)

    theory = generate_theory(keywords)
    papers = get_arxiv_papers(query)
    search_results = get_google_search_results(query)

    return {
        "keywords": keywords,
        "generated_theory":theory,
        "arxiv_papers": papers,
        "google_search_results": search_results
    }