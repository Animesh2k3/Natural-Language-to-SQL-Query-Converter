import os
import streamlit as st
import pandas as pd
from database import (
    initialize_database,
    create_custom_table,
    get_table_info,
    execute_query,
    get_all_table_names,
    get_table_columns,
    insert_data
)
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

def get_sql_query(user_query: str, table_info: str = None) -> str:
    """
    Convert natural language to SQL using Groq
    Args:
        user_query: Natural language query
        table_info: Information about database tables
    Returns:
        SQL query string
    """
    template = """
    You are an expert in converting English questions to SQL query!
    The available tables are:
    {table_info}
    
    For example:
    Example 1 - How many entries of records are present in STUDENT?
        SQL: SELECT COUNT(*) FROM STUDENT;
    Example 2 - Tell me all the students studying in Data Science COURSE?
        SQL: SELECT * FROM STUDENT where COURSE="Data Science";
    
    The SQL code should not have ``` in beginning or end and sql word in output.
    Now convert the following question to a valid SQL Query: {user_query}.
    No preamble, only valid SQL please
    """
    
    if table_info is None:
        table_info = get_table_info()
    
    groq_sys_prompt = ChatPromptTemplate.from_template(template)
    
    llm = ChatGroq(
        groq_api_key=os.environ.get("GROQ_API_KEY"),
        model_name="llama3-8b-8192"
    )

    chain = groq_sys_prompt | llm | StrOutputParser()
    response = chain.invoke({"user_query": user_query, "table_info": table_info})
    return response.strip()

def show_table_creation_form():
    """Display form for creating new tables"""
    with st.expander("➕ Create New Table"):
        table_name = st.text_input("Table Name")
        num_columns = st.number_input("Number of Columns", min_value=1, max_value=20, value=3)
        
        columns = []
        for i in range(num_columns):
            col1, col2 = st.columns(2)
            with col1:
                col_name = st.text_input(f"Column {i+1} Name", key=f"col_name_{i}")
            with col2:
                col_type = st.selectbox(
                    f"Column {i+1} Type",
                    ["INTEGER", "TEXT", "REAL", "NUMERIC", "BLOB"],
                    key=f"col_type_{i}"
                )
            columns.append({"name": col_name, "type": col_type})
        
        if st.button("Create Table"):
            if table_name and all(col["name"] for col in columns):
                success, message = create_custom_table(table_name, columns)
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.warning("Please provide a table name and all column names")

def show_data_insertion_form():
    """Display form for inserting data into tables"""
    with st.expander("📝 Insert Data"):
        table_names = get_all_table_names()
        if not table_names:
            st.warning("No tables available. Create a table first.")
            return
            
        selected_table = st.selectbox("Select Table", table_names)
        columns_info = get_table_columns(selected_table)
        
        data = {}
        for col in columns_info:
            col_name = col["name"]
            col_type = col["type"].upper()
            
            if col_type in ["INTEGER", "REAL", "NUMERIC"]:
                data[col_name] = st.number_input(col_name, key=f"input_{selected_table}_{col_name}")
            else:  # TEXT, BLOB, etc.
                data[col_name] = st.text_input(col_name, key=f"input_{selected_table}_{col_name}")
        
        if st.button("Insert Data"):
            if all(value != "" for value in data.values()):
                success, message = insert_data(selected_table, data)
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.warning("Please fill all fields")

def main():
    """Main Streamlit application"""
    st.set_page_config(page_title="Text To SQL with Custom Tables", layout="wide")
    st.title("📊 Database Explorer with Natural Language")
    
    # Initialize database
    initialize_database()
    
    # Sidebar for table management
    with st.sidebar:
        st.header("📂 Table Management")
        show_table_creation_form()
        show_data_insertion_form()
        
        with st.expander("🔍 View Existing Tables"):
            table_info = get_table_info()
            if table_info:
                st.text(table_info)
            else:
                st.info("No tables found in the database")
    
    # Main content area
    tab1, tab2 = st.tabs(["🔍 Query Database", "📝 Direct SQL"])
    
    with tab1:
        st.header("Natural Language to SQL")
        user_query = st.text_input("Ask a question about your data:")
        
        if st.button("Generate SQL") and user_query:
            table_info = get_table_info()
            sql_query = get_sql_query(user_query, table_info)
            
            st.subheader("Generated SQL Query:")
            st.code(sql_query, language="sql")
            
            try:
                columns, rows = execute_query(sql_query)
                if rows:
                    df = pd.DataFrame(rows, columns=columns)
                    st.subheader("Query Results:")
                    st.dataframe(df)
                else:
                    st.info("No results found for this query.")
            except Exception as e:
                st.error(f"Error executing query: {str(e)}")
    
    with tab2:
        st.header("Execute Direct SQL Query")
        sql_query = st.text_area("Enter SQL Query:")
        
        if st.button("Execute SQL"):
            try:
                columns, rows = execute_query(sql_query)
                if rows:
                    df = pd.DataFrame(rows, columns=columns)
                    st.subheader("Query Results:")
                    st.dataframe(df)
                else:
                    st.info("Query executed successfully but returned no results.")
            except Exception as e:
                st.error(f"Error executing query: {str(e)}")

if __name__ == '__main__':
    main()