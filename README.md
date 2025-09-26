# ClimateScope Weather Dashboard

A clean, interactive weather analytics platform built with Python and Dash.

## Features

- **Interactive World Map**: Visualize global weather conditions with temperature and humidity overlays
- **Regional Analysis**: Filter data by geographic regions and countries
- **Temperature Distribution**: Analyze temperature patterns across different regions
- **Humidity Analysis**: Compare humidity levels regionally and by distribution
- **Clean Interface**: Simple, intuitive controls for data exploration

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the dashboard**:
   ```bash
   python weather_dashboard.py
   ```

3. **Open in browser**:
   Navigate to `http://127.0.0.1:8050`

## Data Processing

The `ClimateScope.ipynb` notebook contains the complete data processing pipeline:

- Data loading and cleaning
- Geographic region classification
- Statistical analysis and visualization
- Export of processed datasets

## Project Structure

```
├── ClimateScope.ipynb          # Data processing notebook
├── weather_dashboard.py        # Main dashboard application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── data/
│   └── raw/
│       ├── enhanced_weather_with_regions.csv
│       └── GlobalWeatherRepository.csv
└── assets/
    └── style.css               # Dashboard styling
```

## Data Sources

- Global Weather Repository dataset from Kaggle
- Enhanced with geographic region classifications
- 95,000+ weather data points worldwide

## Technical Stack

- **Python 3.8+**
- **Dash**: Interactive web applications
- **Plotly**: Data visualization
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing

---

*ClimateScope provides comprehensive weather analytics with a clean, professional interface.*