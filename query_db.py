import argparse
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from generate import generate_response
from dotenv import load_dotenv

CHROMA_PATH = "chroma"

def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Veritabanında arama yap.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    context_text = ""  # Bağlamı başlangıçta boş olarak ayarla.
    # Eğer iyi sonuçlar varsa, bağlamı oluştur.
    if len(results) > 0 and results[0][1] > 0.7:
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Her zaman (boş bağlamla bile olsa) yanıt üreticiyi çağır.
    final_response = generate_response(context_text, query_text)
    print(final_response)


if __name__ == "__main__":
    main()