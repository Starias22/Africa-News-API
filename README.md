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
The database design for the Africa-News-API is structured to efficiently store and retrieve news articles. It organizes data into well-defined tables to support rapid querying and scalability. Below is an Entity-Relationship (ER) diagram (ERD) that outlines the structure of the database, designed using **PgModeler**.

![Database Design](./database/design/design.png)


The diagram illustrates the relationships between these entities, such as how each article is linked to a media source and categorized under specific tags.

### Model Files:
- **Database Model**: The ER model file generated using PgModeler can be found [here](./database/design/design.dbm) in the repository.
- **SQL File**: [Here](./database/init/utils/init_script.sql) is the SQL file used to create the database schema. It is generated in PgModeler.

This design ensures the Africa-News-API can scale as the volume of news articles grows while maintaining quick access to information through efficient database queries.


## API endpoints

### 1. **Root Endpoint**

- **Endpoint**: `/`
- **Method**: `GET`
- **Description**: Returns a welcome message.
- **Response**: 
    ```json
    "Welcome to Africa News API"
    ```

### 2. **Get all Languages**

- **Endpoint**: `/languages`
- **Method**: `GET`
- **Description**: Retrieve a list of all languages available in the database.
- **Response**: A list of languages in the following format:

    ```json
    [
    {
        "id": 1,
        "name": "english",
        "code": "en"
    },
    {
        "id": 2,
        "name": "french",
        "code": "fr"
    }
    ]
    ```

---

### 3. **Get all Countries**

- **Endpoint**: `/countries`
- **Method**: `GET`
- **Description**: Retrieve a list of all countries available in the database.
- **Response**: A list of countries in the following format:

    ```json
        [
    {
        "id": 1,
        "name": "algeria",
        "code": "DZ"
    },
    {
        "id": 2,
        "name": "angola",
        "code": "AO"
    },
    {
        "id": 3,
        "name": "benin",
        "code": "BJ"
    },
    
    
    {
        "id": 54,
        "name": "zambia",
        "code": "ZM"
    },
    {
        "id": 55,
        "name": "zimbabwe",
        "code": "ZW"
    },
    {
        "id": 56,
        "name": null,
        "code": "ZZ"
    }
    ]
    ```

---

### 4. **Get all Categories**

- **Endpoint**: `/categories`
- **Method**: `GET`
- **Description**: Retrieve a list of all categories available in the database.
- **Response**: A list of categories in the following format:

    ```json
        [
    {
        "id": 1,
        "name": "analysis-interpretation"
    },
    {
        "id": 2,
        "name": "business-economy-finance"
    },
    {
        "id": 3,
        "name": "celebrity"
    },

    {
        "id": 18,
        "name": "music"
    },
    {
        "id": 19,
        "name": "council of ministers"
    },
    {
        "id": 20,
        "name": null
    }
    ]
    ```

---

### 5. **Get all Authors**

- **Endpoint**: `/authors`
- **Method**: `GET`
- **Description**: Retrieve a list of all authors available in the database.
- **Response**: A list of authors in the following format:

    ```json
    [
      {
    "id": 1,
    "name": null,
    "URL": null
  },
  {
    "id": 2,
    "name": "Romaric Déguénon",
    "URL": "https://beninwebtv.com/author/romaric/"
  },
  {
    "id": 3,
    "name": "Leandro Zomassi",
    "URL": "https://beninwebtv.com/author/libence/"
  },
  {
    "id": 4,
    "name": "Kevin Aka",
    "URL": "https://beninwebtv.com/author/kevin/"
  },
  {
    "id": 5,
    "name": "Aya N'goran",
    "URL": "https://beninwebtv.com/author/aya/"
  },
  {
    "id": 6,
    "name": "Ange Banouwin",
    "URL": "https://beninwebtv.com/author/banouwin/"
  },
  {
    "id": 7,
    "name": "Angèle M. ADANLE",
    "URL": "https://beninwebtv.com/author/angele/"
  },
  {
    "id": 8,
    "name": "Edouard Djogbénou",
    "URL": "https://beninwebtv.com/author/edouard/"
  }
    ]
    ```

---

### 6. **Get all Articles**

- **Endpoint**: `/articles`
- **Method**: `GET`
- **Description**: Retrieve a list of articles based on various filters.
- **Query Parameters**: They are all optional
  - `country`: Filter articles by country (either country name or country code).
  - `lang`: Filter articles by language (either language name or language code).
  - `category`: Filter articles by category name.
  - `author`: Filter articles by author name.
  - `source`: Filter articles by source name.
  - `start_date`: Start date for filtering by publication date (in `YYYY-MM-DD` format).
  - `end_date`: End date for filtering by publication date (in `YYYY-MM-DD` format).
  - `order_by`: Field to order the results by (default is `publication_date`).
  - `order`: Sort order, either `asc` or `desc` (default is `desc`).
  - `limit`: Maximum number of articles to return (default is 10, maximum is 100).
  - `offset`: Number of articles to skip for pagination (default is 0).

- **Response**: A list of articles in the following format:

    ```json
    [
      {
    "id": 31,
    "author": {
      "id": 1,
      "name": null,
      "url": null
    },
    "category": {
      "id": 20,
      "name": null
    },
    "source": {
      "id": 9,
      "name": "Nation"
    },
    "country": {
      "id": 34,
      "name": "morocco",
      "code": "MA"
    },
    "language": {
      "id": 1,
      "name": "english",
      "code": "en"
    },
    "publication_date": "None",
    "title": "Western Sahara issue threatens Morocco’s business deals",
    "description": "The Western Sahara region was initially a colony of Spain but after the colonialists departed, it was administered by Mauritania and Morocco before Morocco...",
    "img_url": "data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==",
    "url": "https://nation.africa/kenya/news/africa/western-sahara-issue-threatens-morocco-s-business-deals-4793176&ved=2ahUKEwjp2PLOz4uJAxUu48kDHfy5OLoQxfQBegQIBxAC&usg=AOvVaw3Ia4CCqqIvc0_oR66GvXxv",
    "content_preview": null,
    "content": null
  }
    ]
    ```

---




<!-- ### Tables
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
