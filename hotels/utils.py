import requests

def rewrite_with_ollama(title, description):
    api_url = 'http://127.0.0.1:11434/rewrite'  
    payload = {
        'title': title,
        'description': description
    }
    response = requests.post(api_url, json=payload)
    
    if response.status_code == 200:
        return response.json() 
    else:
        print(f"Error: {response.status_code}")
        return None
