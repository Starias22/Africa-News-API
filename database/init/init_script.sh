# Create a new PostgreSQL user 'starias' with the specified password
psql -U postgres -c "CREATE USER starias WITH PASSWORD 'my_password';"

# Create a new database 'africa_news_db' and assign 'starias' as the owner
psql -U postgres -c "CREATE DATABASE africa_news_db WITH OWNER starias;"

# Grant all privileges on the 'africa_news_db' to the user 'starias'
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE africa_news_db TO starias;"

# Change directory to where the initialization SQL script is located and run it to create tables and insert initial data
cd docker-entrypoint-initdb.d/utils/
psql -U starias -d "africa_news_db" -c "\i init_script.sql"

# Create a new PostgreSQL user 'airflow' with the password 'airflow'
psql -U postgres -c "CREATE USER airflow WITH PASSWORD 'airflow';"

# Create a new database 'airflow' and assign 'starias' as the owner (since 'airflow' will be a user interacting with the DB)
psql -U postgres -c "CREATE DATABASE airflow WITH OWNER starias;"

# Grant all privileges on the 'airflow' database to the 'airflow' user for full access
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;"
