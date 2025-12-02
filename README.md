# Daily Growth Digest

Automated daily digest of strategic insights for B2B CEOs, CROs & CMOs.

Curates and analyzes the latest news in AI & Automation, Growth Marketing, and B2B SaaS using Claude AI.

🔗 **Live:** [negreflorian.com/daily-digest-en](https://www.negreflorian.com/daily-digest-en)

---

## 🎯 Features

- **Automated curation** from 8+ premium sources (TechCrunch, VentureBeat, Marketing Week, SaaStr)
- **AI-powered analysis** with Claude Sonnet 4 for relevance filtering and insight generation
- **Strategic insights** tailored for B2B executives
- **Key metrics** from industry benchmarks (Pitchbook, Gartner, LinkedIn)
- **Daily updates** via GitHub Actions
- **Beautiful editorial design** with Lora + Inter typography

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Anthropic API key ([get one here](https://console.anthropic.com))

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/daily-growth-digest.git
cd daily-growth-digest

# Install dependencies
pip install -r requirements.txt

# Run the script
python digest_final.py
```

On first run, you'll be prompted to enter your Anthropic API key. It will be saved in `config.json` for future runs.

---

## 📋 How It Works

1. **Fetch:** Collects latest articles from RSS feeds (last 24h)
2. **Analyze:** Claude AI filters for relevance and generates insights
3. **Generate:** Creates HTML digest with editorial design
4. **Publish:** Automated deployment via GitHub Actions

---

## ⚙️ Configuration

### RSS Feeds

Edit `digest_final.py` to customize sources:

```python
RSS_FEEDS = {
    "ai": [
        "https://techcrunch.com/tag/artificial-intelligence/feed/",
        "https://venturebeat.com/category/ai/feed/",
    ],
    "growth": [
        "https://marketingweek.com/feed/",
        # Add your feeds here
    ],
}
```

### Categories

Customize categories and icons:

```python
CATEGORIES = {
    "ai": {"icon": "🤖", "title": "AI & Automation"},
    "growth": {"icon": "📈", "title": "Growth Marketing"},
    # Add your categories
}
```

---

## 🤖 Automation

### GitHub Actions

The digest generates automatically every day at 7:00 AM UTC via GitHub Actions.

**Setup:**

1. Add your Anthropic API key as a GitHub secret:
   - Go to `Settings` → `Secrets and variables` → `Actions`
   - Click `New repository secret`
   - Name: `ANTHROPIC_API_KEY`
   - Value: Your API key (starts with `sk-ant-`)

2. Enable GitHub Actions:
   - Go to `Actions` tab
   - Enable workflows if prompted

3. Manual trigger:
   - Go to `Actions` → `Daily Growth Digest`
   - Click `Run workflow`

### Local Automation (Windows)

Use Task Scheduler to run daily:

```bash
# Task Scheduler command
python C:\path\to\daily-growth-digest\digest_final.py
```

---

## 📊 Cost

- **Anthropic API:** ~$0.05 per digest
- **Monthly cost:** ~$1.50 (30 days)
- **GitHub Actions:** Free (within limits)

---

## 🎨 Customization

### Design

Edit the `HTML_TEMPLATE` in `digest_final.py`:

- **Colors:** Modify CSS variables
- **Typography:** Change Google Fonts
- **Layout:** Adjust grid and spacing

### Content

Modify Claude's prompt in `filter_with_claude()` function to adjust:

- Number of articles selected
- Analysis criteria
- Insight generation

---

## 📝 Output

Generates `output.html` with:

- **Header:** Date and title
- **Sections:** Categorized articles
- **Articles:** Title, source, summary, insight
- **Metrics:** Key industry benchmarks
- **Footer:** Attribution

---

## 🔒 Security

- API keys stored in `config.json` (git-ignored)
- GitHub Actions uses encrypted secrets
- No sensitive data in repository

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 👤 Author

**Florian Nègre**  
Fractional Chief Growth Officer  
[negreflorian.com](https://negreflorian.com)

---

## 🤝 Contributing

Contributions welcome! Feel free to:

- Report bugs
- Suggest features
- Submit pull requests

---

## 📚 Resources

- [Anthropic API Documentation](https://docs.anthropic.com)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [RSS Feed Specification](https://www.rssboard.org/rss-specification)

---

**Last updated:** December 2025
