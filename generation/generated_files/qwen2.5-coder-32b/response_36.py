import requests
from bs4 import BeautifulSoup

def login_and_scrape(url, username, password):
    session = requests.Session()
    
    # Fetch the login page to get any necessary tokens
    login_page = session.get(url)
    soup = BeautifulSoup(login_page.text, 'html.parser')
    
    # Find the form and extract hidden fields if necessary
    form = soup.find('form')
    data = {input['name']: input['value'] for input in form.find_all('input') if input.has_attr('name')}
    
    # Add username and password to the data
    data['username'] = username
    data['password'] = password
    
    # Submit the login form
    response = session.post(url, data=data)
    
    # Check if login was successful
    if 'login failed' in response.text.lower():
        raise Exception('Login failed')
    
    # Scrape user-specific data from a protected page
    protected_page = session.get('https://example.com/user/data')
    soup = BeautifulSoup(protected_page.text, 'html.parser')
    
    # Extract and return the desired data
    user_data = soup.find('div', {'id': 'user-data'}).text.strip()
    return user_data

# Example usage
url = 'https://example.com/login'
username = 'your_username'
password = 'your_password'
data = login_and_scrape(url, username, password)
print(data)