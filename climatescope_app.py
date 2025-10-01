#!/usr/bin/env python3
"""
ClimateScope - Global Weather Patterns Visualization Dashboard

A comprehensive Plotly Dash application for visualizing global weather patterns
and extreme events with interactive controls.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
from datetime import datetime, date
import json

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "ClimateScope - Global Weather Analytics"

# Load and prepare data
def load_data():
    """Load and preprocess the weather data"""
    try:
        print("📊 Loading data from ./data/raw/enhanced_weather_with_regions.csv...")
        # Load the enhanced weather data with regions
        df = pd.read_csv('./data/raw/enhanced_weather_with_regions.csv')
        print(f"✅ Data loaded successfully: {len(df)} records")
        
        # Convert date column to datetime
        df['last_updated'] = pd.to_datetime(df['last_updated'])
        df['date'] = df['last_updated'].dt.date
        df['year'] = df['last_updated'].dt.year
        df['month'] = df['last_updated'].dt.month
        df['month_name'] = df['last_updated'].dt.strftime('%B')
        
        # Handle missing values
        numeric_columns = ['temperature_celsius', 'humidity', 'pressure_mb', 'wind_kph', 'uv_index']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())
        
        # Create precipitation column (if not available, use humidity as proxy)
        if 'precipitation' not in df.columns:
            df['precipitation'] = df['humidity'] * 0.1  # Simple proxy
        
        # Create wind_speed column (alias for wind_kph)
        df['wind_speed'] = df['wind_kph']
        
        print(f"📍 Countries: {df['normalized_country'].nunique()}")
        print(f"🌍 Regions: {df['geographic_region'].nunique()}")
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        print("🔍 Please check if the file exists and has the correct format")
        return pd.DataFrame()

# Load data
print("🌍 Initializing ClimateScope Dashboard...")
df = load_data()

# Get unique values for dropdowns
if not df.empty:
    countries = sorted(df['normalized_country'].unique())
    regions = sorted(df['geographic_region'].unique())
    print(f"✅ Loaded {len(countries)} countries and {len(regions)} regions")
else:
    countries = ['No Data Available']
    regions = ['No Data Available']
    print("⚠️ No data loaded - using fallback values")

metrics = ['temperature_celsius', 'humidity', 'wind_speed', 'precipitation']
metric_labels = {
    'temperature_celsius': 'Temperature (°C)',
    'humidity': 'Humidity (%)',
    'wind_speed': 'Wind Speed (km/h)',
    'precipitation': 'Precipitation (proxy)'
}

# Get date range
if not df.empty:
    min_date = df['date'].min()
    max_date = df['date'].max()
else:
    min_date = date(2024, 1, 1)
    max_date = date(2024, 12, 31)

# App layout
app.layout = dbc.Container([
    # Header with gradient background and report button
    dbc.Row([
        dbc.Col([
            html.Div([
                # Top section with logo and report button
                html.Div([
                    html.Div([
                        html.Span("🌍", style={'fontSize': '3rem', 'marginRight': '15px'}),
                        html.Span("ClimateScope Weather Dashboard", 
                                 style={'fontSize': '2.5rem', 'fontWeight': 'bold', 'color': 'white'})
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                    
                    # Generate Report button positioned at top right
                    html.Div([
                        dbc.Button(
                            "📄 Generate Report", 
                            id="btn-report", 
                            color="light", 
                            size="sm",
                            style={
                                'position': 'absolute',
                                'top': '15px',
                                'right': '20px',
                                'fontWeight': 'bold',
                                'boxShadow': '0 2px 8px rgba(0,0,0,0.2)'
                            }
                        )
                    ])
                ], style={'position': 'relative', 'marginBottom': '10px'}),
                
                html.P("Advanced Global Weather Analytics & Interactive Visualizations",
                      style={'fontSize': '1.2rem', 'color': 'white', 'textAlign': 'center', 'margin': '0'})
            ], style={
                'background': 'linear-gradient(135deg, #4a90e2 0%, #f093fb 100%)',
                'padding': '30px 20px',
                'borderRadius': '10px',
                'marginBottom': '20px'
            })
        ])
    ]),
    
    # Download component for report
    dcc.Download(id="download-report"),
    
    # Statistics Cards Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(id='total-locations', children=f"{len(df):,}" if not df.empty else "0", 
                           style={'color': '#4a90e2', 'fontWeight': 'bold', 'margin': '0'}),
                    html.P("Total Locations", style={'color': '#666', 'margin': '0', 'fontSize': '0.9rem'})
                ])
            ], style={'textAlign': 'center', 'border': 'none', 'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'})
        ], width=2),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(id='avg-temperature', children=f"{df['temperature_celsius'].mean():.1f}°C" if not df.empty else "0°C", 
                           style={'color': '#e74c3c', 'fontWeight': 'bold', 'margin': '0'}),
                    html.P("Average Temperature", style={'color': '#666', 'margin': '0', 'fontSize': '0.9rem'})
                ])
            ], style={'textAlign': 'center', 'border': 'none', 'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'})
        ], width=2),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(id='avg-humidity', children=f"{df['humidity'].mean():.1f}%" if not df.empty else "0%", 
                           style={'color': '#27ae60', 'fontWeight': 'bold', 'margin': '0'}),
                    html.P("Average Humidity", style={'color': '#666', 'margin': '0', 'fontSize': '0.9rem'})
                ])
            ], style={'textAlign': 'center', 'border': 'none', 'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'})
        ], width=2),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(id='avg-windspeed', children=f"{df['wind_kph'].mean():.1f}" if not df.empty else "0", 
                           style={'color': '#f39c12', 'fontWeight': 'bold', 'margin': '0'}),
                    html.P("Avg Wind Speed (km/h)", style={'color': '#666', 'margin': '0', 'fontSize': '0.9rem'})
                ])
            ], style={'textAlign': 'center', 'border': 'none', 'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'})
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(id='avg-uv-index', children=f"{df['uv_index'].mean():.1f}" if not df.empty else "0", 
                           style={'color': '#9b59b6', 'fontWeight': 'bold', 'margin': '0'}),
                    html.P("Average UV Index", style={'color': '#666', 'margin': '0', 'fontSize': '0.9rem'})
                ])
            ], style={'textAlign': 'center', 'border': 'none', 'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'})
        ], width=3)
    ], className="mb-4"),
    
    # Controls Section
    dbc.Card([
        dbc.CardHeader([
            html.H5("📊 Interactive Controls", className="mb-0", style={'color': '#2E86AB'})
        ]),
        dbc.CardBody([
            # Date Selection Mode Toggle
            dbc.Row([
                dbc.Col([
                    html.Label("📅 Date Selection Mode:", className="fw-bold mb-2"),
                    dbc.RadioItems(
                        id='date-mode-toggle',
                        options=[
                            {'label': ' Date Range', 'value': 'range'},
                            {'label': ' Only One Day', 'value': 'single'}
                        ],
                        value='range',
                        inline=True,
                        style={'marginBottom': '10px'}
                    )
                ], width=12)
            ], className="mb-3"),
            
            # Date Controls Row
            dbc.Row([
                # Date Range Picker
                dbc.Col([
                    html.Div([
                        html.Label("📅 Date Range:", className="fw-bold"),
                        dcc.DatePickerRange(
                            id='date-picker-range',
                            start_date=min_date,
                            end_date=max_date,
                            display_format='YYYY-MM-DD',
                            min_date_allowed=min_date,
                            max_date_allowed=max_date,
                            style={'width': '100%'}
                        )
                    ], id='date-range-container'),
                    
                    # Single Date Picker (initially hidden)
                    html.Div([
                        html.Label("📅 Select Date:", className="fw-bold"),
                        dcc.DatePickerSingle(
                            id='single-date-picker',
                            date=min_date,
                            display_format='YYYY-MM-DD',
                            min_date_allowed=min_date,
                            max_date_allowed=max_date,
                            style={'width': '100%'}
                        )
                    ], id='single-date-container', style={'display': 'none'})
                ], width=3),
                
                # Region/Country Multi-select
                dbc.Col([
                    html.Label("🌍 Regions:", className="fw-bold"),
                    dcc.Dropdown(
                        id='region-dropdown',
                        options=[{'label': region, 'value': region} for region in regions],
                        value=regions[:3] if len(regions) >= 3 else regions,
                        multi=True,
                        placeholder="Select regions..."
                    )
                ], width=3),
                
                dbc.Col([
                    html.Label("🏳️ Countries:", className="fw-bold"),
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': country, 'value': country} for country in countries],
                        value=countries[:5] if len(countries) >= 5 else countries,
                        multi=True,
                        placeholder="Select countries..."
                    )
                ], width=3),
                
                # Metric Selector
                dbc.Col([
                    html.Label("📈 Primary Metric:", className="fw-bold"),
                    dcc.Dropdown(
                        id='metric-dropdown',
                        options=[{'label': metric_labels[metric], 'value': metric} for metric in metrics],
                        value='temperature_celsius',
                        clearable=False
                    )
                ], width=3)
            ])
        ])
    ], className="mb-4"),
    
    # Date Validation Message Area
    html.Div(id='date-validation-message', className="mb-3"),
    
    # Main Visualizations
    dbc.Row([
        # World Map
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H6("🗺️ Global Choropleth Map", className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='world-map', config={'displayModeBar': False})
                ])
            ])
        ], width=6),
        
        # Time Series
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H6("📈 Time Series Trend", className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='time-series', config={'displayModeBar': False})
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    dbc.Row([
        # Scatter Plot
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H6("🔍 Correlation Analysis", className="mb-0"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("X-Axis:", style={'font-size': '0.8em'}),
                            dcc.Dropdown(
                                id='scatter-x-dropdown',
                                options=[{'label': metric_labels[metric], 'value': metric} for metric in metrics],
                                value='temperature_celsius',
                                clearable=False,
                                style={'font-size': '0.8em'}
                            )
                        ], width=6),
                        dbc.Col([
                            html.Label("Y-Axis:", style={'font-size': '0.8em'}),
                            dcc.Dropdown(
                                id='scatter-y-dropdown',
                                options=[{'label': metric_labels[metric], 'value': metric} for metric in metrics],
                                value='humidity',
                                clearable=False,
                                style={'font-size': '0.8em'}
                            )
                        ], width=6)
                    ])
                ]),
                dbc.CardBody([
                    dcc.Graph(id='scatter-plot', config={'displayModeBar': False})
                ])
            ])
        ], width=6),
        
        # Seasonality Heatmap
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H6("🔥 Seasonality Heatmap", className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='seasonality-heatmap', config={'displayModeBar': False})
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    

    
    # Download component for report only
    dcc.Download(id="download-report"),
    
    # Insights Panel
    dbc.Card([
        dbc.CardHeader([
            html.H5("💡 Key Insights", className="mb-0", style={'color': '#2E86AB'})
        ]),
        dbc.CardBody([
            html.Div(id='insights-panel', className="p-3")
        ])
    ], className="mb-4"),
    
    # Footer
    html.Hr(),
    html.P("🌡️ ClimateScope Dashboard - Powered by Plotly Dash", 
           className="text-center text-muted", style={'font-size': '0.9em'})
], fluid=True)

# Callback to toggle between date range and single date modes
@app.callback(
    [Output('date-range-container', 'style'),
     Output('single-date-container', 'style')],
    [Input('date-mode-toggle', 'value')]
)
def toggle_date_mode(mode):
    """Toggle between date range and single date selection"""
    if mode == 'range':
        return {'display': 'block'}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'display': 'block'}

# Callback for date validation
@app.callback(
    Output('date-validation-message', 'children'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('single-date-picker', 'date'),
     Input('date-mode-toggle', 'value')]
)
def validate_dates(start_date, end_date, single_date, mode):
    """Validate selected dates and show appropriate messages"""
    if df.empty:
        return dbc.Alert("⚠️ No data available for validation", color="warning", className="mb-3")
    
    # Get available date range
    available_min = min_date
    available_max = max_date
    
    if mode == 'range':
        if start_date and end_date:
            start_date_obj = pd.to_datetime(start_date).date()
            end_date_obj = pd.to_datetime(end_date).date()
            
            # Check if dates are outside available range
            if start_date_obj < available_min or end_date_obj > available_max:
                return dbc.Alert(
                    [
                        html.Strong("📅 Date Range Error: "),
                        f"Data is only available from {available_min} to {available_max}. "
                        f"Please select dates within this range."
                    ],
                    color="danger",
                    className="mb-3"
                )
            
            # Check if start date is after end date
            if start_date_obj > end_date_obj:
                return dbc.Alert(
                    [
                        html.Strong("📅 Date Range Error: "),
                        "Start date cannot be after end date. Please adjust your selection."
                    ],
                    color="danger",
                    className="mb-3"
                )
            
            # Valid range - no message needed
            return html.Div()
    
    else:  # single date mode
        if single_date:
            single_date_obj = pd.to_datetime(single_date).date()
            
            # Check if date is outside available range
            if single_date_obj < available_min or single_date_obj > available_max:
                return dbc.Alert(
                    [
                        html.Strong("📅 Date Error: "),
                        f"Data is only available from {available_min} to {available_max}. "
                        f"Please select a date within this range."
                    ],
                    color="danger",
                    className="mb-3"
                )
            
            # Valid single date - no message needed
            return html.Div()
    
    return html.Div()  # No message

# Callback for updating all visualizations
@app.callback(
    [Output('world-map', 'figure'),
     Output('time-series', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('seasonality-heatmap', 'figure'),
     Output('insights-panel', 'children'),
     Output('total-locations', 'children'),
     Output('avg-temperature', 'children'),
     Output('avg-humidity', 'children'),
     Output('avg-windspeed', 'children'),
     Output('avg-uv-index', 'children')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('single-date-picker', 'date'),
     Input('date-mode-toggle', 'value'),
     Input('region-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('metric-dropdown', 'value'),
     Input('scatter-x-dropdown', 'value'),
     Input('scatter-y-dropdown', 'value')]
)
def update_visualizations(start_date, end_date, single_date, date_mode, selected_regions, selected_countries, 
                         selected_metric, scatter_x, scatter_y):
    """Update all visualizations based on filter selections"""
    
    if df.empty:
        # Return empty figures if no data
        empty_fig = go.Figure().add_annotation(
            text="No data available", 
            xref="paper", yref="paper", x=0.5, y=0.5, 
            showarrow=False, font_size=16
        )
        return empty_fig, empty_fig, empty_fig, empty_fig, "No data available for analysis.", "0", "0°C", "0%", "0", "0"
    
    # Filter data based on selections
    filtered_df = df.copy()
    
    # Date filtering based on mode
    if date_mode == 'range':
        # Date range filtering
        if start_date and end_date:
            start_date_obj = pd.to_datetime(start_date).date()
            end_date_obj = pd.to_datetime(end_date).date()
            
            # Validate dates are within available range
            if start_date_obj < min_date or end_date_obj > max_date:
                # Return empty result for invalid dates
                empty_fig = go.Figure().add_annotation(
                    text="Selected dates are outside available data range", 
                    xref="paper", yref="paper", x=0.5, y=0.5, 
                    showarrow=False, font_size=14
                )
                return empty_fig, empty_fig, empty_fig, empty_fig, "Selected dates are outside available data range.", "0", "0°C", "0%", "0", "0"
            
            filtered_df = filtered_df[(filtered_df['date'] >= start_date_obj) & 
                                     (filtered_df['date'] <= end_date_obj)]
    else:
        # Single date filtering
        if single_date:
            single_date_obj = pd.to_datetime(single_date).date()
            
            # Validate date is within available range
            if single_date_obj < min_date or single_date_obj > max_date:
                # Return empty result for invalid date
                empty_fig = go.Figure().add_annotation(
                    text="Selected date is outside available data range", 
                    xref="paper", yref="paper", x=0.5, y=0.5, 
                    showarrow=False, font_size=14
                )
                return empty_fig, empty_fig, empty_fig, empty_fig, "Selected date is outside available data range.", "0", "0°C", "0%", "0", "0"
            
            filtered_df = filtered_df[filtered_df['date'] == single_date_obj]
    
    # Region filtering
    if selected_regions:
        filtered_df = filtered_df[filtered_df['geographic_region'].isin(selected_regions)]
    
    # Country filtering
    if selected_countries:
        filtered_df = filtered_df[filtered_df['normalized_country'].isin(selected_countries)]
    
    if filtered_df.empty:
        empty_fig = go.Figure().add_annotation(
            text="No data matches the selected filters", 
            xref="paper", yref="paper", x=0.5, y=0.5, 
            showarrow=False, font_size=14
        )
        return empty_fig, empty_fig, empty_fig, empty_fig, "No data matches the current filter selection.", "0", "0°C", "0%", "0", "0"
    
    # 1. World Map (Choropleth)
    try:
        country_agg = filtered_df.groupby('normalized_country')[selected_metric].mean().reset_index()
        world_map = px.choropleth(
            country_agg,
            locations='normalized_country',
            color=selected_metric,
            locationmode='country names',
            title=f"Global {metric_labels[selected_metric]} Distribution",
            color_continuous_scale='Viridis',
            hover_name='normalized_country',
            hover_data={selected_metric: ':.2f'}
        )
        world_map.update_layout(
            geo=dict(showframe=False, showcoastlines=True),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
    except Exception as e:
        world_map = go.Figure().add_annotation(
            text=f"Error creating world map: {str(e)}", 
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
    
    # 2. Time Series
    try:
        # Monthly aggregation
        filtered_df['year_month'] = filtered_df['last_updated'].dt.to_period('M')
        time_series_data = filtered_df.groupby('year_month')[selected_metric].mean().reset_index()
        time_series_data['year_month'] = time_series_data['year_month'].dt.to_timestamp()
        
        time_series = px.line(
            time_series_data,
            x='year_month',
            y=selected_metric,
            title=f"{metric_labels[selected_metric]} Trend Over Time",
            markers=True
        )
        time_series.update_layout(
            xaxis_title="Date",
            yaxis_title=metric_labels[selected_metric],
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        time_series.update_traces(line_color='#2E86AB')
    except Exception as e:
        time_series = go.Figure().add_annotation(
            text=f"Error creating time series: {str(e)}", 
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
    
    # 3. Scatter Plot
    try:
        scatter_plot = px.scatter(
            filtered_df.sample(min(1000, len(filtered_df))),  # Sample for performance
            x=scatter_x,
            y=scatter_y,
            color='geographic_region',
            title=f"{metric_labels[scatter_x]} vs {metric_labels[scatter_y]}",
            hover_data=['normalized_country'],
            opacity=0.7
        )
        scatter_plot.update_layout(
            xaxis_title=metric_labels[scatter_x],
            yaxis_title=metric_labels[scatter_y],
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
    except Exception as e:
        scatter_plot = go.Figure().add_annotation(
            text=f"Error creating scatter plot: {str(e)}", 
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
    
    # 4. Seasonality Heatmap
    try:
        # Create month-year matrix
        heatmap_data = filtered_df.pivot_table(
            values=selected_metric,
            index='month',
            columns='year',
            aggfunc='mean'
        )
        
        seasonality_heatmap = px.imshow(
            heatmap_data.values,
            x=heatmap_data.columns,
            y=[datetime(2024, i, 1).strftime('%B') for i in heatmap_data.index],
            color_continuous_scale='RdYlBu_r',
            title=f"{metric_labels[selected_metric]} Seasonality Pattern",
            aspect='auto'
        )
        seasonality_heatmap.update_layout(
            xaxis_title="Year",
            yaxis_title="Month",
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
    except Exception as e:
        seasonality_heatmap = go.Figure().add_annotation(
            text=f"Error creating heatmap: {str(e)}", 
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
    
    # 5. Generate Insights
    try:
        insights = generate_insights(filtered_df, selected_metric)
    except Exception as e:
        insights = f"Error generating insights: {str(e)}"
    
    # 6. Calculate Statistics for Cards
    try:
        total_locations = f"{len(filtered_df):,}"
        avg_temperature = f"{filtered_df['temperature_celsius'].mean():.1f}°C"
        avg_humidity = f"{filtered_df['humidity'].mean():.1f}%"
        avg_windspeed = f"{filtered_df['wind_kph'].mean():.1f}"
        avg_uv_index = f"{filtered_df['uv_index'].mean():.1f}"
    except Exception as e:
        total_locations = "0"
        avg_temperature = "0°C"
        avg_humidity = "0%"
        avg_windspeed = "0"
        avg_uv_index = "0"
    
    return world_map, time_series, scatter_plot, seasonality_heatmap, insights, total_locations, avg_temperature, avg_humidity, avg_windspeed, avg_uv_index

def generate_insights(data, metric):
    """Generate key insights from the filtered data"""
    if data.empty:
        return "No data available for generating insights."
    
    insights = []
    
    try:
        # Basic statistics
        metric_stats = data[metric].describe()
        insights.append(f"📊 **{metric_labels[metric]} Overview**: Mean = {metric_stats['mean']:.2f}, "
                       f"Range = {metric_stats['min']:.2f} to {metric_stats['max']:.2f}")
        
        # Regional analysis
        regional_stats = data.groupby('geographic_region')[metric].mean().sort_values(ascending=False)
        if len(regional_stats) > 0:
            highest_region = regional_stats.index[0]
            lowest_region = regional_stats.index[-1]
            insights.append(f"🌍 **Regional Leaders**: {highest_region} has the highest average "
                           f"{metric_labels[metric].lower()} ({regional_stats.iloc[0]:.2f}), "
                           f"while {lowest_region} has the lowest ({regional_stats.iloc[-1]:.2f})")
        
        # Country analysis
        country_stats = data.groupby('normalized_country')[metric].mean().sort_values(ascending=False)
        if len(country_stats) > 0:
            top_country = country_stats.index[0]
            insights.append(f"🏆 **Top Country**: {top_country} leads with an average "
                           f"{metric_labels[metric].lower()} of {country_stats.iloc[0]:.2f}")
        
        # Temporal analysis
        if 'last_updated' in data.columns:
            monthly_trend = data.groupby(data['last_updated'].dt.month)[metric].mean()
            peak_month = monthly_trend.idxmax()
            peak_month_name = datetime(2024, peak_month, 1).strftime('%B')
            insights.append(f"📅 **Seasonal Peak**: {peak_month_name} shows the highest average "
                           f"{metric_labels[metric].lower()} ({monthly_trend.max():.2f})")
        
        # Data coverage
        total_countries = data['normalized_country'].nunique()
        total_regions = data['geographic_region'].nunique()
        date_range = f"{data['date'].min()} to {data['date'].max()}"
        insights.append(f"📈 **Data Coverage**: {total_countries} countries across {total_regions} regions "
                       f"from {date_range}")
        
    except Exception as e:
        insights.append(f"⚠️ Error in analysis: {str(e)}")
    
    # Format insights as HTML
    insight_html = []
    for insight in insights:
        insight_html.append(html.P(insight, className="mb-2"))
    
    return insight_html

# Callback to update country dropdown based on region selection
@app.callback(
    Output('country-dropdown', 'options'),
    [Input('region-dropdown', 'value')]
)
def update_country_options(selected_regions):
    """Update country dropdown based on selected regions"""
    if not selected_regions or df.empty:
        return [{'label': country, 'value': country} for country in countries]
    
    filtered_countries = df[df['geographic_region'].isin(selected_regions)]['normalized_country'].unique()
    filtered_countries = sorted(filtered_countries)
    return [{'label': country, 'value': country} for country in filtered_countries]

# Report export callback function

@app.callback(
    Output("download-report", "data"),
    Input("btn-report", "n_clicks"),
    [State('region-dropdown', 'value'),
     State('country-dropdown', 'value'),
     State('date-picker-range', 'start_date'),
     State('date-picker-range', 'end_date'),
     State('single-date-picker', 'date'),
     State('date-mode-toggle', 'value')],
    prevent_initial_call=True
)
def export_report(n_clicks, selected_regions, selected_countries, start_date, end_date, single_date, date_mode):
    """Export comprehensive markdown report"""
    if n_clicks:
        # Apply same filtering logic
        filtered_df = df.copy()
        
        if selected_regions:
            filtered_df = filtered_df[filtered_df['geographic_region'].isin(selected_regions)]
        if selected_countries:
            filtered_df = filtered_df[filtered_df['normalized_country'].isin(selected_countries)]
        
        # Date filtering
        if date_mode == "single" and single_date:
            filtered_df = filtered_df[filtered_df['date'] == pd.to_datetime(single_date).date()]
        elif date_mode == "range" and start_date and end_date:
            filtered_df = filtered_df[
                (filtered_df['date'] >= pd.to_datetime(start_date).date()) &
                (filtered_df['date'] <= pd.to_datetime(end_date).date())
            ]
        
        # Generate comprehensive report
        report = generate_comprehensive_report(filtered_df, selected_regions, selected_countries, date_mode)
        
        return dict(
            content=report,
            filename=f"climatescope_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )

def generate_comprehensive_report(df, selected_regions, selected_countries, date_mode):
    """Generate a comprehensive climate report"""
    report = f"""# 🌍 ClimateScope Dashboard - Comprehensive Analysis Report

