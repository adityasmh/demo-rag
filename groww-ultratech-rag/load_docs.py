import json
from urllib.request import Request, urlopen

from search import load_paragraphs

API = "http://127.0.0.1:8001"

for company in ["groww", "ultratech"]:
    if json.load(urlopen(f"{API}/documents?company={company}")):
        print(company, "already loaded")
        continue
    for p in load_paragraphs(company):
        body = json.dumps({"company": company, "heading": p["heading"], "text": p["text"]}).encode()
        urlopen(Request(f"{API}/documents", data=body, headers={"Content-Type": "application/json"}))
    print(company, "loaded")
