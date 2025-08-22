import os
import re
from datetime import datetime

def export_markdown(query, selected_signals, insight, output_dir="output"):
    # Sanitize query for filename
    safe_query = re.sub(r"[^\w\s-]", "", query).strip().lower().replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"insight_{safe_query}_{timestamp}.md"

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    # Build markdown content
    lines = [
        "# 🧠 Agent Insight",
        f"**Query:** {query}",
        f"**Generated:** {timestamp}",
        "",
        "## 🔍 Top Relevant Signals"
    ]

    for i, signal in enumerate(selected_signals, 1):
        title = signal.get("title", f"Signal {i}")
        summary = signal.get("summary", signal.get("content", "No summary available."))
        lines.append(f"### {i}. {title}")
        lines.append(f"{summary}\n")

    lines.append("## 🧠 Synthesized Insight")
    lines.append(insight.strip())

    # Write to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n📄 Markdown exported to `{filepath}`")