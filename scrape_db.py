from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from pydantic import BaseModel

engine = create_engine("sqlite:///example.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()


class HarFile(Base):
    """Table for storing HAR files."""

    __tablename__ = "har_files"

    # Using URL as the primary key (id)
    url = Column(String, primary_key=True)
    har_data = Column(Text)

    def __repr__(self):
        return f"HarFile(url='{self.url}', har_data='{self.har_data[:100]}...)"


class RawHtml(Base):
    """Table for storing raw HTML."""

    __tablename__ = "raw_html"

    # Using URL as the primary key (id)
    url = Column(String, primary_key=True)
    html_content = Column(Text)

    def __repr__(self):
        return f"RawHtml(url='{self.url}', html_content='{self.html_content[:100]}...)"


Base.metadata.create_all(engine)


class HarFileModel(BaseModel):
    url: str
    har_data: str


class RawHtmlModel(BaseModel):
    url: str
    html_content: str


app = FastAPI()


@app.get("/har")
def get_har():
    session = Session()
    har_entries = session.query(HarFile).all()
    return [{"url": entry.url, "har_data": entry.har_data} for entry in har_entries]


@app.post("/har")
def insert_har(har_file: HarFileModel):
    session = Session()
    new_har_entry = HarFile(url=har_file.url, har_data=har_file.har_data)
    session.add(new_har_entry)
    session.commit()
    return {"url": new_har_entry.url, "har_data": new_har_entry.har_data}


@app.get("/html")
def get_html():
    session = Session()
    raw_html_entries = session.query(RawHtml).all()
    return [
        {"url": entry.url, "html_content": entry.html_content}
        for entry in raw_html_entries
    ]


@app.post("/html")
def insert_html(raw_html: RawHtmlModel):
    session = Session()
    new_raw_html_entry = RawHtml(url=raw_html.url, html_content=raw_html.html_content)
    session.add(new_raw_html_entry)
    session.commit()
    return {"url": new_raw_html_entry.url, "html_content": new_raw_html_entry.html_content}
