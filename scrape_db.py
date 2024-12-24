from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from pydantic import BaseModel

# Create a database engine (in this case, SQLite)
engine = create_engine('sqlite:///example.db')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Base class which maintains a catalog of Table objects within a database.
Base = declarative_base()

class HarFile(Base):
    """Table for storing HAR files."""
    __tablename__ = 'har_files'
    
    # Using URL as the primary key (id)
    url = Column(String, primary_key=True)
    har_data = Column(Text)

    def __repr__(self):
        return f"HarFile(url='{self.url}', har_data='{self.har_data[:100]}...)"


class RawHtml(Base):
    """Table for storing raw HTML."""
    __tablename__ = 'raw_html'
    
    # Using URL as the primary key (id)
    url = Column(String, primary_key=True)
    html_content = Column(Text)

    def __repr__(self):
        return f"RawHtml(url='{self.url}', html_content='{self.html_content[:100]}...)"


# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)


class HarFileModel(BaseModel):
    url: str
    har_data: str

class RawHtmlModel(BaseModel):
    url: str
    html_content: str

app = FastAPI()

# Example usage
if __name__ == '__main__':
    # To start, create a new session
    session = Session()

    # Adding an example HAR file entry
    har_entry = HarFile(url="https://example.com", har_data="<HAR_FILE_CONTENT>")
    session.add(har_entry)
    session.commit()

    # Adding an example raw HTML entry
    html_entry = RawHtml(url="https://example.net", html_content="<HTML_CONTENT>")
    session.add(html_entry)
    session.commit()

    # Querying the database for entries
    har_entries = session.query(HarFile).all()
    for entry in har_entries:
        print(entry)

    raw_html_entries = session.query(RawHtml).all()
    for entry in raw_html_entries:
        print(entry)


@app.get("/har")
def get_har():
    session = Session()
    har_entries = session.query(HarFile).all()
    return [{"url": entry.url, "har_data": entry.har_data} for entry in har_entries]

@app.get("/html")
def get_html():
    session = Session()
    raw_html_entries = session.query(RawHtml).all()
    return [{"url": entry.url, "html_content": entry.html_content} for entry in raw_html_entries]
