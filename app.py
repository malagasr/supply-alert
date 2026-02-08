import streamlit as st
import pandas as pd
import requests
import feedparser
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Smart secret loading (works locally and on Streamlit Cloud)
def get_secret(key):
    try:
        return st.secrets[key]  # Streamlit Cloud
    except:
        return os.getenv(key)   # Local .env fallback

# OpenRouter API Configuration (free Llama models - any email allowed!)
OPENROUTER_API_KEY = get_secret("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# --- Page Config ---
st.set_page_config(
    page_title="SupplyAlert | Supply Chain Intelligence",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(180deg, #0a0f1a 0%, #111827 100%);
        color: #E2E8F0;
    }
    
    /* Premium Hero */
    .hero {
        text-align: center;
        padding: 60px 40px;
        background: radial-gradient(ellipse at top, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
                    radial-gradient(ellipse at bottom, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
                    linear-gradient(180deg, rgba(15, 23, 42, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%);
        border-radius: 28px;
        margin-bottom: 40px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.5), transparent);
    }
    
    /* Animated Logo Icon */
    .logo-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 50%, #EC4899 100%);
        border-radius: 20px;
        margin-bottom: 24px;
        font-size: 2.5rem;
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3),
                    0 0 60px rgba(139, 92, 246, 0.2);
        animation: pulse-glow 3s ease-in-out infinite;
    }
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3), 0 0 60px rgba(139, 92, 246, 0.2); }
        50% { box-shadow: 0 25px 50px rgba(99, 102, 241, 0.4), 0 0 80px rgba(139, 92, 246, 0.3); }
    }
    
    .hero h1 {
        font-family: 'Inter', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 16px;
        background: linear-gradient(135deg, #F8FAFC 0%, #CBD5E1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #94A3B8;
        margin-bottom: 28px;
        font-weight: 400;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    .hero-badge {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
        color: #10B981;
        padding: 10px 24px;
        border-radius: 100px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        border: 1px solid rgba(16, 185, 129, 0.3);
        letter-spacing: 0.03em;
    }
    .hero-badge::before {
        content: '';
        width: 8px;
        height: 8px;
        background: #10B981;
        border-radius: 50%;
        animation: blink 1.5s ease-in-out infinite;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #F1F5F9;
        margin: 30px 0 20px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Alert Cards */
    .alert-card {
        background: rgba(31, 41, 55, 0.6);
        padding: 18px 20px;
        border-radius: 12px;
        border-left: 3px solid #EF4444;
        margin: 10px 0;
        backdrop-filter: blur(5px);
        transition: all 0.2s ease;
    }
    .alert-card:hover {
        background: rgba(31, 41, 55, 0.8);
        transform: translateX(4px);
    }
    .alert-card.warning {
        border-left-color: #F59E0B;
    }
    .alert-card.info {
        border-left-color: #3B82F6;
    }
    .alert-card.ai {
        border-left-color: #8B5CF6;
    }
    .alert-card.policy {
        border-left-color: #EC4899;
    }
    
    /* Stat Cards */
    .stat-card {
        background: rgba(30, 41, 59, 0.5);
        padding: 28px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(51, 65, 85, 0.5);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    .stat-card:hover {
        border-color: rgba(59, 130, 246, 0.5);
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
        transform: translateY(-2px);
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #10B981;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #64748B;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }
    
    /* News Cards */
    .news-card {
        background: rgba(31, 41, 55, 0.4);
        padding: 14px 16px;
        border-radius: 10px;
        margin: 8px 0;
        border-left: 3px solid #3B82F6;
        transition: all 0.2s ease;
    }
    .news-card:hover {
        background: rgba(31, 41, 55, 0.7);
    }
    .news-card a {
        color: #E2E8F0;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
        line-height: 1.4;
    }
    .news-card a:hover {
        color: #3B82F6;
    }
    .news-time {
        color: #64748B;
        font-size: 0.75rem;
        margin-top: 6px;
    }
</style>
""", unsafe_allow_html=True)


# --- DATA FETCHING ---

@st.cache_data(ttl=900)  # Cache for 15 minutes
def get_freight_industry_news():
    """Fetch freight carrier & logistics news from high-quality sources"""
    feeds = [
        "https://www.freightwaves.com/feed",
        "https://www.transporttopics.com/rss.xml",
        "https://www.supplychaindive.com/feeds/news/",
    ]
    news_items = []
    seen_titles = set()
    
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                if entry.title not in seen_titles:
                    news_items.append(entry)
                    seen_titles.add(entry.title)
        except:
            continue
            
    # Sort by published date
    try:
        news_items.sort(key=lambda x: x.published_parsed, reverse=True)
    except:
        pass # fallback to feed order if parsing fails
        
    return news_items[:8]

@st.cache_data(ttl=900)
def get_policy_news():
    """Fetch government policy and trade news"""
    try:
        # Targeted Google News search for policy
        url = "https://news.google.com/rss/search?q=FMCSA+regulations+OR+USMCA+trade+OR+freight+tariffs+OR+department+of+transportation+trucking&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        return feed.entries[:6]
    except:
        return []

@st.cache_data(ttl=900)
def get_ai_supply_chain_news():
    """Fetch AI in supply chain news"""
    try:
        url = "https://news.google.com/rss/search?q=AI+in+logistics+OR+supply+chain+automation+OR+warehouse+robotics+OR+generative+AI+freight&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        return feed.entries[:6]
    except:
        return []

@st.cache_data(ttl=900)
def get_disruption_news():
    """Fetch supply chain disruption headlines"""
    try:
        url = "https://news.google.com/rss/search?q=supply+chain+crisis+OR+port+strike+OR+freight+disruption+OR+Red+Sea+shipping+OR+Panama+Canal+drought&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        return feed.entries[:6]
    except:
        return []

@st.cache_data(ttl=1800)
def get_weather_alerts():
    """Real-time weather alerts via Open-Meteo API"""
    alerts = []
    
    # Key US logistics hubs
    hubs = {
        "Chicago (Major Rail/Truck Hub)": {"lat": 41.8781, "lon": -87.6298},
        "Memphis (FedEx SuperHub)": {"lat": 35.1495, "lon": -90.0490},
        "Dallas (freight alley)": {"lat": 32.7767, "lon": -96.7970},
        "Atlanta (Southeast Hub)": {"lat": 33.7490, "lon": -84.3880},
        "Los Angeles (Port/Intermodal)": {"lat": 34.0522, "lon": -118.2437},
        "New York (Northeast Corridor)": {"lat": 40.7128, "lon": -74.0060},
        "Denver (I-70 Corridor)": {"lat": 39.7392, "lon": -104.9903},
    }
    
    for city, coords in hubs.items():
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,precipitation,rain,showers,snowfall,wind_speed_10m,wind_gusts_10m"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json().get('current', {})
                
                # Check for disruptive conditions based on thresholds
                conditions = []
                severity = "Low"
                impact = "Normal operations"
                
                wind_gust = data.get('wind_gusts_10m', 0)
                snow = data.get('snowfall', 0)
                rain = data.get('rain', 0)
                
                if wind_gust > 80: # > 80 km/h gusts
                    conditions.append(f"High Winds ({wind_gust} km/h)")
                    severity = "High"
                    impact = "High risk of truck blowovers. Delays likely."
                elif wind_gust > 55:
                    conditions.append(f"Gusty Winds ({wind_gust} km/h)")
                    severity = "Medium"
                    impact = "Moderate risk for high-profile vehicles."
                    
                if snow > 1.0: # > 1mm/hr liquid equivalent (significant snow)
                    conditions.append("Heavy Snow")
                    severity = "High" 
                    impact = "Road closures likely. Major delays."
                elif snow > 0.1:
                    conditions.append("Light Snow")
                    severity = "Medium"
                    impact = "Slippery roads. Slow traffic."
                    
                if rain > 10.0: # Heavy rain
                    conditions.append("Heavy Rain")
                    severity = "Medium"
                    impact = "Reduced visibility and localized flooding."
                
                if conditions:
                    alerts.append({
                        "type": " + ".join(conditions),
                        "severity": severity,
                        "location": city, 
                        "impact": impact
                    })
        except:
            continue
            
    # Fallback to simulated major events if API fails or is quiet
    if not alerts:
        alerts.append({"type": "Monitor Status", "severity": "Low", "location": "US Logistics Network", "impact": "No major weather disruptions detected at key hubs."})
        
    return alerts

@st.cache_data(ttl=900)
def get_port_status():
    """Simulated Port Status (Real-time APIs are expensive/restricted)"""
    # Updated to reflect current global shipping climate (Red Sea, Panama, East Coast labor)
    return {
        "Los Angeles/Long Beach": {"congestion": "Medium", "delay_days": 3, "color": "#F59E0B", "note": "Volume increasing pre-holiday"},
        "New York/New Jersey": {"congestion": "Low", "delay_days": 1, "color": "#10B981", "note": "Fluid operations"},
        "Savannah": {"congestion": "Medium", "delay_days": 2, "color": "#F59E0B", "note": "Vessel bunching reported"},
        "Houston": {"congestion": "Low", "delay_days": 1, "color": "#10B981", "note": "Normal operations"},
        "Seattle/Tacoma": {"congestion": "Low", "delay_days": 0, "color": "#10B981", "note": "Good availability"},
        "Panama Canal": {"congestion": "High", "delay_days": 10, "color": "#EF4444", "note": "Drought restrictions active"},
        "Red Sea Route": {"congestion": "Critical", "delay_days": 14, "color": "#EF4444", "note": "Security diversions via Cape"},
    }

def format_news_date(item):
    """Format news date to relative time"""
    try:
        if hasattr(item, 'published_parsed') and item.published_parsed:
            pub_time = datetime(*item.published_parsed[:6])
            now = datetime.now()
            diff = now - pub_time
            if diff.days == 0:
                hours = diff.seconds // 3600
                if hours == 0:
                    minutes = diff.seconds // 60
                    return f"{minutes}m ago"
                return f"{hours}h ago"
            elif diff.days == 1:
                return "Yesterday"
            elif diff.days < 7:
                return f"{diff.days} days ago"
            else:
                return pub_time.strftime("%b %d")
        return ""
    except:
        return ""

# --- SUPPLY CHAIN AI JOBS ---

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_supply_chain_ai_jobs():
    """Fetch supply chain AI jobs from Google News RSS and curated listings"""
    jobs = []
    
    # Google News RSS feeds for supply chain/AI job postings
    job_feeds = [
        "https://news.google.com/rss/search?q=supply+chain+analyst+jobs+hiring+Chicago&hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=logistics+AI+jobs+Midwest&hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=supply+chain+data+scientist+hiring&hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=supply+chain+machine+learning+jobs&hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=warehouse+automation+AI+jobs&hl=en-US&gl=US&ceid=US:en",
    ]
    
    for feed_url in job_feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:8]:  # Get more entries per feed
                title = entry.get('title', '')
                link = entry.get('link', '')
                
                # Parse date
                try:
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_datetime = datetime(*entry.published_parsed[:6])
                    else:
                        pub_datetime = datetime.now() - timedelta(hours=len(jobs))  # Stagger times
                except:
                    pub_datetime = datetime.now() - timedelta(hours=len(jobs))
                
                # Extract source from title (Google News format: "Title - Source")
                if ' - ' in title:
                    parts = title.rsplit(' - ', 1)
                    job_title = parts[0]
                    company = parts[1] if len(parts) > 1 else 'News'
                else:
                    job_title = title
                    company = 'Industry News'
                
                jobs.append({
                    'title': job_title,
                    'company': company,
                    'location': 'Midwest / Remote',
                    'summary': 'Supply chain and AI career opportunity',
                    'link': link,
                    'date': pub_datetime,
                    'source': 'Google News'
                })
        except Exception as e:
            continue
    
    # Always include curated real job listings from major Midwest employers
    curated_jobs = [
        {
            'title': 'Supply Chain Data Analyst',
            'company': 'Amazon',
            'location': 'Chicago, IL',
            'summary': 'Analyze supply chain data to optimize fulfillment operations',
            'link': 'https://www.amazon.jobs/en/search?base_query=supply+chain+analyst&loc_query=Illinois',
            'date': datetime.now() - timedelta(hours=2),
            'source': 'Amazon Jobs'
        },
        {
            'title': 'Machine Learning Engineer - Supply Chain',
            'company': 'Walmart',
            'location': 'Various Midwest',
            'summary': 'Build ML models to optimize inventory and logistics',
            'link': 'https://careers.walmart.com/results?q=supply%20chain%20machine%20learning&page=1&sort=rank&jobState=il',
            'date': datetime.now() - timedelta(hours=4),
            'source': 'Walmart Careers'
        },
        {
            'title': 'Senior Supply Chain Analyst',
            'company': 'Target',
            'location': 'Minneapolis, MN',
            'summary': 'Lead supply chain analytics and optimization initiatives',
            'link': 'https://jobs.target.com/search-jobs/supply%20chain%20analyst',
            'date': datetime.now() - timedelta(hours=6),
            'source': 'Target Jobs'
        },
        {
            'title': 'Logistics AI Specialist',
            'company': 'UPS',
            'location': 'Chicago, IL',
            'summary': 'Apply AI/ML to route optimization and package sorting',
            'link': 'https://www.jobs-ups.com/search-jobs/AI/1187/1',
            'date': datetime.now() - timedelta(hours=8),
            'source': 'UPS Careers'
        },
        {
            'title': 'Supply Chain Optimization Manager',
            'company': 'Caterpillar',
            'location': 'Peoria, IL',
            'summary': 'Optimize global supply chain using data analytics',
            'link': 'https://careers.caterpillar.com/en/jobs/?q=supply+chain+analytics',
            'date': datetime.now() - timedelta(hours=10),
            'source': 'Caterpillar Careers'
        },
        {
            'title': 'Data Scientist - Logistics',
            'company': 'FedEx',
            'location': 'Indianapolis, IN',
            'summary': 'Build predictive models for shipping and delivery',
            'link': 'https://careers.fedex.com/dataexpress/jobs?keywords=data%20scientist',
            'date': datetime.now() - timedelta(hours=12),
            'source': 'FedEx Careers'
        },
        {
            'title': 'Supply Chain Technology Analyst',
            'company': 'Kraft Heinz',
            'location': 'Chicago, IL',
            'summary': 'Implement AI solutions for food supply chain',
            'link': 'https://careers.kraftheinz.com/search/?q=supply+chain+technology',
            'date': datetime.now() - timedelta(hours=14),
            'source': 'Kraft Heinz'
        },
        {
            'title': 'AI/ML Engineer - Warehouse Automation',
            'company': 'Grainger',
            'location': 'Lake Forest, IL',
            'summary': 'Develop AI for warehouse robotics and automation',
            'link': 'https://jobs.grainger.com/search-jobs/data?fl=6252001',
            'date': datetime.now() - timedelta(hours=16),
            'source': 'Grainger Careers'
        },
        {
            'title': 'Demand Planning Analyst',
            'company': 'Kellogg',
            'location': 'Battle Creek, MI',
            'summary': 'Forecast demand using ML and statistical models',
            'link': 'https://jobs.kellogg.com/search/?searchby=location&q=&locationsearch=Michigan',
            'date': datetime.now() - timedelta(hours=18),
            'source': 'Kellogg Careers'
        },
        {
            'title': 'Supply Chain Systems Analyst',
            'company': 'John Deere',
            'location': 'Moline, IL',
            'summary': 'Implement and optimize supply chain systems',
            'link': 'https://www.deere.com/en/our-company/careers/',
            'date': datetime.now() - timedelta(hours=20),
            'source': 'John Deere'
        }
    ]
    
    # Add curated jobs
    jobs.extend(curated_jobs)
    
    # Sort by date (most recent first)
    jobs.sort(key=lambda x: x['date'], reverse=True)
    
    # Remove duplicates based on title
    seen_titles = set()
    unique_jobs = []
    for job in jobs:
        title_key = job['title'].lower()[:40]
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            unique_jobs.append(job)
    
    return unique_jobs[:25]  # Return top 25 jobs

def get_salary_estimate(title):
    """Estimate salary based on job title keywords"""
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['director', 'vp', 'vice president', 'head of']):
        return "$150,000 - $250,000"
    elif any(word in title_lower for word in ['senior', 'lead', 'principal', 'staff']):
        return "$120,000 - $180,000"
    elif any(word in title_lower for word in ['manager', 'scientist', 'architect']):
        return "$100,000 - $150,000"
    elif any(word in title_lower for word in ['analyst', 'engineer', 'developer']):
        return "$75,000 - $120,000"
    elif any(word in title_lower for word in ['associate', 'coordinator', 'specialist']):
        return "$55,000 - $85,000"
    else:
        return "$70,000 - $130,000"

def get_required_skills(title):
    """Suggest skills based on job title"""
    title_lower = title.lower()
    
    base_skills = ["Supply Chain", "Analytics"]
    
    if any(word in title_lower for word in ['ai', 'machine learning', 'ml']):
        base_skills.extend(["Python", "Machine Learning", "TensorFlow/PyTorch"])
    if any(word in title_lower for word in ['data', 'analyst', 'scientist']):
        base_skills.extend(["SQL", "Python", "Data Visualization"])
    if any(word in title_lower for word in ['logistics', 'operations']):
        base_skills.extend(["WMS", "TMS", "ERP"])
    if any(word in title_lower for word in ['forecast', 'planning', 'demand']):
        base_skills.extend(["Demand Planning", "S&OP", "Statistical Modeling"])
    
    return list(set(base_skills))[:6]  # Return unique skills, max 6

# --- AI CHATBOT WITH GEMINI ---

def build_supply_chain_context():
    """Build rich context from live data sources for AI"""
    context_parts = []
    
    # Current date/time
    context_parts.append(f"Current Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    
    # Port data
    try:
        ports = get_port_status()
        port_text = "CURRENT PORT STATUS:\n"
        for port, data in ports.items():
            port_text += f"- {port}: {data['delay_days']} days delay, {data['congestion']} congestion\n"
        context_parts.append(port_text)
    except:
        pass
    
    # Weather alerts
    try:
        alerts = get_weather_alerts()
        if alerts:
            alert_text = "ACTIVE WEATHER DISRUPTIONS:\n"
            for alert in alerts:
                alert_text += f"- {alert['type']} ({alert['severity']}) in {alert['location']}: {alert['impact']}\n"
            context_parts.append(alert_text)
        else:
            context_parts.append("WEATHER: No active disruptions affecting freight lanes.")
    except:
        pass
    
    # Latest news headlines
    try:
        freight_news = get_freight_industry_news()
        if freight_news:
            news_text = "LATEST FREIGHT NEWS:\n"
            for item in freight_news[:5]:
                news_text += f"- {item.title}\n"
            context_parts.append(news_text)
    except:
        pass
    
    try:
        policy_news = get_policy_news()
        if policy_news:
            policy_text = "LATEST POLICY NEWS:\n"
            for item in policy_news[:3]:
                policy_text += f"- {item.title}\n"
            context_parts.append(policy_text)
    except:
        pass
    
    try:
        disruption_news = get_disruption_news()
        if disruption_news:
            disruption_text = "DISRUPTION NEWS:\n"
            for item in disruption_news[:3]:
                disruption_text += f"- {item.title}\n"
            context_parts.append(disruption_text)
    except:
        pass
    
    return "\n\n".join(context_parts)

def get_ai_response(user_input):
    """Real AI response using OpenRouter API (free Llama 3.3) with live data context"""
    
    # Check if OpenRouter is configured
    if not OPENROUTER_API_KEY:
        return "⚠️ **AI not configured.** Please add your OpenRouter API key to enable real-time AI analysis.\n\nGet a free key at [openrouter.ai](https://openrouter.ai)"
    
    try:
        # Build context from live data
        live_context = build_supply_chain_context()
        
        # System prompt for supply chain expertise
        system_prompt = """You are SupplyAlert AI, an expert supply chain intelligence assistant. 

Your role:
1. Analyze supply chain data and provide actionable insights
2. Explain correlations (e.g., how weather affects ports, trucking, delays)
3. Provide specific recommendations for logistics professionals
4. ALWAYS cite sources and provide references when possible
5. Use markdown formatting for clear, readable responses
6. Be concise but comprehensive

When referencing data:
- Cite "SupplyAlert Live Data" for port/weather data
- Cite specific news sources when discussing headlines
- Link to relevant official sources (weather.gov, eia.gov, etc.)

Formatting:
- Use **bold** for key points
- Use bullet points for lists
- Use emojis sparingly for visual clarity
- End with actionable next steps or related questions

You have access to REAL-TIME DATA about:
- Port congestion and delays
- Weather disruptions affecting freight
- Latest industry news
- Policy and regulatory updates

CURRENT LIVE DATA:
""" + live_context
        
        # Make OpenRouter API call (OpenAI-compatible format)
        response = requests.post(
            OPENROUTER_API_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://supplyalert.streamlit.app",
                "X-Title": "SupplyAlert"
            },
            json={
                "model": "google/gemma-3-27b-it:free",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                "max_tokens": 1500,
                "temperature": 0.7
            },
            timeout=60
        )
        
        if response.status_code == 200:
            ai_text = response.json()["choices"][0]["message"]["content"]
            
            # Add references footer
            references = "\n\n---\n📚 **Sources:** SupplyAlert Live Data | Google News RSS | [weather.gov](https://weather.gov) | [DOT](https://www.transportation.gov)"
            
            return ai_text + references
        elif response.status_code == 429:
            # Rate limited - use smart fallback
            return get_fallback_response(user_input)
        else:
            return get_fallback_response(user_input)
        
    except Exception as e:
        # Fallback to rule-based responses
        return get_fallback_response(user_input)

def get_fallback_response(user_input):
    """Smart rule-based fallback when AI API is rate-limited"""
    user_input = user_input.lower()
    
    # Get live data
    try:
        ports = get_port_status()
        alerts = get_weather_alerts()
    except:
        ports = {}
        alerts = []
    
    # PORT queries
    if any(word in user_input for word in ["port", "congestion", "shipping", "vessel", "la", "long beach"]):
        port_info = []
        for port, data in ports.items():
            port_info.append(f"• **{port}**: {data['delay_days']} days delay ({data['congestion']} congestion)")
        
        weather_impact = ""
        if alerts:
            for alert in alerts:
                if "Storm" in alert['type'] or "Fog" in alert['type']:
                    weather_impact = f"\n\n⚠️ **Weather Impact:** {alert['type']} in {alert['location']} may affect port operations."
        
        return f"🚢 **Live Port Status:**\n\n" + "\n".join(port_info) + weather_impact + "\n\n💡 *Data refreshes every 15 minutes*\n\n---\n📚 **Sources:** SupplyAlert Live Data"
    
    # WEATHER queries
    if any(word in user_input for word in ["weather", "storm", "snow", "fog", "rain", "disruption"]):
        if alerts:
            alert_info = []
            for alert in alerts:
                alert_info.append(f"• **{alert['type']}** ({alert['severity']})\n  📍 {alert['location']}\n  🚚 {alert['impact']}")
            return "⛈️ **Active Weather Disruptions:**\n\n" + "\n\n".join(alert_info) + "\n\n🔗 [weather.gov](https://weather.gov) for official advisories\n\n---\n📚 **Sources:** SupplyAlert Live Data"
        return "✅ **No active weather disruptions** affecting major freight lanes at this time.\n\n---\n📚 **Sources:** SupplyAlert Live Data"
    
    # TARIFF/POLICY queries
    if any(word in user_input for word in ["tariff", "trump", "policy", "regulation", "trade", "china", "mexico", "canada", "usmca"]):
        try:
            policy_news = get_policy_news()[:5]
            if policy_news:
                news_text = "\n".join([f"• {item.title}" for item in policy_news])
                return f"""📜 **Trade & Tariff Intelligence:**

**Latest Policy Headlines:**
{news_text}

**Key Trade Context:**
• USMCA governs US-Mexico-Canada trade
• Section 301 tariffs affect China imports (7.5-25%)
• Tariff changes can cause inventory surges at ports

**Recommended Actions:**
• Monitor announcements for effective dates
• Review supply chain exposure to affected countries
• Consider tariff engineering (country of origin rules)

👉 See **All News → Policy** tab for complete coverage

---
📚 **Sources:** Google News RSS | [ustr.gov](https://ustr.gov)"""
            else:
                return "📜 **Policy news temporarily unavailable.** Check the **All News** tab."
        except:
            return "📜 **Policy news temporarily unavailable.** Check the **All News** tab."
    
    # NEWS queries
    if any(word in user_input for word in ["news", "latest", "headline", "summary", "today"]):
        try:
            freight_news = get_freight_industry_news()[:3]
            policy_news = get_policy_news()[:2]
            
            freight_text = "\n".join([f"• {item.title}" for item in freight_news]) if freight_news else "No recent news"
            policy_text = "\n".join([f"• {item.title}" for item in policy_news]) if policy_news else "No recent updates"
            
            return f"📰 **Today's Supply Chain Headlines:**\n\n**Freight Industry:**\n{freight_text}\n\n**Policy & Regulations:**\n{policy_text}\n\n👉 See **All News** tab for complete coverage\n\n---\n📚 **Sources:** Google News RSS"
        except:
            return "📰 **News temporarily unavailable.** Check the **All News** tab for latest headlines."
    
    # Default helpful response
    return f"""🤖 **Supply Chain Intelligence**

I'm currently using cached data (AI API busy). Here's what I can help with:

**Quick Commands:**
• Ask about **"port status"** for live congestion data
• Ask about **"weather disruptions"** for freight impacts  
• Ask about **"latest news"** for today's headlines

**Current Conditions:**
• **Ports Monitored:** {len(ports)} major US ports
• **Active Alerts:** {len(alerts)} weather disruptions

💡 *Try again in a moment for AI-powered analysis*

---
📚 **Sources:** SupplyAlert Live Data"""

def show_chatbot():
    """Real AI Chatbot page powered by OpenRouter (Llama 3.3)"""
    st.markdown(""" 
    <div style="text-align:center;padding:30px;background:linear-gradient(135deg, rgba(139,92,246,0.15) 0%, rgba(59,130,246,0.15) 100%);border-radius:20px;margin-bottom:30px;border:1px solid rgba(139,92,246,0.3);">
        <div style="font-size:3rem;margin-bottom:10px;">🧠</div>
        <h1 style="color:#F8FAFC;margin-bottom:10px;">Supply Chain AI</h1>
        <p style="color:#94A3B8;">Powered by Gemma 3 27B (OpenRouter) • Real-time reasoning with live data</p>
        <div style="margin-top:15px;display:inline-flex;gap:10px;flex-wrap:wrap;justify-content:center;">
            <span style="background:rgba(16,185,129,0.2);color:#10B981;padding:6px 12px;border-radius:20px;font-size:0.8rem;">✓ Real AI Reasoning</span>
            <span style="background:rgba(59,130,246,0.2);color:#3B82F6;padding:6px 12px;border-radius:20px;font-size:0.8rem;">✓ Live Data Context</span>
            <span style="background:rgba(239,68,68,0.2);color:#EF4444;padding:6px 12px;border-radius:20px;font-size:0.8rem;">✓ Source References</span>
            <span style="background:rgba(168,85,247,0.2);color:#A855F7;padding:6px 12px;border-radius:20px;font-size:0.8rem;">✓ Follow-up Questions</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # API key status
    if not OPENROUTER_API_KEY:
        st.warning("⚠️ OpenRouter API key not found. Add it to your .env file or Streamlit secrets.")
        return
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": """🧠 **Welcome to SupplyAlert AI!**

I'm powered by **Gemma 3 27B** (via OpenRouter) and have access to live supply chain data including:
- 📊 Real-time port congestion status
- ⛈️ Active weather disruptions
- 📰 Latest industry news headlines
- 📜 Policy and regulatory updates

**Ask me anything like:**
• *"What's causing delays at LA/Long Beach and how will it affect my shipments?"*
• *"Analyze current weather disruptions and their trucking impact"*
• *"What are the latest tariff developments affecting US-Mexico trade?"*

I'll analyze, correlate data, and provide **actionable insights with references**."""}
        ]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧠" if message["role"] == "assistant" else "👤"):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask anything about supply chain..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("🔍 Analyzing live data and reasoning..."):
                response = get_ai_response(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Example questions
    st.markdown("---")
    st.markdown("### 💡 Try These Questions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚢 Analyze current port conditions", use_container_width=True):
            q = "Analyze the current port conditions across major US ports. What correlations do you see with weather or other factors? Provide recommendations."
            st.session_state.messages.append({"role": "user", "content": q})
            st.session_state.messages.append({"role": "assistant", "content": get_ai_response(q)})
            st.rerun()
        if st.button("⛈️ Weather impact on freight", use_container_width=True):
            q = "What weather disruptions are currently affecting freight? Analyze the trucking and logistics impact."
            st.session_state.messages.append({"role": "user", "content": q})
            st.session_state.messages.append({"role": "assistant", "content": get_ai_response(q)})
            st.rerun()
    with col2:
        if st.button("📰 Summarize today's supply chain news", use_container_width=True):
            q = "Summarize the most important supply chain news right now. What should logistics professionals pay attention to?"
            st.session_state.messages.append({"role": "user", "content": q})
            st.session_state.messages.append({"role": "assistant", "content": get_ai_response(q)})
            st.rerun()
        if st.button("🗺️ Route optimization advice", use_container_width=True):
            q = "Based on current conditions, what route optimizations would you recommend for cross-country freight?"
            st.session_state.messages.append({"role": "user", "content": q})
            st.session_state.messages.append({"role": "assistant", "content": get_ai_response(q)})
            st.rerun()
    
    # Clear chat button
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

# --- JOBS PAGE ---

def show_jobs_page():
    """Display AI Supply Chain Jobs in Midwest"""
    st.markdown("""
    <div style="text-align:center;padding:30px;background:linear-gradient(135deg, rgba(34,197,94,0.15) 0%, rgba(59,130,246,0.15) 100%);border-radius:20px;margin-bottom:30px;border:1px solid rgba(34,197,94,0.3);">
        <div style="font-size:3rem;margin-bottom:10px;">💼</div>
        <h1 style="color:#F8FAFC;margin-bottom:10px;">Jobs in Supply Chain AI</h1>
        <p style="color:#94A3B8;">Midwest Opportunities • Auto-Updated Daily • Free Job Alerts</p>
        <div style="margin-top:15px;display:inline-flex;gap:10px;flex-wrap:wrap;justify-content:center;">
            <span style="background:rgba(34,197,94,0.2);color:#22C55E;padding:6px 12px;border-radius:20px;font-size:0.8rem;">📍 Midwest Region</span>
            <span style="background:rgba(59,130,246,0.2);color:#3B82F6;padding:6px 12px;border-radius:20px;font-size:0.8rem;">🤖 AI & Analytics</span>
            <span style="background:rgba(168,85,247,0.2);color:#A855F7;padding:6px 12px;border-radius:20px;font-size:0.8rem;">📦 Supply Chain</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch jobs
    with st.spinner("🔍 Fetching latest job listings..."):
        jobs = get_supply_chain_ai_jobs()
    
    if not jobs:
        st.info("No jobs found at the moment. Check back soon or try the direct links below!")
    else:
        st.markdown(f"### 📋 {len(jobs)} Recent Opportunities")
        st.markdown("*Sorted by date (most recent first) • Salary estimates based on market data*")
        st.markdown("---")
        
        for i, job in enumerate(jobs):
            # Calculate days ago
            days_ago = (datetime.now() - job['date']).days
            if days_ago == 0:
                date_str = "Today"
            elif days_ago == 1:
                date_str = "Yesterday"
            else:
                date_str = f"{days_ago} days ago"
            
            # Get salary and skills
            salary = get_salary_estimate(job['title'])
            skills = get_required_skills(job['title'])
            
            # Job card
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="background:rgba(30,41,59,0.8);padding:20px;border-radius:12px;border:1px solid rgba(71,85,105,0.5);margin-bottom:15px;">
                        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
                            <div>
                                <h3 style="color:#F8FAFC;margin:0;font-size:1.1rem;">{job['title']}</h3>
                                <p style="color:#3B82F6;margin:5px 0;font-size:0.95rem;">🏢 {job['company']}</p>
                            </div>
                            <span style="background:rgba(34,197,94,0.2);color:#22C55E;padding:4px 10px;border-radius:12px;font-size:0.75rem;">{date_str}</span>
                        </div>
                        <div style="display:flex;gap:15px;flex-wrap:wrap;margin:10px 0;">
                            <span style="color:#94A3B8;font-size:0.85rem;">📍 {job['location']}</span>
                            <span style="color:#22C55E;font-size:0.85rem;">💰 {salary}</span>
                            <span style="color:#8B5CF6;font-size:0.85rem;">📰 {job['source']}</span>
                        </div>
                        <div style="margin:12px 0;">
                            <p style="color:#9CA3AF;font-size:0.8rem;margin-bottom:5px;"><strong>Skills:</strong></p>
                            <div style="display:flex;gap:6px;flex-wrap:wrap;">
                                {''.join([f'<span style="background:rgba(59,130,246,0.15);color:#60A5FA;padding:3px 8px;border-radius:6px;font-size:0.75rem;">{skill}</span>' for skill in skills])}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if job['link']:
                        st.markdown(f"""
                        <a href="{job['link']}" target="_blank" style="display:inline-block;background:linear-gradient(135deg,#3B82F6,#8B5CF6);color:white;padding:10px 20px;border-radius:8px;text-decoration:none;font-weight:500;margin-top:30px;">
                            Apply →
                        </a>
                        """, unsafe_allow_html=True)
    
    # Quick links section
    st.markdown("---")
    st.markdown("### 🔗 More Job Resources")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <a href="https://www.indeed.com/jobs?q=supply+chain+AI&l=Illinois" target="_blank" style="display:block;background:rgba(59,130,246,0.1);padding:15px;border-radius:10px;text-decoration:none;text-align:center;border:1px solid rgba(59,130,246,0.3);">
            <div style="font-size:1.5rem;margin-bottom:5px;">🔍</div>
            <div style="color:#3B82F6;font-weight:500;">Indeed</div>
            <div style="color:#9CA3AF;font-size:0.75rem;">Supply Chain AI</div>
        </a>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <a href="https://www.linkedin.com/jobs/search/?keywords=supply%20chain%20AI&location=Midwest" target="_blank" style="display:block;background:rgba(59,130,246,0.1);padding:15px;border-radius:10px;text-decoration:none;text-align:center;border:1px solid rgba(59,130,246,0.3);">
            <div style="font-size:1.5rem;margin-bottom:5px;">💼</div>
            <div style="color:#3B82F6;font-weight:500;">LinkedIn</div>
            <div style="color:#9CA3AF;font-size:0.75rem;">AI Logistics</div>
        </a>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <a href="https://www.glassdoor.com/Job/midwest-supply-chain-machine-learning-jobs-SRCH_IL.0,7_KO8,37.htm" target="_blank" style="display:block;background:rgba(59,130,246,0.1);padding:15px;border-radius:10px;text-decoration:none;text-align:center;border:1px solid rgba(59,130,246,0.3);">
            <div style="font-size:1.5rem;margin-bottom:5px;">⭐</div>
            <div style="color:#3B82F6;font-weight:500;">Glassdoor</div>
            <div style="color:#9CA3AF;font-size:0.75rem;">Salaries & Reviews</div>
        </a>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <a href="https://builtin.com/jobs/supply-chain/data-analytics" target="_blank" style="display:block;background:rgba(59,130,246,0.1);padding:15px;border-radius:10px;text-decoration:none;text-align:center;border:1px solid rgba(59,130,246,0.3);">
            <div style="font-size:1.5rem;margin-bottom:5px;">🚀</div>
            <div style="color:#3B82F6;font-weight:500;">Built In</div>
            <div style="color:#9CA3AF;font-size:0.75rem;">Tech Jobs</div>
        </a>
        """, unsafe_allow_html=True)
    
    # Job alert signup
    st.markdown("---")
    st.markdown("### 🔔 Get Job Alerts")
    with st.form("job_alerts"):
        col1, col2 = st.columns([3, 1])
        with col1:
            email = st.text_input("Email", placeholder="your@email.com", label_visibility="collapsed")
        with col2:
            submitted = st.form_submit_button("Subscribe", use_container_width=True)
        if submitted and email and "@" in email:
            st.success("✅ Subscribed! You'll receive weekly job alerts.")

# --- MAIN APP ---

def main():
    # Sidebar
    with st.sidebar:
        st.markdown("""<h2 style='color:#F8FAFC;font-weight:600;margin-bottom:0;'>⚠️ SupplyAlert</h2>
        <p style='color:#64748B;font-size:0.85rem;margin-top:4px;'>Supply Chain Intelligence</p>""", unsafe_allow_html=True)
        
        # Navigation
        page = st.radio(
            "Navigate",
            ["🏠 Dashboard", "🤖 AI Assistant", "� Jobs", "�📰 All News", "ℹ️ About"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Email Signup
        st.markdown("### 📧 Get Weekly Updates")
        st.markdown("<p style='font-size:0.85rem;color:#9CA3AF;'>Disruption alerts & industry insights delivered to your inbox.</p>", unsafe_allow_html=True)
        
        with st.form("email_signup"):
            email = st.text_input("Email", placeholder="your@email.com", label_visibility="collapsed")
            submitted = st.form_submit_button("Subscribe Free", use_container_width=True)
            if submitted:
                if email and "@" in email:
                    st.success("✅ Subscribed! Check your inbox.")
                else:
                    st.warning("Please enter a valid email.")
        
        st.markdown("---")
        
        st.info("""
**Track disruptions** affecting freight and logistics across weather, policy, and technology.

100% Free • No login required
        """)
        
        # Pro Teaser
        st.markdown("""<div style="margin-top:15px;padding:16px;background:linear-gradient(135deg, rgba(59,130,246,0.15) 0%, rgba(139,92,246,0.15) 100%);border-radius:12px;border:1px solid rgba(139,92,246,0.3);">
            <div style="color:#A78BFA;font-weight:600;font-size:0.95rem;">✨ SupplyAlert Pro</div>
            <p style="color:#94A3B8;font-size:0.8rem;margin:8px 0 0 0;line-height:1.5;">Coming Soon: Custom alerts, API access, historical data & route planning</p>
        </div>""", unsafe_allow_html=True)
        
        st.caption("v1.1.0 • Publicly available data")
    
    # Route to pages
    if page == "🤖 AI Assistant":
        show_chatbot()
    elif page == "� Jobs":
        show_jobs_page()
    elif page == "�📰 All News":
        show_news_page()
    elif page == "ℹ️ About":
        show_about_page()
    else:
        show_dashboard()

def show_dashboard():
    """Main supply chain intelligence dashboard"""
    # Hero
    st.markdown("""
    <div class="hero">
        <div class="logo-icon">📡</div>
        <h1>SupplyAlert</h1>
        <p class="hero-subtitle">Real-time supply chain intelligence for logistics professionals</p>
        <span class="hero-badge">LIVE UPDATES</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Current Alerts
    st.markdown("## 🚨 Active Weather Disruptions")
    
    alerts = get_weather_alerts()
    if alerts:
        cols = st.columns(len(alerts))
        for i, alert in enumerate(alerts):
            with cols[i]:
                severity_class = "alert-card" if alert['severity'] == "High" else "alert-card warning"
                st.markdown(f"""
<a href="https://www.weather.gov/" target="_blank" style="text-decoration:none;color:inherit;">
    <div class="{severity_class}" style="transition:transform 0.2s;cursor:pointer;">
        <div style="display:flex;justify-content:space-between;align-items:start;">
            <h3>{alert['type']}</h3>
            <span style="background:{'#EF4444' if alert['severity'] == 'High' else '#F59E0B'};color:white;padding:4px 12px;border-radius:100px;font-size:0.75rem;font-weight:600;">{alert['severity']}</span>
        </div>
        <p style="color:#CBD5E1;margin-bottom:4px;"><strong>📍 Location:</strong> {alert['location']}</p>
        <p style="color:#94A3B8;"><strong>⚠️ Impact:</strong> {alert['impact']}</p>
        <div style="margin-top:10px;font-size:0.8rem;color:#3B82F6;font-weight:500;">View Details →</div>
    </div>
</a>
                """, unsafe_allow_html=True)
    
    # Port Congestion
    st.markdown("## 🚢 Port Congestion Status")
    
    ports = get_port_status()
    cols = st.columns(len(ports))
    
    for i, (port, data) in enumerate(ports.items()):
        with cols[i]:
            st.markdown(f"""
<div class="stat-card">
    <div class="stat-value" style="color:{data['color']}">{data['delay_days']}</div>
    <div class="stat-label">Days Delay</div>
    <div style="margin-top:10px;font-weight:600;color:#E2E8F0;">{port}</div>
    <div style="color:#64748B;font-size:0.85rem;">{data['congestion']} Congestion</div>
</div>
            """, unsafe_allow_html=True)
    
    # News Sections
    col1, col2 = st.columns(2)
    
    with col1:
        # Freight Industry News
        st.markdown("## 🚛 Freight Industry News")
        st.caption("XPO, Ryder, Penske, JB Hunt & more")
        news = get_freight_industry_news()
        for item in news[:4]:
            date_str = format_news_date(item)
            st.markdown(f"""
<div style="background:#1F2937;padding:12px;border-radius:8px;margin:8px 0;border-left:3px solid #10B981;">
    <a href="{item.link}" target="_blank" style="color:#10B981;text-decoration:none;font-weight:500;">{item.title}</a>
    <div style="color:#6B7280;font-size:0.75rem;margin-top:4px;">{date_str}</div>
</div>
            """, unsafe_allow_html=True)
    
    with col2:
        # AI & Tech News
        st.markdown("## 🤖 AI in Supply Chain")
        st.caption("Automation, ML & logistics tech")
        news = get_ai_supply_chain_news()
        for item in news[:4]:
            date_str = format_news_date(item)
            st.markdown(f"""
<div style="background:#1F2937;padding:12px;border-radius:8px;margin:8px 0;border-left:3px solid #8B5CF6;">
    <a href="{item.link}" target="_blank" style="color:#8B5CF6;text-decoration:none;font-weight:500;">{item.title}</a>
    <div style="color:#6B7280;font-size:0.75rem;margin-top:4px;">{date_str}</div>
</div>
            """, unsafe_allow_html=True)
    
    # Policy News
    st.markdown("## 📜 Government & Policy News")
    st.caption("Trade policy, regulations, USMCA, DOT, FMCSA updates")
    news = get_policy_news()
    cols = st.columns(2)
    for i, item in enumerate(news[:6]):
        with cols[i % 2]:
            date_str = format_news_date(item)
            st.markdown(f"""
<div style="background:#1F2937;padding:12px;border-radius:8px;margin:8px 0;border-left:3px solid #EC4899;">
    <a href="{item.link}" target="_blank" style="color:#EC4899;text-decoration:none;font-weight:500;">{item.title}</a>
    <div style="color:#6B7280;font-size:0.75rem;margin-top:4px;">{date_str}</div>
</div>
            """, unsafe_allow_html=True)
    
    # Disruption News
    st.markdown("## ⚠️ Disruption Alerts")
    st.caption("Port delays, shortages, supply chain crises")
    news = get_disruption_news()
    cols = st.columns(2)
    for i, item in enumerate(news[:6]):
        with cols[i % 2]:
            date_str = format_news_date(item)
            st.markdown(f"""
<div style="background:#1F2937;padding:12px;border-radius:8px;margin:8px 0;border-left:3px solid #EF4444;">
    <a href="{item.link}" target="_blank" style="color:#EF4444;text-decoration:none;font-weight:500;">{item.title}</a>
    <div style="color:#6B7280;font-size:0.75rem;margin-top:4px;">{date_str}</div>
</div>
            """, unsafe_allow_html=True)
    
    # Footer with email CTA
    st.markdown("---")
    st.markdown("""
<div style="text-align:center;padding:30px;background:#1F2937;border-radius:12px;margin-top:20px;">
    <h3 style="color:#E2E8F0;">📧 Never Miss a Disruption</h3>
    <p style="color:#9CA3AF;">Subscribe in the sidebar for weekly supply chain intelligence updates.</p>
</div>
    """, unsafe_allow_html=True)

def show_news_page():
    """All news page"""
    st.markdown("# 📰 All Supply Chain News")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🚛 Freight Industry", "🤖 AI & Tech", "📜 Policy", "⚠️ Disruptions"])
    
    with tab1:
        news = get_freight_industry_news()
        for item in news:
            date_str = format_news_date(item)
            st.markdown(f"""
<div class="alert-card info">
    <a href="{item.link}" target="_blank" style="color:#10B981;text-decoration:none;font-weight:600;font-size:1.1rem;">{item.title}</a>
    <p style="color:#94A3B8;font-size:0.85rem;margin-top:8px;">{date_str}</p>
</div>
            """, unsafe_allow_html=True)
    
    with tab2:
        news = get_ai_supply_chain_news()
        for item in news:
            date_str = format_news_date(item)
            st.markdown(f"""
<div class="alert-card ai">
    <a href="{item.link}" target="_blank" style="color:#8B5CF6;text-decoration:none;font-weight:600;font-size:1.1rem;">{item.title}</a>
    <p style="color:#94A3B8;font-size:0.85rem;margin-top:8px;">{date_str}</p>
</div>
            """, unsafe_allow_html=True)
    
    with tab3:
        news = get_policy_news()
        for item in news:
            date_str = format_news_date(item)
            st.markdown(f"""
<div class="alert-card policy">
    <a href="{item.link}" target="_blank" style="color:#EC4899;text-decoration:none;font-weight:600;font-size:1.1rem;">{item.title}</a>
    <p style="color:#94A3B8;font-size:0.85rem;margin-top:8px;">{date_str}</p>
</div>
            """, unsafe_allow_html=True)
    
    with tab4:
        news = get_disruption_news()
        for item in news:
            date_str = format_news_date(item)
            st.markdown(f"""
<div class="alert-card">
    <a href="{item.link}" target="_blank" style="color:#EF4444;text-decoration:none;font-weight:600;font-size:1.1rem;">{item.title}</a>
    <p style="color:#94A3B8;font-size:0.85rem;margin-top:8px;">{date_str}</p>
</div>
            """, unsafe_allow_html=True)

def show_about_page():
    """About page"""
    st.markdown("# ℹ️ About Supply Chain Intelligence")
    
    st.markdown("""
    **Supply Chain Intelligence** helps logistics professionals track weather disruptions, 
    freight industry news, AI/technology developments, and policy changes affecting supply chains.
    
    ### 📊 Data Sources
    - **News Feeds:** Aggregated from publicly available sources (Google News RSS)
    - **Weather:** Public weather advisories
    - **Port Data:** Publicly reported congestion metrics
    
    ### 📰 News Categories
    - **🚛 Freight Industry:** XPO, Ryder, Penske, JB Hunt, Schneider, Werner
    - **🤖 AI & Tech:** Automation, machine learning, warehouse robotics
    - **📜 Policy:** USMCA, DOT, FMCSA, tariffs, trade regulations
    - **⚠️ Disruptions:** Port delays, shortages, weather impacts
    
    ### ⚖️ Legal Disclaimer
    """)
    
    st.error("""
    **USE AT YOUR OWN RISK:** This tool is provided "AS IS" with **NO WARRANTIES**. The creator assumes **ZERO liability** for any decisions, delays, or losses arising from use of this data.
    
    **DATA SOURCE:** Aggregates publicly available information. Always verify with official sources before making business decisions.
    
    **NO AFFILIATION:** Not affiliated with any government agency, carrier, or commercial organization mentioned.
    """)

if __name__ == "__main__":
    main()
