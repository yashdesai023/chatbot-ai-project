import os
from flask import Flask, render_template, request
import google.generativeai as genai
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# --- Initialization ---
app = Flask(__name__)
load_dotenv()

# --- Configuration ---
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_INDEX_NAME = "upsc-chatbot"
EMBEDDING_MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'

# --- Global Service Initialization ---
print("Initializing services...")
try:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    # The Pinecone connection object is stored in 'pinecone_index'
    pinecone_index = pc.Index(PINECONE_INDEX_NAME)
    print("✅ Successfully connected to Pinecone index.")

    embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    print("✅ Embedding model loaded successfully.")

    genai.configure(api_key=GOOGLE_API_KEY)
    llm = genai.GenerativeModel('gemini-2.0-flash')
    print("✅ Gemini model loaded successfully.")
    print("\n--- Application is ready ---")

except Exception as e:
    print(f"❌ Error during service initialization: {e}")
    pinecone_index = None
    embedding_model = None
    llm = None

# --- RAG Function ---
def get_rag_response(user_query):
    if not all([pinecone_index, embedding_model, llm]):
        return "One or more services failed to initialize. Please check the server logs for errors."

    print(f"Creating embedding for query: '{user_query}'")
    query_embedding = embedding_model.encode(user_query).tolist()
    
    print("Querying Pinecone index...")
    # Use the correctly named variable 'pinecone_index'
    query_results = pinecone_index.query(
        vector=query_embedding,
        top_k=3,
        include_metadata=True
    )
    
    context_chunks = [match['metadata'].get('text', '') for match in query_results['matches']]
    context_string = "\n\n---\n\n".join(context_chunks)
    print(f"Retrieved context: {context_string[:300]}...")

    prompt_template = f"""
    You are a helpful assistant for the UPSC exam. 
    Answer the following question based ONLY on the context provided below.
    If the context does not contain the answer, state that you don't have enough information. Do not make up answers.

    CONTEXT:
    {context_string}

    QUESTION:
    {user_query}

    ANSWER:
    """

    try:
        print("Generating response with Gemini...")
        response = llm.generate_content(prompt_template)
        return response.text
    except Exception as e:
        print(f"Error during Gemini generation: {e}")
        return f"An error occurred while generating the response: {e}"

# --- Flask Routes ---
@app.route("/")
def home(): # <<< RENAMED THIS FUNCTION
    """Render the chat interface."""
    return render_template('chat.html')


@app.route("/get", methods=["POST"])
def chat():
    try:
        user_message = request.form["msg"]
        print(f"Received User Input: {user_message}")
        response = get_rag_response(user_message)
        print(f"Sending Response: {response}")
        return response
    except Exception as e:
        print(f"Error in /get route: {e}")
        return "An internal server error occurred. Please check the logs.", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

