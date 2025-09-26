"""
ClimateScope Weather Dashboard
Interactive weather analytics platform
"""

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def load_data():
    """Load and preprocess weather data"""
    try:
        df = pd.read_csv('data/raw/enhanced_weather_with_regions.csv')
        df['last_updated'] = pd.to_datetime(df['last_updated'])
        
        # Clean numeric columns
        numeric_cols = ['temperature_celsius', 'humidity', 'pressure_mb', 'wind_kph', 'uv_index']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna(subset=['latitude', 'longitude', 'temperature_celsius'])
        
        # Fill missing values with median
        for col in ['humidity', 'pressure_mb', 'wind_kph', 'uv_index']:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())
        
        print(f"Data loaded: {len(df):,} records")
        return df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

# Load data
df = load_data()

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "ClimateScope Weather Dashboard"

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("ClimateScope Weather Dashboard", 
                style={'textAlign': 'center', 'color': 'white', 'margin': '0'}),
        html.P("Global Weather Analytics Platform", 
               style={'textAlign': 'center', 'color': 'white', 'margin': '10px 0 0 0'})
    ], style={
        'background': 'linear-gradient(135deg, #1f77b4, #ff7f0e)',
        'padding': '30px',
        'marginBottom': '20px'
    }),
    
    # Controls
    html.Div([
        html.Div([
            html.Label("Region:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': 'All Regions', 'value': 'All'}] + 
                        [{'label': region, 'value': region}
                         for region in sorted(df['geographic_region'].dropna().unique())] if not df.empty else [],
                value='All',
                clearable=False
            )
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '4%'}),
        
        html.Div([
            html.Label("Country:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='country-filter',
                options=[{'label': 'All Countries', 'value': 'All'}],
                value='All',
                clearable=False
            )
        ], style={'width': '48%', 'display': 'inline-block'})
    ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'}),
    
    # Main content
    html.Div([
        # World map
        html.Div([
            dcc.Graph(id='world-map')
        ], style={'width': '100%', 'marginBottom': '20px'}),
        
        # Charts row
        html.Div([
            html.Div([
                dcc.Graph(id='temperature-chart')
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(id='humidity-chart')
            ], style={'width': '50%', 'display': 'inline-block'})
        ])
    ], style={'margin': '20px'})
])

# Callback for country dropdown
@app.callback(
    Output('country-filter', 'options'),
    Input('region-filter', 'value')
)
def update_countries(selected_region):
    if df.empty:
        return [{'label': 'No data', 'value': 'None'}]
    
    if selected_region == 'All':
        countries = sorted(df['normalized_country'].dropna().unique())
    else:
        filtered_df = df[df['geographic_region'] == selected_region]
        countries = sorted(filtered_df['normalized_country'].dropna().unique())
    
    options = [{'label': 'All Countries', 'value': 'All'}]
    options.extend([{'label': country, 'value': country} for country in countries])
    return options

# Callback for world map
@app.callback(
    Output('world-map', 'figure'),
    [Input('region-filter', 'value'),
     Input('country-filter', 'value')]
)
def update_world_map(selected_region, selected_country):
    if df.empty:
        return go.Figure().add_annotation(text="No data available", 
                                        xref="paper", yref="paper",
                                        x=0.5, y=0.5, showarrow=False)
    
    filtered_df = df.copy()
    
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['geographic_region'] == selected_region]
    
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df['normalized_country'] == selected_country]
    
    if filtered_df.empty:
        return go.Figure().add_annotation(text="No data for selected filters", 
                                        xref="paper", yref="paper",
                                        x=0.5, y=0.5, showarrow=False)
    
    fig = px.scatter_mapbox(
        filtered_df,
        lat="latitude",
        lon="longitude",
        color="temperature_celsius",
        size="humidity",
        hover_name="location_name",
        hover_data={"normalized_country": True, "geographic_region": True},
        color_continuous_scale="RdYlBu_r",
        mapbox_style="open-street-map",
        title="Global Weather Conditions",
        zoom=1
    )
    
    fig.update_layout(height=600, margin={"r":0,"t":30,"l":0,"b":0})
    return fig

# Callback for temperature chart
@app.callback(
    Output('temperature-chart', 'figure'),
    [Input('region-filter', 'value'),
     Input('country-filter', 'value')]
)
def update_temperature_chart(selected_region, selected_country):
    if df.empty:
        return go.Figure().add_annotation(text="No data available", 
                                        xref="paper", yref="paper",
                                        x=0.5, y=0.5, showarrow=False)
    
    filtered_df = df.copy()
    
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['geographic_region'] == selected_region]
    
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df['normalized_country'] == selected_country]
    
    if filtered_df.empty:
        return go.Figure().add_annotation(text="No data for selected filters", 
                                        xref="paper", yref="paper",
                                        x=0.5, y=0.5, showarrow=False)
    
    # Temperature distribution
    fig = px.histogram(
        filtered_df,
        x="temperature_celsius",
        nbins=30,
        title="Temperature Distribution",
        labels={"temperature_celsius": "Temperature (°C)", "count": "Frequency"}
    )
    
    fig.update_layout(height=400)
    return fig

# Callback for humidity chart
@app.callback(
    Output('humidity-chart', 'figure'),
    [Input('region-filter', 'value'),
     Input('country-filter', 'value')]
)
def update_humidity_chart(selected_region, selected_country):
    if df.empty:
        return go.Figure().add_annotation(text="No data available", 
                                        xref="paper", yref="paper",
                                        x=0.5, y=0.5, showarrow=False)
    
    filtered_df = df.copy()
    
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['geographic_region'] == selected_region]
    
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df['normalized_country'] == selected_country]
    
    if filtered_df.empty:
        return go.Figure().add_annotation(text="No data for selected filters", 
                                        xref="paper", yref="paper",
                                        x=0.5, y=0.5, showarrow=False)
    
    # Regional temperature comparison
    if selected_region == 'All' and selected_country == 'All':
        # Show by region
        regional_avg = filtered_df.groupby('geographic_region')['humidity'].mean().reset_index()
        fig = px.bar(
            regional_avg,
            x="geographic_region",
            y="humidity",
            title="Average Humidity by Region",
            labels={"geographic_region": "Region", "humidity": "Humidity (%)"}
        )
    else:
        # Show humidity distribution
        fig = px.histogram(
            filtered_df,
            x="humidity",
            nbins=30,
            title="Humidity Distribution",
            labels={"humidity": "Humidity (%)", "count": "Frequency"}
        )
    
    fig.update_layout(height=400)
    return fig

if __name__ == '__main__':
    print("Starting ClimateScope Weather Dashboard...")
    print("Access the dashboard at: http://127.0.0.1:8050")
    app.run(debug=True, host='127.0.0.1', port=8050)