## 📊 Executive Summary

**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Data Export Mode**: Filtered Analysis

### Applied Filters
- **Regions**: {', '.join(selected_regions) if selected_regions else 'All Regions'}
- **Countries**: {', '.join(selected_countries[:5]) if selected_countries else 'All Countries'}{' (and more...)' if selected_countries and len(selected_countries) > 5 else ''}
- **Date Mode**: {date_mode.title()}

### Dataset Overview
- **Total Locations**: {len(df):,}
- **Countries Covered**: {df['normalized_country'].nunique() if 'normalized_country' in df.columns and len(df) > 0 else 'N/A'}
- **Regions Covered**: {df['geographic_region'].nunique() if 'geographic_region' in df.columns and len(df) > 0 else 'N/A'}
- **Date Range**: {df['date'].min()} to {df['date'].max() if 'date' in df.columns and len(df) > 0 else 'N/A'}

## 🌡️ Climate Analysis

### Temperature Statistics
"""
    
    if len(df) > 0:
        report += f"""
- **Global Average**: {df['temperature_celsius'].mean():.1f}°C
- **Temperature Range**: {df['temperature_celsius'].min():.1f}°C to {df['temperature_celsius'].max():.1f}°C
- **Standard Deviation**: {df['temperature_celsius'].std():.1f}°C

