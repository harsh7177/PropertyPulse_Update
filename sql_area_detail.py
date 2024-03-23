
import mysql.connector
import pandas as pd
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
            sql = f"INSERT INTO {table_name} (Area, ProjectC, city,page_num) VALUES (%s, %s, %s,%s)"
            cursor.execute(sql, (row['Area'], row['ProjectC'], row['city'],row['page_num']))
        
        connection.commit()

    except mysql.connector.Error as error:
        print(f"Error inserting data: {error}")

    finally:
        cursor.close()
        connection.close()

def create_detail(city):
    cursor, con = conn_detail()
    table_name = city.lower() + '_href'
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Area VARCHAR(255),
        ProjectC INT,
        city VARCHAR(255),
        page_num INT
    )
    """

    cursor.execute(create_table_query)
    con.commit()
    cursor.close()
    con.close()