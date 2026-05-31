# Metadata Similarity Search

A semantic book search tool powered by ChromaDB and sentence embeddings, with a Gradio web interface.

## What it does

Enter a natural language query (e.g. *"survival story on another planet"*) and optionally filter by author. The app returns the top 5 most semantically similar books from a curated dataset of 27 titles across genres including Sci-Fi, Mystery, Fiction, Historical Fiction, Romance, Biography, Self-Help, and Non-Fiction.

## How it works

1. Book metadata and descriptions are embedded using the `all-MiniLM-L6-v2` sentence transformer model
2. Embeddings are stored in an in-memory ChromaDB collection with cosine similarity
3. Queries are embedded at runtime and matched against the collection
4. Results are returned as a ranked table with title, author, year, genre, pages, language, rating, and award status

## Project structure

```
├── books_data.py      # Dataset of 27 books with metadata and descriptions
├── functionality.py   # ChromaDB setup, embedding, querying, and result formatting
├── interface.py       # Gradio UI
```

## Setup

```bash
python -m venv path/to/venv
source path/to/venv/bin/activate
pip install chromadb gradio pandas sentence-transformers
```

## Usage

```bash
python interface.py
```

Then open [http://127.0.0.1:7900](http://127.0.0.1:7900) in your browser.

- **Query** — describe what kind of book you're looking for in plain English
- **Metadata** — optionally enter an author name to filter results to that author only
