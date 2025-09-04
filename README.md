# Cross-Border Drone Flight Mapper

A powerful web application for visualizing and analyzing cross-border drone flight data with AI-powered chat filtering. Built with Streamlit, Folium, and Anthropic Claude.

## ✨ Features

### Interactive Map Visualization
- **Destination Heatmap**: Visualize flight density with altitude-weighted intensity
- **Flow Lines**: Curved polylines showing origin-to-destination routes (performance-optimized)
- **Clustered Markers**: Interactive markers for origins and destinations with rich popups
- **Multiple Tile Layers**: CartoDB Positron, Dark Matter, and OpenStreetMap
- **Layer Control**: Toggle different visualization layers on/off

### Advanced Filtering
- **Time Range**: Filter flights by specific date ranges
- **Altitude Range**: Filter by minimum/maximum altitude
- **Speed Range**: Filter by speed in knots
- **Geographic Filters**: Filter by US/Mexico destinations
- **City Filters**: Filter by specific origin or destination cities
- **Quick Presets**: One-click filters for common scenarios

### AI-Powered Chat Interface
- **Natural Language Queries**: Ask questions in plain English
- **Structured Filter Generation**: Claude translates intent to structured filters
- **Chat History**: Track your conversation with the data
- **Applied Filters Badge**: See which filters were applied via chat

### Analytics & KPIs
- **Real-time Metrics**: Total flights, unique origins/destinations, averages
- **Top Destinations**: Top 5 destination cities by flight count
- **Data Preview**: Paginated table view of filtered data
- **Export Functionality**: Download filtered data as CSV

### Performance Features
- **Data Sampling**: Intelligent sampling for large datasets (50k+ rows)
- **Caching**: Streamlit caching for expensive operations
- **Responsive Updates**: Map and KPIs update within 1 second
- **Memory Efficient**: Optimized for large flight datasets

## Quick Start

### Prerequisites
- Python 3.10 or higher
- ANTHROPIC_API_KEY environment variable

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd drone_mapping3
   ```

2. **Install dependencies**
   ```bash
   # Option 1: Use the installation script
   python install.py
   
   # Option 2: Manual installation
   pip install -r requirements.txt
   ```

3. **Set up Anthropic API key**
   ```bash
   # Option 1: Use the setup script (recommended)
   python setup_api_key.py
   
   # Option 2: Manual setup
   # Edit config.env and replace 'your-anthropic-api-key-here' with your actual API key
   # Or set environment variable:
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

4. **Test the installation (optional)**
   ```bash
   python test_installation.py
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 📁 Data Format

The application expects CSV files with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `flight_id` | String | Unique flight identifier |
| `origin_city` | String | Origin city name |
| `origin_lat` | Float | Origin latitude |
| `origin_lon` | Float | Origin longitude |
| `dest_city` | String | Destination city name |
| `dest_lat` | Float | Destination latitude |
| `dest_lon` | Float | Destination longitude |
| `timestamp` | DateTime | Flight timestamp |
| `speed_kts` | Float | Speed in knots |
| `altitude_ft` | Float | Altitude in feet |

### Sample Data
A `sample_data.csv` file is included with 50 sample flights for testing.

## 💬 Chat Examples

### Filter Queries
- **"Show flights to Laredo in the last 24 hours above 500 ft"**
- **"Only destinations in Mexico, altitude < 1000 ft, and speed 20–60 kts"**
- **"Show flights from McAllen to Mexico destinations"**

### Analysis Queries
- **"Compare McAllen vs Brownsville by average altitude"**
- **"What are the busiest destination cities?"**
- **"Show flights above 1000 ft with speed over 50 knots"**

## 🎯 Use Cases

### Border Security
- Monitor cross-border drone activity
- Identify high-traffic crossing points
- Track altitude and speed patterns

## 🛠️ Technical Architecture

### Frontend
- **Streamlit**: Modern web interface with reactive components
- **Folium**: Interactive maps with Leaflet.js backend
- **Plotly**: Advanced charting and visualization

### Backend
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Geopandas**: Geographic data processing

### AI Integration
- **Anthropic Claude**: Natural language understanding using Claude 3.5 Haiku
- **Structured Output**: JSON schema validation
- **Security**: No code execution from LLM

### Performance
- **Caching**: Streamlit caching for expensive operations
- **Sampling**: Intelligent data sampling for large datasets
- **Lazy Loading**: Load map layers on demand

## 🔧 Configuration

### Environment Variables

The application supports multiple ways to set the API key:

1. **config.env file (recommended)**: Create a `config.env` file with:
   ```bash
   ANTHROPIC_API_KEY=your-anthropic-api-key
   ```

2. **Environment variable**: Set directly in your shell:
   ```bash
   export ANTHROPIC_API_KEY=your-anthropic-api-key
   ```

3. **Setup script**: Use the interactive setup:
   ```bash
   python setup_api_key.py
   ```


## 🚧 Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'streamlit_folium'"**
   - Run: `pip install streamlit-folium`
   - If still failing, the app will use a fallback method automatically
   - Alternative: `pip install --upgrade streamlit-folium`

2. **"ANTHROPIC_API_KEY not set"**
   - Ensure environment variable is set
   - Restart terminal/IDE after setting


### Performance Tips

- **Large Datasets**: Use sampling and filtering
- **Real-time Updates**: Minimize data processing in loops
- **Memory Management**: Clear session state when needed
- **Caching**: Leverage Streamlit's caching decorators

