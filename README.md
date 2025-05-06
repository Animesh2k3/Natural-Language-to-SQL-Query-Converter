<p align="center">
  <img src="https://raw.githubusercontent.com/Animesh2k3/natural-language-to-sql-query-converter/main/assets/logo.png" width="120" alt="Logo" />
</p>

<h1 align="center">Natural Language to SQL Query Converter</h1>

<p align="center">
  💬 Convert everyday language into executable SQL queries using AI<br>
  Built with FastAPI, Streamlit, and LLMs like OpenAI & Groq.
</p>

<p align="center">
  <a href="https://github.com/Animesh2k3/natural-language-to-sql-query-converter">
    <img alt="Stars" src="https://img.shields.io/github/stars/Animesh2k3/natural-language-to-sql-query-converter?style=social" />
  </a>
  <a href="https://github.com/Animesh2k3/natural-language-to-sql-query-converter">
    <img alt="Forks" src="https://img.shields.io/github/forks/Animesh2k3/natural-language-to-sql-query-converter?style=social" />
  </a>
  <a href="https://github.com/Animesh2k3/natural-language-to-sql-query-converter/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/Animesh2k3/natural-language-to-sql-query-converter?color=blue" />
  </a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.9+-blue?logo=python" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-💨-green?logo=fastapi" />
</p>

# 🧠🔄 Natural Language to SQL Query Converter

A simple and effective AI-powered tool that converts plain English queries into executable SQL statements. Ideal for data analysts, developers, and even non-technical users who want to interact with databases without writing SQL manually.

---

## 🚀 Demo

> **"Show me all orders placed in January"** → `SELECT * FROM orders WHERE order_date BETWEEN '2023-01-01' AND '2023-01-31';`

---

## ✨ Features

- 💬 **Natural Language Input** — Just type your question in plain English.
- 🧠 **AI-Powered SQL Conversion** — Uses large language models (LLMs) to generate accurate SQL queries.
- 🧩 **Schema Awareness** — (Optional) Provide a table schema or metadata to guide the model.
- 📦 **Lightweight Backend** — Built with FastAPI.
- 🖥️ **Simple Frontend** — Streamlit or web-based UI for instant testing.
- ✅ **Great for Education & Prototyping** — Help students, teams, and users learn and query faster.

---

## 🛠️ Tech Stack

- Python 3.x
- FastAPI (Backend API)
- Streamlit / HTML / JS (Frontend)
- OpenAI / Groq (LLM-based NLP to SQL conversion)
- Optional: SQLite / PostgreSQL / MySQL (For testing)

---

## 📂 Project Structure

```

.
├── backend.py          # FastAPI backend for handling requests
├── frontend.py         # Streamlit or UI interface
├── model\_utils.py      # (Optional) LLM integration logic
├── schema\_example.json # (Optional) Table schema for better query accuracy
├── requirements.txt    # Python dependencies
└── README.md           # You're here!

````

---

## ⚙️ Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/Animesh2k3/natural-language-to-sql-query-converter.git
cd natural-language-to-sql-query-converter
````

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set your API Key**
   Create a `.env` file and add your OpenAI or Groq API key:

```
OPENAI_API_KEY=your_openai_key_here
```

4. **Run the backend**

```bash
uvicorn backend:app --reload --port 8000
```

5. **Run the frontend**

```bash
streamlit run frontend.py
```

---

## 🔒 Example Usage

1. Input:
   `Find all users who signed up in March 2024`

2. Output:

   ```sql
   SELECT * FROM users WHERE signup_date BETWEEN '2024-03-01' AND '2024-03-31';
   ```

---

## 🧠 How It Works

The app sends your natural language input, along with any optional schema context, to a language model API. The model returns a syntactically valid SQL query tailored to your request. You can then copy-paste or execute this query on your own DB.

---

## 🛡️ Disclaimer

* Always **review generated SQL queries** before running them on live databases.
* This tool is meant for **assisted query generation**, not as a substitute for validation or secure DB access controls.

---

## 📄 License

MIT License — feel free to use, modify, and contribute.

---

## 🙌 Acknowledgements

* [OpenAI](https://openai.com/)
* [FastAPI](https://fastapi.tiangolo.com/)
* \[LangChain / LangGraph] (if used)

---

## 🤝 Contributing

Contributions, suggestions, and feedback are welcome! Please open an issue or submit a PR.

```


```