### Humidity Analysis
- **Average Humidity**: {df['humidity'].mean():.1f}%
- **Humidity Range**: {df['humidity'].min():.1f}% to {df['humidity'].max():.1f}%

### Wind Patterns
- **Average Wind Speed**: {df['wind_kph'].mean():.1f} km/h
- **Maximum Wind Speed**: {df['wind_kph'].max():.1f} km/h

### UV Index
- **Average UV Index**: {df['uv_index'].mean():.1f}
- **Maximum UV Index**: {df['uv_index'].max():.1f}

## 🏆 Notable Locations

### Climate Extremes
- **Hottest Location**: {df.loc[df['temperature_celsius'].idxmax(), 'location_name']}, {df.loc[df['temperature_celsius'].idxmax(), 'normalized_country']} ({df['temperature_celsius'].max():.1f}°C)
- **Coldest Location**: {df.loc[df['temperature_celsius'].idxmin(), 'location_name']}, {df.loc[df['temperature_celsius'].idxmin(), 'normalized_country']} ({df['temperature_celsius'].min():.1f}°C)
- **Most Humid**: {df.loc[df['humidity'].idxmax(), 'location_name']}, {df.loc[df['humidity'].idxmax(), 'normalized_country']} ({df['humidity'].max():.1f}%)
- **Windiest**: {df.loc[df['wind_kph'].idxmax(), 'location_name']}, {df.loc[df['wind_kph'].idxmax(), 'normalized_country']} ({df['wind_kph'].max():.1f} km/h)

