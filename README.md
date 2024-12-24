# Instructions on how to run the FastAPI server and use curl commands
"""
To run the FastAPI server, navigate to the directory containing this file and run:
uvicorn scrape_db:app --host 0.0.0.0 --port 8000

You can then access the API at http://localhost:8000

To get all HAR entries, use the following curl command:
curl http://localhost:8000/har

To insert a new HAR entry, use the following curl command:
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com", "har_data": "example_har_data"}' http://localhost:8000/har

To get all raw HTML entries, use the following curl command:
curl http://localhost:8000/html

To insert a new raw HTML entry, use the following curl command:
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com", "html_content": "example_html_content"}' http://localhost:8000/html
"""