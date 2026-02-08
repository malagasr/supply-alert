# System Architecture - Agentic Supply Chain Intelligence

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE (Streamlit)                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │   Dashboard  │  │ AI Assistant │  │  All News    │  │   About    │ │
│  │      🏠      │  │      🤖      │  │      📰      │  │     ℹ️     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          DATA LAYER                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  News Feeds (Google RSS):                                              │
│  ┌──────────────┬──────────────┬──────────────┬──────────────────────┐ │
│  │   Freight    │    Policy    │   AI & Tech  │   Disruptions        │ │
│  │   Industry   │     News     │     News     │                      │ │
│  └──────────────┴──────────────┴──────────────┴──────────────────────┘ │
│                                                                         │
│  ┌──────────────┬──────────────┬──────────────┬──────────────────────┐ │
│  │   Southern   │    Border    │   Weather    │   Port Status        │ │
│  │    Border    │   Weather    │    Alerts    │                      │ │
│  └──────────────┴──────────────┴──────────────┴──────────────────────┘ │
│                                                                         │
│  Cache: 5-minute TTL for fresh data                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    AI INTELLIGENCE LAYER                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. DATA COMPILATION                                                   │
│     │                                                                   │
│     ├─► get_all_news_as_json()                                        │
│     │   • Fetches all 8 data sources                                   │
│     │   • Converts to structured JSON                                  │
│     │   • Includes weather alerts & port status                        │
│     │                                                                   │
│  2. RAG FILTERING (Retrieval-Augmented Generation)                     │
│     │                                                                   │
│     ├─► filter_relevant_news(query, news_data)                        │
│     │   • Keyword matching against user query                          │
│     │   • Scores articles by relevance                                 │
│     │   • Returns top 10 most relevant items                           │
│     │   • BENEFIT: Reduces API calls, increases accuracy               │
│     │                                                                   │
│  3. CONTEXT BUILDING                                                   │
│     │                                                                   │
│     ├─► Build comprehensive context:                                  │
│     │   • Weather alerts (all current)                                 │
│     │   • Port status (all ports)                                      │
│     │   • Filtered relevant news (top 10)                              │
│     │   • Structured as markdown document                              │
│     │                                                                   │
│  4. AI AGENT PROMPT                                                    │
│     │                                                                   │
│     ├─► Specialized System Prompt:                                    │
│     │   ┌────────────────────────────────────────────────────────┐    │
│     │   │ Role: Supply Chain Logistics Analyst                   │    │
│     │   │ Focus: Southern Border Operations                      │    │
│     │   │                                                         │    │
│     │   │ Instructions:                                           │    │
│     │   │ • Data Triangulation (weather/border/policy)           │    │
│     │   │ • Correlation Engine (explain IMPACT)                  │    │
│     │   │ • Professional, predictive tone                        │    │
│     │   │ • Cite sources                                         │    │
│     │   │ • No hallucinations                                    │    │
│     │   └────────────────────────────────────────────────────────┘    │
│     │                                                                   │
│  5. GEMINI API CALL                                                    │
│     │                                                                   │
│     └─► Google Gemini API (gemini-2.0-flash-exp)                      │
│         • Free Tier: 60 requests/minute                                │
│         • Fast, efficient model                                        │
│         • Receives: System prompt + Context + User query               │
│         • Returns: Professional analysis                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        CHAT INTERFACE                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  • Message history (session state)                                     │
│  • User messages (blue bubbles)                                        │
│  • AI responses (dark bubbles)                                         │
│  • Suggested questions                                                 │
│  • Clear chat button                                                   │
│  • Real-time streaming                                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Example

```
User: "How will Texas storms affect border freight?"
  │
  ├─► System fetches all 8 data sources
  │
  ├─► RAG filters for relevant articles:
  │   • Keyword match: "texas" → 3 articles
  │   • Keyword match: "storm" → 2 articles  
  │   • Keyword match: "border" → 4 articles
  │   • Keyword match: "freight" → 5 articles
  │   → Top 10 most relevant selected
  │
  ├─► Context built:
  │   • Weather Alert: "Winter Storm Warning - Upper Midwest"
  │   • Weather Alert: "Fog Advisory - Central Valley, CA"
  │   • Port Status: Houston (Medium congestion, 3 days)
  │   • 10 filtered news articles
  │
  ├─► Sent to Gemini AI with analyst prompt
  │
  └─► AI Response:
      "Based on current data, I see a Winter Storm Warning
       affecting the Upper Midwest, which could impact I-94
       and I-90 freight routes. However, the current news feed
       does not contain specific information about Texas storms
       affecting border crossings. 
       
       I do note that Houston port shows medium congestion with
       3-day delays, which could compound any weather-related
       issues if storms develop in that region.
       
       Source: Weather Alerts, Port Status data."
```

## Key Design Decisions

### 1. RAG Implementation
- **Why**: Reduce API costs, improve accuracy
- **How**: Keyword-based relevance scoring
- **Result**: Only 10 most relevant items sent to AI

### 2. Gemini-2.0-Flash-Exp Model
- **Why**: Free tier, fast responses, good quality
- **Trade-off**: Less powerful than Pro, but sufficient for this use case

### 3. 5-Minute Cache
- **Why**: Balance freshness vs API rate limits
- **Result**: Users get near-real-time data without overwhelming news APIs

### 4. Specialized Prompt
- **Why**: General AI would give generic answers
- **Result**: Focused, professional, logistics-specific analysis

### 5. No Hallucination Constraint
- **Why**: Reliability is critical for logistics decisions
- **Result**: AI states when data is unavailable rather than guessing

## Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│              ENVIRONMENT VARIABLES                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Local Development:                                     │
│    .env file → load_dotenv() → os.getenv()            │
│                                                         │
│  Production (Streamlit Cloud):                         │
│    Streamlit Secrets → st.secrets.get()                │
│                                                         │
│  Protection:                                            │
│    • .env in .gitignore                                │
│    • No hardcoded keys                                 │
│    • Graceful fallback if missing                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Performance Characteristics

- **Cold Start**: ~2-3 seconds (fetch all feeds)
- **Cached Response**: <100ms (dashboard)
- **AI Query**: 2-5 seconds (RAG filter + API call)
- **News Refresh**: Every 5 minutes (automatic)
- **Scalability**: Limited by Gemini free tier (60 req/min)

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Streamlit | Web UI framework |
| Data Fetching | feedparser | RSS feed parsing |
| Caching | Streamlit cache | 5-min TTL |
| AI Model | Google Gemini | Natural language analysis |
| RAG Logic | Python (custom) | Relevance filtering |
| Environment | python-dotenv | API key management |
| Visualization | Plotly | Charts (future use) |

## Zero-Cost Architecture

All components use free tiers:
- ✓ Google News RSS (free, public)
- ✓ Google Gemini API (60 req/min free)
- ✓ Streamlit Community Cloud (free hosting)
- ✓ All Python libraries (open source)

**Total Cost**: $0/month for typical usage
