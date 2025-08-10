import os
from flask import Flask, request, jsonify, render_template, session
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from generate import generate_response
from build_db import generate_data_store

CHROMA_PATH = "chroma"


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.environ.get("APP_SECRET_KEY", os.urandom(24))

    # OPENAI_API_KEY kontrolü
    load_dotenv()
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise RuntimeError("OPENAI_API_KEY ortam değişkeni bulunamadı. Lütfen anahtarı ayarlayın ve uygulamayı tekrar başlatın.")

    # Veri deposu yoksa oluştur
    if not os.path.exists(CHROMA_PATH):
        generate_data_store()

    # Embedding ve vektör veritabanı (uygulama ömrü boyunca tek kez)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=openai_api_key)
    vector_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    @app.route("/", methods=["GET"]) 
    def index():
        return render_template("index.html")

    @app.route("/ask", methods=["POST"]) 
    def ask():
        payload = request.get_json(silent=True) or {}
        query_text = (payload.get("query") or "").strip()
        if not query_text:
            return jsonify({"error": "'query' alanı zorunludur."}), 400

        results = vector_db.similarity_search_with_relevance_scores(query_text, k=3)
        context_text = ""
        if len(results) > 0 and results[0][1] > 0.7:
            context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

        # Konuşma geçmişini session'da tut
        history = session.get("chat_history", [])
        history = [
            {"role": msg.get("role", "user"), "content": str(msg.get("content", ""))[:4000]}
            for msg in history
        ][-8:]

        answer_text = generate_response(context_text, query_text, history=history)

        # Geçmişi güncelle (user + assistant turu)
        history.append({"role": "user", "content": query_text})
        history.append({"role": "assistant", "content": answer_text})
        session["chat_history"] = history

        return jsonify({"answer": answer_text})

    @app.route("/reset", methods=["POST"]) 
    def reset_chat():
        session.pop("chat_history", None)
        return jsonify({"ok": True})

    @app.route("/history", methods=["GET"]) 
    def history():
        return jsonify({"history": session.get("chat_history", [])})

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, debug=True)
