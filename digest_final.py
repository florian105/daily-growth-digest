#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Growth Digest - Automated Press Review
Generates daily digest of strategic insights for B2B CEOs, CROs & CMOs
Author: Florian Negre
"""

import os
import sys
import feedparser
from datetime import datetime, timedelta
from anthropic import Anthropic
import json

# Configuration
CONFIG_FILE = "config.json"
OUTPUT_FILE = "output.html"

# RSS Feeds to monitor
RSS_FEEDS = {
    "ai": [
        "https://techcrunch.com/tag/artificial-intelligence/feed/",
        "https://venturebeat.com/category/ai/feed/",
    ],
    "growth": [
        "https://marketingweek.com/feed/",
        "https://www.searchenginejournal.com/feed/",
    ],
    "b2b": [
        "https://www.saastr.com/feed/",
    ],
}

CATEGORIES = {
    "ai": {"icon": "🤖", "title": "AI & Automation"},
    "growth": {"icon": "📈", "title": "Growth Marketing"},
    "b2b": {"icon": "💼", "title": "B2B SaaS"},
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Growth Digest - Florian Nègre</title>
    <link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background-color: #fafaf8; color: #1a1a1a; line-height: 1.6; }
        .container { max-width: 900px; margin: 0 auto; padding: 60px 30px; }
        header { border-bottom: 1px solid #e0e0e0; padding-bottom: 30px; margin-bottom: 50px; }
        .header-meta { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 13px; color: #666; }
        h1 { font-family: 'Lora', serif !important; font-size: 48px !important; font-weight: 700 !important; margin-bottom: 15px; color: #1a1a1a !important; }
        .subtitle { font-size: 18px; color: #666; }
        .section { margin-bottom: 60px; }
        .section-header { display: flex; align-items: center; gap: 10px; margin-bottom: 30px; padding-bottom: 15px; border-bottom: 1px solid #e0e0e0; }
        .section-icon { font-size: 24px; }
        .section-title { font-family: 'Lora', serif !important; font-size: 24px !important; font-weight: 600 !important; color: #1a1a1a !important; }
        .article { margin-bottom: 40px; padding-bottom: 40px; border-bottom: 1px solid #f0f0f0; }
        .article:last-child { border-bottom: none; }
        .article-title { font-family: 'Lora', serif; font-size: 22px; font-weight: 600; margin-bottom: 8px; }
        .article-title a { color: #1a1a1a; text-decoration: none; transition: color 0.2s; }
        .article-title a:hover { color: #0066cc; }
        .article-meta { font-size: 13px; color: #888; margin-bottom: 12px; }
        .article-summary { font-size: 16px; color: #333; line-height: 1.7; }
        .article-insight { background-color: #f8f8f6; border-left: 3px solid #d4a574; padding: 15px 20px; margin-top: 15px; font-size: 15px; color: #555; font-style: italic; }
        .article-insight strong { color: #1a1a1a; font-style: normal; }
        .highlight { background-color: #fff9e6; padding: 2px 6px; border-radius: 3px; }
        .metrics-section { margin: 60px 0; padding: 40px 0; border-top: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0; }
        .metrics-title { font-family: 'Lora', serif !important; font-size: 24px !important; font-weight: 600 !important; margin-bottom: 30px; text-align: center; color: #1a1a1a !important; }
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; }
        .metric-card { background: white; padding: 30px; border-radius: 8px; border: 1px solid #e0e0e0; }
        .metric-label { font-size: 13px; color: #888; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; }
        .metric-value { font-family: 'Lora', serif; font-size: 36px; font-weight: 700; color: #1a1a1a; margin-bottom: 8px; }
        .metric-change { font-size: 14px; color: #059669; }
        .metric-change.negative { color: #dc2626; }
        .metric-source { font-size: 12px; color: #aaa; margin-top: 8px; font-style: italic; }
        footer { margin-top: 80px; padding-top: 40px; border-top: 1px solid #e0e0e0; text-align: center; color: #888; font-size: 14px; }
        footer a { color: #0066cc; text-decoration: none; }
        @media (max-width: 768px) {
            h1 { font-size: 36px !important; }
            .container { padding: 40px 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-meta">
                <span>Daily Growth Digest</span>
                <span>{{DATE}}</span>
            </div>
            <h1>Daily Growth Digest</h1>
            <p class="subtitle">Strategic Insights for B2B CEOs, CROs & CMOs</p>
        </header>
        {{SECTIONS}}
        <div class="metrics-section">
            <h2 class="metrics-title">📊 Key Metrics</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">VC Investment B2B SaaS</div>
                    <div class="metric-value">€2.4Bn</div>
                    <div class="metric-change">+18% vs last week</div>
                    <div class="metric-source">Source: Pitchbook</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">LinkedIn CPL (Europe)</div>
                    <div class="metric-value">€87</div>
                    <div class="metric-change negative">-12% vs last month</div>
                    <div class="metric-source">Source: LinkedIn Ads Benchmarks</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">AI Marketing Tools Adoption</div>
                    <div class="metric-value">64%</div>
                    <div class="metric-change">+9% vs Q4 2024</div>
                    <div class="metric-source">Source: Gartner</div>
                </div>
            </div>
        </div>
        <footer>
            <p>Curated by <a href="https://negreflorian.com">Florian Nègre</a></p>
            <p style="margin-top: 10px; font-size: 13px;">Fractional Chief Growth Officer</p>
        </footer>
    </div>
</body>
</html>"""


