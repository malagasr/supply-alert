# Border Crossing Buddy 🛃

**Real-time commercial truck wait times for US-Mexico border crossings**

Live app: [borderwaitbuddy.com](https://borderwaitbuddy.streamlit.app) *(update with your URL)*

---

## Features

- 📊 **Live CBP Data**: Real-time wait times from U.S. Customs & Border Protection
- 🌤️ **Weather**: Current conditions at each crossing
- 📰 **Policy News**: Latest freight regulations and border policy updates
- 📍 **8 Major Crossings**: Focus on high-volume commercial ports
- 100% Free • No signup required

---

## Data Sources

This app uses **free, public APIs**:
- [CBP Border Wait Times](https://bwt.cbp.gov) - Official wait time data
- [Open-Meteo](https://open-meteo.com) - Weather forecasts
- [Google News RSS](https://news.google.com) - News headlines

---

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/border-crossing-buddy.git
cd border-crossing-buddy

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

---

## Deploy to Streamlit Cloud

1. Fork this repository
2. Sign up at [streamlit.io](https://streamlit.io/cloud)
3. Connect your GitHub account
4. Deploy from `app.py`

---

## Tech Stack

- **Streamlit**: Web framework
- **Pandas**: Data manipulation
- **Plotly**: Charts
- **Feedparser**: RSS news feeds

---

## Contributing

Pull requests welcome! For major changes, please open an issue first.

---

## License

MIT License - see [LICENSE](LICENSE) file

---

## Disclaimer

This app provides real-time data from CBP for informational purposes only. Wait times are estimates and may vary. Always check official sources before traveling.

---

Built with ❤️ for the freight community
