from datetime import datetime

from requests import request
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from fastapi import FastAPI
import json
from pydantic import BaseModel
from typing import Optional
import re
from sqlalchemy.sql import text


engine = create_engine("postgresql://XVdIBT:HciJiV@localhost:5436/db")
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


class Url(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True)
    source = Column(String)  # e.g. 'request' or 'response'
    response_id = Column(Integer, ForeignKey('responses.id'))
    value = Column(String)
    # response = relationship("Response", backref="urls")
    
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    source = Column(String)
    url_id = Column(Integer, ForeignKey('urls.id'), nullable=True)
    cookies = Column(String)
    request_id = Column(Integer, ForeignKey('requests.id'), nullable=True)
    time = Column(DateTime)

    # Establish relationships with other models
    url = relationship("Url", backref="tasks")
    request = relationship("Request", backref="tasks")


# Base.metadata.drop_all(engine)
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

@app.get("/tasks")
def get_tasks():
    session = Session()
    tasks = session.query(Task).all()
    return [
        {
            "id": task.id,
            "source": task.source,
            "url_id": task.url_id,
            "cookies": task.cookies,
            "request_id": task.request_id,
            "time": task.time,
        }
        for task in tasks
    ]
    
class CreateTaskRequest(BaseModel):
    url_id: int

@app.post("/tasks")
def create_task(task_request: CreateTaskRequest):
    session = Session()
    new_task = Task(
        source="url",
        url_id=task_request.url_id,
        cookies="{}",
        request_id=None,
        time=datetime.now(),
    )
    session.add(new_task)
    session.commit()
    return {
        "id": new_task.id,
        "source": new_task.source,
        "url_id": new_task.url_id,
        "cookies": new_task.cookies,
        "request_id": new_task.request_id,
        "time": new_task.time,
    }

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


class UrlBase(BaseModel):
    source: str
    response_id: Optional[int]
    value: str

@app.get("/urls")
async def get_urls(url_value_filter: Optional[str] = None):
    session = Session()
    if url_value_filter:
        urls = session.query(Url).filter(text('value ~ :reg')).params(reg=url_value_filter).all()
    else:
        urls = session.query(Url).all()

    return [
        {
            "id": url.id,
            "source": url.source,
            "response_id": url.response_id,
            "value": url.value
        }
        for url in urls
    ]

# @app.post("/urls")
# async def create_url(url: UrlBase):
@app.get("/responses/{response_id}")
async def get_response_content(response_id: int):
    session = Session()
    new_url = Url(
        source=url.source,
        response_id=url.response_id,
        value=url.value
    )
    session.add(new_url)
    session.commit()
    response = session.query(Response).filter_by(id=response_id).first()
    return {
        "id": new_url.id,
        "source": new_url.source,
        "response_id": new_url.response_id,
        "value": new_url.value,
        "id": response.id,
        "content_text": response.content_text
    }

class ExtractUrlsRequest(BaseModel):
    response_id: int

@app.post("/extract_urls")
async def extract_urls(extract_request: ExtractUrlsRequest):
    session = Session()
    response = session.query(Response).filter_by(id=extract_request.response_id).first()
    if response:
        content_text = response.content_text
        # Implement logic to extract URLs from the content text
        # For this example, assume we have a function called 'extract_urls_from_text'
        urls = extract_urls_from_text(content_text)
        
        new_urls = []
        for url in urls:
            new_url = Url(
                source='response',
                response_id=extract_request.response_id,
                value=url
            )
            session.add(new_url)
            new_urls.append({
                "id": new_url.id,
                "source": new_url.source,
                "response_id": new_url.response_id,
                "value": new_url.value
            })
        session.commit()
        return new_urls
    else:
        return {"error": "Response not found"}

def extract_urls_from_text(text: str):
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)
    return urls


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