## 📈 Distribution Analysis

### Temperature Distribution
"""
        
        # Temperature distribution
        hot_locations = len(df[df['temperature_celsius'] > 30])
        cold_locations = len(df[df['temperature_celsius'] < 10])
        moderate_locations = len(df[(df['temperature_celsius'] >= 10) & (df['temperature_celsius'] <= 30)])
        
        report += f"""
- **Hot Locations (>30°C)**: {hot_locations} ({hot_locations/len(df)*100:.1f}%)
- **Cold Locations (<10°C)**: {cold_locations} ({cold_locations/len(df)*100:.1f}%)
- **Moderate Locations (10-30°C)**: {moderate_locations} ({moderate_locations/len(df)*100:.1f}%)

### Humidity Patterns
"""
        
        # Humidity analysis
        high_humidity = len(df[df['humidity'] > 70])
        low_humidity = len(df[df['humidity'] < 40])
        
        report += f"""
- **High Humidity (>70%)**: {high_humidity} ({high_humidity/len(df)*100:.1f}%)
- **Low Humidity (<40%)**: {low_humidity} ({low_humidity/len(df)*100:.1f}%)

### Wind Analysis
"""
        
        # Wind analysis
        windy_locations = len(df[df['wind_kph'] > 20])
        calm_locations = len(df[df['wind_kph'] < 10])
        
        report += f"""
