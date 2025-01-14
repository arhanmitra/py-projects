import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

def get_top_words(url, top_n=5):

    # Adding header so as not to get blocked or rate limted by the server. Pretending to be a browser
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    try:
        # Fetch the page
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text from the content sections
        content = soup.find('div', {'class': 'mw-parser-output'})
        if not content:
            print("Could not find content on the page.")
            return
        
        text = content.get_text()
        
        # Clean and split the text into words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Count the word frequencies
        word_counts = Counter(words)
        
        # Exclude common stop words (you can add more to this list)
        stop_words = {
            "the", "and", "of", "to", "in", "is", "that", "it", "as", "with",
            "for", "was", "on", "by", "an", "are", "this", "from", "or", "at",
            "be", "not", "which", "but", "has", "had", "have", "he", "she", "his", "all"
        }
        
        filtered_counts = {word: count for word, count in word_counts.items() if word not in stop_words}
        
        # Get the top N words
        top_words = Counter(filtered_counts).most_common(top_n)
        
        print(f"Top {top_n} words:")
        for word, count in top_words:
            print(f"{word}: {count}")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage
url = "https://en.wikipedia.org/wiki/Shorewood,_Wisconsin"  # Replace with your desired Wikipedia URL
get_top_words(url)

