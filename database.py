import sqlite3
from typing import List, Dict, Tuple, Union

def initialize_database():
    """Initialize the database with default STUDENT table if it doesn't exist"""
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    
    # Check if STUDENT table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='STUDENT'")
    if not cursor.fetchone():
        cursor.execute("""
        CREATE TABLE STUDENT (
            NAME    VARCHAR(25),
            COURSE   VARCHAR(25),
            SECTION VARCHAR(25),
            MARKS   INT
        );
        """)
        # Insert sample data
        cursor.executemany(
            "INSERT INTO STUDENT (NAME, COURSE, SECTION, MARKS) VALUES (?, ?, ?, ?)",
            [
                ('Student1', 'Data Science', 'A', 90),
                ('Student2', 'Data Science', 'B', 100),
                ('Student3', 'Data Science', 'A', 86),
                ('Student4', 'DEVOPS', 'A', 50),
                ('Student5', 'DEVOPS', 'A', 35)
            ]
        )
        conn.commit()
    conn.close()

def create_custom_table(table_name: str, columns: List[Dict[str, str]]) -> Tuple[bool, str]:
    """
    Create a new table with custom columns
    Args:
        table_name: Name of the table to create
        columns: List of dictionaries with 'name' and 'type' keys
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        
        # Generate column definitions
        column_defs = ", ".join([f"{col['name']} {col['type']}" for col in columns])
        create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})"
        
        cursor.execute(create_query)
        conn.commit()
        return True, f"Table '{table_name}' created successfully!"
    except Exception as e:
        return False, f"Error creating table: {str(e)}"
    finally:
        if conn:
            conn.close()

def get_table_info() -> str:
    """Get information about all tables in the database"""
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    table_info = []
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_info = [f"{col[1]} ({col[2]})" for col in columns]
        table_info.append(f"- {table_name}: {', '.join(column_info)}")
    
    conn.close()
    return "\n".join(table_info)

def execute_query(sql_query: str) -> Tuple[List[str], List[Tuple]]:
    """
    Execute a SQL query and return results
    Args:
        sql_query: SQL query to execute
    Returns:
        Tuple of (column_names, rows)
    """
    with sqlite3.connect("student.db") as conn:
        cursor = conn.execute(sql_query)
        columns = [description[0] for description in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
    return columns, rows

def get_all_table_names() -> List[str]:
    """Get list of all table names in the database"""
    with sqlite3.connect("student.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [table[0] for table in cursor.fetchall()]

def get_table_columns(table_name: str) -> List[Dict[str, str]]:
    """Get column names and types for a specific table"""
    with sqlite3.connect("student.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        return [{"name": col[1], "type": col[2]} for col in cursor.fetchall()]

def insert_data(table_name: str, data: Dict[str, Union[str, int, float]]) -> Tuple[bool, str]:
    """
    Insert data into a table
    Args:
        table_name: Name of the table
        data: Dictionary with column names as keys and values to insert
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        cursor.execute(query, tuple(data.values()))
        conn.commit()
        return True, f"Data inserted successfully into {table_name}"
    except Exception as e:
        return False, f"Error inserting data: {str(e)}"
    finally:
        if conn:
            conn.close()