- **Windy Locations (>20 km/h)**: {windy_locations} ({windy_locations/len(df)*100:.1f}%)
- **Calm Locations (<10 km/h)**: {calm_locations} ({calm_locations/len(df)*100:.1f}%)

## 🌍 Regional Breakdown
"""
        
        # Regional analysis
        if 'geographic_region' in df.columns:
            regional_temps = df.groupby('geographic_region')['temperature_celsius'].mean().sort_values(ascending=False)
            report += "\n### Average Temperature by Region\n"
            for region, temp in regional_temps.head(10).items():
                report += f"- **{region}**: {temp:.1f}°C\n"
            
            regional_humidity = df.groupby('geographic_region')['humidity'].mean().sort_values(ascending=False)
            report += "\n### Average Humidity by Region\n"
            for region, humidity in regional_humidity.head(5).items():
                report += f"- **{region}**: {humidity:.1f}%\n"
        
        report += f"""

## 🔍 Data Quality Assessment

- **Complete Temperature Records**: {df['temperature_celsius'].notna().sum():,} ({df['temperature_celsius'].notna().sum()/len(df)*100:.1f}%)
- **Complete Humidity Records**: {df['humidity'].notna().sum():,} ({df['humidity'].notna().sum()/len(df)*100:.1f}%)
- **Complete Wind Records**: {df['wind_kph'].notna().sum():,} ({df['wind_kph'].notna().sum()/len(df)*100:.1f}%)

