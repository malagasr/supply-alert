# Supply Chain Intelligence Dashboard

**AI-Powered real-time weather, geopolitical alerts, and disruption tracking for logistics professionals**

Live app: TBD

---

## ✨ New Features: AI-Powered Intelligence

- 🤖 **AI Supply Chain Analyst**: Ask complex questions and get predictive analysis
- 🌎 **Southern Border Focus**: Specialized intelligence on cross-border freight operations
- 🔍 **RAG Technology**: Efficient context-aware responses using Retrieval-Augmented Generation
- 💡 **Data Triangulation**: Synthesizes weather, policy, and logistics data
- 🎯 **Correlation Engine**: Identifies cascading effects across the supply chain
- 💰 **100% Free**: Powered by Google Gemini's free tier API

---

## Features

- 🌪️ **Weather Disruptions**: Hurricane tracking, storm alerts affecting freight routes
- 🚨 **Geopolitical Alerts**: Port strikes, fuel crises, trade policy changes
- 📊 **Port Congestion**: Real-time status of major US ports
- 🛣️ **Route Disruptions**: Road closures, rail strikes, carrier delays
- 📰 **Supply Chain News**: Latest policy updates and industry alerts
- 🌎 **Southern Border Intelligence**: Cross-border freight, customs, USMCA updates
- 🤖 **AI Chatbot**: Ask complex questions about supply chain impacts
- 100% Free • No signup required

---

## Data Sources

This app uses **free, public APIs and data sources**:
- [Open-Meteo](https://open-meteo.com) - Weather forecasts and hurricane tracking
- [Google News RSS](https://news.google.com) - Supply chain news and alerts
- [Google Gemini API](https://ai.google.dev/) - AI-powered analysis (free tier)
- Public freight and logistics data

---

## AI Assistant Setup

The AI Supply Chain Analyst uses Google's Gemini API (free tier):

1. **Get a Free API Key:**
   - Visit [Google AI Studio](https://ai.google.dev/)
   - Sign in with your Google account
   - Click "Get API Key" and create a new key

2. **Configure the App:**
   ```bash
   # Create a .env file in the project root
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

3. **For Streamlit Cloud:**
   - Go to your app settings
   - Add `GEMINI_API_KEY` to Secrets
   - Format: `GEMINI_API_KEY = "your_api_key_here"`

---

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/supply-chain-intelligence.git
cd supply-chain-intelligence

# Install dependencies
pip install -r requirements.txt

# Set up AI Assistant (optional but recommended)
cp .env.example .env
# Edit .env and add your Gemini API key

# Run locally
streamlit run app.py
```

---

## Deploy to Streamlit Cloud

1. Fork this repository
2. Sign up at [streamlit.io](https://streamlit.io/cloud)
3. Connect your GitHub account
4. Deploy from `app.py`
5. Add `GEMINI_API_KEY` to Secrets (optional, for AI features)

---

## Tech Stack

- **Streamlit**: Web framework
- **Pandas**: Data manipulation
- **Plotly**: Charts and visualizations
- **Feedparser**: RSS news feeds
- **Requests**: API calls
- **Google Gemini AI**: Generative AI for intelligent analysis
- **Python-dotenv**: Environment variable management

---

## Contributing

Pull requests welcome! For major changes, please open an issue first.

---

## License

MIT License - see [LICENSE](LICENSE) file

---

## Disclaimer

This app provides real-time data from public sources for informational purposes only. Supply Chain Intelligence makes no warranties regarding accuracy or completeness. Always verify with official sources before making business decisions. Not affiliated with any government agency or commercial organization.

---

Built with ❤️ for the logistics community
