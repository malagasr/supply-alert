# Freight Weather Intelligence Dashboard - Technical Specification

## 1. Executive Summary
This project delivers a **Streamlit-based Intelligence Dashboard** designed for logistics managers. It aggregates real-time weather data, geopolitical news, and freight-specific impact logic to predict delays and cost surcharges for LTL trucking operations across the Midwest-to-Border (Lisle to Laredo) corridor.

## 2. System Architecture

### 2.1 Tech Stack
-   **Frontend/App Framework**: Streamlit (Python)
-   **Data Processing**: Pandas
-   **Visualization**: Plotly (Maps), Altair (Charts)
-   **API Integration**: `requests`, `feedparser`
-   **Deployment target**: Streamlit Cloud (headless, serverless)

### 2.2 Data Sources (Free/Public)
1.  **Open-Meteo API**:
    -   *Endpoint*: `https://api.open-meteo.com/v1/forecast`
    -   *Data*: Hourly temperature, precipitation, wind speed, weather codes (WMO).
    -   *Coverage*: Global (lat/lon).
    -   *Auth*: None required.
2.  **Google News RSS**:
    -   *Endpoint*: `https://news.google.com/rss/search`
    -   *Data*: Real-time news articles.
    -   *Queries*: "diesel prices", "freight logistics", "border delays", "USMCA trade".
3.  **GDELT (Simulated via RSS for Demo)**:
    -   *Purpose*: Monitor geopolitical stability (protests, policy changes).
    -   *Implementation*: Uses targeted news queries to approximate GDELT Event/GKG data for simplicity in this MVP.

## 3. core Logic: Weather-to-Freight Impact

The application implements a rule-based engine (`calculate_impact`) to translate raw weather metrics into logistics KPIs.

| Weather Condition | Threshold | Impact (Delay) | Impact (Cost Surcharge) | Risk Level |
| :--- | :--- | :--- | :--- | :--- |
| **Snow/Ice** | WMO Codes 71-86 | +4-6 Hours | +5-8% | High/Critical |
| **High Winds** | > 60 km/h | +2 Hours | +2% | Medium |
| **Extreme Winds** | > 80 km/h | +4 Hours | +4% | High |
| **Heavy Rain** | > 20mm or Storms | +1 Hour | +1% | Medium |
| **Extreme Cold** | < -15°C | +1 Hour | +3% (Fuel gelling) | Medium |

## 4. UI/UX Design

### 4.1 Dashboard Page
-   **KPI Cards**: Average Network Delay, Max Risk Level, Corridor Status (Active/Critical).
-   **Interactive Map**: Plotly Scatter Geo map showing corridor nodes colored by risk level.
-   **Active Alerts**: Dynamic text alerts for high-risk locations.

### 4.2 Weather Detail
-   **Location Selector**: Dropdown for specific corridor cities.
-   **Charts**:
    -   Line chart for Temperature & Wind Speed.
    -   Bar chart for Precipitation.
    -   Raw data table.

### 4.3 Geopolitical Risks & News
-   **Risk Monitor**: Accordion-style feed of high-priority risk terms (border delays, tariffs).
-   **News Feed**: Categorized feeds for "Fuel & Energy" and "Regulations".

### 4.4 Impact Report
-   **Summary Table**: Aggregated delays and surcharges per location.
-   **Export**: CSV download functionality for integration with TMS (Transportation Management Systems).

## 5. Deployment Guide
1.  Push `app.py`, `requirements.txt`, and `README.md` to GitHub.
2.  Log in to [share.streamlit.io](https://share.streamlit.io).
3.  Connect repository and select `app.py` as the entry point.
4.  Click **Deploy**.

## 6. Future Roadmap
-   **Refined GDELT**: Integrate strict GDELT 2.0 API for quantitative instability scores.
-   **TMS Integration**: Webhook support to push delay updates directly to Oracle/SAP OTM.
-   **Predictive AI**: Replace rule-based logic with ML model trained on historical lane data.
