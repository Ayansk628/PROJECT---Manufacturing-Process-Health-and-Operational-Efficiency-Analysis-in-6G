"""
Configuration module for Manufacturing Process Health Analysis
Handles all constants, thresholds, and configuration settings
"""

import os
from typing import Dict, List
from pathlib import Path

# ==================== PROJECT PATHS ====================
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
DOCS_DIR = PROJECT_ROOT / "docs"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)

# ==================== DATA CONFIGURATION ====================
# Handle different deployment environments
def _find_data_file():
    """Find data file in various possible locations"""
    possible_paths = [
        PROJECT_ROOT / "Thales_Group_Manufacturing (1).csv",
        Path.cwd() / "Thales_Group_Manufacturing (1).csv",
        Path("/mount/src/manufacturing-process-health-dashboard/Thales_Group_Manufacturing (1).csv"),
    ]
    
    # Search for the file
    for path in possible_paths:
        if path.exists():
            return path
    
    # If not found, return default (will be caught by DataLoader with proper error)
    return PROJECT_ROOT / "Thales_Group_Manufacturing (1).csv"

DATA_FILE = _find_data_file()

REQUIRED_COLUMNS = [
    'Date',
    'Timestamp',
    'Machine_ID',
    'Operation_Mode',
    'Temperature_C',
    'Vibration_Hz',
    'Power_Consumption_kW',
    'Network_Latency_ms',
    'Packet_Loss_%',
    'Quality_Control_Defect_Rate_%',
    'Production_Speed_units_per_hr',
    'Predictive_Maintenance_Score',
    'Error_Rate_%',
    'Efficiency_Status'
]

# ==================== SENSOR THRESHOLDS ====================
"""
Thresholds for sensor health assessment
Based on industrial manufacturing standards
"""
SENSOR_THRESHOLDS = {
    'Temperature_C': {
        'normal_min': 20.0,
        'normal_max': 80.0,
        'warning_max': 95.0,
        'critical_max': 105.0,
    },
    'Vibration_Hz': {
        'normal_max': 3.0,
        'warning_max': 4.5,
        'critical_max': 6.0,
    },
    'Power_Consumption_kW': {
        'normal_min': 1.0,
        'normal_max': 10.0,
        'warning_max': 12.0,
    },
    'Network_Latency_ms': {
        'normal_max': 30.0,
        'warning_max': 50.0,
        'critical_max': 100.0,
    },
    'Packet_Loss_%': {
        'normal_max': 1.0,
        'warning_max': 3.0,
        'critical_max': 5.0,
    },
    'Quality_Control_Defect_Rate_%': {
        'good_max': 2.0,
        'acceptable_max': 5.0,
        'warning_max': 10.0,
    },
    'Error_Rate_%': {
        'good_max': 3.0,
        'acceptable_max': 8.0,
        'warning_max': 15.0,
    },
    'Production_Speed_units_per_hr': {
        'minimum': 50.0,  # Below this is concerning
    }
}

# ==================== OPERATION MODES ====================
VALID_OPERATION_MODES = [
    'Idle',
    'Active',
    'High-Load',
    'Maintenance',
    'Standby'
]

# ==================== EFFICIENCY STATUS ====================
EFFICIENCY_STATUSES = ['High', 'Medium', 'Low']

EFFICIENCY_COLORS = {
    'High': '#10B981',      # Green
    'Medium': '#F59E0B',    # Amber
    'Low': '#EF4444'        # Red
}

# ==================== KPI CONFIGURATION ====================
KPI_WEIGHTS = {
    'temperature_stability': 0.25,
    'vibration_control': 0.25,
    'power_efficiency': 0.20,
    'network_reliability': 0.15,
    'predictive_maintenance': 0.15,
}

# ==================== STREAMLIT CONFIGURATION ====================
STREAMLIT_CONFIG = {
    'page_title': 'Manufacturing Process Health Dashboard',
    'page_icon': '🏭',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
}

# ==================== DISPLAY CONFIGURATION ====================
DATE_FORMAT = '%d-%m-%Y'
TIME_FORMAT = '%H:%M:%S'
DATETIME_FORMAT = f'{DATE_FORMAT} {TIME_FORMAT}'

# Chart colors
CHART_COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'warning': '#d62728',
    'info': '#9467bd',
}

# ==================== ANALYSIS CONFIGURATION ====================
ROLLING_WINDOW_HOURS = 24  # For trend analysis
SAMPLING_RATE = 'H'  # Hourly sampling

# Statistical thresholds
ANOMALY_THRESHOLD_ZSCORE = 3.0  # Standard deviations
EFFICIENCY_PERCENTILES = {
    'high': 66.67,
    'medium': 33.33,
}

# ==================== MACHINE GROUPS ====================
"""
Machines can be grouped for comparative analysis
"""
MACHINE_GROUPS = {
    'all_machines': None,  # No filtering
}

# ==================== LOGGING CONFIGURATION ====================
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# ==================== DATA VALIDATION RULES ====================
VALIDATION_RULES = {
    'Machine_ID': {
        'type': 'numeric',
        'min': 1,
        'max': 500,
    },
    'Temperature_C': {
        'type': 'float',
        'min': 0.0,
        'max': 120.0,
    },
    'Vibration_Hz': {
        'type': 'float',
        'min': 0.0,
        'max': 10.0,
    },
    'Power_Consumption_kW': {
        'type': 'float',
        'min': 0.0,
        'max': 20.0,
    },
    'Network_Latency_ms': {
        'type': 'float',
        'min': 0.0,
        'max': 200.0,
    },
    'Packet_Loss_%': {
        'type': 'float',
        'min': 0.0,
        'max': 100.0,
    },
    'Quality_Control_Defect_Rate_%': {
        'type': 'float',
        'min': 0.0,
        'max': 100.0,
    },
    'Error_Rate_%': {
        'type': 'float',
        'min': 0.0,
        'max': 100.0,
    },
    'Production_Speed_units_per_hr': {
        'type': 'float',
        'min': 0.0,
        'max': 1000.0,
    },
    'Predictive_Maintenance_Score': {
        'type': 'float',
        'min': 0.0,
        'max': 1.0,
    },
}

# ==================== BENCHMARK VALUES ====================
"""
Industry benchmarks for performance comparison
"""
BENCHMARK_VALUES = {
    'temperature_optimal': 50.0,  # Celsius
    'vibration_acceptable': 2.5,  # Hz
    'defect_rate_target': 2.0,  # Percentage
    'error_rate_target': 3.0,  # Percentage
    'production_efficiency_target': 85.0,  # Percentage
}

# ==================== API/EXPORT CONFIGURATION ====================
EXPORT_FORMATS = ['CSV', 'JSON', 'Excel']
REPORT_FORMATS = ['PDF', 'HTML']

# ==================== CACHING CONFIGURATION ====================
CACHE_TTL = 3600  # 1 hour in seconds

# ==================== DEVELOPMENT SETTINGS ====================
DEBUG_MODE = False
VERBOSE_LOGGING = False

# ==================== VERSION INFO ====================
PROJECT_VERSION = '1.0.0'
PYTHON_MIN_VERSION = '3.8'
