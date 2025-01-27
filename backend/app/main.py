from flask import Flask, request, jsonify
from app.langchain_agent import LangChainAgent
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

# Use PostgreSQL database URI instead of SQLite
DATABASE_URL = os.getenv("DATABASE_URL")
agent = LangChainAgent(db_url=DATABASE_URL)

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    user_query = data.get("query")

    try:
        # Use translate_query to handle the user query
        raw_results = agent.get_data_and_summarize(user_query)  # This calls the translate_query method
        # if raw_results and not raw_results.startswith("Error"):
        #         summary = agent.summarize_data(raw_results)
        # else:
        #         summary = "No data to summarize."

        return jsonify({
                "raw_results": raw_results,
                # "summary": summary,
            })
    except Exception as e:
        return jsonify({
                "error": str(e),
                "raw_results": "",
                # "summary": "Error occurred while processing your request.",
            }),500

    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
