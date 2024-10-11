from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from datetime import datetime
import sys
import os
from fastapi import Query
from fastapi import HTTPException
# Add the src directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import *

# uvicorn main:app --reload



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
async def get_articles(
    country: str = Query(None),
    lang: str = Query(None),
    category: str = Query(None),
    author: str = Query(None),
    source: str = Query(None),
    start_date: str = Query(None),  # Start date for the publication date range
    end_date: str = Query(None),    # End date for the publication date range
    order_by: str = Query("publication_date"),  # Field to order by (default: publication_date)
    order: str = Query("desc"),  # Sort order: 'asc' for ascending, 'desc' for descending
    limit: int = Query(10, gt=0, le=100),  # Maximum number of results to return (default 10, max 100)
    offset: int = Query(0, ge=0)  # Number of results to skip for pagination (default 0)
):
    async with SessionLocal() as session:
        # Base query for articles
        query = (
            select(Article)
            .options(
                joinedload(Article.author),
                joinedload(Article.category),
                joinedload(Article.country),
                joinedload(Article.language),
                joinedload(Article.source),
            )
        )

        # Add filters based on provided query parameters
        if country:
            if len(country) == 2:
                query = query.join(Article.country).filter(func.lower(Country.country_code) == func.lower(country))
            else:
                query = query.join(Article.country).filter(func.lower(Country.country_name) == func.lower(country))
        
        if lang:
            if len(lang) == 2:
                query = query.join(Article.language).filter(func.lower(Language.lang_code) == func.lower(lang))
            else:
                query = query.join(Article.language).filter(func.lower(Language.lang_name) == func.lower(lang))
            
        if category:
            query = query.join(Article.category).filter(func.lower(Category.category_name) == func.lower(category))
        
        if author:
            query = query.join(Article.author).filter(func.lower(Author.author_name) == func.lower(author))
        
        if source:
            query = query.join(Article.source).filter(func.lower(Source.source_name) == func.lower(source))

        # Filter by publication date range
        if start_date and end_date:
            try:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                query = query.filter(Article.publication_date.between(start_dt, end_dt))
            except ValueError:
                return {"error": "Invalid date format. Use YYYY-MM-DD."}

        # Apply ordering
        valid_order_by_fields = {
            "publication_date": Article.publication_date,
        }

        if order_by not in valid_order_by_fields:
            raise HTTPException(status_code=400, detail=f"Invalid order_by field. Choose from {list(valid_order_by_fields.keys())}.")

        # Apply sort order (ascending or descending)
        if order == "desc":
            query = query.order_by(valid_order_by_fields[order_by].desc())
        else:
            query = query.order_by(valid_order_by_fields[order_by].asc())

        # Apply pagination (limit and offset)
        query = query.limit(limit).offset(offset)

        # Execute query and fetch results
        result = await session.execute(query)
        articles = result.scalars().all()
        
        # Convert to list of dictionaries
        return [
            {
                "id": article.article_id,
                "author": {
                    "id": article.author.author_id,
                    "name": article.author.author_name,
                    "url": article.author.author_url
                },
                "category": {
                    "id": article.category.category_id,
                    "name": article.category.category_name
                },
                "source": {
                    "id": article.source.source_id,
                    "name": article.source.source_name
                },
                "country": {
                    "id": article.country.country_id,
                    "name": article.country.country_name,
                    "code": article.country.country_code
                },
                "language": {
                    "id": article.language.lang_id,
                    "name": article.language.lang_name,
                    "code": article.language.lang_code
                },
                "publication_date": str(article.publication_date),
                "title": article.title,
                "description": article.description,
                "img_url": article.img_url,
                "url": article.url,
                "content_preview": article.content_preview,
                "content": article.content,
                #"source": article.source,
            } for article in articles
        ]



    
@app.get("/")
def index():
    return "Welcome to Africa News API"
