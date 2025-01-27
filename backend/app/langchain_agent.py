from langchain_community.utilities import SQLDatabase
from transformers import pipeline  # Import Hugging Face pipeline
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

class LangChainAgent:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.db = SQLDatabase.from_uri(db_url)  # Initialize LangChain's SQLDatabase with URL
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")  # Initialize Hugging Face summarizer

    def translate_query(self, natural_query: str) -> str:
        """Translate natural language queries into SQL."""
        if "all products under brand" in natural_query.lower():
            brand = natural_query.split("under brand")[-1].strip()
            return f"SELECT * FROM products WHERE brand = '{brand}'"
        elif "list products" in natural_query.lower():
            category = natural_query.split("list products")[-1].strip()
            return f"SELECT * FROM products WHERE category = '{category}'"
        elif "details of product" in natural_query.lower():
            product_name = natural_query.split("details of product")[-1].strip()
            return f"SELECT * FROM products WHERE name = '{product_name}'"
        elif "which suppliers provide" in natural_query.lower():
            category = natural_query.split("provide")[-1].strip()
            return f"SELECT DISTINCT suppliers.name FROM suppliers JOIN products ON suppliers.id = products.supplier_id WHERE products.category = '{category}'"
        else:
            return natural_query
    def format_query_results(self,results):
        """
        Format the query results into JSON-friendly structures.
        """
        results=eval(results)
        l=[]
        formatted_results = [] 
        for item in results:
            for value in item:
                l.append(value)
            formatted_results.append(l)
        return formatted_results

    def query_database(self, query: str) -> str:
        """Run the query on the database and fetch results."""
        try:
            print(f"Executing SQL Query: {query}")  # Debug log
            results = self.db.run(query)
            print(f"Query Results: {results}")  # Debug log
            format_result=self.format_query_results(results)
            # print(f"Formated Result: {format_result}")
            return format_result
          
        except Exception as e:
            print(f"Database Query Error: {e}")  # Debug log
            return f"Error querying database: {e}"

    def summarize_data(self, data: str) -> str:
        """Summarize the query results using Hugging Face Transformers."""
        try:
            if not data:
                return "No data to summarize."

            # Ensure data length is within the summarizer's limit
            input_length = len(data.split())  # Word count of the input
            max_length = min(50, input_length * 2)  # Max length: no more than twice the input length
            min_length = max(10, input_length // 2)  # Min length: at least half the input length

            # Ensure max_length >= min_length to avoid inconsistencies
            if max_length < min_length:
                max_length = min_length + 5

            result = self.summarizer(data, max_length=max_length, min_length=min_length ,truncate=True)

            # Extract and return the summarized text
            summary = result[0]['summary_text']
            print(f"Summary: {summary}")
            return summary

        except Exception as e:
            return f"Error summarizing data: {e}"

    def get_data_and_summarize(self, natural_query: str) -> dict:
        """Handle the complete flow of translation, querying, and summarizing."""
        try:
            # Step 1: Translate query
            sql_query = self.translate_query(natural_query)
            print(f"Translated SQL Query: {sql_query}")  # Debug log

            # Step 2: Query database
            raw_results = self.query_database(sql_query)
            return raw_results
            # Step 3: Summarize results if any
        except Exception as e:
            return f"Error in get data: {e}"    
