from books_data import BOOKS
import chromadb
import pandas as pd
from chromadb.utils import embedding_functions

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.Client()
collection_name = "books_collection"
collection = None

def create_collection():
    global collection
    try:
        collection = client.create_collection(
            name=collection_name,
            embedding_function=ef,
            metadata={"hnsw:space": "cosine", "description": "A collection for storing employee data"}
        )
        print(f"Collection created: {collection.name}")

        book_documents = []
        for book in BOOKS:
            document = f"{book['title']} by {book['author']} published in {book['year']}. "
            document += f"Pages: {book['pages']}. Rating: {book['rating']}. "
            document += f"Genre: {book['genre']}. Language: {book['language']}. "
            document += f"Award winner: {book['award_winner']}."
            document += f"Description: {book['description']}."
            book_documents.append(document)

        collection.add(
            documents=book_documents,
            metadatas=[{
                "author": book["author"],
                "title": book["title"],
                "year": book["year"],
                "pages": book["pages"],
                "rating": book["rating"],
                "genre": book["genre"],
                "language": book["language"],
                "award_winner": book["award_winner"],
                "description": book["description"]
            } for book in BOOKS],
            ids=[book["id"] for book in BOOKS]
        )
    except Exception as e:
        print(f"Error creating collection: {e}")
        return None

def _ensure_collection():
    global collection
    if collection is None:
        create_collection()

def get_data():
    try:
        all_items = collection.get()
        return all_items
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return None

def send_query(query):
    print(f"Query sent: {query}")

def send_metadata(metadata):
    return metadata.get("author", "Unknown")

def format_results(docs, metadatas):
    if not docs:
        return pd.DataFrame()

    rows = []
    for i, (doc, meta) in enumerate(zip(docs, metadatas), 1):
        desc = meta.get("description", "")
        if len(desc) > 80:
            desc = desc[:77] + "..."
        rows.append({
            "#": i,
            "Title": meta.get("title", ""),
            "Author": meta.get("author", ""),
            "Year": meta.get("year", ""),
            "Genre": meta.get("genre", ""),
            "Pages": meta.get("pages", ""),
            "Language": meta.get("language", ""),
            "Rating": meta.get("rating", ""),
            "Award Winner": "Yes" if meta.get("award_winner") else "No",
            "Description": desc,
        })

    return pd.DataFrame(rows)

def main(query, metadata):
    _ensure_collection()
    send_query(query)
    where_filter = {"author": metadata} if metadata.strip() else None
    try:
        results = collection.query(
            query_texts=[query],
            n_results=5,
            where=where_filter,
        )
        docs = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        return format_results(docs, metadatas)
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    main("What is the meaning of life?", "Alice")