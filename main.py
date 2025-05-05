import os
import sqlite3
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# ✅ Core logic to get SQL from NL
def get_sql_query(user_query):
    groq_sys_prompt = ChatPromptTemplate.from_template("""
        You are an expert in converting English questions to SQL query!
        The SQL database has the name STUDENT and has the following columns - NAME, COURSE, 
        SECTION and MARKS. For example, 
        Example 1 - How many entries of records are present?, 
            the SQL command will be something like this SELECT COUNT(*) FROM STUDENT;
        Example 2 - Tell me all the students studying in Data Science COURSE?, 
            the SQL command will be something like this SELECT * FROM STUDENT 
            where COURSE="Data Science"; 
        also the sql code should not have ``` in beginning or end and sql word in output.
        Now convert the following question in English to a valid SQL Query: {user_query}. 
        No preamble, only valid SQL please
    """)

    model = "llama3-8b-8192"
    llm = ChatGroq(
        groq_api_key=os.environ.get("GROQ_API_KEY"),
        model_name=model
    )

    chain = groq_sys_prompt | llm | StrOutputParser()
    response = chain.invoke({"user_query": user_query})
    return response

# ✅ SQL execution and result with columns
def return_sql_response(sql_query):
    database = "student.db"
    with sqlite3.connect(database) as conn:
        cursor = conn.execute(sql_query)
        rows = cursor.fetchall()  # Get data rows
    return rows

# ✅ Create a new custom table
def create_custom_table(table_name, columns):
    database = "student.db"
    column_definitions = ", ".join([f"{col[0]} {col[1]}" for col in columns])
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions});"
    
    with sqlite3.connect(database) as conn:
        conn.execute(create_table_query)
    return f"Table '{table_name}' created successfully."

# ✅ Insert data into a custom table
def insert_into_custom_table(table_name, data):
    database = "student.db"
    placeholders = ", ".join(["?" for _ in data[0]])
    insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
    
    with sqlite3.connect(database) as conn:
        conn.executemany(insert_query, data)
    return f"{len(data)} rows inserted into '{table_name}'."

# ✅ Streamlit UI for creating a table and inserting data
def main():
    st.set_page_config(page_title="Text To SQL")
    st.header("Talk to your Database!")

    # Query section for SQL from user input
    user_query = st.text_input("Input your query:")
    submit_query = st.button("Enter Query")
    
    if submit_query:
        sql_query = get_sql_query(user_query)
        st.subheader("Generated SQL Query:")
        st.code(sql_query, language="sql")

        try:
            rows = return_sql_response(sql_query)
            if rows:
                st.subheader("Query Results:")
                for row in rows:
                    st.write(row)  # Display each row as plain text
            else:
                st.info("No results found for this query.")
        except Exception as e:
            st.error(f"Error running SQL: {e}")

    # Section to create and customize new tables
    st.subheader("Create a New Custom Table")

    table_name = st.text_input("Enter table name:")
    columns_input = st.text_area("Enter columns and data types (e.g., 'name TEXT, age INTEGER'):")

    if st.button("Create Table"):
        if table_name and columns_input:
            columns = [col.strip().split() for col in columns_input.split(",")]
            result = create_custom_table(table_name, columns)
            st.success(result)
        else:
            st.error("Please provide a table name and columns.")

    # Section to insert data into custom table
    st.subheader("Insert Data into Table")

    table_to_insert = st.text_input("Enter the table name to insert data into:")
    data_input = st.text_area("Enter data to insert (e.g., 'Alice, Data Science, A, 85'):")

    if st.button("Insert Data"):
        if table_to_insert and data_input:
            data = [tuple(item.split(", ")) for item in data_input.split("\n")]
            result = insert_into_custom_table(table_to_insert, data)
            st.success(result)
        else:
            st.error("Please provide a table name and data.")

if __name__ == '__main__':
    main()
