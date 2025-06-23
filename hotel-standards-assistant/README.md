
# Hotel Standards Assistant

A multilingual Streamlit app that allows hotel staff to upload and query brand standards in English, Greek, or Spanish using OpenAI GPT-3.5.

## Features
- ✅ Upload PDF standards
- ✅ Ask questions in English, Greek, or Spanish
- ✅ Persistent PDF storage and auto re-indexing
- ✅ Free deployment via Streamlit Cloud

## How to Deploy

1. Push to GitHub
2. Go to https://streamlit.io/cloud
3. Create a new app and point to `app.py`
4. Add your OpenAI API key to Streamlit Secrets:

```toml
OPENAI_API_KEY = "your-openai-key"
```

## Local Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
