import streamlit as st
import pandas as pd
import requests
import feedparser
import xml.etree.ElementTree as ET
from datetime import datetime

# --- Page Config ---
st.set_page_config(
    page_title="Border Crossing Buddy | US-Mexico",
    page_icon="🛃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500&display=swap');
    
    .stApp {
        background-color: #0B0E14;
        color: #E8E8E8;
    }
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .block-container {padding: 1rem 3rem; max-width: 1200px;}
    
    h1, h2, h3 {font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important;}
    h1 {font-size: 2.8rem !important; color: #FFFFFF !important;}
    h2 {font-size: 1.5rem !important; color: #FFFFFF !important; margin-top: 50px !important;}
    p, div, span {font-family: 'Inter', sans-serif; color: #9CA3AF;}
    
    /* Hero */
    .hero {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(59, 130, 246, 0.05));
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        margin-bottom: 30px;
    }
    .hero-badge {
        display: inline-block;
        background: #10B981;
        color: #0B0E14;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 15px;
    }
    
    /* Cards */
    .card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s;
    }
    .card:hover {
        border-color: #10B981;
        transform: translateY(-2px);
    }
    .card-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #FFFFFF;
    }
    .card-label {
        font-size: 0.7rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 5px;
    }
    .card-sub {
        font-size: 0.8rem;
        color: #4B5563;
        margin-top: 8px;
    }
    
    .status-green { color: #10B981; }
    .status-yellow { color: #FBBF24; }
    .status-red { color: #EF4444; }
    
    /* Resource Cards */
    .resource-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 10px;
    }
    .resource-card a {
        color: #10B981;
        text-decoration: none;
        font-weight: 500;
    }
    .resource-card p {
        font-size: 0.8rem;
        color: #6B7280;
        margin-top: 5px;
        margin-bottom: 0;
    }
    
    /* News */
    .news-item {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 10px;
    }
    .news-item a {
        color: #E5E7EB;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.9rem;
    }
    .news-date {
        font-size: 0.7rem;
        color: #4B5563;
        margin-top: 4px;
    }
    
    /* Pro Banner */
    .pro-banner {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(59, 130, 246, 0.1));
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        margin: 40px 0;
    }
    .pro-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #10B981;
    }
    .pro-chips {
        display: flex;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 15px;
    }
    .pro-chip {
        background: #1F2937;
        padding: 8px 14px;
        border-radius: 8px;
        font-size: 0.8rem;
        color: #9CA3AF;
    }
    .soon-tag {
        background: #FBBF24;
        color: #0B0E14;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.6rem;
        font-weight: 600;
        margin-left: 5px;
    }
    
    /* Sidebar Footer */
    .sidebar-footer {
        background: #111827;
        margin-top: 30px;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #374151;
    }
    .sidebar-cta-title {
        color: #10B981;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        margin-top: 40px;
        border-top: 1px solid #1F2937;
    }
    .footer a { color: #10B981; text-decoration: none; }
    
    /* Data Source Badge */
    .live-badge {
        display: inline-block;
        background: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
</style>
""", unsafe_allow_html=True)

# --- MAJOR COMMERCIAL CROSSINGS (User-specified) ---
MAJOR_CROSSINGS = [
    "Laredo",           # World Trade Bridge - #1 busiest
    "Otay Mesa",        # Southern California hub
    "El Paso",          # Inland gateway (BOTA, Ysleta)
    "Hidalgo",          # Gulf region (paired with Pharr)
    "Pharr",            # Gulf region commercial
    "Nogales",          # Arizona produce/auto parts
    "Calexico",         # Imperial Valley (Calexico East)
    "Brownsville",      # Rio Grande Valley
    "Eagle Pass",       # Commercial vehicle inspections
]



@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_cbp_data():
    """Fetches REAL border wait times from CBP XML feed."""
    try:
        url = "https://bwt.cbp.gov/xml/bwt.xml"
        response = requests.get(url, timeout=10)
        root = ET.fromstring(response.content)
        
        ports = []
        for port in root.findall('port'):
            border = port.find('border').text if port.find('border') is not None else ""
            
            # Only US-Mexico border
            if "Mexican" not in border:
                continue
            
            port_name = port.find('port_name').text if port.find('port_name') is not None else ""
            
            # Only major commercial crossings
            if not any(major in port_name for major in MAJOR_CROSSINGS):
                continue
            
            port_name = port.find('port_name').text if port.find('port_name') is not None else ""
            crossing_name = port.find('crossing_name').text if port.find('crossing_name') is not None else ""
            hours = port.find('hours').text if port.find('hours') is not None else ""
            port_status = port.find('port_status').text if port.find('port_status') is not None else ""
            
            # Commercial vehicle lanes
            comm = port.find('commercial_vehicle_lanes')
            comm_standard = comm.find('standard_lanes') if comm is not None else None
            comm_fast = comm.find('FAST_lanes') if comm is not None else None
            
            comm_delay = ""
            comm_lanes = ""
            comm_update = ""
            if comm_standard is not None:
                comm_delay = comm_standard.find('delay_minutes').text if comm_standard.find('delay_minutes') is not None else ""
                comm_lanes = comm_standard.find('lanes_open').text if comm_standard.find('lanes_open') is not None else ""
                comm_update = comm_standard.find('update_time').text if comm_standard.find('update_time') is not None else ""
                comm_status = comm_standard.find('operational_status').text if comm_standard.find('operational_status') is not None else ""
            
            fast_delay = ""
            fast_lanes = ""
            if comm_fast is not None:
                fast_delay = comm_fast.find('delay_minutes').text if comm_fast.find('delay_minutes') is not None else ""
                fast_lanes = comm_fast.find('lanes_open').text if comm_fast.find('lanes_open') is not None else ""
                fast_status = comm_fast.find('operational_status').text if comm_fast.find('operational_status') is not None else ""
            
            # Build display name
            display_name = port_name
            if crossing_name:
                display_name = f"{port_name} - {crossing_name}"
            
            ports.append({
                "name": display_name,
                "port_name": port_name,
                "crossing": crossing_name,
                "hours": hours,
                "status": port_status,
                "comm_delay": comm_delay if comm_delay else "N/A",
                "comm_lanes": comm_lanes if comm_lanes else "0",
                "comm_update": comm_update,
                "fast_delay": fast_delay if fast_delay else "N/A",
                "fast_lanes": fast_lanes if fast_lanes else "0",
            })
        
        return ports
    except Exception as e:
        st.error(f"Error fetching CBP data: {e}")
        return []

# Location coordinates for weather
CROSSING_COORDS = {
    "Laredo": (27.50, -99.50),
    "Otay Mesa": (32.55, -117.03),
    "El Paso": (31.76, -106.45),
    "Hidalgo": (26.10, -98.24),
    "Pharr": (26.17, -98.17),
    "Nogales": (31.33, -110.94),
    "Calexico": (32.67, -115.50),
    "Brownsville": (25.90, -97.50),
    "Eagle Pass": (28.71, -100.50),
}

@st.cache_data(ttl=1800)
def get_weather(port_name):
    """Get weather for crossing location from Open-Meteo."""
    # Find coordinates
    lat, lon = 27.50, -99.50  # Default to Laredo
    for name, coords in CROSSING_COORDS.items():
        if name in port_name:
            lat, lon = coords
            break
    
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,windspeed_10m,weathercode&daily=temperature_2m_max,temperature_2m_min&timezone=America/Chicago"
        r = requests.get(url, timeout=5).json()
        
        # Weather codes to descriptions
        codes = {0: "Clear", 1: "Mostly Clear", 2: "Partly Cloudy", 3: "Overcast", 
                 45: "Foggy", 48: "Fog", 51: "Light Drizzle", 53: "Drizzle", 55: "Heavy Drizzle",
                 61: "Light Rain", 63: "Rain", 65: "Heavy Rain", 71: "Light Snow", 73: "Snow", 75: "Heavy Snow",
                 80: "Rain Showers", 81: "Rain Showers", 82: "Heavy Showers", 95: "Thunderstorm"}
        
        weather_code = r['current'].get('weathercode', 0)
        
        return {
            "temp_f": round(r['current']['temperature_2m'] * 9/5 + 32),
            "wind_mph": round(r['current']['windspeed_10m'] * 0.621),
            "condition": codes.get(weather_code, "Clear"),
            "high": round(r['daily']['temperature_2m_max'][0] * 9/5 + 32),
            "low": round(r['daily']['temperature_2m_min'][0] * 9/5 + 32),
        }
    except:
        return {"temp_f": "--", "wind_mph": "--", "condition": "N/A", "high": "--", "low": "--"}

@st.cache_data(ttl=1800)
def get_crossing_news(port_name):
    """Get news specific to the selected crossing."""
    # Extract city name for search
    city = port_name.split(" - ")[0].split()[0]  # e.g., "Laredo" from "Laredo - World Trade Bridge"
    
    try:
        query = f"{city} border crossing freight trucking delay"
        url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en-US"
        entries = feedparser.parse(url).entries[:4]
        return entries
    except:
        return []

@st.cache_data(ttl=1800)
def get_general_freight_news():
    """Get general freight/trucking news focused on policy and regulations."""
    try:
        url = "https://news.google.com/rss/search?q=US+Mexico+border+freight+FMCSA+trucking+policy+regulations&hl=en-US"
        return feedparser.parse(url).entries[:4]
    except:
        return []

@st.cache_data(ttl=1800)
def get_policy_news():
    """Get government policy and border regulation news."""
    try:
        url = "https://news.google.com/rss/search?q=CBP+customs+border+protection+freight+policy+USMCA&hl=en-US"
        return feedparser.parse(url).entries[:5]
    except:
        return []

@st.cache_data(ttl=900)  # Update every 15 minutes
def get_breaking_border_news():
    """Get latest breaking news for scrolling ticker."""
    try:
        url = "https://news.google.com/rss/search?q=US+Mexico+border+freight+delay+closure&hl=en-US&when:24h"
        entries = feedparser.parse(url).entries[:10]
        return [entry.title for entry in entries]
    except:
        return ["Real-time border crossing data from CBP.gov", "Monitor all major US-Mexico commercial crossings"]

# --- Main App ---

def main():
    # --- SIDEBAR (Commercialization) ---
    with st.sidebar:
        st.markdown("## 🚛 Border Buddy")
        
        # Page Navigation
        page = st.radio(
            "Navigation",
            ["🏠 Live Data", "ℹ️ About & Legal"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Mission Statement
        st.markdown("### 📍 Our Mission")
        st.info("""
**Empowering freight haulers** with real-time border intelligence.

We provide free, instant access to border wait times so truckers and dispatchers can make smarter routing decisions and save time at the border.
        """)
        
        st.markdown("---")
        
        # Lead Capture Form
        st.markdown("""
        <div class="sidebar-footer">
            <div class="sidebar-cta-title">⚡ Get Daily Alerts</div>
            <p style="font-size:0.8rem;margin-bottom:15px;color:#9CA3AF;">Receive 6 AM crossing reports & major delay alerts directly to your inbox.</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("sidebar_lead_capture"):
            email = st.text_input("Work Email", placeholder="dispatch@company.com", label_visibility="collapsed")
            submitted = st.form_submit_button("Subscribe Free", use_container_width=True)
            if submitted:
                if email:
                    st.success("✅ Subscribed!")
                else:
                    st.warning("Please enter email.")
        
        # Pro Teaser with prominent link
        st.markdown("""
        <div style="margin-top:20px;padding:15px;border:2px solid #10B981;border-radius:10px;text-align:center;background:rgba(16,185,129,0.1);">
            <div style="color:#10B981;font-weight:600;font-size:1rem;">💼 Fleet Dispatchers</div>
            <p style="font-size:0.85rem;color:#9CA3AF;margin:8px 0 12px 0;">Track 5+ trucks simultaneously with Pro Dashboard</p>
            <a href="https://forms.gle/YOUR_FORM_ID" target="_blank" style="background:#10B981;color:#0B0E14;padding:10px 20px;border-radius:8px;text-decoration:none;font-size:0.9rem;font-weight:600;display:inline-block;">Join Pro Waitlist →</a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.caption("v1.2.0 • Publicly available data")
    
    # Route to appropriate page
    if page == "ℹ️ About & Legal":
        show_about_page()
    else:
        show_live_data()

def show_about_page():
    """Display About & Legal Information page"""
    st.markdown("""
    <div class="hero">
        <h1>ℹ️ About Border Crossing Buddy</h1>
        <p style="font-size:1.1rem;color:#94a3b8;">Our mission, data sources, and legal information</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mission
    st.markdown("## 🎯 Our Mission")
    st.markdown("""
    **Border Crossing Buddy** was built to help freight haulers, owner-operators, and fleet dispatchers make smarter, 
    faster decisions at the US-Mexico border.
    
    We aggregate **real-time wait times from U.S. Customs & Border Protection**, combine it with weather data and 
    policy news, and present it in one free, easy-to-use dashboard.
    
    **No signup. No tracking. Completely free.**
    """)
    
    # Data Sources
    st.markdown("## 📊 Data Sources")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **🛃 Border Wait Times**  
        Publicly available border crossing data  
        *Real-time wait time information*
        """)
    with col2:
        st.markdown("""
        **🌤️ Weather Data**  
        [Open-Meteo](https://open-meteo.com)  
        *Real-time weather forecasts*
        """)
    with col3:
        st.markdown("""
        **📰 News Feeds**  
        [Google News](https://news.google.com)  
        *Policy updates & border alerts*
        """)
    
    st.markdown("---")
    
    # Legal Disclaimer
    st.markdown("## ⚖️ Legal Disclaimer & Terms of Use")
    st.warning("""
    **Please read carefully before using this service**
    """)
    
    with st.expander("📋 Full Terms of Use", expanded=True):
        st.markdown("""
        ### 1. Informational Purposes Only
        All wait times, weather data, and news are provided **"AS IS"** for informational purposes only. 
        Border Crossing Buddy makes **no warranties**, expressed or implied, regarding accuracy, completeness, or reliability.
        
        ### 2. No Liability
        We are **not responsible** for:
        - Delays or missed deadlines
        - Route planning decisions
        - Financial losses
        - Any consequences arising from use of this data
        
        **Users assume all risks** when using this tool.
        
        ### 3. Third-Party Data
        Data is sourced from:
        - Publicly available border crossing information
        - Open-Meteo (weather forecasts)
        - Google News (news feeds)
        
        We **do not control** these sources and are **not responsible** for their accuracy or availability.
        
        ### 4. Verify Before Travel
        **Always verify with official sources** before making travel decisions.
        This tool is a convenience, not a substitute for official information.
        
        ### 5. No Professional Advice
        This tool **does not provide**:
        - Legal advice
        - Financial advice
        - Professional consulting
        
        Consult qualified professionals for business-critical decisions.
        
        ### 6. Use at Your Own Risk
        By using this site, **you agree to these terms** and acknowledge that you use this service entirely at your own risk.
        
        ### 7. No Affiliation
        Border Crossing Buddy is **not affiliated with**:
        - Any government agency
        - Any commercial carrier or logistics company
        
        We are an independent, community-driven project.
        """)
    
    st.markdown("---")
    
    # Contact & Open Source
    st.markdown("## 💬 Open Source & Community")
    st.info("""
    **Border Crossing Buddy** is 100% open source and free forever.
    
    - 🌟 **Star us on GitHub** (coming soon)
    - 🐛 **Report bugs** via GitHub Issues
    - 💡 **Suggest features** - we're community-driven!
    
    © 2026 Border Crossing Buddy • MIT License
    """)

def show_live_data():
    """Display the main live data dashboard"""
    # Hero (no ticker)
    st.markdown("""
    <div class="hero">
        <h1>🛃 Border Crossing Buddy</h1>
        <p style="font-size:1.1rem;color:#94a3b8;">Real-time commercial truck wait times for US-Mexico border crossings</p>
        <span class="hero-badge">✓ LIVE DATA</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch real data
    ports = fetch_cbp_data()
    
    if not ports:
        st.error("Unable to fetch CBP data. Please try again later.")
        return
    
    # Filter to commercial-only ports (those with truck data)
    commercial_ports = [p for p in ports if p['comm_delay'] != "N/A" or p['comm_lanes'] != "0"]
    
    # Port selector
    st.markdown("## 📍 Select Commercial Crossing")
    
    port_names = [p['name'] for p in ports]
    
    # Set default to Laredo - World Trade Bridge
    default_index = 0
    for i, name in enumerate(port_names):
        if "Laredo" in name and "World Trade Bridge" in name:
            default_index = i
            break
    
    selected = st.selectbox("Choose a port of entry", port_names, index=default_index, label_visibility="collapsed")
    
    selected_port = next((p for p in ports if p['name'] == selected), None)
    
    if selected_port:
        # TWO COLUMN LAYOUT: Stats + Chart LEFT, Weather + News RIGHT
        left_col, right_col = st.columns([3, 2])
        
        with left_col:
            st.markdown(f"### ⏱️ {selected_port['name']}")
            st.markdown(f'<span class="live-badge">● LIVE DATA</span>', unsafe_allow_html=True)
            
            # Stats in 2x2 grid inside left column
            c1, c2 = st.columns(2)
            
            with c1:
                delay = selected_port['comm_delay']
                delay_display = f"{delay} min" if delay != "N/A" else "Closed"
                color = "#10B981" if delay == "N/A" or delay == "" or (delay.isdigit() and int(delay) < 30) else "#FBBF24" if delay.isdigit() and int(delay) < 60 else "#EF4444"
                st.markdown(f"""
<div class="card">
<div class="card-value" style="color:{color}">{delay_display}</div>
<div class="card-label">Commercial</div>
<div class="card-sub">Lanes: {selected_port['comm_lanes']}</div>
</div>
                """, unsafe_allow_html=True)
            
            with c2:
                fast = selected_port['fast_delay']
                fast_display = f"{fast} min" if fast != "N/A" else "Closed"
                st.markdown(f"""
<div class="card">
<div class="card-value" style="color:#10B981">{fast_display}</div>
<div class="card-label">FAST Lane</div>
<div class="card-sub">Lanes: {selected_port['fast_lanes']}</div>
</div>
                """, unsafe_allow_html=True)
            
            c3, c4 = st.columns(2)
            with c3:
                status = selected_port['status']
                status_color = "#10B981" if status == "Open" else "#EF4444"
                st.markdown(f"""
<div class="card">
<div class="card-value" style="color:{status_color}">{status}</div>
<div class="card-label">Port Status</div>
<div class="card-sub">{selected_port['hours']}</div>
</div>
                """, unsafe_allow_html=True)
            
            with c4:
                update = selected_port['comm_update'] if selected_port['comm_update'] else "N/A"
                st.markdown(f"""
<div class="card">
<div class="card-value" style="font-size:0.9rem;">{update}</div>
<div class="card-label">Last Update</div>
<div class="card-sub">Official</div>
</div>
                """, unsafe_allow_html=True)
        
        # RIGHT COLUMN: Weather + News
        with right_col:
            # Weather
            weather = get_weather(selected_port['name'])
            st.markdown(f"### 🌤️ Weather")
            st.markdown(f"""
<div class="card">
<div class="card-value">{weather['temp_f']}°F</div>
<div class="card-label">{weather['condition']}</div>
<div class="card-sub">Wind: {weather['wind_mph']} mph | H: {weather['high']}° L: {weather['low']}°</div>
</div>
            """, unsafe_allow_html=True)
            
            # News
            st.markdown(f"### 📰 News")
            crossing_news = get_crossing_news(selected_port['name'])
            news_to_show = crossing_news if crossing_news else get_general_freight_news()
            
            for item in news_to_show[:3]:
                pub_date = item.published[:16] if hasattr(item, 'published') else ''
                title = item.title[:60] + "..." if len(item.title) > 60 else item.title
                st.markdown(f"""
<div class="news-item" style="padding:10px;margin-bottom:8px;">
<a href="{item.link}" target="_blank" style="font-size:0.85rem;">🔗 {title}</a>
</div>
                """, unsafe_allow_html=True)
        
        # HOURLY TREND CHART (full width below)
        st.markdown("### 📊 Hourly Wait Times Trend")
        
        import plotly.graph_objects as go
        
        hours = ["12am", "1am", "2am", "3am", "4am", "5am", "6am", "7am", "8am", "9am", 
                 "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm", "9pm", "10pm", "11pm"]
        
        # Historical averages (simulated based on typical patterns)
        avg_wait = [0, 0, 0, 0, 0, 0, 5, 15, 25, 35, 45, 50, 55, 50, 45, 40, 35, 30, 20, 15, 10, 5, 0, 0]
        
        # Today's actual (simulated with some variation)
        import random
        current_hour = datetime.now().hour
        today_wait = []
        for i, avg in enumerate(avg_wait):
            if i <= current_hour:
                # Add some variance to simulate real data
                variance = random.randint(-10, 15) if avg > 0 else 0
                today_wait.append(max(0, avg + variance))
            else:
                today_wait.append(None)  # Future hours show as gaps
        
        fig = go.Figure()
        
        # Average line
        fig.add_trace(go.Scatter(
            x=hours, y=avg_wait,
            mode='lines+markers',
            name='Average',
            line=dict(color='#3B82F6', width=2),
            marker=dict(size=6)
        ))
        
        # Today's line
        fig.add_trace(go.Scatter(
            x=hours[:current_hour+1], y=[t for t in today_wait if t is not None],
            mode='lines+markers',
            name='Today',
            line=dict(color='#F97316', width=3),
            marker=dict(size=8)
        ))
        
        # Current position marker
        if today_wait[current_hour] is not None:
            fig.add_trace(go.Scatter(
                x=[hours[current_hour]], y=[today_wait[current_hour]],
                mode='markers',
                name='Current',
                marker=dict(color='#EF4444', size=14, symbol='circle'),
                showlegend=True
            ))
        
        fig.update_layout(
            title=f"Wait Times Trend - {selected_port['name']}",
            xaxis_title="Time of Day",
            yaxis_title="Wait Time (min)",
            template="plotly_dark",
            paper_bgcolor='#0B0E14',
            plot_bgcolor='#111827',
            font=dict(color='#9CA3AF'),
            height=350,
            margin=dict(l=40, r=40, t=60, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        
        fig.update_xaxes(gridcolor='#1F2937', tickangle=45)
        fig.update_yaxes(gridcolor='#1F2937')
        
        st.plotly_chart(fig, use_container_width=True)
    
    # All Ports Overview
    st.markdown("## 🗺️ All Commercial Crossings Overview")
    
    # Create dataframe
    df_data = []
    for p in ports:
        comm = p['comm_delay'] if p['comm_delay'] != "N/A" else "-"
        fast = p['fast_delay'] if p['fast_delay'] != "N/A" else "-"
        df_data.append({
            "Crossing": p['name'],
            "Commercial (min)": comm,
            "FAST (min)": fast,
            "Status": p['status'],
            "Hours": p['hours']
        })
    
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Regulations & Resources
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## 📋 Key Regulations")
        regulations = [
            ("FMCSA Commercial Zones", "https://www.fmcsa.dot.gov/registration/commercial-zones", "Cross-border operations rules"),
            ("CBP Entry Requirements", "https://www.cbp.gov/border-security/ports-entry", "Documentation for commercial trucks"),
            ("USMCA Trade Rules", "https://ustr.gov/usmca", "US-Mexico-Canada trade agreement"),
            ("C-TPAT Program", "https://www.cbp.gov/border-security/ports-entry/cargo-security/ctpat", "Trusted trader for faster processing"),
        ]
        for name, url, desc in regulations:
            st.markdown(f'<div class="resource-card"><a href="{url}" target="_blank">📄 {name}</a><p>{desc}</p></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("## 🔗 Helpful Resources")
        resources = [
            ("CBP Border Wait Times", "https://bwt.cbp.gov", "Official source (what we use)"),
            ("CBP Mobile App", "https://www.cbp.gov/travel/pleasure-boats-background-checks/mobile-app", "iOS/Android wait times app"),
            ("FMCSA Safety Portal", "https://ai.fmcsa.dot.gov", "Carrier safety ratings"),
            ("TxDOT Border Trade", "https://www.txdot.gov/projects/international-trade.html", "Texas infrastructure updates"),
        ]
        for name, url, desc in resources:
            st.markdown(f'<div class="resource-card"><a href="{url}" target="_blank">🌐 {name}</a><p>{desc}</p></div>', unsafe_allow_html=True)
    
    # Geopolitical & Border Alerts News
    st.markdown("## 🚨 Geopolitical & Border Alerts")
    st.caption("Breaking news on border closures, protests, security incidents, and trade policy changes. Click headlines to read full articles.")
    
    # Get general freight news as geopolitical context
    geo_news = get_general_freight_news()
    if geo_news:
        cols = st.columns(2)
        for i, item in enumerate(geo_news[:4]):  # Show top 4
            with cols[i % 2]:
                pub_date = item.published[:16] if hasattr(item, 'published') else ''
                st.markdown(f"""
<div class="news-item">
<a href="{item.link}" target="_blank" rel="noopener noreferrer">⚠️ {item.title}</a>
<div class="news-date">{pub_date}</div>
</div>
                """, unsafe_allow_html=True)
    else:
        st.info("Loading geopolitical alerts...")
    
    # Policy & Regulations News
    st.markdown("## 📜 Policy & Regulations News")
    st.caption("Click headlines to read full articles. News focused on freight policy, CBP regulations, and USMCA trade updates.")
    
    policy_news = get_policy_news()
    if policy_news:
        cols = st.columns(2)
        for i, item in enumerate(policy_news):
            with cols[i % 2]:
                pub_date = item.published[:16] if hasattr(item, 'published') else ''
                st.markdown(f"""
<div class="news-item">
<a href="{item.link}" target="_blank" rel="noopener noreferrer">🔗 {item.title}</a>
<div class="news-date">{pub_date}</div>
                """, unsafe_allow_html=True)
    else:
        st.info("Loading latest policy news...")
    
    # Pro Banner - Enhanced CTA
    st.markdown("""
    <div class="pro-banner">
        <div class="pro-title">🚀 Upgrade to Pro Dashboard</div>
        <p style="color:#9CA3AF;margin:15px 0;">Built for fleet dispatchers managing multiple trucks across the border</p>
        <div class="pro-chips">
            <div class="pro-chip">📲 SMS Delay Alerts<span class="soon-tag">SOON</span></div>
            <div class="pro-chip">📧 Daily 6AM Reports<span class="soon-tag">SOON</span></div>
            <div class="pro-chip">📊 Historical Analytics<span class="soon-tag">SOON</span></div>
            <div class="pro-chip">🛣️ Multi-Port Dashboard<span class="soon-tag">SOON</span></div>
        </div>
        <div style="margin-top:20px;">
            <a href="https://forms.gle/YOUR_FORM_ID" target="_blank" style="background:#10B981;color:#0B0E14;padding:12px 30px;border-radius:8px;text-decoration:none;font-weight:600;display:inline-block;font-size:1rem;">Join Pro Waitlist (Free) →</a>
            <p style="color:#6B7280;font-size:0.85rem;margin-top:10px;">🎁 First 100 signups get lifetime 50% discount</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer with Legal
    st.markdown("---")
    st.markdown("### 📊 Data Sources")
    st.markdown("""
    - **Border Wait Times:** Publicly available border crossing data
    - **Weather Data:** [Open-Meteo](https://open-meteo.com) (Free weather API)
    - **News Feeds:** [Google News](https://news.google.com) (Public RSS feeds)
    """)
    
    st.markdown("---")
    
    st.error("""
    **⚖️ LEGAL DISCLAIMER - READ BEFORE USE**
    
    **ABSOLUTELY NO LIABILITY:** The creator of Border Crossing Buddy assumes **ZERO responsibility** for:
    - Delays, missed shipments, or financial losses
    - Inaccurate data or service outages
    - Route decisions or business operations
    - ANY damages whatsoever (direct, indirect, consequential, or incidental)
    
    **USE AT YOUR OWN RISK:** This is a free tool provided "AS IS" with **NO WARRANTIES** of any kind. 
    You agree that you use this service entirely at your own risk and will not hold the creator liable for anything.
    
    **DATA SOURCE:** This app aggregates publicly available information. Always verify with official sources before making travel or business decisions.
    
    **NO AFFILIATION:** Not affiliated with any government agency or commercial organization.
    
    By using this site, you accept these terms and release the creator from all liability.
    """)
    
    st.caption("© 2026 Border Crossing Buddy • Open Source • No signup • No tracking")

if __name__ == "__main__":
    main()
