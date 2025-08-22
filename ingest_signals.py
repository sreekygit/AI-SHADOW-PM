import os
import yaml
import feedparser


def load_config(filename="config.yaml"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, filename)
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def parse_feeds(rss_feeds):
    articles = []
    for url in rss_feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # Limit to top 5 per feed
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", ""),
                "source": url
            })
    return articles

def main():
    config = load_config()
    rss_feeds = config.get("rss_feeds", [])
    articles = parse_feeds(rss_feeds)

    print(f"\nParsed {len(articles)} articles:")
    for article in articles:
        print(f"- {article['title']} ({article['link']})")

if __name__ == "__main__":
    main()
