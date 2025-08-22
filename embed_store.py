import json
import yaml
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from langchain_openai import OpenAIEmbeddings

def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def load_signals(path="signals.json"):
    with open(path, "r") as f:
        return json.load(f)

def get_embeddings(texts, config):
    provider = config.get("embedding_provider", "openai")

    if provider == "huggingface":
        model_name = config.get("hf_model", "all-MiniLM-L6-v2")
        model = SentenceTransformer(model_name)
        return model.encode(texts, convert_to_numpy=True)

    elif provider == "openai":
        embeddings = OpenAIEmbeddings(
            openai_api_key=config["openai_api_key"],
            model=config.get("embedding_model", "text-embedding-3-small")
        )
        return embeddings.embed_documents(texts)

    else:
        raise ValueError(f"Unknown embedding provider: {provider}")

def build_index(vectors, index_path="signals.index"):
    dim = len(vectors[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(vectors).astype("float32"))
    faiss.write_index(index, index_path)

def main():
    config = load_config()
    signals = load_signals()
    texts = [s["title"] + " " + s["summary"] for s in signals]

    print(f"Embedding {len(texts)} signals using {config['embedding_provider']}...")
    vectors = get_embeddings(texts, config)
    build_index(vectors)

    print(f"FAISS index created and saved to 'signals.index'")

if __name__ == "__main__":
    main()