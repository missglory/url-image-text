from sqlalchemy import create_engine, Column, String, Text, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from fastapi import FastAPI
from pydantic import BaseModel

engine = create_engine("sqlite:///example.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Request(Base):
    """Table for storing requests."""

    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    method = Column(String)
    headers = Column(Text)
    data = Column(Text)

    responses = relationship("Response", back_populates="request")


class Response(Base):
    """Table for storing responses."""

    __tablename__ = "responses"

    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey('requests.id'))
    status_code = Column(Integer)
    headers = Column(Text)
    content = Column(Text)

    request = relationship("Request", back_populates="responses")


class RequestModel(BaseModel):
    url: str
    method: str
    headers: str
    data: str


class ResponseModel(BaseModel):
    status_code: int
    headers: str
    content: str


app = FastAPI()


@app.get("/requests")
def get_requests():
    session = Session()
    request_entries = session.query(Request).all()
    return [
        {
            "id": entry.id,
            "url": entry.url,
            "method": entry.method,
            "headers": entry.headers,
            "data": entry.data,
        }
        for entry in request_entries
    ]


@app.post("/requests")
def insert_request(request: RequestModel):
    session = Session()
    new_request_entry = Request(
        url=request.url, method=request.method, headers=request.headers, data=request.data
    )
    session.add(new_request_entry)
    session.commit()
    return {"id": new_request_entry.id, "url": new_request_entry.url}


@app.get("/responses")
def get_responses():
    session = Session()
    response_entries = session.query(Response).all()
    return [
        {
            "id": entry.id,
            "request_id": entry.request_id,
            "status_code": entry.status_code,
            "headers": entry.headers,
            "content": entry.content,
        }
        for entry in response_entries
    ]


@app.post("/responses")
def insert_response(response: ResponseModel, request_id: int):
    session = Session()
    new_response_entry = Response(
        request_id=request_id, status_code=response.status_code, headers=response.headers, content=response.content
    )
    session.add(new_response_entry)
    session.commit()
    return {"id": new_response_entry.id, "request_id": new_response_entry.request_id}


# Instructions on how to run the FastAPI server and use curl commands
"""
To run the FastAPI server, navigate to the directory containing this file and run:
uvicorn scrape_db:app --host 0.0.0.0 --port 8000

You can then access the API at http://localhost:8000

To get all request entries, use the following curl command:
curl http://localhost:8000/requests

To insert a new request entry, use the following curl command:
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com", "method": "GET", "headers": "{}", "data": ""}' http://localhost:8000/requests

To get all response entries, use the following curl command:
curl http://localhost:8000/responses

To insert a new response entry, use the following curl command:
curl -X POST -H "Content-Type: application/json" -d '{"status_code": 200, "headers": "{}", "content": ""}' http://localhost:8000/responses
"""
