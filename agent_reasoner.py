import os
import argparse
import requests
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.runnables import RunnableLambda
from utils.config_loader import load_config
from utils.signal_loader import load_signals
from utils.markdown_exporter import export_markdown

# Load environment variables
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")

def validate_model(model_name: str, token: str):
    """Check if the model is available for hosted inference."""
    url = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"❌ Model '{model_name}' is not available for hosted inference.")

def build_llm(config: dict, validate: bool = False):
    """Construct the HuggingFaceEndpoint LLM."""
    model_name = config.get("hf_chat_model")
    if not model_name:
        raise ValueError("⚠️ No model name found in config under 'hf_chat_model'.")

    if validate:
        validate_model(model_name, HF_API_KEY)

    print(f"🔍 Using model: {model_name}")
    print(f"🔑 Token prefix: {HF_API_KEY[:5]}...")

    endpoint_url = f"https://api-inference.huggingface.co/models/{model_name}"
    return HuggingFaceEndpoint(
        endpoint_url=endpoint_url,
        huggingfacehub_api_token=HF_API_KEY,
        task="text-generation",
        temperature=0.3,
        max_new_tokens=512
    )

def synthesize_insight(query: str, signals: list, config: dict):
    """Generate insight from signals and query using the configured LLM."""
    signal_text = "\n\n".join([
        s.get("content", s.get("summary", "No content available.")) for s in signals
    ])

    llm = build_llm(config, validate=False)

    prompt_template = lambda inputs: f"""You are an expert AI analyst. Based on the following signals, synthesize a concise insight about the query.

Query: {inputs['query']}

Signals:
{inputs['signals']}

Insight:"""

    chain = RunnableLambda(prompt_template) | llm
    response = chain.invoke({"signals": signal_text, "query": query})
    export_markdown(query, signals, response)
    print("\n✅ Insight synthesized and exported.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--top_k", type=int, default=5)
    parser.add_argument("--signal_path", type=str, default="signals.json")
    args = parser.parse_args()

    config = load_config()
    all_signals = load_signals(args.signal_path)
    selected_signals = all_signals[:args.top_k]
    synthesize_insight(args.query, selected_signals, config)

if __name__ == "__main__":
    main()