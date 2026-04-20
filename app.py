"""
Manufacturing Process Health Dashboard
Streamlit web application for real-time manufacturing analytics
"""

import streamlit as st
import pandas as pd
import numpy as np
import logging
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import modules
from config.config import (
    STREAMLIT_CONFIG,
    DATA_FILE,
    EFFICIENCY_COLORS,
    PROJECT_VERSION,
    LOG_LEVEL
)
from src.data_loader import load_and_validate_data
from src.data_processor import preprocess_data
from src.analyzer import perform_analysis
from src.kpi_calculator import calculate_kpis
from src.dashboard_components import (
    metric_card,
    efficiency_gauge,
    efficiency_distribution_pie,
    machine_health_heatmap,
    comparison_bar_chart,
    scatter_plot,
    box_plot,
    create_sidebar_filters,
    filter_data,
    display_kpi_row,
    create_data_table,
    time_series_plot,
    correlation_heatmap,
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== STREAMLIT PAGE CONFIGURATION ====================
st.set_page_config(**STREAMLIT_CONFIG)
st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 28px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==================== CACHE FUNCTIONS ====================
@st.cache_data
def load_data():
    """Load and validate data"""
    logger.info("Loading data...")
    try:
        data, is_valid, validation_report = load_and_validate_data(DATA_FILE)
        
        if not is_valid:
            st.warning("Data validation completed with warnings")
            logger.warning(f"Validation report: {validation_report}")
        
        logger.info("Data loaded successfully")
        return data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        logger.error(f"Data loading failed: {str(e)}")
        return None


@st.cache_data
def process_data(data):
    """Process and preprocess data"""
    logger.info("Processing data...")
    try:
        processed_data, report = preprocess_data(data)
        logger.info(f"Data processing completed: {report['steps_applied']}")
        return processed_data
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        logger.error(f"Data processing failed: {str(e)}")
        return None


@st.cache_data
def analyze_data(data):
    """Perform analysis"""
    logger.info("Analyzing data...")
    try:
        analysis_results = perform_analysis(data)
        logger.info("Analysis completed successfully")
        return analysis_results
    except Exception as e:
        st.error(f"Error analyzing data: {str(e)}")
        logger.error(f"Analysis failed: {str(e)}")
        return None


@st.cache_data
def compute_kpis(data):
    """Calculate KPIs"""
    logger.info("Computing KPIs...")
    try:
        kpis = calculate_kpis(data)
        logger.info("KPI calculation completed")
        return kpis
    except Exception as e:
        st.error(f"Error computing KPIs: {str(e)}")
        logger.error(f"KPI computation failed: {str(e)}")
        return None


# ==================== MAIN APPLICATION ====================
def main():
    """Main application function"""
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🏭 Manufacturing Process Health Dashboard")
        st.caption(f"6G-Enabled Smart Factory Analytics | v{PROJECT_VERSION}")
    
    with col2:
        st.info(f"📊 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load data
    with st.spinner("Loading data..."):
        raw_data = load_data()
    
    if raw_data is None or raw_data.empty:
        st.error("Failed to load data. Please check the data file.")
        return
    
    # Process data
    with st.spinner("Processing data..."):
        data = process_data(raw_data)
    
    if data is None or data.empty:
        st.error("Failed to process data.")
        return
    
    # Analyze data
    with st.spinner("Analyzing data..."):
        analysis_results = analyze_data(data)
    
    # Calculate KPIs
    with st.spinner("Computing KPIs..."):
        kpis = compute_kpis(data)
    
    # Create filters
    selected_machines, selected_modes, selected_efficiency = create_sidebar_filters(data)
    
    # Filter data
    filtered_data = filter_data(
        data,
        machines=selected_machines if selected_machines else None,
        modes=selected_modes if selected_modes else None,
        efficiency_status=selected_efficiency if selected_efficiency else None
    )
    
    if filtered_data.empty:
        st.warning("No data matches the selected filters. Please adjust your selection.")
        return
    
    # ==================== TABS ====================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Factory Health Overview",
        "🤖 Machine Health Dashboard",
        "📈 Production & Quality",
        "⚡ Efficiency Diagnostics",
        "📋 Data Explorer"
    ])
    
    # ==================== TAB 1: FACTORY HEALTH OVERVIEW ====================
    with tab1:
        st.markdown("### Factory Health Overview")
        
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Total Records",
                f"{len(filtered_data):,}",
                help="Total number of records analyzed"
            )
        with col2:
            avg_efficiency_high = (filtered_data['Efficiency_Status'] == 'High').sum() / len(filtered_data) * 100
            st.metric(
                "High Efficiency %",
                f"{avg_efficiency_high:.1f}%",
                help="Percentage of high efficiency operations"
            )
        with col3:
            avg_temp = filtered_data['Temperature_C'].mean()
            st.metric(
                "Avg Temperature",
                f"{avg_temp:.1f}°C",
                help="Average machine temperature"
            )
        with col4:
            avg_error = filtered_data['Error_Rate_%'].mean()
            st.metric(
                "Avg Error Rate",
                f"{avg_error:.2f}%",
                help="Average operational error rate"
            )
        
        st.divider()
        
        # Efficiency Distribution
        col1, col2 = st.columns(2)
        with col1:
            efficiency_distribution_pie(filtered_data, "Efficiency Status Distribution")
        
        with col2:
            efficiency_data = filtered_data['Efficiency_Status'].value_counts().reset_index()
            efficiency_data.columns = ['Efficiency_Status', 'Count']
            st.write("### Efficiency Breakdown")
            for _, row in efficiency_data.iterrows():
                color = EFFICIENCY_COLORS.get(row['Efficiency_Status'], '#gray')
                st.write(
                    f"<span style='color:{color}'>●</span> "
                    f"<b>{row['Efficiency_Status']}</b>: {row['Count']} records",
                    unsafe_allow_html=True
                )
        
        st.divider()
        
        # Sensor Metrics Overview
        st.write("### Average Sensor Metrics")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Temperature", f"{filtered_data['Temperature_C'].mean():.1f}°C")
        with col2:
            st.metric("Vibration", f"{filtered_data['Vibration_Hz'].mean():.2f} Hz")
        with col3:
            st.metric("Power", f"{filtered_data['Power_Consumption_kW'].mean():.2f} kW")
        with col4:
            st.metric("Network Latency", f"{filtered_data['Network_Latency_ms'].mean():.1f} ms")
        with col5:
            st.metric("Packet Loss", f"{filtered_data['Packet_Loss_%'].mean():.2f}%")
        
        st.divider()
        
        # Efficiency by Operation Mode
        st.write("### Efficiency by Operation Mode")
        mode_efficiency = filtered_data.groupby('Operation_Mode')['Efficiency_Status'].value_counts(normalize=True).unstack(fill_value=0) * 100
        
        comparison_bar_chart(
            mode_efficiency.reset_index().melt(
                id_vars='Operation_Mode',
                var_name='Efficiency_Status',
                value_name='Percentage'
            ),
            x_col='Operation_Mode',
            y_col='Percentage',
            title="Efficiency Distribution by Operation Mode",
            color_col='Efficiency_Status',
        )
    
    # ==================== TAB 2: MACHINE HEALTH DASHBOARD ====================
    with tab2:
        st.markdown("### Machine Health Dashboard")
        
        # Machine Health Index
        if kpis and 'machine_health_index' in kpis:
            st.write("### Machine Health Scores")
            health_data = kpis['machine_health_index'].reset_index()
            health_data.columns = ['Machine_ID', 'Health_Score', 'Health_Status']
            
            machine_health_heatmap(kpis['machine_health_index'])
            
            st.write("### Machine Health Rankings")
            create_data_table(health_data.head(15))
        
        st.divider()
        
        # Machine Performance Comparison
        if analysis_results and 'machine_performance' in analysis_results:
            st.write("### Machine Performance Metrics")
            
            performance_data = []
            for machine_id, metrics in analysis_results['machine_performance'].items():
                if machine_id in selected_machines:
                    performance_data.append({
                        'Machine_ID': machine_id,
                        'Efficiency_High_%': metrics['efficiency_high_pct'],
                        'Avg_Temperature': metrics['avg_temperature'],
                        'Avg_Vibration': metrics['avg_vibration'],
                        'Maintenance_Score': metrics['maintenance_score'],
                    })
            
            if performance_data:
                perf_df = pd.DataFrame(performance_data)
                create_data_table(perf_df)
        
        st.divider()
        
        # Machine Selection for Detailed View
        st.write("### Detailed Machine Analysis")
        selected_machine = st.selectbox(
            "Select a Machine",
            options=sorted(filtered_data['Machine_ID'].unique())
        )
        
        if selected_machine:
            machine_data = filtered_data[filtered_data['Machine_ID'] == selected_machine]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Records", len(machine_data))
            with col2:
                high_eff = (machine_data['Efficiency_Status'] == 'High').sum() / len(machine_data) * 100
                st.metric("High Efficiency %", f"{high_eff:.1f}%")
            with col3:
                st.metric("Avg Error Rate", f"{machine_data['Error_Rate_%'].mean():.2f}%")
            with col4:
                st.metric("Avg Production Speed", f"{machine_data['Production_Speed_units_per_hr'].mean():.0f}")
            
            # Machine sensor trends
            if 'Hour' in machine_data.columns:
                hourly_data = machine_data.groupby('Hour').agg({
                    'Temperature_C': 'mean',
                    'Vibration_Hz': 'mean',
                    'Power_Consumption_kW': 'mean',
                }).reset_index()
                
                st.write("### Sensor Trends (Hourly)")
                time_series_plot(
                    hourly_data,
                    'Hour',
                    ['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW'],
                    title=f"Sensor Trends - Machine {selected_machine}",
                    y_axis_title="Value"
                )
    
    # ==================== TAB 3: PRODUCTION & QUALITY ====================
    with tab3:
        st.markdown("### Production & Quality Analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Avg Production Speed",
                f"{filtered_data['Production_Speed_units_per_hr'].mean():.0f}",
                help="Units per hour"
            )
        with col2:
            st.metric(
                "Avg Defect Rate",
                f"{filtered_data['Quality_Control_Defect_Rate_%'].mean():.2f}%"
            )
        with col3:
            st.metric(
                "Avg Error Rate",
                f"{filtered_data['Error_Rate_%'].mean():.2f}%"
            )
        with col4:
            st.metric(
                "Total Defects",
                f"{(filtered_data['Quality_Control_Defect_Rate_%'] > 0).sum():,}"
            )
        
        st.divider()
        
        # Production vs Defect Rate
        st.write("### Production Speed vs Defect Rate")
        scatter_plot(
            filtered_data,
            'Production_Speed_units_per_hr',
            'Quality_Control_Defect_Rate_%',
            title="Production Speed vs Defect Rate",
            color_col='Efficiency_Status',
            size_max=15
        )
        
        st.divider()
        
        # Error Rate Distribution
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Error Rate by Machine")
            machine_errors = filtered_data.groupby('Machine_ID')['Error_Rate_%'].mean().reset_index()
            comparison_bar_chart(
                machine_errors.sort_values('Error_Rate_%', ascending=False).head(15),
                'Machine_ID',
                'Error_Rate_%',
                title="Top 15 Machines by Error Rate"
            )
        
        with col2:
            st.write("### Defect Rate by Machine")
            machine_defects = filtered_data.groupby('Machine_ID')['Quality_Control_Defect_Rate_%'].mean().reset_index()
            comparison_bar_chart(
                machine_defects.sort_values('Quality_Control_Defect_Rate_%', ascending=False).head(15),
                'Machine_ID',
                'Quality_Control_Defect_Rate_%',
                title="Top 15 Machines by Defect Rate"
            )
        
        st.divider()
        
        # Quality Control by Operation Mode
        st.write("### Quality Metrics by Operation Mode")
        mode_quality = filtered_data.groupby('Operation_Mode').agg({
            'Quality_Control_Defect_Rate_%': 'mean',
            'Error_Rate_%': 'mean',
            'Production_Speed_units_per_hr': 'mean',
        }).reset_index()
        
        create_data_table(mode_quality.round(2))
    
    # ==================== TAB 4: EFFICIENCY DIAGNOSTICS ====================
    with tab4:
        st.markdown("### Efficiency Diagnostics")
        
        # Efficiency Status Breakdown
        st.write("### Efficiency Distribution Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            efficiency_dist = filtered_data['Efficiency_Status'].value_counts()
            st.write("#### Status Counts")
            for status, count in efficiency_dist.items():
                percentage = (count / len(filtered_data)) * 100
                st.write(f"**{status}**: {count} ({percentage:.1f}%)")
        
        with col2:
            # Efficiency by mode
            mode_dist = pd.crosstab(
                filtered_data['Operation_Mode'],
                filtered_data['Efficiency_Status'],
                margins=True
            )
            st.write("#### Efficiency by Operation Mode")
            st.dataframe(mode_dist)
        
        st.divider()
        
        # Box plot: Efficiency-related metrics
        st.write("### Metric Distributions by Efficiency Status")
        col1, col2 = st.columns(2)
        
        with col1:
            box_plot(
                filtered_data,
                'Efficiency_Status',
                'Temperature_C',
                title="Temperature by Efficiency Status"
            )
        
        with col2:
            box_plot(
                filtered_data,
                'Efficiency_Status',
                'Error_Rate_%',
                title="Error Rate by Efficiency Status"
            )
        
        st.divider()
        
        # Metrics correlation with efficiency
        if analysis_results and 'sensor_correlations' in analysis_results:
            st.write("### Sensor Correlation with Efficiency")
            corr_data = analysis_results['sensor_correlations']
            st.dataframe(corr_data)
        
        st.divider()
        
        # Critical machines
        if analysis_results and 'critical_machines' in analysis_results:
            critical = analysis_results['critical_machines']
            if critical:
                st.write("### ⚠️ Critical Machines Requiring Attention")
                for machine_id, info in critical.items():
                    if machine_id in selected_machines:
                        with st.expander(f"Machine {machine_id} - Low Efficiency {info['low_efficiency_pct']:.1f}%"):
                            st.write(f"**Issues:** {', '.join(info['issues']) if info['issues'] else 'No specific issues detected'}")
            else:
                st.info("✅ No critical machines detected")
    
    # ==================== TAB 5: DATA EXPLORER ====================
    with tab5:
        st.markdown("### Data Explorer")
        
        # Data Summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Machines", filtered_data['Machine_ID'].nunique())
        with col2:
            st.metric("Total Records", f"{len(filtered_data):,}")
        with col3:
            st.metric("Operation Modes", filtered_data['Operation_Mode'].nunique())
        with col4:
            st.metric("Memory Usage", f"{filtered_data.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        st.divider()
        
        # Data Table
        st.write("### Raw Data")
        page_size = st.selectbox("Records per page", [10, 25, 50, 100, 250])
        
        # Pagination
        total_pages = (len(filtered_data) + page_size - 1) // page_size
        page = st.selectbox("Page", range(1, total_pages + 1))
        
        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, len(filtered_data))
        
        st.write(f"Showing {start_idx + 1} to {end_idx} of {len(filtered_data)} records")
        
        display_cols = st.multiselect(
            "Select columns to display",
            options=filtered_data.columns.tolist(),
            default=filtered_data.columns.tolist()[:10]
        )
        
        if display_cols:
            st.dataframe(
                filtered_data.iloc[start_idx:end_idx][display_cols],
                use_container_width=True,
                height=400
            )
        
        st.divider()
        
        # Download Data
        st.write("### Download Data")
        csv = filtered_data.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"manufacturing_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # ==================== FOOTER ====================
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("🏭 6G-Enabled Smart Manufacturing Analytics")
    with col2:
        st.caption(f"Data Records: {len(raw_data):,}")
    with col3:
        st.caption(f"Analysis Version: {PROJECT_VERSION}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        logger.error(f"Application crashed: {str(e)}", exc_info=True)