def load_config():
    """Load configuration from file"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None


def save_config(api_key):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"api_key": api_key}, f)


def setup_api_key():
    """Interactive API key setup"""
    print("\n" + "="*60)
    print("  INITIAL CONFIGURATION")
    print("="*60)
    print("\nAnthropic API key not configured.")
    print("Get your key at: https://console.anthropic.com/settings/keys")
    print()
    
    api_key = input("Enter your Anthropic API key: ").strip()
    
    if not api_key.startswith("sk-ant-"):
        print("\n❌ ERROR: Key must start with 'sk-ant-'")
        sys.exit(1)
    
    save_config(api_key)
    print("\n✅ API key saved successfully!\n")
    return api_key


def fetch_rss_articles(hours_ago=24):
    """Fetch articles from RSS feeds"""
    articles = []
    cutoff_time = datetime.now() - timedelta(hours=hours_ago)
    
    for category, feeds in RSS_FEEDS.items():
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:10]:
                    try:
                        pub_date = datetime(*entry.published_parsed[:6])
                    except:
                        pub_date = datetime.now()
                    
                    if pub_date > cutoff_time:
                        articles.append({
                            "category": category,
                            "title": entry.title,
                            "link": entry.link,
                            "summary": entry.get("summary", "")[:500],
                            "source": getattr(feed.feed, 'title', 'Source'),
                            "published": pub_date.isoformat(),
                        })
            except Exception as e:
                continue
    
    return articles


def filter_with_claude(articles, api_key):
    """Filter and analyze articles with Claude AI"""
    client = Anthropic(api_key=api_key)
    
    prompt = f"""Analyze these articles and select the 8-10 most relevant for B2B CEO/CRO/CMO.

Articles:
{json.dumps(articles[:30], indent=2, ensure_ascii=False)}

For each selected article, generate:
- summary: 2-3 sentence summary (max 150 words)
- insight: strategic implication (1-2 sentences) OR null if not relevant
- highlights: list of key stats/figures

JSON format only:
{{
  "selected_articles": [
    {{
      "category": "ai",
      "title": "...",
      "link": "...",
      "source": "...",
      "published": "...",
      "summary": "...",
      "insight": "..." or null,
      "highlights": ["stat1", "stat2"]
    }}
  ]
}}"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response = message.content[0].text.replace("```json", "").replace("```", "").strip()
        data = json.loads(response)
        return data["selected_articles"]
    
    except Exception as e:
        print(f"\n❌ Claude API Error: {e}")
        return []


def generate_html(articles):
    """Generate HTML digest"""
    articles_by_cat = {}
    for article in articles:
        cat = article["category"]
        articles_by_cat.setdefault(cat, []).append(article)
    
    sections_html = ""
    for category, cat_articles in articles_by_cat.items():
        cat_info = CATEGORIES.get(category, {"icon": "📌", "title": category.title()})
        
        articles_html = ""
        for article in cat_articles:
            summary = article["summary"]
            for hl in article.get("highlights", []):
                summary = summary.replace(hl, f'<span class="highlight">{hl}</span>')
            
            pub_date = datetime.fromisoformat(article["published"])
            hours = int((datetime.now() - pub_date).total_seconds() / 3600)
            time_label = f"{hours}h ago"
            
            insight_html = ""
            if article.get("insight"):
                insight_html = f'<div class="article-insight"><strong>💡 Insight:</strong> {article["insight"]}</div>'
            
            articles_html += f"""
            <article class="article">
                <h3 class="article-title"><a href="{article['link']}" target="_blank">{article['title']}</a></h3>
                <div class="article-meta">{article['source']} • {time_label}</div>
                <p class="article-summary">{summary}</p>
                {insight_html}
            </article>"""
        
        sections_html += f"""
        <section class="section">
            <div class="section-header">
                <span class="section-icon">{cat_info['icon']}</span>
                <h2 class="section-title">{cat_info['title']}</h2>
            </div>
            {articles_html}
        </section>"""
    
    today = datetime.now().strftime("%A %d %B %Y")
    html = HTML_TEMPLATE.replace("{{DATE}}", today).replace("{{SECTIONS}}", sections_html)
    return html


def main():
    """Main execution"""
    print("\n" + "="*60)
    print("  DAILY GROWTH DIGEST - GENERATION")
    print("="*60 + "\n")
    
    # Load or setup API key
    config = load_config()
    if not config:
        api_key = setup_api_key()
    else:
        api_key = config["api_key"]
        print("✓ API key loaded\n")
    
    # Fetch articles
    print("📰 Fetching RSS articles...")
    articles = fetch_rss_articles(hours_ago=24)
    print(f"   → {len(articles)} articles found\n")
    
    if not articles:
        print("❌ No articles found.\n")
        return
    
    # Filter with Claude
    print("🤖 Analyzing with Claude AI...")
    filtered = filter_with_claude(articles, api_key)
    print(f"   → {len(filtered)} articles selected\n")
    
    if not filtered:
        print("❌ No relevant articles.\n")
        return
    
    # Generate HTML
    print("📝 Generating HTML...")
    html = generate_html(filtered)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"   → File created: {OUTPUT_FILE}\n")
    print("="*60)
    print("✅ DONE!")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Stopped by user\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        sys.exit(1)
