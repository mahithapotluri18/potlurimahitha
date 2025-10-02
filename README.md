# 🌍 ClimateScope - Global Weather Analytics Platform

A comprehensive climate data analysis platform featuring automated data processing, exploratory analysis through Jupyter notebooks, and an interactive dashboard for real-time weather pattern visualization.

---

## 📦 Project Components

### 🔬 **Jupyter Notebook** (`ClimateScope.ipynb`)
Milestone-based exploratory data analysis with automated data pipeline

### 📊 **Interactive Dashboard** (`climatescope_dashboard.py`) 
Professional Plotly Dash application for real-time climate visualization

---

## 📓 Notebook Analysis - Milestones

### 🎯 **Milestone 1: Data Pipeline & Automation**
- **Kaggle Integration**: Auto-download from `nelgiriyewithana/global-weather-repository`
- **Smart Refresh**: 6-hour intervals with epoch-based change detection
- **File Management**: Streamlined ETL with error handling

### 📊 **Milestone 2: Core Analysis & Visualization**
- **Statistical Profiling**: Descriptive statistics and correlation analysis
- **Seasonal Patterns**: Monthly trends and extreme weather detection
- **Regional Comparisons**: Cross-geographic statistical analysis

### 🌍 **Milestone 3: Geographic Enhancement**
- **Regional Classification**: 7-region mapping system (97,824 records)
- **Data Quality**: Country normalization and validation

---

## 📊 Dashboard Features

### 🗺️ **Global Visualizations**
- **World Map**: Interactive choropleth with 191 countries, 7 regions
- **Time Series**: Historical trends and patterns
- **Correlation Analysis**: Interactive scatter plots
- **Air Quality Index**: Composite environmental indicators

### 🎯 **Insights System**
- **📊 Statistical Overview**: Comprehensive statistics
- **🌍 Regional Analysis**: Geographic comparisons
- **☀️ Highest Temperature**: Top performers by metric
- **📈 Trends & Patterns**: Temporal analysis

### 🎨 **User Experience**
- **Dark/Light Themes**: Adaptive visualizations
- **Interactive Controls**: Date, region, country, metric filtering
- **Export Reports**: Professional markdown generation

---

## 🚀 Quick Start

### 📋 Prerequisites
```bash
Python 3.8+
pip install -r requirements.txt
```

### 🔬 Run Notebook Analysis
```bash
jupyter notebook ClimateScope.ipynb
# Run all cells for complete milestone analysis
```

### 📊 Run Dashboard
```bash
python climatescope_dashboard.py
# Access: http://127.0.0.1:8062
```

### 🎯 Usage Flow
1. **Explore**: Start with notebook for data analysis
2. **Visualize**: Use dashboard for interactive exploration
3. **Export**: Generate comprehensive reports

---

## 📁 Project Structure

```
project_6.0/
├── 📓 ClimateScope.ipynb              # Milestone analysis notebook
├── 📊 climatescope_app.py             # Interactive dashboard
├── 📄 requirements.txt                # Dependencies
├── 📖 README.md                       # This guide
│
├── 📂 data/
│   ├── 📂 raw/                        # Raw datasets
│   │   ├── 🌍 enhanced_weather_with_regions.csv  # Main dataset (97,824 records)
│   │   ├── 🌡️ GlobalWeatherRepository.csv        # Original Kaggle data
│   │   └── 💾 state.db                           # Database state
│   │
│   ├── 📂 clean/                      # Processed data
│   │   ├── 📊 latest_monthly.parquet  # Aggregated data
│   │   ├── 📂 2024/                   # Historical by year/month
│   │   └── 📂 2025/                   # Current year data
│   │
│   └── 📂 tmp/                        # Automation files
│       ├── ⏰ last_fetch_date.txt     # Timing tracker
│       ├── 🔄 last_epoch.txt          # Version tracker
│       └── 📂 k_meta/                 # Kaggle metadata
```

---

## 📈 Dataset Information

### 🌍 **Coverage**
- **Records**: 97,824 weather observations
- **Countries**: 191 countries worldwide  
- **Regions**: 7 geographic regions
- **Metrics**: Temperature, humidity, wind, pressure, UV, air quality

### 🔧 **Technical**
- **Framework**: Plotly Dash + Bootstrap
- **Performance**: 5000-point sampling optimization
- **Themes**: Dark/light mode with adaptive styling
- **Export**: Markdown report generation

---

## 🌟 Key Features

### ✅ **Automation**
- 6-hour auto-refresh with Kaggle integration
- Epoch-based change detection
- Graceful error handling

### ✅ **Analytics** 
- 97K+ records across 191 countries
- Multi-metric analysis (temperature, humidity, wind, air quality)
- Real-time statistical computations

### ✅ **Interface**
- Responsive Bootstrap design
- Interactive filtering controls
- Professional report generation

---

*ClimateScope - Comprehensive Global Weather Analytics Platform*
