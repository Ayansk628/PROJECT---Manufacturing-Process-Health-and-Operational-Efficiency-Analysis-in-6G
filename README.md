# Manufacturing Process Health and Operational Efficiency Analysis Dashboard

## Project Overview

This is a professional-grade, production-ready dashboard and analytics platform for analyzing manufacturing process health and operational efficiency in 6G-enabled smart factories. The project provides comprehensive real-time monitoring, diagnostics, and insights for identifying machine health issues, production inefficiencies, and quality bottlenecks.

### Key Features

- **Real-time Machine Health Monitoring**: Track temperature, vibration, power consumption, and network metrics
- **Comprehensive Data Analysis**: Exploratory data analysis with statistical insights
- **Interactive Dashboard**: Multi-tab Streamlit interface with real-time filtering and visualizations
- **KPI Calculations**: Industry-standard performance indicators and benchmarking
- **Production & Quality Analytics**: Defect rate analysis, error frequency tracking, and quality diagnostics
- **Efficiency Diagnostics**: Analyze efficiency status distribution across machines and operation modes
- **Data Validation**: Robust error handling and data quality checks
- **Production-Ready**: Python 3.8+ support with comprehensive logging and error handling

---

## Project Structure

```
Manufacturing Process Health Dashboard/
├── app.py                              # Main Streamlit application
├── requirements.txt                    # Project dependencies
├── README.md                           # This file
├── .gitignore                          # Git ignore rules
│
├── config/                             # Configuration module
│   ├── __init__.py
│   └── config.py                       # All configuration constants
│
├── src/                                # Source code modules
│   ├── __init__.py
│   ├── data_loader.py                  # Data loading & validation
│   ├── data_processor.py               # Data preprocessing & cleaning
│   ├── analyzer.py                     # EDA & analysis functions
│   ├── kpi_calculator.py               # KPI computation
│   └── dashboard_components.py         # Reusable Streamlit components
│
├── notebooks/                          # Jupyter notebooks
│   └── EDA_Research.ipynb              # Exploratory data analysis & insights
│
├── docs/                               # Documentation
│   ├── RESEARCH_PAPER.md               # Detailed research findings
│   └── EXECUTIVE_SUMMARY.md            # Executive summary for stakeholders
│
├── utils/                              # Utility functions
│
├── data/                               # Data directory
│
└── Thales_Group_Manufacturing (1).csv  # Input dataset
```

---

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip or conda package manager

### Step 1: Clone/Download Project

```bash
cd "Manufacturing Process Health and Operational Efficiency Analysis"
```

### Step 2: Create Virtual Environment (Recommended)

**Using venv (Python built-in):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Using conda:**
```bash
conda create -n mfg-analysis python=3.10
conda activate mfg-analysis
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**For Python 3.8 specifically:**
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "import pandas; import streamlit; print('Installation successful!')"
```

---

## Quick Start

### Running the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

### Using the Analysis Modules Directly

```python
from src.data_loader import load_and_validate_data
from src.data_processor import preprocess_data
from src.analyzer import perform_analysis
from src.kpi_calculator import calculate_kpis

# Load data
data, is_valid, report = load_and_validate_data()

# Process data
processed_data, proc_report = preprocess_data(data)

# Analyze
analysis_results = perform_analysis(processed_data)

# Calculate KPIs
kpis = calculate_kpis(processed_data)

# Access results
print(analysis_results['insights'])
print(kpis['machine_health_index'])
```

---

## Dashboard Modules

### 1. **Factory Health Overview** 📊
- Overall efficiency distribution (High/Medium/Low)
- Average sensor metrics (Temperature, Vibration, Power, Network)
- Efficiency breakdown by operation mode
- Real-time KPI summary

### 2. **Machine Health Dashboard** 🤖
- Machine health index scores and heatmap
- Detailed machine performance metrics
- Per-machine sensor trend analysis
- Health status rankings

