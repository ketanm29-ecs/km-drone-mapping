import streamlit as st
import pandas as pd
import numpy as np
import folium
import json
import os
from datetime import datetime, timedelta
import anthropic
from typing import Dict, List, Optional, Tuple
import plotly.express as px
import plotly.graph_objects as go
from folium.plugins import MarkerCluster, HeatMap
import tempfile
import io

from dotenv import load_dotenv
load_dotenv('config.env')

# Try to import streamlit_folium, fallback to alternative if not available
try:
    from streamlit_folium import folium_static
except ImportError:
    # Fallback: use st.components.v1.html for folium maps
    def folium_static(fig, width=700, height=500):
        return st.components.v1.html(fig._repr_html_(), width=width, height=height)

# Page configuration
st.set_page_config(
    page_title="Drone Flight Mapper",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for black background and white text
st.markdown("""
<style>
    /* Global styles */
    .stApp {
        background-color: black !important;
        color: white !important;
    }
    
    .main .block-container {
        background-color: black !important;
        color: white !important;
    }
    
    /* Header and navigation */
    .stApp > header {
        background-color: black !important;
        color: white !important;
    }
    
    /* Sidebar */
    .stSidebar {
        background-color: #1a1a1a !important;
        color: white !important;
    }
    
    .stSidebar .sidebar-content {
        background-color: #1a1a1a !important;
        color: white !important;
    }
    
    /* All text elements */
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: white !important;
    }
    
    /* Title styling */
    h1 {
        font-size: 35px !important;
        font-family: 'Arial', 'Helvetica', sans-serif !important;
        font-weight: normal !important;
    }
    
    /* KPI card styling */
    .stMetric {
        background-color: black !important;
        color: white !important;
        border: 1px solid #666 !important;
        border-radius: 8px !important;
        padding: 10px !important;
        margin: 5px !important;
    }
    
    .stMetric > div {
        # border: 1px solid #666 !important;
        # border-radius: 8px !important;
        # padding: 10px !important;
    }
    
    .stMetric > div > div {
        # border: 1px solid #666 !important;
        # border-radius: 8px !important;
        # padding: 10px !important;
    }
    
    /* Form elements */
    .stSelectbox > div > div {
        background-color: #333 !important;
        color: white !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #333 !important;
        color: white !important;
        border: 1px solid #555 !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #333 !important;
        color: white !important;
        border: 1px solid #555 !important;
    }
    
    .stSlider > div > div > div > div {
        background-color: #333 !important;
        color: white !important;
    }
    
    /* Slider handle styling */
    .stSlider [role="slider"] {
        background-color: white !important;
        border: 2px solid #007bff !important;
    }
    
    .stSlider [role="slider"]:hover {
        background-color: white !important;
        border: 2px solid #0056b3 !important;
    }
    
    .stSlider [role="slider"]:focus {
        background-color: white !important;
        border: 2px solid #007bff !important;
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25) !important;
    }
    
    /* Slider track styling */
    .stSlider [role="slider"]::before {
        background-color: #555 !important;
    }
    
    .stSlider [role="slider"]::after {
        background-color: #007bff !important;
    }
    
    /* Alternative slider handle selectors */
    .stSlider .stSlider > div > div > div > div > div {
        background-color: white !important;
        border: 2px solid #007bff !important;
    }
    
    .stSlider .stSlider > div > div > div > div > div:hover {
        background-color: white !important;
        border: 2px solid #0056b3 !important;
    }
    
    /* Streamlit slider specific styling */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: white !important;
        border: 2px solid #007bff !important;
    }
    
    .stSlider [data-baseweb="slider"] [role="slider"]:hover {
        background-color: white !important;
        border: 2px solid #0056b3 !important;
    }
    
    /* Slider thumb/handle */
    .stSlider .stSlider > div > div > div > div > div > div {
        background-color: white !important;
        border: 2px solid #007bff !important;
    }
    
    .stDateInput > div > div > input {
        background-color: #333 !important;
        color: white !important;
        border: 1px solid #555 !important;
    }
    
    .stMultiSelect > div > div > div {
        background-color: #333 !important;
        color: white !important;
    }
    
    /* List box and dropdown text styling */
    .stSelectbox .stSelectbox > div > div > div {
        color: white !important;
    }
    
    .stSelectbox .stSelectbox > div > div > div > div {
        color: white !important;
    }
    
    .stSelectbox .stSelectbox > div > div > div > div > div {
        color: white !important;
    }
    
    /* Multi-select list box text */
    .stMultiSelect .stMultiSelect > div > div > div {
        color: white !important;
    }
    
    .stMultiSelect .stMultiSelect > div > div > div > div {
        color: white !important;
    }
    
    /* Dropdown options text */
    .stSelectbox [data-baseweb="select"] {
        color: white !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        color: white !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div > div {
        color: white !important;
    }
    
    /* Multi-select options text */
    .stMultiSelect [data-baseweb="select"] {
        color: white !important;
    }
    
    .stMultiSelect [data-baseweb="select"] > div {
        color: white !important;
    }
    
    .stMultiSelect [data-baseweb="select"] > div > div {
        color: white !important;
    }
    
    /* Dropdown menu items */
    .stSelectbox [role="listbox"] {
        background-color: #333 !important;
        color: white !important;
    }
    
    .stSelectbox [role="listbox"] [role="option"] {
        background-color: #333 !important;
        color: white !important;
    }
    
    .stSelectbox [role="listbox"] [role="option"]:hover {
        background-color: #555 !important;
        color: white !important;
    }
    
    /* Multi-select menu items */
    .stMultiSelect [role="listbox"] {
        background-color: #333 !important;
        color: white !important;
    }
    
    .stMultiSelect [role="listbox"] [role="option"] {
        background-color: #333 !important;
        color: white !important;
    }
    
    .stMultiSelect [role="listbox"] [role="option"]:hover {
        background-color: #555 !important;
        color: white !important;
    }
    
    /* Selected items in multi-select */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #555 !important;
        color: white !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] > span {
        color: white !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #007bff !important;
        color: white !important;
        border: 1px solid #007bff !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: block !important;
    }
    
    .stButton > button:hover {
        background-color: #0056b3 !important;
        color: white !important;
        opacity: 1 !important;
    }
    
    /* Ensure all buttons are visible */
    button {
        background-color: #007bff !important;
        color: white !important;
        border: 1px solid #007bff !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: inline-block !important;
    }
    
    button:hover {
        background-color: #0056b3 !important;
        color: white !important;
        opacity: 1 !important;
    }
    
    /* Primary buttons */
    .stButton > button[data-testid="baseButton-primary"] {
        background-color: #007bff !important;
        color: white !important;
        border: 1px solid #007bff !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Secondary buttons */
    .stButton > button[data-testid="baseButton-secondary"] {
        background-color: #6c757d !important;
        color: white !important;
        border: 1px solid #6c757d !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Data displays */
    .stDataFrame {
        background-color: #333 !important;
        color: white !important;
    }
    
    .stMetric {
        background-color: black !important;
        color: white !important;
    }
    
    .stJson {
        background-color: #333 !important;
        color: white !important;
    }
    
    .stExpander {
        background-color: #333 !important;
        color: white !important;
    }
    
    /* Tables */
    .stDataFrame table {
        background-color: #333 !important;
        color: white !important;
    }
    
    .stDataFrame th {
        background-color: #555 !important;
        color: white !important;
    }
    
    .stDataFrame td {
        background-color: #333 !important;
        color: white !important;
    }
    
    /* Alert messages - keep minimal styling */
    .stInfo {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #007bff !important;
    }
    
    .stSuccess {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #28a745 !important;
    }
    
    .stWarning {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #ffc107 !important;
    }
    
    .stError {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #dc3545 !important;
    }
    
    /* Markdown content */
    .stMarkdown {
        background-color: black !important;
        color: white !important;
    }
    
    /* File uploader */
    .stFileUploader {
        background-color: #333 !important;
        color: white !important;
    }
    
    /* Checkbox and radio */
    .stCheckbox {
        background-color: black !important;
        color: white !important;
    }
    
    .stRadio {
        background-color: black !important;
        color: white !important;
    }
    
    /* Progress bar */
    .stProgress {
        background-color: #333 !important;
    }
    
    /* Code blocks */
    .stCode {
        background-color: #1a1a1a !important;
        color: white !important;
    }
    
    /* Override any dark theme elements */
    [data-testid="stAppViewContainer"] {
        background-color: black !important;
        color: white !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
        color: white !important;
    }
    
    [data-testid="stHeader"] {
        background-color: black !important;
        color: white !important;
    }
    
    /* Additional dark theme overrides */
    .stApp > div {
        background-color: black !important;
        color: white !important;
    }
    
    .stApp > div > div {
        background-color: black !important;
        color: white !important;
    }
    
    /* Ensure all text is white */
    * {
        color: white !important;
    }
    
    /* Override specific elements that might have different colors */
    .stSelectbox label,
    .stMultiSelect label,
    .stTextInput label,
    .stTextArea label,
    .stDateInput label,
    .stSlider label,
    .stCheckbox label,
    .stRadio label {
        color: white !important;
    }
    
    /* Button text visibility */
    .stButton > button > div {
        color: white !important;
    }
    
    .stButton > button > div > div {
        color: white !important;
    }
    
    /* Ensure button text is white and visible */
    .stButton > button * {
        color: white !important;
    }
    
    /* Button container visibility */
    .stButton {
        opacity: 1 !important;
        visibility: visible !important;
        display: block !important;
    }
    
    /* Fix any hidden buttons */
    .stButton[style*="display: none"] {
        display: block !important;
    }
    
    .stButton[style*="visibility: hidden"] {
        visibility: visible !important;
    }
    
    .stButton[style*="opacity: 0"] {
        opacity: 1 !important;
    }
</style>
""", unsafe_allow_html=True)

# Constants
MEXICO_BOUNDS = {
    'north': 32.7183,
    'south': 14.5344,
    'east': -86.5964,
    'west': -118.5989
}

US_BOUNDS = {
    'north': 49.3844,
    'south': 24.3963,
    'east': -66.9346,
    'west': -125.0000
}

# Initialize Anthropic client
@st.cache_resource
def get_anthropic_client():
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        st.error("ANTHROPIC_API_KEY environment variable not set")
        return None
    return anthropic.Anthropic(api_key=api_key)

# Data processing functions
@st.cache_data
def load_and_process_csv(uploaded_file):
    """Load CSV and perform initial data processing"""
    try:
        df = pd.read_csv(uploaded_file)
        required_columns = [
            'flight_id', 'origin_city', 'origin_lat', 'origin_lon',
            'dest_city', 'dest_lat', 'dest_lon', 'timestamp', 'speed_kts', 'altitude_ft'
        ]
        
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {missing_cols}")
            return None
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Ensure numeric columns
        numeric_cols = ['origin_lat', 'origin_lon', 'dest_lat', 'dest_lon', 'speed_kts', 'altitude_ft']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove rows with invalid coordinates
        df = df.dropna(subset=['origin_lat', 'origin_lon', 'dest_lat', 'dest_lon'])
        
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {str(e)}")
        return None

def apply_filters(df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
    """Apply filters to the dataframe"""
    filtered_df = df.copy()
    
    if filters.get('time_range'):
        start_time, end_time = filters['time_range']
        filtered_df = filtered_df[
            (filtered_df['timestamp'] >= start_time) & 
            (filtered_df['timestamp'] <= end_time)
        ]
    
    if filters.get('altitude_range'):
        min_alt, max_alt = filters['altitude_range']
        filtered_df = filtered_df[
            (filtered_df['altitude_ft'] >= min_alt) & 
            (filtered_df['altitude_ft'] <= max_alt)
        ]
    
    if filters.get('speed_range'):
        min_speed, max_speed = filters['speed_range']
        filtered_df = filtered_df[
            (filtered_df['speed_kts'] >= min_speed) & 
            (filtered_df['speed_kts'] <= max_speed)
        ]
    
    if filters.get('destinations'):
        if 'mexico' in filters['destinations']:
            filtered_df = filtered_df[
                (filtered_df['dest_lat'] >= MEXICO_BOUNDS['south']) &
                (filtered_df['dest_lat'] <= MEXICO_BOUNDS['north']) &
                (filtered_df['dest_lon'] >= MEXICO_BOUNDS['west']) &
                (filtered_df['dest_lon'] <= MEXICO_BOUNDS['east'])
            ]
        if 'us' in filters['destinations']:
            filtered_df = filtered_df[
                (filtered_df['dest_lat'] >= US_BOUNDS['south']) &
                (filtered_df['dest_lat'] <= US_BOUNDS['north']) &
                (filtered_df['dest_lon'] >= US_BOUNDS['west']) &
                (filtered_df['dest_lon'] <= US_BOUNDS['east'])
            ]
    
    if filters.get('origin_cities'):
        filtered_df = filtered_df[filtered_df['origin_city'].isin(filters['origin_cities'])]
    
    if filters.get('dest_cities'):
        filtered_df = filtered_df[filtered_df['dest_city'].isin(filters['dest_cities'])]
    
    return filtered_df

def create_map(df: pd.DataFrame, show_flows: bool = True, show_markers: bool = True) -> folium.Map:
    """Create the main map with layers"""
    # Calculate center
    center_lat = (df['origin_lat'].mean() + df['dest_lat'].mean()) / 2
    center_lon = (df['origin_lon'].mean() + df['dest_lon'].mean()) / 2
    
    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6,
        tiles='CartoDB positron'
    )
    
    # Add tile layer control
    folium.TileLayer('CartoDB positron', name='Light').add_to(m)
    folium.TileLayer('CartoDB dark_matter', name='Dark').add_to(m)
    folium.TileLayer('OpenStreetMap', name='Street').add_to(m)
    
    # Layer A: Destination Heatmap
    if not df.empty:
        heatmap_data = df[['dest_lat', 'dest_lon', 'altitude_ft']].values.tolist()
        HeatMap(
            heatmap_data,
            name='Destination Heatmap',
            radius=20,
            blur=15,
            max_zoom=13
        ).add_to(m)
    
    # Layer B: Flow Lines (sampled for performance)
    if show_flows and not df.empty:
        # Sample data for performance
        sample_size = min(1000, len(df))
        sample_df = df.sample(n=sample_size, random_state=42)
        
        for _, row in sample_df.iterrows():
            # Create curved line
            points = [
                [row['origin_lat'], row['origin_lon']],
                [row['dest_lat'], row['dest_lon']]
            ]
            
            folium.PolyLine(
                points,
                color='red',
                weight=2,
                opacity=0.6,
                popup=f"Flight: {row['flight_id']}<br>"
                      f"From: {row['origin_city']}<br>"
                      f"To: {row['dest_city']}<br>"
                      f"Altitude: {row['altitude_ft']:.0f} ft<br>"
                      f"Speed: {row['speed_kts']:.0f} kts"
            ).add_to(m)
    
    # Layer C: Markers (clustered)
    if show_markers and not df.empty:
        marker_cluster = MarkerCluster(name='Flight Markers')
        
        # Sample markers for performance
        marker_sample = df.sample(n=min(500, len(df)), random_state=42)
        
        for _, row in marker_sample.iterrows():
            # Origin marker
            folium.Marker(
                [row['origin_lat'], row['origin_lon']],
                popup=f"<b>Origin</b><br>"
                      f"City: {row['origin_city']}<br>"
                      f"Flight: {row['flight_id']}<br>"
                      f"Time: {row['timestamp'].strftime('%Y-%m-%d %H:%M')}",
                icon=folium.Icon(color='green', icon='plane')
            ).add_to(marker_cluster)
            
            # Destination marker
            folium.Marker(
                [row['dest_lat'], row['dest_lon']],
                popup=f"<b>Destination</b><br>"
                      f"City: {row['dest_city']}<br>"
                      f"Flight: {row['flight_id']}<br>"
                      f"Altitude: {row['altitude_ft']:.0f} ft<br>"
                      f"Speed: {row['speed_kts']:.0f} kts",
                icon=folium.Icon(color='red', icon='flag')
            ).add_to(marker_cluster)
        
        marker_cluster.add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m

def calculate_kpis(df: pd.DataFrame) -> Dict:
    """Calculate key performance indicators"""
    if df.empty:
        return {
            'total_flights': 0,
            'unique_origins': 0,
            'unique_destinations': 0,
            'top_destinations': [],
            'avg_altitude': 0,
            'avg_speed': 0
        }
    
    return {
        'total_flights': len(df),
        'unique_origins': df['origin_city'].nunique(),
        'unique_destinations': df['dest_city'].nunique(),
        'top_destinations': df['dest_city'].value_counts().head(5).to_dict(),
        'avg_altitude': df['altitude_ft'].mean(),
        'avg_speed': df['speed_kts'].mean()
    }

def chat_with_data(user_query: str, df: pd.DataFrame, client) -> Tuple[Dict, str]:
    """Process user query through Anthropic Claude and return structured filters"""
    
    system_prompt = """You are a data-query planner for drone flight data. The user will ask questions about drone flights.
Only return a JSON object matching the schema below. Do not include prose.
You must translate the user's intent into filters over the columns and optional aggregations.
Never execute code or return SQL. Never access external tools.
If a value is unknown, omit the field.

Available columns: flight_id, origin_city, origin_lat, origin_lon, dest_city, dest_lat, dest_lon, timestamp, speed_kts, altitude_ft

Schema:
{
    "filters": {
        "time_range": ["start_datetime", "end_datetime"] (optional),
        "altitude_range": [min_altitude, max_altitude] (optional),
        "speed_range": [min_speed, max_speed] (optional),
        "destinations": ["mexico", "us"] (optional),
        "origin_cities": ["city1", "city2"] (optional),
        "dest_cities": ["city1", "city2"] (optional)
    },
    "aggregation": {
        "type": "count" | "average" | "group_by",
        "column": "column_name" (optional),
        "group_by": "column_name" (optional)
    }
}

Examples:
- "Show flights to Laredo in the last 24 hours above 500 ft" → filters with dest_cities: ["Laredo"], time_range, altitude_range
- "Only destinations in Mexico, altitude < 1000 ft" → filters with destinations: ["mexico"], altitude_range
- "Compare McAllen vs Brownsville by average altitude" → aggregation with group_by: "dest_city" and dest_cities filter"""

    try:
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_query}]
        )
        
        # Extract JSON from response
        content = response.content[0].text
        try:
            # Try to parse the JSON response
            parsed_response = json.loads(content)
            return parsed_response, "success"
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                try:
                    parsed_response = json.loads(json_match.group())
                    return parsed_response, "success"
                except:
                    pass
            
            return {}, f"Failed to parse LLM response: {content}"
            
    except Exception as e:
        return {}, f"Error communicating with Anthropic: {str(e)}"

