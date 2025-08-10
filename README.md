## Thrones Archive RAG

Dark medieval fantasy, Game of Thrones / A Song of Ice and Fire–themed Retrieval-Augmented Generation (RAG) web app. Uses Chroma for vector search and OpenAI for generation. Includes an immersive, gold-on-black UI and multi-turn chat memory.

### Features
- RAG pipeline: Chroma vector DB + OpenAI Embeddings (`text-embedding-3-small`)
- Multi-turn chat with session-based memory
- Cinematic GOT UI (Cinzel for headings, Inter for body)
- Semi-transparent dark overlays for readability
- Custom background image: `/static/img/got-bg.png` (replaceable)
- Auto-builds the vector DB on first run if missing

### Tech Stack
- Flask, LangChain (Chroma, OpenAI)
- OpenAI API (chat + embeddings)
- ChromaDB
- python-dotenv, gunicorn (for deployment)

### Setup
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Create a `.env` file:
```
OPENAI_API_KEY=sk-proj-XXXXXXXX
# Optional
# APP_SECRET_KEY=some_long_random_string
```

Optional (DB can be built automatically on first run):
```bash
python build_db.py
```

Run locally:
```bash
python app.py
# http://localhost:5000
```

### Usage
- Ask questions; answers appear in the “Cevap” panel.
- “Sohbet” shows multi-turn chat history.
- Use “Geçmişi Temizle” to reset the conversation.

### Project Structure
```
RAG-GOT/
  app.py
  build_db.py
  query_db.py
  generate.py
  templates/
    index.html
  static/
    css/styles.css
    img/got-bg.png     # background (add your image)
  books/               # source markdown data
  chroma/              # vector DB (generated)
  requirements.txt
  .env                 # local env vars
```

### Deploy (Render – recommended)
- Build Command:
```
pip install --upgrade pip && pip install -r requirements.txt
```
- Start Command:
```
gunicorn "app:create_app()" --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120
```
- Environment Variables: `OPENAI_API_KEY`

### Customization
- Replace `/static/img/got-bg.png` with your own (webp/png recommended).
- Adjust colors, glow, panel opacity, and fonts in `static/css/styles.css`.

### Notes
- Free hosting may sleep; app will cold-start.
- `chroma/` and `.env` are ignored via `.gitignore`.