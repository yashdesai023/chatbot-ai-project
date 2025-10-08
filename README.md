# 🧠 AI-Powered UPSC Chatbot using Gemini 2.0 Flash & Pinecone Vector DB

An intelligent Retrieval-Augmented Generation (RAG) chatbot that leverages **Google’s Gemini 2.0 Flash model** and **Pinecone Vector Database** to provide accurate, context-aware answers for UPSC exam preparation.

---

## 🚀 Features

- **RAG-based Contextual Answers:** Retrieves the most relevant information from your Pinecone vector store before generating responses.  
- **Powered by Gemini 2.0 Flash:** Uses Google’s cutting-edge generative AI model for intelligent and concise answers.  
- **Semantic Search with Sentence Transformers:** Converts queries into embeddings using `all-MiniLM-L6-v2`.  
- **Flask Web App:** Lightweight and interactive chat interface built using Flask and HTML templates.  
- **Scalable Vector Store:** Uses Pinecone for efficient similarity search and retrieval.  
- **Environment Secure:** Uses `.env` file for API keys and configuration secrets.  

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **LLM** | Google Gemini 2.0 Flash |
| **Vector Database** | Pinecone |
| **Embedding Model** | Sentence Transformers (`all-MiniLM-L6-v2`) |
| **Framework** | Flask |
| **Frontend** | HTML + CSS (via `templates/chat.html`) |
| **Environment Management** | dotenv |
| **Language** | Python 3.11+ |


## 📂 Project Structure

```

upsc-chatbot/
│
├── templates/
│   └── chat.html                # Frontend chat interface
│
├── app.py                       # Main Flask application
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (excluded from Git)
├── .gitignore                   # Ignored files and folders
└── README.md                    # You are here!

````

---

## ⚙️ Setup & Installation

Follow these steps to set up and run the chatbot locally:

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/upsc-chatbot.git
cd upsc-chatbot
````

### 2️⃣ Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate    # On Windows use: .venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory and add your credentials:

```bash
GOOGLE_API_KEY="your-google-api-key"
PINECONE_API_KEY="your-pinecone-api-key"
```

> ⚠️ Keep your `.env` file private. Do not upload it to GitHub.

### 5️⃣ Run the Application

```bash
python app.py
```

The Flask app will start on:

```
http://127.0.0.1:8080
```

---

## 🧠 How It Works

1. **User Input:** The chatbot receives a query from the user interface.
2. **Embedding Generation:** The query is converted into vector embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
3. **Vector Search:** The embeddings are sent to **Pinecone**, which retrieves the top 3 most relevant context chunks.
4. **Prompt Construction:** The retrieved text chunks are combined into a prompt for Gemini.
5. **Response Generation:** The **Gemini 2.0 Flash** model generates a context-based, accurate response.
6. **Display:** The answer is returned to the Flask front-end and displayed to the user.

---

## 🧰 Example Prompt Flow

**User Query:**

> What are the functions of the Election Commission of India?

**Model Workflow:**

1. Create embeddings → Pinecone search for UPSC-related data.
2. Retrieve top 3 matching contexts.
3. Build RAG prompt → Send to Gemini 2.0 Flash.
4. Return factual answer in human-readable format.

---

## 🔐 Environment Variables

| Variable              | Description                                           |
| --------------------- | ----------------------------------------------------- |
| `GOOGLE_API_KEY`      | API key for Google Gemini                             |
| `PINECONE_API_KEY`    | API key for Pinecone Vector DB                        |
| `PINECONE_INDEX_NAME` | Name of your Pinecone index (default: `upsc-chatbot`) |

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.



## 🧩 Future Improvements

* [ ] Add chat history with context retention
* [ ] Integrate Streamlit or React frontend
* [ ] Add fine-tuned embedding models for domain-specific responses
* [ ] Deploy on Render / Hugging Face Spaces

---



## 👤 About The Author

Hi, I'm **Yash Desai** 👋

**Generative AI & LLM Engineer | Java • Python • Spring Boot | Exploring DevOps & SDET | Building Scalable AI Solutions**

With a strong foundation in Java backend engineering and a growing expertise in Generative AI, I specialize in building intelligent, production-ready applications that merge the robustness of enterprise systems with the innovation of Large Language Models (LLMs).

I thrive on designing solutions that are scalable, impactful, and deployment-ready—bridging backend reliability with AI innovation to deliver real-world value for businesses and communities.

<p align="center">
  <a href="https://www.linkedin.com/in/yash-s-desai-/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
  </a>
  <a href="https://github.com/yashdesai023">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
  <a href="mailto:desaisyash1000@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail"/>
  </a>
</p>


>⭐ If you like this project, don’t forget to star the repository!
