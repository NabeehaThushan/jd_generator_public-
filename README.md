# JD Generator — Public Standalone Tool

Two-pass AI job description generator. Produces specific, filtering JDs — not generic templates.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud (free public link)

1. Push this folder to a GitHub repo (can be public or private)
2. Go to https://share.streamlit.io
3. Click "New app" → connect your GitHub repo
4. Set main file path: `app.py`
5. Deploy → get a public link like `https://yourname-jd-generator.streamlit.app`

## API Key
- Add your OpenAI API key in the sidebar at runtime, OR
- For a deployed app: go to App Settings → Secrets and add:
  ```toml
  OPENAI_API_KEY = "sk-..."
  ```
  Then in app.py replace the text_input with:
  `api_key = st.secrets["OPENAI_API_KEY"]`

## Cost
- gpt-4o-mini: ~$0.001 per JD (recommended for demos)
- gpt-4o: ~$0.02 per JD (higher quality)
