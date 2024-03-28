import mysql.connector
import pandas as pd
import streamlit as st

def conn_href():
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
        host=st.secrets['host_href'],
        user=st.secrets['user_href'],
        password=st.secrets['password_href'],
        database=st.secrets['database_href']
    )
    
        cursor = conn.cursor()

        return cursor, conn

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None
def insert_href_table(df, city):
    table_name = city + '_href'
    cursor, connection = conn_href()  # Assuming conn_href() returns cursor and connection objects

    try:
        # Iterate over rows in the DataFrame and insert into the MySQL table
        for index, row in df.iterrows():
            sql = f"INSERT INTO {table_name} (Area, ProjectC, href,city) VALUES (%s, %s, %s,%s)"
            # Replace 'column1', 'column2', 'column3' with actual column names in your table
            cursor.execute(sql, (row['Area'], row['ProjectC'], row['href'],row['city']))
        
        # Commit the transaction
        connection.commit()

    except mysql.connector.Error as error:
        print(f"Error inserting data: {error}")

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
    
def create_href(city):
    cursor,con=conn_href()
    table_name=city+'_href'
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Area VARCHAR(255),
        ProjectC INT,
        href VARCHAR(255),
        city VARCHAR(255)
    )
    """

    # Execute the SQL query
    cursor.execute(create_table_query)

    # Commit the transaction
    con.commit()

    # Close the cursor and connection
    cursor.close()
    con.close()
def href_tables():
    cursor,con=conn_href()
    try:
        sql_query = "SHOW TABLES"

        # Execute the SQL query
        cursor.execute(sql_query)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Extract table names from the result set
        table = [row[0] for row in rows]
        return table

    finally:
        cursor.close()
        con.close()

def get_href_data(table_name):
    cursor,con=conn_href()
    try:
        sql_query = f"Select * from {table_name}"

        # Execute the SQL query
        cursor.execute(sql_query)

        # Fetch all rows from the result set
        rows = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]
        # Extract table names from the result set
        df = pd.DataFrame(rows, columns=column_names)
        return df

    finally:
        cursor.close()
        con.close()
