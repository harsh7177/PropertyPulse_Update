import mysql.connector
import pandas as pd
import streamlit as st

def conn_detail():
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
        host=st.secrets['cities_details_host'],
        user="admin",
        password=st.secrets['cities_password'],
        database=st.secrets['cities_database']
    )
    
        cursor = conn.cursor()

        return cursor, conn

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None

def insert_detail_table(df, city):
    table_name = city.lower() 
    cursor, connection = conn_detail()


    for index, row in df.iterrows():
            sql = f"INSERT INTO `{table_name}` (BHK, Status, Size_Sq_ft, Price_Sqft, Price, bath, area, project) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            try:
                values = (
                    int(row['BHK']) ,
                    str(row['Status']),
                    float(row['Size_Sq_ft']) ,
                    int(row['Price_Sqft']),
                    float(row['Price']),
                    int(row['bath']) ,
                    str(row['area']),
                    str(row['project'])
                )
            except:
                continue
            cursor.execute(sql, values)
        
            connection.commit()
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
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        table = [row[0] for row in rows]
        return table
    finally:
        cursor.close()
        con.close()

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
