from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/preview', methods=['POST'])
def preview_url():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').get_text() if soup.find('title') else 'No Title Found'
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')[:3]]
        
        return jsonify({
            "url": url,
            "title": title,
            "preview": "\n".join(paragraphs)
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)