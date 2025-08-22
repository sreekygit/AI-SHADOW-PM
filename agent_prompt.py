from langchain.prompts import PromptTemplate

def get_prompt():
    return PromptTemplate.from_template("""
You are a strategic product analyst reviewing recent signals from global commerce and supply chain feeds.

Given the following signals:
{signals}

And the user query:
"{query}"

Synthesize a concise insight that connects the signals to the query. Highlight any emerging patterns, risks, or opportunities. Be clear, analytical, and actionable.
""")