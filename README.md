# demo-rag
# RAG chatbot for Groww and UltraTech

A chatbot that answers questions about Groww's charges and UltraTech's products using documents stored in my own CRUD API. To run it, install the packages with `pip install -r requirements.txt`, start the API with `python -m uvicorn api:app --port 8001`, load the documents once with `python load_docs.py`, then ask a question like `python agent.py groww "what is the brokerage for stocks"`. You can add, view, edit and delete the documents at http://127.0.0.1:8001/docs.
