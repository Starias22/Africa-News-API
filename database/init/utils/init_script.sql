-- psql -U starias -d africa_news_db
-- Create tables.
-- \include create_tables.sql
\include create_tables.sql

-- Load extractors
\COPY extractor(extractor_name, extractor_url, extractor_description ) FROM 'extractor.csv' DELIMITER ',' CSV HEADER;

-- Load languages
\COPY language(lang_name, lang_code) FROM 'language.csv' DELIMITER ',' CSV HEADER;

-- Load countries
\COPY country(country_name, country_code) FROM 'country.csv' DELIMITER ',' CSV HEADER;

-- Load categories
\COPY category(category_name) FROM 'category.csv' DELIMITER ',' CSV HEADER;

