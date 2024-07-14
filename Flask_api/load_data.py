import pandas as pd
import mysql.connector
import os
import re

def clean_string(s):
    """Remove non-printable and non-ASCII characters from strings."""
    cleaned = re.sub(r'[^\x00-\x7F]+', ' ', s)  # Remove non-ASCII characters
    cleaned = cleaned.replace(u'\ufeff', '').replace(u'\u202F', '').replace(u'\u200B', '')  # Remove specific problematic characters
    return cleaned

def get_db_connection():
    """Create or connect to a MySQL database with error handling."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'db'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'password'),
            database=os.getenv('MYSQL_DB', 'Zomato_SQL'),
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database():
    """Create the database if it doesn't exist."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'db'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'password'),
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('MYSQL_DB', 'Zomato_SQL')} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error creating MySQL database: {err}")

def load_csv_to_db(csv_path):
    """Load CSV data to the MySQL database."""
    create_database()
    conn = get_db_connection()
    if conn is None:
        return
    cursor = conn.cursor()

    # Ensure the table supports utf8mb4
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS zomato_final_SQL_docker (
        Restaurant_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        Location VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        Average_rating FLOAT,
        delivery_vs_dine_in_preference TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        Popular_cuisines VARCHAR(600) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        Open_day VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        Closed_day VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        Honest_review TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        overall_review TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        Links TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        operational_hours TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
    );
    """)

    df = pd.read_csv(csv_path, encoding='utf-8')
    df = df.applymap(lambda x: clean_string(x) if isinstance(x, str) else x)
    data_tuples = [tuple(x) for x in df.to_numpy()]

    insert_query = """
    INSERT INTO zomato_final_SQL_docker (Restaurant_name, Location, Average_rating, delivery_vs_dine_in_preference,
                                         Popular_cuisines, Open_day, Closed_day, Honest_review, overall_review,
                                         Links, operational_hours) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor.executemany(insert_query, data_tuples)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_csv_to_db('/app/Zomato_final_dockers.csv')
