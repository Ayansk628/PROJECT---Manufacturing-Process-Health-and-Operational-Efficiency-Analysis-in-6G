"""
Dashboard Components Module
Reusable Streamlit components for the dashboard
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import EFFICIENCY_COLORS, CHART_COLORS


def metric_card(
    title: str,
    value: any,
    unit: str = "",
    delta: Optional[float] = None,
    delta_color: str = "normal",
    help_text: Optional[str] = None,
    col_width: float = 1.0
) -> None:
    """
    Display a metric card
    
    Args:
        title: Metric title
        value: Metric value
        unit: Unit of measurement
        delta: Change in value
        delta_color: Color for delta ('normal', 'inverse', 'off')
        help_text: Help text tooltip
        col_width: Column width (0-1)
    """
    with st.container():
        col1, col2 = st.columns([1, 10])
        
        with col1:
            st.write("")
        
        with col2:
            if isinstance(value, float):
                value_str = f"{value:,.2f}"
            else:
                value_str = str(value)
            
            metric_text = f"## {value_str}"
            if unit:
                metric_text += f" {unit}"
            
            st.write(metric_text)
            st.write(f"**{title}**")
            
            if help_text:
                st.caption(help_text)


def efficiency_gauge(
    value: float,
    min_val: float = 0,
    max_val: float = 100,
    title: str = "Efficiency Score"
) -> None:
    """
    Display an efficiency gauge chart
    
    Args:
        value: Current value
        min_val: Minimum value
        max_val: Maximum value
        title: Chart title
    """
    fig = go.Figure(data=[go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [min_val, max_val], 'y': [min_val, max_val]},
        title={'text': title},
        delta={'reference': max_val * 0.8},
        gauge={
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [min_val, max_val * 0.33], 'color': "lightgray"},
                {'range': [max_val * 0.33, max_val * 0.66], 'color': "gray"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_val}
        }
    )])
    
    fig.update_layout(height=400, margin=dict(l=15, r=15, t=15, b=15))
    st.plotly_chart(fig, use_container_width=True)


def efficiency_distribution_pie(
    data: pd.DataFrame,
    title: str = "Efficiency Status Distribution"
) -> None:
    """
    Display efficiency distribution as pie chart
    
    Args:
        data: DataFrame with Efficiency_Status column
        title: Chart title
    """
    efficiency_counts = data['Efficiency_Status'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=efficiency_counts.index,
        values=efficiency_counts.values,
        marker=dict(colors=[
            EFFICIENCY_COLORS.get(label, '#gray')
            for label in efficiency_counts.index
        ]),
        textposition='inside',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=title,
        height=400,
        margin=dict(l=15, r=15, t=40, b=15),
    )
    
    st.plotly_chart(fig, use_container_width=True)


def machine_health_heatmap(
    machine_health_df: pd.DataFrame,
    title: str = "Machine Health Index Heatmap"
) -> None:
    """
    Display machine health as heatmap
    
    Args:
        machine_health_df: DataFrame with machine health scores
        title: Chart title
    """
    if machine_health_df.empty:
        st.warning("No data available for heatmap")
        return
    
    # Prepare data
    health_matrix = machine_health_df[['Health_Score']].T
    
    fig = go.Figure(data=go.Heatmap(
        z=health_matrix.values,
        x=health_matrix.columns,
        y=health_matrix.index,
        colorscale='RdYlGn',
        zmid=0.5,
        zmin=0,
        zmax=1,
        hovertemplate='Machine: %{x}<br>Score: %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        height=300,
        margin=dict(l=15, r=15, t=40, b=80),
        xaxis_title='Machine ID',
    )
    
    st.plotly_chart(fig, use_container_width=True)


def time_series_plot(
    data: pd.DataFrame,
    x_col: str,
    y_cols: List[str],
    title: str = "Time Series Analysis",
    y_axis_title: str = "Value"
) -> None:
    """
    Display time series line plot
    
    Args:
        data: DataFrame with data
        x_col: X-axis column name
        y_cols: List of Y-axis column names
        title: Chart title
        y_axis_title: Y-axis label
    """
    fig = go.Figure()
    
    for y_col in y_cols:
        if y_col in data.columns:
            fig.add_trace(go.Scatter(
                x=data[x_col],
                y=data[y_col],
                mode='lines',
                name=y_col,
                hovertemplate='<b>' + y_col + '</b><br>' +
                             x_col + ': %{x}<br>' +
                             'Value: %{y:.2f}<extra></extra>'
            ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title=y_axis_title,
        height=400,
        hovermode='x unified',
        margin=dict(l=15, r=15, t=40, b=15),
    )
    
    st.plotly_chart(fig, use_container_width=True)


def comparison_bar_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "Comparison Chart",
    color_col: Optional[str] = None,
    orientation: str = 'v'
) -> None:
    """
    Display comparison bar chart
    
    Args:
        data: DataFrame with data
        x_col: X-axis column name
        y_col: Y-axis column name
        title: Chart title
        color_col: Column for color coding
        orientation: 'v' for vertical, 'h' for horizontal
    """
    fig = px.bar(
        data,
        x=x_col if orientation == 'v' else y_col,
        y=y_col if orientation == 'v' else x_col,
        color=color_col,
        title=title,
        labels={x_col: x_col, y_col: y_col},
        orientation=orientation,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    
    fig.update_layout(
        height=400,
        margin=dict(l=15, r=15, t=40, b=15),
        hovermode='closest',
    )
    
    st.plotly_chart(fig, use_container_width=True)


def scatter_plot(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "Scatter Plot",
    size_col: Optional[str] = None,
    color_col: Optional[str] = None,
    size_max: int = 10
) -> None:
    """
    Display scatter plot
    
    Args:
        data: DataFrame with data
        x_col: X-axis column name
        y_col: Y-axis column name
        title: Chart title
        size_col: Column for bubble size
        color_col: Column for color coding
        size_max: Maximum bubble size
    """
    fig = px.scatter(
        data,
        x=x_col,
        y=y_col,
        size=size_col,
        color=color_col,
        title=title,
        size_max=size_max,
        color_continuous_scale='Viridis' if color_col else None,
        hover_data={'Machine_ID': True} if 'Machine_ID' in data.columns else None
    )
    
    fig.update_layout(
        height=400,
        margin=dict(l=15, r=15, t=40, b=15),
        hovermode='closest',
    )
    
    st.plotly_chart(fig, use_container_width=True)


def distribution_histogram(
    data: pd.Series,
    title: str = "Distribution",
    nbins: int = 30,
    x_title: str = "Value",
) -> None:
    """
    Display distribution histogram
    
    Args:
        data: Series with data
        title: Chart title
        nbins: Number of bins
        x_title: X-axis label
    """
    fig = go.Figure(data=[go.Histogram(
        x=data,
        nbinsx=nbins,
        marker=dict(color=CHART_COLORS['primary']),
        hovertemplate='Range: %{x}<br>Count: %{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title='Frequency',
        height=400,
        margin=dict(l=15, r=15, t=40, b=15),
    )
    
    st.plotly_chart(fig, use_container_width=True)


def box_plot(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "Distribution Comparison",
    color_col: Optional[str] = None
) -> None:
    """
    Display box plot
    
    Args:
        data: DataFrame with data
        x_col: X-axis column name (categorical)
        y_col: Y-axis column name (numeric)
        title: Chart title
        color_col: Column for color coding
    """
    fig = px.box(
        data,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        points='outliers'
    )
    
    fig.update_layout(
        height=400,
        margin=dict(l=15, r=15, t=40, b=15),
    )
    
    st.plotly_chart(fig, use_container_width=True)


def correlation_heatmap(
    correlation_matrix: pd.DataFrame,
    title: str = "Correlation Matrix"
) -> None:
    """
    Display correlation heatmap
    
    Args:
        correlation_matrix: Correlation DataFrame
        title: Chart title
    """
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        colorscale='RdBu',
        zmid=0,
        zmin=-1,
        zmax=1,
        text=correlation_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        hovertemplate='%{x} - %{y}<br>Correlation: %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        height=500,
        margin=dict(l=100, r=15, t=40, b=100),
    )
    
    st.plotly_chart(fig, use_container_width=True)


def create_sidebar_filters(data: pd.DataFrame) -> Tuple[List[int], List[str], Tuple]:
    """
    Create sidebar filter controls
    
    Args:
        data: DataFrame to filter
        
    Returns:
        Tuple of (selected_machines, selected_modes, date_range)
    """
    st.sidebar.markdown("### 🎛️ Filters")
    
    # Machine selector
    all_machines = sorted(data['Machine_ID'].unique())
    selected_machines = st.sidebar.multiselect(
        "Select Machines",
        options=all_machines,
        default=all_machines[:5] if len(all_machines) > 5 else all_machines,
        help="Choose one or more machines to analyze"
    )
    
    # Operation mode selector
    all_modes = data['Operation_Mode'].unique()
    selected_modes = st.sidebar.multiselect(
        "Select Operation Modes",
        options=all_modes,
        default=list(all_modes),
        help="Choose operation modes to include"
    )
    
    # Efficiency status filter
    efficiency_filter = st.sidebar.multiselect(
        "Select Efficiency Status",
        options=['High', 'Medium', 'Low'],
        default=['High', 'Medium', 'Low'],
        help="Filter by efficiency level"
    )
    
    return selected_machines, selected_modes, efficiency_filter


def filter_data(
    data: pd.DataFrame,
    machines: Optional[List[int]] = None,
    modes: Optional[List[str]] = None,
    efficiency_status: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Filter data based on provided criteria
    
    Args:
        data: DataFrame to filter
        machines: List of machine IDs
        modes: List of operation modes
        efficiency_status: List of efficiency statuses
        
    Returns:
        Filtered DataFrame
    """
    filtered = data.copy()
    
    if machines:
        filtered = filtered[filtered['Machine_ID'].isin(machines)]
    
    if modes:
        filtered = filtered[filtered['Operation_Mode'].isin(modes)]
    
    if efficiency_status:
        filtered = filtered[filtered['Efficiency_Status'].isin(efficiency_status)]
    
    return filtered


def display_kpi_row(kpi_data: Dict) -> None:
    """
    Display KPI metrics in a row
    
    Args:
        kpi_data: Dictionary with KPI name and value pairs
    """
    cols = st.columns(len(kpi_data))
    
    for col, (kpi_name, kpi_value) in zip(cols, kpi_data.items()):
        with col:
            if isinstance(kpi_value, float):
                st.metric(kpi_name, f"{kpi_value:.2f}")
            else:
                st.metric(kpi_name, kpi_value)


def create_data_table(
    data: pd.DataFrame,
    title: str = "Data Table",
    height: int = 400,
    use_container_width: bool = True
) -> None:
    """
    Display interactive data table
    
    Args:
        data: DataFrame to display
        title: Table title
        height: Table height in pixels
        use_container_width: Whether to use full container width
    """
    st.write(f"### {title}")
    st.dataframe(
        data,
        height=height,
        use_container_width=use_container_width,
        hide_index=False
    )
