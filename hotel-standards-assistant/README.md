
# Hotel Standards Assistant (GPT-Only Translation)

This version removes Google Translate and uses GPT-3.5 for translation (Greek, Spanish, English).

## Features
- Upload & store hotel standards PDF
- Query in English, Greek, or Spanish
- GPT-3.5 used for both Q&A and translation
- Persistent PDF storage and reindexing
- Ready for Streamlit Cloud

## Deploy Instructions
1. Push to GitHub
2. Go to https://streamlit.io/cloud
3. Set repo and main file = app.py
4. Add your OpenAI API Key in Secrets:

```toml
OPENAI_API_KEY = "your-key"
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