def reset_all_filters():
    """Reset all filters and chat history"""
    st.session_state.filters = {}
    st.session_state.applied_filters = {}
    st.session_state.chat_history = []

def main():
    st.title("ECS Demo - Cross-Border Drone Flight Mapper")
    st.markdown("Visualize and analyze drone flight data with AI-powered chat filtering")
    
    # Initialize session state
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'filters' not in st.session_state:
        st.session_state.filters = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'applied_filters' not in st.session_state:
        st.session_state.applied_filters = {}
    
    # Sidebar
    with st.sidebar:
        st.header("📁 Data Upload")
        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=['csv'],
            help="Upload a CSV with columns: flight_id, origin_city, origin_lat, origin_lon, dest_city, dest_lat, dest_lon, timestamp, speed_kts, altitude_ft"
        )
        
        if uploaded_file is not None:
            if st.session_state.data is None:
                with st.spinner("Processing CSV..."):
                    st.session_state.data = load_and_process_csv(uploaded_file)
            
            if st.session_state.data is not None:
                st.success(f"✅ Loaded {len(st.session_state.data)} flights")
                
                # Manual filters
                st.header("🔍 Manual Filters")
                
                # Time range filter
                if st.session_state.data is not None:
                    min_time = st.session_state.data['timestamp'].min()
                    max_time = st.session_state.data['timestamp'].max()
                    
                    time_range = st.date_input(
                        "Time Range",
                        value=(min_time.date(), max_time.date()),
                        min_value=min_time.date(),
                        max_value=max_time.date()
                    )
                    
                    if len(time_range) == 2:
                        start_time = datetime.combine(time_range[0], datetime.min.time())
                        end_time = datetime.combine(time_range[1], datetime.max.time())
                        st.session_state.filters['time_range'] = [start_time, end_time]
                
                # Altitude range
                if st.session_state.data is not None:
                    min_alt = float(st.session_state.data['altitude_ft'].min())
                    max_alt = float(st.session_state.data['altitude_ft'].max())
                    
                    altitude_range = st.slider(
                        "Altitude Range (ft)",
                        min_value=min_alt,
                        max_value=max_alt,
                        value=(min_alt, max_alt)
                    )
                    st.session_state.filters['altitude_range'] = altitude_range
                
                # Speed range
                if st.session_state.data is not None:
                    min_speed = float(st.session_state.data['speed_kts'].min())
                    max_speed = float(st.session_state.data['speed_kts'].max())
                    
                    speed_range = st.slider(
                        "Speed Range (kts)",
                        min_value=min_speed,
                        max_value=max_speed,
                        value=(min_speed, max_speed)
                    )
                    st.session_state.filters['speed_range'] = speed_range
                
                # Destination filter
                destinations = st.multiselect(
                    "Destinations",
                    options=["mexico", "us"],
                    default=["mexico", "us"]
                )
                if destinations:
                    st.session_state.filters['destinations'] = destinations
                
                # City filters
                if st.session_state.data is not None:
                    origin_cities = st.multiselect(
                        "Origin Cities",
                        options=sorted(st.session_state.data['origin_city'].unique())
                    )
                    if origin_cities:
                        st.session_state.filters['origin_cities'] = origin_cities
                    
                    dest_cities = st.multiselect(
                        "Destination Cities",
                        options=sorted(st.session_state.data['dest_city'].unique())
                    )
                    if dest_cities:
                        st.session_state.filters['dest_cities'] = dest_cities
                
                # Map display options
                st.header("🗺️ Map Options")
                show_flows = st.checkbox("Show Flow Lines", value=True)
                show_markers = st.checkbox("Show Markers", value=True)
                
                # Reset and Quick preset chips
                st.header("🔄 Reset & Quick Presets")
                
                # Reset button - prominent placement
                if st.button("🔄 Reset All Filters", type="primary", use_container_width=True):
                    reset_all_filters()
                    st.rerun()
                
    # Main content
    if st.session_state.data is not None:
        
        
        # Map
        st.subheader("🗺️ Flight Map")
       # Apply filters
        filtered_data = apply_filters(st.session_state.data, st.session_state.filters)
         
        # Create map
        map_obj = create_map(
            filtered_data,
            show_flows=show_flows if 'show_flows' in locals() else True,
            show_markers=show_markers if 'show_markers' in locals() else True
        )
        
        # Display map
        folium_static(map_obj, width=1200, height=600)
        
        
        # Calculate KPIs
        kpis = calculate_kpis(filtered_data)
        
        # KPI Cards with Reset Button
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        
        with col1:
            st.metric("Total Flights", f"{kpis['total_flights']:,}")
        
        with col2:
            st.metric("Unique Origins", f"{kpis['unique_origins']:,}")
        
        with col3:
            st.metric("Unique Destinations", f"{kpis['unique_destinations']:,}")
        
        with col4:
            st.metric("Avg Altitude", f"{kpis['avg_altitude']:.0f} ft")
        
        with col5:
            st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
            if st.button("🔄 Reset Data", help="Reset all filters", key="reset_main"):
                reset_all_filters()
                st.rerun()
        
        # Top destinations
        if kpis['top_destinations']:
            st.subheader("Top 5 Destination Cities")
            dest_cols = st.columns(len(kpis['top_destinations']))
            for i, (city, count) in enumerate(kpis['top_destinations'].items()):
                with dest_cols[i]:
                    st.metric(city, f"{count:,}")

        # Chat with Data
        st.subheader("💬 Chat with Your Data")
        st.markdown("Ask questions about your data in natural language!")
        
        # Chat input
        user_query = st.text_input(
            "Ask a question about your data:",
            placeholder="e.g., 'Show flights to Laredo in the last 24 hours above 500 ft'"
        )
        
        # Always show the Ask button
        col1, col2 = st.columns([1, 4])
        with col1:
            ask_clicked = st.button("Ask", type="primary", disabled=not user_query.strip())
        
        if ask_clicked and user_query.strip():
            client = get_anthropic_client()
            if client:
                with st.spinner("Processing your question..."):
                    response, status = chat_with_data(user_query, filtered_data, client)
                    
                    if status == "success" and response:
                        # Apply filters from chat
                        if 'filters' in response:
                            st.session_state.filters.update(response['filters'])
                            st.session_state.applied_filters = response['filters']
                            st.success("✅ Applied filters from chat!")
                            st.rerun()
                        
                        # Show response
                        st.json(response)
                        
                        # Add to chat history
                        st.session_state.chat_history.append({
                            'user': user_query,
                            'assistant': response,
                            'timestamp': datetime.now()
                        })
                    else:
                        st.error(f"❌ {status}")
            else:
                st.error("Anthropic client not available. Please set ANTHROPIC_API_KEY environment variable.")
        
        # Chat history
        if st.session_state.chat_history:
            st.subheader("📝 Chat History")
            for chat in reversed(st.session_state.chat_history[-5:]):  # Show last 5
                with st.expander(f"Q: {chat['user'][:50]}..."):
                    st.write(f"**User:** {chat['user']}")
                    st.write(f"**Assistant:**")
                    st.json(chat['assistant'])
                    st.write(f"*{chat['timestamp'].strftime('%Y-%m-%d %H:%M')}*")
        
        # Applied filters badge with reset option
        if st.session_state.applied_filters:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("🎯 **Applied via chat:** " + ", ".join([f"{k}: {v}" for k, v in st.session_state.applied_filters.items()]))
            with col2:
                if st.button("Clear Chat Filters", key="clear_chat_filters"):
                    st.session_state.applied_filters = {}
                    st.rerun()
        
        # Data table
        st.subheader("📊 Data Preview")
        st.dataframe(
            filtered_data.head(100),
            use_container_width=True,
            hide_index=True
        )
        
        # Download filtered data
        if not filtered_data.empty:
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data (CSV)",
                data=csv,
                file_name=f"filtered_drone_flights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    else:
        st.info("👆 Please upload a CSV file to get started!")
        
        # Sample data format
        st.subheader("📋 Expected CSV Format")
        sample_data = {
            'flight_id': ['FL001', 'FL002', 'FL003'],
            'origin_city': ['McAllen', 'Brownsville', 'Laredo'],
            'origin_lat': [26.2034, 25.9018, 27.5064],
            'origin_lon': [-98.2300, -97.4975, -99.5075],
            'dest_city': ['Monterrey', 'Reynosa', 'Nuevo Laredo'],
            'dest_lat': [25.6866, 26.0419, 27.4763],
            'dest_lon': [-100.3161, -98.2782, -99.5163],
            'timestamp': ['2024-01-01 10:00:00', '2024-01-01 11:00:00', '2024-01-01 12:00:00'],
            'speed_kts': [45, 52, 38],
            'altitude_ft': [1200, 800, 1500]
        }
        st.dataframe(pd.DataFrame(sample_data), use_container_width=True)

if __name__ == "__main__":
    main()
