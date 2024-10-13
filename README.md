# Africa-News-API

## Table of Contents
1. [Summary](#summary)
2. [Features](#features)
3. [Tools](#tools)
4. [Architecture](#architecture)
5. [Database Design](#database-design)
6. [Installation](#installation)
   - [Prerequisites](#prerequisites)
   - [Setup Steps](#setup-steps)
7. [Usage](#usage)
8. [API Endpoints](#api-endpoints)
9. [ETL Pipeline](#etl-pipeline)
10. [Contributing](#contributing)
11. [License](#license)

## Summary
The Africa-News-API is a personal project designed to aggregate news from various African media platforms and existing news APIs into a centralized database. News articles are retrieved, transformed, and stored hourly, making them accessible to users through dedicated API endpoints, facilitating easy access to news events across the continent.

## Features
- Aggregates news from multiple African media websites and news APIs.
- Efficiently processes large volumes of news articles using Apache Spark.
- Stores news articles in a PostgreSQL database.
- Provides a FastAPI-based API for accessing news data.
- Automated ETL (Extract, Transform, Load) pipeline using Apache Airflow.
- Supports containerized deployment with Docker and Docker Compose.

## Tools
- **PgModeler**: For database modeling and design.
- **PostgreSQL**: Relational database management system for storing news articles.
- **SQLAlchemy**: For database interaction and management, serving as an Object-Relational Mapping (ORM) tool.
- **Python**: Primary programming language for data retrieval and processing.
- **Selenium**: For web scraping news articles from media websites.
- **Apache Spark**: For processing and analyzing large volumes of news data efficiently.
- **Apache Airflow**: To orchestrate and automate data workflows and ETL processes.
- **FastAPI**: To create a performant and easy-to-use API for accessing news data.
- **Docker**: For containerizing the application to ensure consistency across different environments.
- **Docker Compose**: For defining and managing multi-container Docker applications, simplifying the setup and orchestration of services.
- **Bash**: For scripting tasks related to database initialization, Airflow user and connection initialization, etc.

<!--## Architecture
*Detailed architecture diagram and explanation here (if available).*-->

## Database Design
The database design for the Africa-News-API is structured to efficiently store and retrieve news articles. Below are the key tables and their relationships:

![Database Design](./database/design/design.png)

<!-- ### Tables

1. **articles**
   - **id**: Serial primary key.
   - **title**: String, the title of the news article.
   - **content**: Text, the body of the article.
   - **source**: String, the media source of the article.
   - **published_at**: Timestamp, the publication date of the article.
   - **url**: String, the URL of the article.
   - **created_at**: Timestamp, the date and time the article was created in the database.
   - **updated_at**: Timestamp, the date and time the article was last updated.

2. **sources**
   - **id**: Serial primary key.
   - **name**: String, the name of the news source.
   - **api_url**: String, the API endpoint for retrieving articles from this source (if applicable).
   - **created_at**: Timestamp, the date and time the source was added to the database.

### Relationships
- Each article can be associated with one source, establishing a one-to-many relationship between `sources` and `articles`.


## Installation
### Prerequisites
*List any prerequisites needed before installation (e.g., Docker, Python, etc.).*

### Setup Steps
*Step-by-step guide to set up the project environment, including commands for Docker and installation of dependencies.*

## Usage
*Instructions on how to run the project and any configuration options.*

## API Endpoints
*Document the API endpoints available, including request methods, parameters, and example responses.*

## ETL Pipeline
*Explain the ETL pipeline process, including any scheduled jobs and how data flows through the system.*

## Contributing
*Guidelines for contributing to the project.*

## License
*Specify the license under which the project is distributed.*-->
