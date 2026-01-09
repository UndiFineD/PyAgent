import requests

def call_api():
    res = requests.get("https://api.example.com")
    return res.text
