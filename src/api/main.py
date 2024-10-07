from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
# uvicorn main:app --reload
import sys
import os

# Add the src directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import *

app = FastAPI()
    

# Create an async database engine
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@app.get("/languages", response_model=list[dict])
async def get_languages():
    async with SessionLocal() as session:
        # Query the languages table
        query = select(Language)
        result = await session.execute(query)
        languages = result.scalars().all()
        
        # Convert to list of dictionaries
        return [lang.to_dict() for lang in languages]

@app.get("/countries", response_model=list[dict])
async def get_countries():
    async with SessionLocal() as session:
        # Query the countries table
        query = select(Country)
        result = await session.execute(query)
        countries = result.scalars().all()
        
        # Convert to list of dictionaries
        return [country.to_dict() for country in countries]

@app.get("/categories", response_model=list[dict])
async def get_categories():
    async with SessionLocal() as session:
        # Query the categories table
        query = select(Category)
        result = await session.execute(query)
        categories = result.scalars().all()
        
        # Convert to list of dictionaries
        return [category.to_dict() for category in categories]

@app.get("/authors", response_model=list[dict])
async def get_authors():
    async with SessionLocal() as session:
        # Query the authors table
        query = select(Author)
        result = await session.execute(query)
        authors = result.scalars().all()
        
        # Convert to list of dictionaries
        return [author.to_dict() for author in authors]

@app.get("/articles", response_model=list[dict])
async def get_articles():
    async with SessionLocal() as session:
        # Query the articles table and join the related tables
        query = (
            select(Article)
            .options(
                joinedload(Article.author),      # Eager load the Author relationship
                joinedload(Article.category),    # Eager load the Category relationship
                joinedload(Article.country),     # Eager load the Country relationship
                joinedload(Article.language)     # Eager load the Language relationship
            )
        )
        result = await session.execute(query)
        articles = result.scalars().all()
        
        # Convert to list of dictionaries
        return [
            {
                "id": article.article_id,
                "author": {
                    "id": article.author.author_id,  # Get author name
                    "name": article.author.author_name,  # Get author name
                    "url": article.author.author_url     # Get author URL
                },
                "category": {
                    "id": article.category.category_id,
                    "name": article.category.category_name  # Get category name
                },
                "country": {
                    "id": article.country.country_id,
                    "name": article.country.country_name,
                    "code": article.country.country_code  # Get country code
                },
                "language": {
                    "id": article.language.lang_id,
                    "name": article.language.lang_name,
                    "code": article.language.lang_code  # Get language code
                },
                "publication_date": str(article.publication_date),  # Convert date to string
                "title": article.title,
                "description": article.description,
                "img_url": article.img_url,
                "url": article.url,
                "content_preview": article.content_preview,
                "content": article.content,
                "source": article.source,
            } for article in articles
        ]


    
@app.get("/")
def index():
    return "Welcome to Africa News API"
