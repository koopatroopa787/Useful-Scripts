import requests

def is_website_online(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except:
        return False

print(is_website_online('https://example.com'))