## 💡 Key Insights

1. **Climate Diversity**: The filtered dataset shows a temperature range of {df['temperature_celsius'].max() - df['temperature_celsius'].min():.1f}°C, indicating significant climate diversity.

2. **Comfort Zones**: {moderate_locations} locations ({moderate_locations/len(df)*100:.1f}%) fall within the moderate temperature range (10-30°C).

3. **Extreme Conditions**: {hot_locations + cold_locations} locations ({(hot_locations + cold_locations)/len(df)*100:.1f}%) experience extreme temperatures.

4. **Humidity Patterns**: {high_humidity} locations have high humidity, which may affect comfort and weather patterns.

## 📊 Statistical Summary

| Metric | Mean | Min | Max | Std Dev |
|--------|------|-----|-----|---------|
| Temperature (°C) | {df['temperature_celsius'].mean():.1f} | {df['temperature_celsius'].min():.1f} | {df['temperature_celsius'].max():.1f} | {df['temperature_celsius'].std():.1f} |
| Humidity (%) | {df['humidity'].mean():.1f} | {df['humidity'].min():.1f} | {df['humidity'].max():.1f} | {df['humidity'].std():.1f} |
| Wind Speed (km/h) | {df['wind_kph'].mean():.1f} | {df['wind_kph'].min():.1f} | {df['wind_kph'].max():.1f} | {df['wind_kph'].std():.1f} |
| UV Index | {df['uv_index'].mean():.1f} | {df['uv_index'].min():.1f} | {df['uv_index'].max():.1f} | {df['uv_index'].std():.1f} |

