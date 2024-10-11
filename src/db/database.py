from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
#app = FastAPI()
DATABASE_URL = "postgresql+asyncpg://starias:my_password@localhost/africa_news_db"

# Define the SQLAlchemy base
Base = declarative_base()


# Define the Language model
class Language(Base):
    __tablename__ = 'language'

    lang_id = Column(Integer, primary_key=True)
    lang_name = Column(String)
    lang_code = Column(String)
    
    def to_dict(self):
        return {"id": self.lang_id, "name": self.lang_name, "code": self.lang_code}

# Define the Country model
class Country(Base):
    __tablename__ = 'country'

    country_id = Column(Integer, primary_key=True)
    country_name = Column(String)
    country_code = Column(String)

    def to_dict(self):
        return {"id": self.country_id, "name": self.country_name, "code": self.country_code}

# Define the Category model
class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String)

    def to_dict(self):
        return {"id": self.category_id, "name": self.category_name}

# Define the Author model
class Author(Base):
    __tablename__ = 'author'  # Replace with your actual table name

    author_id = Column(Integer, primary_key=True)
    author_name = Column(String)
    author_url = Column(Text)

    def to_dict(self):
        return {"id": self.author_id, "name": self.author_name, "URL": self.author_url}

class Extractor(Base):
    __tablename__ = 'extractor'
    extractor_id = Column(Integer, primary_key=True)
    extractor_name = Column(String)

# Define the Article model
class Article(Base):
    __tablename__ = 'article'

    article_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('author.author_id'))
    category_id = Column(Integer, ForeignKey('category.category_id'))
    country_id = Column(Integer, ForeignKey('country.country_id'))
    lang_id = Column(Integer, ForeignKey('language.lang_id'))
    extractor_id = Column(Integer, ForeignKey('extractor.extractor_id'))
    publication_date = Column(Date)
    title = Column(Text)
    description = Column(Text)
    img_url = Column(Text)
    url = Column(Text)
    content_preview = Column(Text)
    content = Column(Text)
    source = Column(String)

    # Relationships
    author = relationship("Author")
    category = relationship("Category")
    country = relationship("Country")
    language = relationship("Language")
    extractor = relationship('Extractor')
    
