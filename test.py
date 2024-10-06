import psycopg2
connection = None
# Establish the database connection
try:
    connection = psycopg2.connect(
        user="starias",
        password="my_password",
        host="127.0.0.1",  # or 'localhost'
        port="5432",
        database="africa_news_db"
    )
    cursor = connection.cursor()

    # SQL query to insert data into the table
    insert_query = """
    INSERT INTO your_table (column1, column2, column3)
    VALUES (%s, %s, %s);
    """

    # Data to insert
    data = ("value1", "value2", "value3")

    # Execute the SQL command
    cursor.execute(insert_query, data)

    # Commit the transaction
    connection.commit()

    # Get the number of inserted rows (optional)
    print(cursor.rowcount, "Record inserted successfully.")

except (Exception, psycopg2.Error) as error:
    print("Error while inserting into PostgreSQL", error)

finally:
    # Close the cursor and connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