### 3. **Production & Quality Panel** 📈
- Production speed trends and analysis
- Quality control defect rate tracking
- Operational error frequency analysis
- Quality metrics by operation mode

### 4. **Efficiency Diagnostics** ⚡
- Efficiency status distribution analysis
- Metric distributions by efficiency level
- Sensor correlations with efficiency
- Critical machine identification
- Root cause analysis indicators

### 5. **Data Explorer** 📋
- Interactive raw data viewer with pagination
- Customizable column selection
- CSV download functionality
- Data summary statistics

---

## Configuration

All configuration settings are centralized in `config/config.py`:

### Key Sections

- **Sensor Thresholds**: Normal/warning/critical ranges for each sensor
- **Benchmark Values**: Industry standard targets for performance metrics
- **KPI Weights**: Weighting factors for composite health scoring
- **Operation Modes**: Valid machine operating states
- **Efficiency Colors**: Color coding for visualization

### Customization Example

```python
# Edit config/config.py
SENSOR_THRESHOLDS = {
    'Temperature_C': {
        'normal_min': 20.0,
        'normal_max': 80.0,
        'warning_max': 95.0,
        'critical_max': 105.0,
    },
    # ...
}
```

---

## Data Format

### Required CSV Columns

| Column | Type | Description |
|--------|------|-------------|
| Date | string (DD-MM-YYYY) | Recording date |
| Timestamp | string (HH:MM:SS) | Recording time |
| Machine_ID | integer | Unique machine identifier |
| Operation_Mode | string | Operating mode (Idle, Active, High-Load, etc.) |
| Temperature_C | float | Temperature in Celsius |
| Vibration_Hz | float | Vibration frequency in Hertz |
| Power_Consumption_kW | float | Power consumption in kilowatts |
| Network_Latency_ms | float | Network latency in milliseconds |
| Packet_Loss_% | float | Data packet loss percentage |
| Quality_Control_Defect_Rate_% | float | Defect rate percentage |
| Production_Speed_units_per_hr | float | Production output per hour |
| Predictive_Maintenance_Score | float | AI maintenance score (0-1) |
| Error_Rate_% | float | Operational error rate percentage |
| Efficiency_Status | string | Status classification (High/Medium/Low) |

---

## Key Performance Indicators (KPIs)

### 1. **Machine Health Index**
Composite score (0-1) calculated from:
- Temperature stability (25% weight)
- Vibration control (25% weight)
- Power efficiency (20% weight)
- Network reliability (15% weight)
- Predictive maintenance readiness (15% weight)

### 2. **Average Production Speed**
- Overall average output rate
- Per-machine production trends
- Mode-based comparisons

### 3. **Defect Density Score**
- Defect rate relative to production volume
- Quality bottleneck identification
- Production speed vs. quality trade-offs

### 4. **Error Frequency Index**
- Operational error rate analysis
- High-error machine identification
- Temporal error patterns

### 5. **Efficiency Distribution**
- High/Medium/Low efficiency breakdown
- Machine-level efficiency profiles
- Mode-based efficiency variations

---

## Data Validation & Quality

### Automated Validation Checks

1. **Schema Validation**: Verifies all required columns present
2. **Data Type Validation**: Ensures correct data types
3. **Range Validation**: Checks values within acceptable bounds
4. **Datetime Validation**: Validates date/time formats
5. **Null Value Handling**: Forward/backward fill or removal

### Data Processing Pipeline

1. Create unified DateTime column
2. Handle missing values (forward fill strategy)
3. Optimize data types (memory efficiency)
4. Add temporal features (Hour, Day, Month, Shift)
5. Add health indicators (Temperature, Vibration, Power, Network health)
6. Remove statistical outliers (IQR method)

---

## Error Handling

The application includes comprehensive error handling:

- **FileNotFoundError**: Data file not found
- **ValueError**: Invalid data structure or empty dataset
- **TypeError**: Data type conversion errors
- **KeyError**: Missing required columns
- **Logging**: All errors logged for debugging

