# Groq Chatbot

A conversational chatbot built with Streamlit, LangChain, and Groq.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and set your Groq API key.
4. Start the app:

   ```powershell
   streamlit run app.py
   ```

## Deploy on Streamlit Community Cloud

Deploy this repository with `app.py` as the app entry point. In the app's **Settings → Secrets**, add:

```toml
GROQ_API_KEY = "your_groq_api_key"
GROQ_MODEL = "openai/gpt-oss-120b"
```

Keep API keys in Streamlit secrets or your local `.env`; never commit them to Git.
