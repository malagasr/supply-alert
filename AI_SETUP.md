# AI Assistant Setup Guide

## Overview

The Supply Chain Intelligence Dashboard now includes an **AI-Powered Supply Chain Analyst** that can answer complex questions about supply chain impacts, correlating data from multiple sources including weather, policy, and logistics news.

## Features

### 🤖 AI Supply Chain Analyst
- **Specialized Knowledge**: Focused on Southern Border logistics and cross-border freight operations
- **Data Triangulation**: Synthesizes weather, policy, and logistics data
- **RAG Technology**: Uses Retrieval-Augmented Generation for efficient, relevant responses
- **No Hallucinations**: Only uses actual news data from feeds, won't make up information
- **Correlation Engine**: Identifies cascading effects across supply chains

## Quick Start

### 1. Get a Free Gemini API Key

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Sign in with your Google account
3. Click **"Get API Key"** in the top navigation
4. Create a new API key or use an existing one
5. Copy your API key

**Note**: The Gemini API has a generous free tier perfect for this application!

### 2. Configure the Application

#### For Local Development:

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your key
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

Or manually create `.env` with:
```
GEMINI_API_KEY=your_actual_api_key_here
```

#### For Streamlit Cloud:

1. Go to your app's settings in Streamlit Cloud
2. Navigate to **Secrets**
3. Add the following content:
```toml
GEMINI_API_KEY = "your_api_key_here"
```

### 3. Run the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Using the AI Assistant

### Navigation

1. Open the application in your browser
2. Click **"🤖 AI Assistant"** in the sidebar navigation

### Ask Questions

The AI Assistant is designed to answer complex, multi-factor questions. Here are some examples:

#### Example Questions:

- **Weather Impact**: "How will the current storms in Texas affect cross-border freight operations?"
- **Policy Analysis**: "What are the latest trade policy changes affecting the Southern Border?"
- **Current Delays**: "What are the current border crossing delays and their causes?"
- **Bottleneck Identification**: "What are the major supply chain bottlenecks at the Southern Border right now?"
- **Correlation**: "If there's a hurricane in the Gulf, how will it affect Laredo freight crossings?"
- **Combined Factors**: "How will new tariffs impact cross-border shipping during peak season?"

### How It Works

1. **You Ask a Question**: Type your question in the chat input
2. **RAG Filtering**: The system finds the most relevant news articles for your query
3. **Context Building**: Combines relevant news with weather alerts and port status
4. **AI Analysis**: Gemini AI analyzes the data and provides insights
5. **Response**: You get a professional analysis with source citations

### Chat Features

- **Message History**: See your full conversation history
- **Suggested Questions**: Quick-start buttons for common queries
- **Clear Chat**: Reset the conversation at any time
- **Source Citations**: AI references which news categories it's using

## Technical Details

### Data Sources Used by AI

The AI has access to:

1. **Freight Industry News** (XPO, Ryder, Penske, JB Hunt, etc.)
2. **Policy News** (USMCA, DOT, FMCSA, tariffs)
3. **AI & Tech News** (Automation, ML in supply chain)
4. **Disruption Alerts** (Port congestion, delays, crises)
5. **Southern Border News** (Cross-border freight, customs)
6. **Border Weather News** (Texas/Mexico weather)
7. **Weather Alerts** (Real-time disruption alerts)
8. **Port Status** (Congestion levels, delay days)

### RAG Implementation

The system uses Retrieval-Augmented Generation (RAG) to:

1. **Filter Relevant Data**: Only sends articles matching your query keywords
2. **Reduce Token Usage**: Keeps API calls efficient and fast
3. **Improve Accuracy**: Focuses AI on the most relevant information
4. **Stay Current**: Always uses the latest news data

### AI Prompt Design

The AI is given a specialized role:

```
Role: Supply Chain Logistics Analyst specializing in Southern Border operations

Objectives:
- Analyze real-time news for bottlenecks
- Triangulate weather, border, and policy data
- Explain IMPACT, not just summarize
- Provide predictive, professional analysis
- Cite sources
- Never hallucinate
```

## Troubleshooting

### "AI Assistant Not Configured" Message

**Problem**: You see a warning that the AI is not configured

**Solution**: 
1. Verify your `.env` file exists and contains `GEMINI_API_KEY=...`
2. Check that the API key is valid (no extra spaces or quotes)
3. Restart the Streamlit app after adding the key

### "Error communicating with AI"

**Possible Causes**:

1. **Invalid API Key**: Verify your key is correct
2. **No Internet Connection**: Check your network
3. **API Quota Exceeded**: Check your Gemini API usage limits
4. **API Service Issues**: Try again in a few minutes

### Empty or Poor Responses

**Possible Causes**:

1. **No Relevant News**: The news feeds may not have data for your specific query
2. **Broad Query**: Try being more specific
3. **Recent Changes**: News cache updates every 5 minutes

**Tips for Better Results**:
- Be specific about locations (e.g., "Laredo" vs "border")
- Mention specific factors (e.g., "weather", "tariffs", "delays")
- Ask about current/recent events
- Use industry-specific terms

## API Costs & Limits

### Google Gemini Free Tier

- **Generous Free Quota**: 60 requests per minute
- **No Credit Card Required**: For free tier
- **Rate Limits**: Suitable for personal/hobbyist use
- **Model Used**: `gemini-2.0-flash-exp` (fast, efficient)

### Monitoring Usage

Check your usage at [Google AI Studio](https://ai.google.dev/)

## Security Notes

- **Never commit** your `.env` file to git (it's already in `.gitignore`)
- **Keep your API key private** - don't share it publicly
- **Rotate keys** if you suspect they've been compromised
- **Use Streamlit Secrets** for deployed applications

## Additional Resources

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [RAG Concepts](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)

## Support

For issues with:
- **The Application**: Open an issue on GitHub
- **Gemini API**: See [Google AI Support](https://ai.google.dev/support)
- **Streamlit**: See [Streamlit Forums](https://discuss.streamlit.io/)
