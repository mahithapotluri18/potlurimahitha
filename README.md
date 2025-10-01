# 🌍 ClimateScope Dashboard

A professional Plotly Dash application for visualizing global weather patterns and climate data.

## 📊 Features

- **Interactive World Map**: Global temperature and climate visualization
- **Time Series Analysis**: Weather trends over time
- **Correlation Analysis**: Scatter plots for metric relationships
- **Seasonality Heatmaps**: Monthly weather patterns
- **Statistics Cards**: Real-time data summaries
- **Advanced Filtering**: By region, country, and date ranges
- **Report Generation**: Comprehensive markdown reports

## 🚀 Quick Start

### Installation

```bash
# Clone or download the project
cd project_6.0

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
python climatescope_app.py
```

### Access

Open your browser and navigate to: **http://127.0.0.1:8052**

## 📁 Project Structure

```
climatescope_app.py      # Main dashboard application
requirements.txt         # Python dependencies  
data/raw/               # Weather datasets
├── enhanced_weather_with_regions.csv   # Main dataset (97,824 records)
└── GlobalWeatherRepository.csv         # Original dataset
```

## 🔧 Usage

1. **Select Filters**: Choose regions, countries, and date ranges
2. **Explore Visualizations**: Interactive maps, charts, and heatmaps
3. **Generate Reports**: Click the "📄 Generate Report" button in the header
4. **Download Analysis**: Get comprehensive markdown reports

## 📈 Data

- **Records**: 97,824 weather observations
- **Countries**: 191 countries covered
- **Regions**: 7 geographic regions
- **Metrics**: Temperature, humidity, wind speed, UV index, precipitation

## 🎯 Key Metrics

- Temperature (°C)
- Humidity (%)
- Wind Speed (km/h)
- UV Index
- Precipitation (proxy)

## 📄 Reports

The dashboard generates comprehensive reports including:
- Executive summary with applied filters
- Climate analysis and statistics
- Extreme weather locations
- Regional comparisons
- Data quality assessment
- Key insights and recommendations

## ⚙️ Technical Requirements

- Python 3.8+
- Dash 2.14+
- Plotly 5.15+
- Pandas 2.0+
- Numpy 1.24+

## 🌟 Interface

- Clean, professional design
- Responsive Bootstrap layout
- Interactive controls
- Real-time statistics
- Streamlined export functionality

---

*ClimateScope Dashboard - Professional Weather Analytics Platform*
