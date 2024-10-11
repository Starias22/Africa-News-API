# Create user starias
psql -U postgres -c "CREATE USER starias WITH PASSWORD 'my_password';"

# Create africa_news_db
psql -U postgres -c "CREATE DATABASE africa_news_db WITH OWNER starias;"

# Set starias the owner of africa_news_db
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE africa_news_db TO starias;"

# Run the script to create database tables and insert initial data
cd docker-entrypoint-initdb.d/utils/
psql -U starias -d "africa_news_db" -c "\i init_script.sql"

