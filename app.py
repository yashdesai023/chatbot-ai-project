import os
from flask import Flask, render_template, request
import google.generativai as genai
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# --- Initialization ---
app = Flask(__name__)
load_dotenv()

# --- Configuration ---
# Load API keys from environment variables for security
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

PINECONE_INDEX_NAME = "upsc-chatbot"  # Your index name
EMBEDDING_MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2' # The embedding model

# --- Global Service Initialization ---
# We initialize the services once when the app starts to avoid reloading models on every request.
print("Initializing services...")
try:
    # Initialize Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX_NAME)
    print("✅ Successfully connected to Pinecone index.")

    # Initialize the embedding model from HuggingFace
    embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    print("✅ Embedding model loaded successfully.")

    # Initialize the Gemini model
    genai.configure(api_key=GOOGLE_API_KEY)
    llm = genai.GenerativeModel('gemini-1.5-flash-latest')
    print("✅ Gemini model loaded successfully.")
    print("\n--- Application is ready ---")

except Exception as e:
    print(f"❌ Error during service initialization: {e}")
    # Set services to None so the app can still run and report the error.
    index = None
    embedding_model = None
    llm = None

# --- RAG Function ---
def get_rag_response(user_query):
    """
    Takes a user query, retrieves context from Pinecone, and generates a response from Gemini.
    """
    if not all([index, embedding_model, llm]):
        return "One or more services failed to initialize. Please check the server logs for errors."

    # 1. Retrieve from Pinecone
    print(f"Creating embedding for query: '{user_query}'")
    query_embedding = embedding_model.encode(user_query).tolist()
    
    print("Querying Pinecone index...")
    query_results = index.query(
        vector=query_embedding,
        top_k=3,  # Retrieve top 3 relevant chunks
        include_metadata=True
    )
    
    context_chunks = [match['metadata'].get('text', '') for match in query_results['matches']]
    context_string = "\n\n---\n\n".join(context_chunks)
    print(f"Retrieved context: {context_string[:300]}...") # Log first 300 chars of context

    # 2. Augment the Prompt for Gemini
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

    # 3. Generate the Response with Gemini
    try:
        print("Generating response with Gemini...")
        response = llm.generate_content(prompt_template)
        return response.text
    except Exception as e:
        print(f"Error during Gemini generation: {e}")
        return f"An error occurred while generating the response: {e}"


# --- Flask Routes ---
@app.route("/")
def index():
    """Render the chat interface."""
    return render_template('chat.html')


@app.route("/get", methods=["POST"])
def chat():
    """Handle the chat message and return the AI's response."""
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
    # Using 0.0.0.0 makes it accessible on your local network
    app.run(host="0.0.0.0", port=8085, debug=True)