All errors are caught and displayed to the user with helpful messages.

---

## Performance Optimization

- **Caching**: Data loading and processing cached with Streamlit
- **Type Optimization**: Numeric columns reduced to float32 where appropriate
- **Memory Efficiency**: Reported in UI for transparency
- **Query Filtering**: Client-side filtering for interactive performance

---

## Extending the Dashboard

### Adding a New Analysis

```python
# In src/analyzer.py
def analyze_new_metric(self) -> Dict:
    """Analyze a new metric"""
    try:
        # Your analysis code here
        result = self.data.groupby('Machine_ID').agg(...)
        self.analysis_results['new_metric'] = result
        return result
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {}
```

### Adding a New Visualization

```python
# In src/dashboard_components.py
def new_chart_type(data: pd.DataFrame, ...):
    """Create a new chart type"""
    fig = px.new_chart(data, ...)
    fig.update_layout(...)
    st.plotly_chart(fig, use_container_width=True)
```

### Adding a New Dashboard Tab

```python
# In app.py
with st.tabs([..., "New Tab"]):
    st.markdown("### New Tab Content")
    # Add components and visualizations
```

---

## Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
pip install -r requirements.txt
# Or reinstall specific package:
pip install streamlit --upgrade
```

### Issue: Data not loading

**Check:**
- CSV file path is correct
- File is not corrupted
- All required columns are present
- Date/time formats match DD-MM-YYYY HH:MM:SS

### Issue: Streamlit app crashes

**Solution:**
```bash
# Clear cache
streamlit cache clear

# Run in verbose mode
streamlit run app.py --logger.level=debug
```

### Issue: Low performance with large dataset

**Solution:**
- Filter data before visualization
- Reduce number of machines selected
- Use "Data Explorer" pagination instead of loading all data

---

## Python Version Compatibility

- ✅ Python 3.8.x
- ✅ Python 3.9.x
- ✅ Python 3.10.x
- ✅ Python 3.11.x
- ✅ Python 3.12.x

Tested with pandas ≥1.3.0 and streamlit ≥1.28.0

---

## Development Workflow

### Running Tests

```bash
# Add pytest to requirements for testing
pytest tests/ -v
```

### Code Formatting

```bash
# Format with black
black src/ config/
```

### Linting

```bash
# Check code quality
flake8 src/ config/
```

---

## Documentation Files

- **RESEARCH_PAPER.md**: Comprehensive EDA findings, statistical analysis, and recommendations
- **EXECUTIVE_SUMMARY.md**: High-level summary for C-level stakeholders and government officials

---

## Key Insights & Findings

The dashboard provides insights into:

1. **Machine Degradation Patterns**: Identify which machines show early signs of failure
2. **Production Efficiency**: Correlate sensor readings with output quality
3. **Network Reliability**: Monitor 6G network performance impact on operations
4. **Maintenance Readiness**: Predictive indicators for maintenance scheduling
5. **Operational Benchmarking**: Compare machines against performance standards

---

## Version History

**v1.0.0** (Current)
- Initial release
- Complete dashboard with 5 main modules
- Full data processing pipeline
- Comprehensive error handling
- Python 3.8+ support

---

## Support & Contributions

For issues, suggestions, or contributions:

1. Check existing documentation
2. Review error logs in terminal
3. Verify data format and column names
4. Check Python and dependency versions

---

## License

This project is designed for Thales Group and manufacturing partners in 6G-enabled smart factory environments.

---

## Contact & Attribution

**Project**: Manufacturing Process Health and Operational Efficiency Analysis  
**Platform**: 6G-Enabled Smart Factories  
**Partner**: Unified Mentor  
**Organization**: Thales Group

---

## Disclaimer

This dashboard is provided for analytical and diagnostic purposes. While efforts have been made to ensure accuracy, users should validate critical findings with domain experts before making operational decisions.

---

**Last Updated**: April 2026  
**Dashboard Version**: 1.0.0  
**Python Support**: 3.8+
