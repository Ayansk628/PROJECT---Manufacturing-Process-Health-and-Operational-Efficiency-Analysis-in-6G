"""
Data Loading Module
Handles loading, validating, and initial processing of manufacturing data
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Tuple, Dict, Optional, List
from datetime import datetime
import sys

# Add config to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import (
    DATA_FILE,
    REQUIRED_COLUMNS,
    VALIDATION_RULES,
    DATE_FORMAT,
    TIME_FORMAT,
    LOG_LEVEL
)

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataLoader:
    """
    Handles loading and initial validation of manufacturing data
    """

    def __init__(self, data_path: Optional[Path] = None):
        """
        Initialize DataLoader
        
        Args:
            data_path: Path to CSV file. If None, uses default from config
        """
        self.data_path = data_path or DATA_FILE
        self.raw_data = None
        self.data = None
        self.validation_report = {}

    def load_data(self, nrows: Optional[int] = None) -> pd.DataFrame:
        """
        Load data from CSV file
        
        Args:
            nrows: Number of rows to load. If None, loads all data
            
        Returns:
            DataFrame with loaded data
            
        Raises:
            FileNotFoundError: If data file not found
            ValueError: If file is empty or corrupted
        """
        try:
            # First, try to find the file if default path doesn't exist
            data_path = self.data_path
            
            if not Path(data_path).exists():
                logger.warning(f"Data file not found at {data_path}, searching alternative locations...")
                
                # Search in common locations
                search_paths = [
                    Path.cwd() / "Thales_Group_Manufacturing (1).csv",
                    Path.cwd().parent / "Thales_Group_Manufacturing (1).csv",
                    Path("/mount/src/manufacturing-process-health-dashboard/Thales_Group_Manufacturing (1).csv"),
                ]
                
                found = False
                for alt_path in search_paths:
                    if Path(alt_path).exists():
                        data_path = alt_path
                        found = True
                        logger.info(f"Found data file at {data_path}")
                        break
                
                if not found:
                    raise FileNotFoundError(
                        f"Data file not found at {self.data_path} or alternative locations. "
                        f"Expected file: 'Thales_Group_Manufacturing (1).csv'"
                    )
            
            logger.info(f"Loading data from {data_path}")
            
            # Load CSV
            self.raw_data = pd.read_csv(
                data_path,
                nrows=nrows,
                dtype={
                    'Machine_ID': 'int64',
                    'Temperature_C': 'float64',
                    'Vibration_Hz': 'float64',
                    'Power_Consumption_kW': 'float64',
                    'Network_Latency_ms': 'float64',
                    'Packet_Loss_%': 'float64',
                    'Quality_Control_Defect_Rate_%': 'float64',
                    'Production_Speed_units_per_hr': 'float64',
                    'Predictive_Maintenance_Score': 'float64',
                    'Error_Rate_%': 'float64',
                }
            )
            
            if self.raw_data.empty:
                raise ValueError("Loaded data is empty")
            
            logger.info(f"Successfully loaded {len(self.raw_data)} records")
            self.data = self.raw_data.copy()
            return self.data
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def validate_schema(self) -> Tuple[bool, Dict]:
        """
        Validate that all required columns are present
        
        Returns:
            Tuple of (is_valid, validation_report)
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        report = {'status': 'passed', 'missing_columns': [], 'extra_columns': []}
        
        # Check for required columns
        missing = [col for col in REQUIRED_COLUMNS if col not in self.data.columns]
        if missing:
            report['status'] = 'failed'
            report['missing_columns'] = missing
            logger.warning(f"Missing columns: {missing}")
        
        # Check for extra columns
        extra = [col for col in self.data.columns if col not in REQUIRED_COLUMNS]
        if extra:
            logger.info(f"Extra columns found: {extra}")
            report['extra_columns'] = extra
        
        self.validation_report['schema'] = report
        return report['status'] == 'passed', report

    def validate_data_types(self) -> Tuple[bool, Dict]:
        """
        Validate data types of columns
        
        Returns:
            Tuple of (is_valid, validation_report)
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        report = {
            'status': 'passed',
            'type_errors': [],
            'columns_checked': len(self.data.columns)
        }
        
        type_mapping = {
            'numeric': ['int64', 'float64', 'int32', 'int'],
            'string': ['object', 'str'],
            'datetime': ['datetime64'],
        }
        
        # Validate specific columns
        try:
            # Numeric validations
            numeric_cols = [
                'Machine_ID', 'Temperature_C', 'Vibration_Hz', 
                'Power_Consumption_kW', 'Network_Latency_ms',
                'Packet_Loss_%', 'Quality_Control_Defect_Rate_%',
                'Production_Speed_units_per_hr', 'Predictive_Maintenance_Score',
                'Error_Rate_%'
            ]
            
            for col in numeric_cols:
                if col in self.data.columns:
                    if not pd.api.types.is_numeric_dtype(self.data[col]):
                        report['status'] = 'warning'
                        report['type_errors'].append(
                            f"{col}: expected numeric, got {self.data[col].dtype}"
                        )
            
            # String validations
            string_cols = ['Operation_Mode', 'Efficiency_Status', 'Date', 'Timestamp']
            for col in string_cols:
                if col in self.data.columns:
                    if not pd.api.types.is_object_dtype(self.data[col]):
                        logger.warning(f"{col}: expected object type")
        
        except Exception as e:
            logger.error(f"Error in type validation: {str(e)}")
            report['status'] = 'failed'
        
        self.validation_report['data_types'] = report
        return report['status'] in ['passed', 'warning'], report

    def validate_value_ranges(self) -> Tuple[bool, Dict]:
        """
        Validate that numeric values are within acceptable ranges
        
        Returns:
            Tuple of (is_valid, validation_report)
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        report = {
            'status': 'passed',
            'out_of_range': {},
            'null_values': {}
        }
        
        try:
            for col, rules in VALIDATION_RULES.items():
                if col not in self.data.columns:
                    continue
                
                # Check for null values
                null_count = self.data[col].isnull().sum()
                if null_count > 0:
                    report['null_values'][col] = null_count
                    logger.warning(f"{col}: {null_count} null values found")
                
                # Check range for numeric columns
                if rules['type'] in ['float', 'numeric']:
                    col_data = self.data[col].dropna()
                    
                    if 'min' in rules:
                        below_min = (col_data < rules['min']).sum()
                        if below_min > 0:
                            report['status'] = 'warning'
                            report['out_of_range'][f"{col}_below_min"] = below_min
                    
                    if 'max' in rules:
                        above_max = (col_data > rules['max']).sum()
                        if above_max > 0:
                            report['status'] = 'warning'
                            report['out_of_range'][f"{col}_above_max"] = above_max
        
        except Exception as e:
            logger.error(f"Error in range validation: {str(e)}")
            report['status'] = 'failed'
        
        self.validation_report['value_ranges'] = report
        return report['status'] in ['passed', 'warning'], report

    def validate_datetime(self) -> Tuple[bool, Dict]:
        """
        Validate datetime columns
        
        Returns:
            Tuple of (is_valid, validation_report)
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        report = {
            'status': 'passed',
            'date_errors': [],
            'time_errors': []
        }
        
        try:
            # Validate Date
            if 'Date' in self.data.columns:
                invalid_dates = 0
                for date_str in self.data['Date']:
                    try:
                        if pd.notna(date_str):
                            datetime.strptime(str(date_str), DATE_FORMAT)
                    except ValueError:
                        invalid_dates += 1
                
                if invalid_dates > 0:
                    report['status'] = 'warning'
                    report['date_errors'].append(
                        f"{invalid_dates} invalid date formats found"
                    )
            
            # Validate Time
            if 'Timestamp' in self.data.columns:
                invalid_times = 0
                for time_str in self.data['Timestamp']:
                    try:
                        if pd.notna(time_str):
                            datetime.strptime(str(time_str), TIME_FORMAT)
                    except ValueError:
                        invalid_times += 1
                
                if invalid_times > 0:
                    report['status'] = 'warning'
                    report['time_errors'].append(
                        f"{invalid_times} invalid time formats found"
                    )
        
        except Exception as e:
            logger.error(f"Error in datetime validation: {str(e)}")
            report['status'] = 'failed'
        
        self.validation_report['datetime'] = report
        return report['status'] in ['passed', 'warning'], report

    def validate_all(self) -> Tuple[bool, Dict]:
        """
        Run all validations
        
        Returns:
            Tuple of (all_valid, complete_report)
        """
        validations = [
            self.validate_schema,
            self.validate_data_types,
            self.validate_value_ranges,
            self.validate_datetime
        ]
        
        all_valid = True
        for validation_func in validations:
            try:
                is_valid, _ = validation_func()
                if not is_valid:
                    all_valid = False
            except Exception as e:
                logger.error(f"Validation {validation_func.__name__} failed: {str(e)}")
                all_valid = False
        
        return all_valid, self.validation_report

    def get_data_summary(self) -> Dict:
        """
        Get summary statistics of the data
        
        Returns:
            Dictionary with data summary
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        summary = {
            'total_records': len(self.data),
            'total_columns': len(self.data.columns),
            'unique_machines': self.data['Machine_ID'].nunique() if 'Machine_ID' in self.data.columns else 0,
            'unique_modes': self.data['Operation_Mode'].nunique() if 'Operation_Mode' in self.data.columns else 0,
            'date_range': None,
            'memory_usage_mb': self.data.memory_usage(deep=True).sum() / 1024 ** 2,
            'missing_values': self.data.isnull().sum().to_dict(),
        }
        
        if 'Date' in self.data.columns:
            try:
                dates = pd.to_datetime(self.data['Date'], format=DATE_FORMAT)
                summary['date_range'] = {
                    'min': dates.min().strftime(DATE_FORMAT),
                    'max': dates.max().strftime(DATE_FORMAT),
                }
            except:
                logger.warning("Could not parse dates for summary")
        
        return summary


def load_and_validate_data(data_path: Optional[Path] = None) -> Tuple[pd.DataFrame, bool, Dict]:
    """
    Convenience function to load and validate data in one call
    
    Args:
        data_path: Path to CSV file
        
    Returns:
        Tuple of (data, is_valid, validation_report)
    """
    loader = DataLoader(data_path)
    loader.load_data()
    is_valid, report = loader.validate_all()
    
    logger.info(f"Data validation result: {'PASSED' if is_valid else 'FAILED'}")
    
    return loader.data, is_valid, report