"""
    else:
        report += "\n**No data available for analysis with current filters.**\n"
    
    report += f"""
## 🔬 Methodology

This report was generated from the ClimateScope Dashboard using filtered weather data based on user selections:

1. **Data Processing**: Applied regional and country filters as specified
2. **Statistical Analysis**: Calculated descriptive statistics for all metrics
3. **Extreme Value Analysis**: Identified locations with maximum and minimum values
4. **Distribution Analysis**: Categorized locations by climate characteristics
5. **Regional Comparison**: Analyzed average values by geographic region

## 📝 Recommendations

Based on the current analysis:

1. **Travel Planning**: Consider the moderate climate locations for comfortable travel experiences
2. **Climate Monitoring**: Monitor locations with extreme temperatures for potential weather events
3. **Health Considerations**: Be aware of high UV index locations requiring sun protection
4. **Regional Insights**: Use regional averages to understand broader climate patterns

---

*Report generated by ClimateScope Dashboard - Advanced Weather Analytics Platform*  
*Export Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*Dashboard Version: Enhanced with Export Features*
"""
    
    return report

# Run the app
if __name__ == '__main__':
    print("🌍 Starting Enhanced ClimateScope Dashboard...")
    print(f"📊 Loaded data with {len(df)} records from {len(df['normalized_country'].unique()) if not df.empty else 0} countries")
    print("🚀 Enhanced features: Comprehensive report generation")
    print("🚀 Access the dashboard at: http://127.0.0.1:8052")
    app.run(debug=True, host='127.0.0.1', port=8052)
