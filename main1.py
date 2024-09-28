import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from urllib.parse import quote_plus, urlparse
import google.generativeai as genai
import openai

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Configure Google Gemini API
genai.configure(api_key='AIzaSyA8pseyBxOvduUtnEikOFyQPsmQqG3SNsk')

# Configure OpenAI API
openai.api_key = 'YOUR_OPENAI_API_KEY'

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
        # Remove script and style elements
        #print(soup)
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        print(text)
        return text
    except Exception as e:
        print(f"Error extracting text from URL: {e}")
        return None

def extract_keywords(text, num_keywords=5):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
    word_freq = Counter(tokens)
    keywords = [word for word, _ in word_freq.most_common(num_keywords)]
    return keywords

def generate_theory(keywords):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Generate a brief theory or explanation about the following topics: {', '.join(keywords)}"
    response = model.generate_content(prompt)
    return response.text
def generate_theory(keywords):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama3-8b-8192",)
    return chat_completion.choices[0].message.content
def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url

def get_arxiv_papers(query, max_papers=4):
    base_url = "http://export.arxiv.org/api/query?"
    search_query = quote_plus(query)
    url = f"{base_url}search_query=all:{search_query}&start=0&max_results={max_papers}"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')

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
        print("URL detected. Extracting content...")
        content = extract_text_from_url(input_text)
        if content is None:
            return "Failed to extract content from the URL."
    else:
        content = input_text

    keywords = extract_keywords(content)
    query = " ".join(keywords)

    print(f"Keywords extracted: {keywords}\n")

    # Generate theory using Gemini
    theory = generate_theory(keywords)
    print("Generated Theory:")
    print(theory)
    print("\n" + "="*50 + "\n")

    

    # Get arXiv papers
    papers = get_arxiv_papers(query)
    print(f"Found {len(papers)} related papers:")
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. Title: {paper['Title']}")
        print(f"   Authors: {paper['Authors']}")
        print(f"   Published: {paper['Published']}")
        print(f"   Abstract: {paper['Abstract']}")
        print(f"   Link: {paper['Link']}")

    # Get Google search results
    search_results = get_google_search_results(query)
    print(f"\nTop {len(search_results)} Google Search Results:")
    for i, result in enumerate(search_results, 1):
        print(f"\n{i}. Title: {result['Title']}")
        print(f"   Link: {result['Link']}")
        print(f"   Snippet: {result['Snippet']}")

# Example usage
if __name__ == "__main__":
    user_input = input("Enter text or a URL to research: ")
    comprehensive_research(user_input)