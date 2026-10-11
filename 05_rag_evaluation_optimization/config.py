from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COLLECTION_NAME = os.getenv("HYBRID_COLLECTION_NAME")
DB_URL = os.getenv("DB_URL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
TEXT_MODEL = os.getenv("TEXT_MODEL")
CHUNK_SIZE = os.getenv("CHUNK_SIZE")
CHUNK_OVERLAP = os.getenv("CHUNK_OVERLAP")
TOP_K = os.getenv("TOP_K")
BM25_EMBEDDING_MODEL = os.getenv("BM25_EMBEDDING_MODEL")
SCORE_THRESHOLD = os.getenv("SCORE_THRESHOLD")
EVALUATE_RAG_COLLECTION = os.getenv("EVALUATE_RAG_COLLECTION")