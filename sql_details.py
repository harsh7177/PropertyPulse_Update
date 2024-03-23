import mysql.connector
import pandas as pd
import streamlit as st

def conn_detail():
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
        host="cities.c58gyweuqusa.us-east-1.rds.amazonaws.com",
        user="admin",
        password="harshkandari",
        database="cities"
    )
    
        cursor = conn.cursor()

        return cursor, conn

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None

def insert_detail_table(df, city):
    table_name = city.lower() 
    cursor, connection = conn_detail()

    try:
        for index, row in df.iterrows():
            sql = f"INSERT INTO `{table_name}` (BHK, Status, Size_Sq_ft, Price_Sqft, Price, bath, area, project) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            # Convert each value to the appropriate type (e.g., str to int)
            values = (
                int(row['BHK']) if not pd.isna(row['BHK']) else None,
                str(row['Status']),
                float(row['Size(Sq/ft)']) if not pd.isna(row['Size(Sq/ft)']) else None,
                int(row['Price/Sqft']) if not pd.isna(row['Price/Sqft']) else None,
                float(row['Price']) if not pd.isna(row['Price']) else None,
                int(row['bath']) if not pd.isna(row['bath']) else None,
                str(row['area']),
                str(row['project'])
            )
            print("Executing SQL query:", sql)  # Print SQL query for debugging
            print("Values:", values)
            cursor.execute(sql, values)
        
        connection.commit()

    except mysql.connector.Error as error:
        print(f"Error inserting data: {error}")

    finally:
        cursor.close()
        connection.close()

def create_detail(suburb):
    cursor, con = conn_detail()
    table_name = suburb
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        id INT AUTO_INCREMENT PRIMARY KEY,
        BHK INT,
        Status VARCHAR(255),
        Size_Sq_ft FLOAT,
        Price_Sqft INT,
        Price FLOAT,
        bath INT,
        area VARCHAR(255),
        project VARCHAR(255)
    )
    """

    cursor.execute(create_table_query)
    con.commit()
    cursor.close()
    con.close()

def detail_tables():
    cursor,con=conn_detail()
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
@st.cache_data
def get_detail_data(table_name):
    cursor,con=conn_detail()
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
