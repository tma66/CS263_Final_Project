import os
from flask import Flask, request, send_from_directory, render_template
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        parsed_url = urlparse(url)
        
        # Check if URL is valid
        if not all([parsed_url.scheme, parsed_url.netloc]):
            return "Invalid URL"

        try:
            content_type = request.files.get('file').content_type
        except AttributeError:
            # Get the content from the provided URL
            import requests
            response = requests.get(url)
            
            if response.status_code == 200:
                file = BytesIO(response.content)
                
                # Check content type and display preview accordingly
                if 'image' in content_type:
                    img = Image.open(file)
                    img.thumbnail((150, 150))  # Resize image to fit within a 150x150 box
                    img.save('static/picture.png', 'PNG')
                    
                    return render_template('index.html', url=url, content_type=content_type)
                elif 'video' in content_type:
                    filename = os.path.basename(url)
                    file.save(os.path.join(app.root_path, 'static', filename))
                    return f"Downloaded {filename}"
                else:
                    return "Unsupported file type"
            else:
                return f"Failed to retrieve {url}: {response.status_code}"
        else:
            # If user provided a local file
            filename = os.path.basename(url)
            file.save(os.path.join(app.root_path, 'static', filename))
            return f"Downloaded {filename}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)