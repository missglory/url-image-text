from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
import json

engine = create_engine("sqlite:///scrape.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    method = Column(String)
    headers = Column(String)
    data = Column(String)
    startedDateTime = Column(String)


class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer)
    status_code = Column(Integer)
    headers = Column(String)
    content_text = Column(String)
    content_mime_type = Column(String)
    content_size = Column(Integer)
    content_compression = Column(Integer)
    time = Column(Integer)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/requests")
def get_requests():
    session = Session()
    requests = session.query(Request).all()
    return [
        {
            "id": request.id,
            "url": request.url,
            "method": request.method,
            "headers": json.loads(request.headers),
            "data": json.loads(request.data),
            "startedDateTime": request.startedDateTime,
        }
        for request in requests
    ]


@app.post("/requests")
def insert_request(request: dict):
    session = Session()
    new_request = Request(
        url=request["url"],
        method=request["method"],
        headers=json.dumps(request["headers"]),
        data=json.dumps(request["data"]),
    )
    session.add(new_request)
    session.commit()
    return {
        "id": new_request.id,
        "url": new_request.url,
        "method": new_request.method,
        "headers": json.loads(new_request.headers),
        "data": json.loads(new_request.data),
        "startedDateTime": new_request.startedDateTime,
    }


@app.get("/responses")
def get_responses():
    session = Session()
    responses = session.query(Response).all()
    return [
        {
            "id": response.id,
            "request_id": response.request_id,
            "status_code": response.status_code,
            "headers": json.loads(response.headers),
            "content_text": response.content_text,
            "content_mime_type": response.content_mime_type,
            "content_size": response.content_size,
            "content_compression": response.content_compression,
            "time": response.time,
        }
        for response in responses
    ]


@app.post("/responses")
def insert_response(response: dict, request_id: int):
    session = Session()
    new_response = Response(
        request_id=request_id,
        status_code=response["status_code"],
        headers=json.dumps(response["headers"]),
        content_text=response["content_text"],
        content_mime_type=response["content_mime_type"],
        content_size=response["content_size"],
        content_compression=response["content_compression"],
        time=response["time"],
    )
    session.add(new_response)
    session.commit()
    return {
        "id": new_response.id,
        "request_id": new_response.request_id,
        "status_code": new_response.status_code,
        "headers": json.loads(new_response.headers),
        "content_text": new_response.content_text,
        "content_mime_type": new_response.content_mime_type,
        "content_size": new_response.content_size,
        "content_compression": new_response.content_compression,
        "time": new_response.time,
    }


@app.get("/schema")
def get_schema():
    return {
        "requests": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "url": {"type": "string"},
                "method": {"type": "string"},
                "headers": {"type": "string"},
                "data": {"type": "string"},
            },
            "required": ["url", "method", "headers", "data"],
        },
        "responses": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "request_id": {"type": "integer"},
                "status_code": {"type": "integer"},
                "headers": {"type": "string"},
                "content_text": {"type": "string"},
                "content_mime_type": {"type": "string"},
                "content_size": {"type": "integer"},
                "content_compression": {"type": "string"},
            },
            "required": [
                "request_id",
                "status_code",
                "headers",
                "content_text",
                "content_mime_type",
                "content_size",
                "content_compression",
            ],
        },
    }


# Instructions on how to run the FastAPI server and use curl commands
"""
To run the FastAPI server, navigate to the directory containing this file and run:
uvicorn scrape_db:app --host 0.0.0.0 --port 8000

You can then access the API at http://localhost:8000

To get all request entries, use the following curl command:
curl http://localhost:8000/requests

To insert a new request entry, use the following curl command:
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com", "method": "GET", "headers": {}, "data": {}}' http://localhost:8000/requests

To get all response entries, use the following curl command:
curl http://localhost:8000/responses

To insert a new response entry, use the following curl command:
curl -X POST -H "Content-Type: application/json" -d '{"status_code": 200, "headers": {}, "content_text": "Hello World", "content_mime_type": "text/plain", "content_size": 12, "content_compression": "none"}' http://localhost:8000/responses

To get the schema of the API, use the following curl command:
curl http://localhost:8000/schema
"""
