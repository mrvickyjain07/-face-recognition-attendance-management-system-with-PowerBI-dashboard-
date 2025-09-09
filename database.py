import os
import sqlite3
import psycopg2
from urllib.parse import urlparse

def get_db_connection():
    """Get database connection based on environment
    
    In development: Uses SQLite
    In production: Uses PostgreSQL if DATABASE_URL is set
    """
    # Check if we're in production with a DATABASE_URL
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # We're in production, use PostgreSQL
        try:
            # Parse the DATABASE_URL
            result = urlparse(database_url)
            username = result.username
            password = result.password
            database = result.path[1:]
            hostname = result.hostname
            port = result.port
            
            # Connect to PostgreSQL
            conn = psycopg2.connect(
                database=database,
                user=username,
                password=password,
                host=hostname,
                port=port
            )
            
            # Enable autocommit for PostgreSQL
            conn.autocommit = True
            
            return conn
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {str(e)}")
            # Fall back to SQLite if there's an error
            return sqlite3.connect('information.db')
    else:
        # We're in development, use SQLite
        return sqlite3.connect('information.db')

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    
    # Check if we're using PostgreSQL
    if isinstance(conn, psycopg2.extensions.connection):
        # PostgreSQL syntax
        conn.cursor().execute('''
        CREATE TABLE IF NOT EXISTS Attendance (
            id SERIAL PRIMARY KEY,
            NAME TEXT NOT NULL,
            Time TEXT NOT NULL,
            Date TEXT NOT NULL
        )
        ''')
    else:
        # SQLite syntax
        conn.execute('''
        CREATE TABLE IF NOT EXISTS Attendance (
            NAME TEXT NOT NULL,
            Time TEXT NOT NULL,
            Date TEXT NOT NULL
        )
        ''')
    
    # Import existing attendance from CSV if available and table is empty
    cursor = conn.cursor()
    
    # Check if table is empty
    if isinstance(conn, psycopg2.extensions.connection):
        cursor.execute("SELECT COUNT(*) FROM Attendance")
    else:
        cursor.execute("SELECT COUNT(*) FROM Attendance")
        
    count = cursor.fetchone()[0]
    
    if count == 0:
        try:
            import csv
            from datetime import date
            
            # Try to import from attendance.csv
            with open('attendance.csv', 'r') as f:
                reader = csv.reader(f)
                today = date.today()
                
                for row in reader:
                    if row and len(row) >= 2:  # Skip empty lines
                        name, time = row[0].strip(), row[1].strip()
                        
                        if isinstance(conn, psycopg2.extensions.connection):
                            cursor.execute(
                                "INSERT INTO Attendance (NAME, Time, Date) VALUES (%s, %s, %s)",
                                (name, time, today)
                            )
                        else:
                            conn.execute(
                                "INSERT INTO Attendance (NAME, Time, Date) VALUES (?, ?, ?)",
                                (name, time, today)
                            )
            
            if not isinstance(conn, psycopg2.extensions.connection):
                conn.commit()
                
            print("Existing attendance data imported successfully")
        except Exception as e:
            print(f"Error importing existing attendance: {str(e)}")
    
    conn.close()