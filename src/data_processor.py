"""
Data Processing Module
Handles data cleaning, transformation, and preprocessing
"""

import pandas as pd
import numpy as np
import logging
from typing import Tuple, Optional, List
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import DATE_FORMAT, TIME_FORMAT, LOG_LEVEL

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Handles data preprocessing and cleaning
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialize DataProcessor
        
        Args:
            data: DataFrame to process
        """
        self.data = data.copy()
        self.original_data = data.copy()
        self.processing_log = []

    def create_datetime_column(self) -> 'DataProcessor':
        """
        Combine Date and Timestamp columns into a single datetime column
        
        Returns:
            Self for method chaining
        """
        try:
            self.data['DateTime'] = pd.to_datetime(
                self.data['Date'] + ' ' + self.data['Timestamp'],
                format=f'{DATE_FORMAT} {TIME_FORMAT}',
                errors='coerce'
            )
            self.processing_log.append("DateTime column created")
            logger.info("DateTime column created successfully")
        except Exception as e:
            logger.error(f"Error creating DateTime column: {str(e)}")
        
        return self

    def handle_missing_values(self, strategy: str = 'forward_fill') -> 'DataProcessor':
        """
        Handle missing values in the dataset
        
        Args:
            strategy: 'forward_fill', 'backward_fill', 'drop', or 'mean'
            
        Returns:
            Self for method chaining
        """
        initial_nulls = self.data.isnull().sum().sum()
        
        try:
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            object_cols = self.data.select_dtypes(include=['object']).columns
            
            if strategy == 'forward_fill':
                self.data[numeric_cols] = self.data[numeric_cols].fillna(method='ffill', limit=5)
                self.data[numeric_cols] = self.data[numeric_cols].fillna(method='bfill')
                self.data[object_cols] = self.data[object_cols].fillna(method='ffill')
            
            elif strategy == 'backward_fill':
                self.data[numeric_cols] = self.data[numeric_cols].fillna(method='bfill', limit=5)
                self.data[numeric_cols] = self.data[numeric_cols].fillna(method='ffill')
            
            elif strategy == 'mean':
                for col in numeric_cols:
                    self.data[col].fillna(self.data[col].mean(), inplace=True)
            
            elif strategy == 'drop':
                self.data = self.data.dropna()
            
            final_nulls = self.data.isnull().sum().sum()
            self.processing_log.append(
                f"Missing values handled (strategy: {strategy}). "
                f"Reduced from {initial_nulls} to {final_nulls}"
            )
            logger.info(f"Missing values: {initial_nulls} -> {final_nulls}")
        
        except Exception as e:
            logger.error(f"Error handling missing values: {str(e)}")
        
        return self

    def remove_outliers(self, method: str = 'iqr', threshold: float = 3.0) -> 'DataProcessor':
        """
        Remove outliers from numeric columns
        
        Args:
            method: 'iqr' (Interquartile Range) or 'zscore'
            threshold: Threshold for zscore method
            
        Returns:
            Self for method chaining
        """
        initial_rows = len(self.data)
        
        try:
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            
            if method == 'iqr':
                for col in numeric_cols:
                    Q1 = self.data[col].quantile(0.25)
                    Q3 = self.data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    self.data = self.data[
                        (self.data[col] >= lower_bound) & 
                        (self.data[col] <= upper_bound)
                    ]
            
            elif method == 'zscore':
                from scipy import stats
                z_scores = np.abs(stats.zscore(self.data[numeric_cols]))
                self.data = self.data[(z_scores < threshold).all(axis=1)]
            
            removed = initial_rows - len(self.data)
            self.processing_log.append(
                f"Outliers removed (method: {method}). "
                f"Rows removed: {removed}"
            )
            logger.info(f"Outliers removed: {removed} rows ({removed/initial_rows*100:.2f}%)")
        
        except Exception as e:
            logger.error(f"Error removing outliers: {str(e)}")
        
        return self

    def normalize_values(self, columns: Optional[List[str]] = None) -> 'DataProcessor':
        """
        Normalize numeric columns to 0-1 range (Min-Max scaling)
        
        Args:
            columns: Specific columns to normalize. If None, normalizes all numeric columns
            
        Returns:
            Self for method chaining
        """
        try:
            if columns is None:
                columns = self.data.select_dtypes(include=[np.number]).columns
            
            for col in columns:
                if col in self.data.columns:
                    min_val = self.data[col].min()
                    max_val = self.data[col].max()
                    if max_val > min_val:
                        self.data[f'{col}_normalized'] = (
                            (self.data[col] - min_val) / (max_val - min_val)
                        )
            
            self.processing_log.append(f"Normalized {len(columns)} columns")
            logger.info(f"Normalization completed for {len(columns)} columns")
        
        except Exception as e:
            logger.error(f"Error normalizing values: {str(e)}")
        
        return self

    def standardize_values(self, columns: Optional[List[str]] = None) -> 'DataProcessor':
        """
        Standardize numeric columns (z-score normalization)
        
        Args:
            columns: Specific columns to standardize. If None, standardizes all numeric columns
            
        Returns:
            Self for method chaining
        """
        try:
            if columns is None:
                columns = self.data.select_dtypes(include=[np.number]).columns
            
            for col in columns:
                if col in self.data.columns:
                    mean = self.data[col].mean()
                    std = self.data[col].std()
                    if std > 0:
                        self.data[f'{col}_standardized'] = (
                            (self.data[col] - mean) / std
                        )
            
            self.processing_log.append(f"Standardized {len(columns)} columns")
            logger.info(f"Standardization completed for {len(columns)} columns")
        
        except Exception as e:
            logger.error(f"Error standardizing values: {str(e)}")
        
        return self

    def fix_data_types(self) -> 'DataProcessor':
        """
        Fix and optimize data types
        
        Returns:
            Self for method chaining
        """
        try:
            type_mapping = {
                'Machine_ID': 'int64',
                'Temperature_C': 'float32',
                'Vibration_Hz': 'float32',
                'Power_Consumption_kW': 'float32',
                'Network_Latency_ms': 'float32',
                'Packet_Loss_%': 'float32',
                'Quality_Control_Defect_Rate_%': 'float32',
                'Production_Speed_units_per_hr': 'float32',
                'Predictive_Maintenance_Score': 'float32',
                'Error_Rate_%': 'float32',
                'Operation_Mode': 'category',
                'Efficiency_Status': 'category',
            }
            
            for col, dtype in type_mapping.items():
                if col in self.data.columns:
                    try:
                        self.data[col] = self.data[col].astype(dtype)
                    except (ValueError, TypeError):
                        logger.warning(f"Could not convert {col} to {dtype}")
            
            self.processing_log.append("Data types optimized")
            logger.info("Data types optimized successfully")
        
        except Exception as e:
            logger.error(f"Error fixing data types: {str(e)}")
        
        return self

    def add_temporal_features(self) -> 'DataProcessor':
        """
        Add temporal features from DateTime
        
        Returns:
            Self for method chaining
        """
        try:
            if 'DateTime' not in self.data.columns:
                self.create_datetime_column()
            
            dt = self.data['DateTime']
            
            self.data['Hour'] = dt.dt.hour
            self.data['Day'] = dt.dt.day
            self.data['Month'] = dt.dt.month
            self.data['Year'] = dt.dt.year
            self.data['DayOfWeek'] = dt.dt.dayofweek
            self.data['Quarter'] = dt.dt.quarter
            self.data['DayOfYear'] = dt.dt.dayofyear
            
            # Shift information
            self.data['Shift'] = pd.cut(
                self.data['Hour'],
                bins=[-1, 8, 16, 24],
                labels=['Night', 'Morning', 'Evening'],
                include_lowest=True
            )
            
            self.processing_log.append("Temporal features added")
            logger.info("Temporal features added successfully")
        
        except Exception as e:
            logger.error(f"Error adding temporal features: {str(e)}")
        
        return self

    def add_health_indicators(self) -> 'DataProcessor':
        """
        Add machine health indicator columns
        
        Returns:
            Self for method chaining
        """
        try:
            # Temperature health
            self.data['Temp_Health'] = pd.cut(
                self.data['Temperature_C'],
                bins=[0, 30, 50, 70, 90, 150],
                labels=['Excellent', 'Good', 'Normal', 'Warning', 'Critical']
            )
            
            # Vibration health
            self.data['Vibration_Health'] = pd.cut(
                self.data['Vibration_Hz'],
                bins=[-0.1, 1.0, 2.5, 4.0, 6.0, 10.0],
                labels=['Excellent', 'Good', 'Normal', 'Warning', 'Critical']
            )
            
            # Power efficiency
            self.data['Power_Efficiency'] = pd.cut(
                self.data['Power_Consumption_kW'],
                bins=[0, 2, 5, 8, 12, 20],
                labels=['Excellent', 'Good', 'Normal', 'Warning', 'Critical']
            )
            
            # Network reliability
            self.data['Network_Health'] = pd.cut(
                self.data['Network_Latency_ms'],
                bins=[0, 10, 25, 50, 100, 200],
                labels=['Excellent', 'Good', 'Normal', 'Warning', 'Critical']
            )
            
            self.processing_log.append("Health indicators added")
            logger.info("Health indicators added successfully")
        
        except Exception as e:
            logger.error(f"Error adding health indicators: {str(e)}")
        
        return self

    def get_processing_report(self) -> dict:
        """
        Get a summary of processing steps applied
        
        Returns:
            Dictionary with processing report
        """
        return {
            'steps_applied': self.processing_log,
            'original_rows': len(self.original_data),
            'final_rows': len(self.data),
            'rows_removed': len(self.original_data) - len(self.data),
            'final_columns': len(self.data.columns),
            'original_columns': len(self.original_data.columns),
        }

    def get_processed_data(self) -> pd.DataFrame:
        """
        Get the processed data
        
        Returns:
            Processed DataFrame
        """
        return self.data

    def reset(self) -> 'DataProcessor':
        """
        Reset to original data
        
        Returns:
            Self for method chaining
        """
        self.data = self.original_data.copy()
        self.processing_log = []
        logger.info("Processor reset to original data")
        return self


def preprocess_data(data: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    """
    Convenience function to apply standard preprocessing pipeline
    
    Args:
        data: Raw DataFrame
        
    Returns:
        Tuple of (processed_data, processing_report)
    """
    processor = DataProcessor(data)
    
    (processor
     .create_datetime_column()
     .handle_missing_values(strategy='forward_fill')
     .fix_data_types()
     .add_temporal_features()
     .add_health_indicators()
     .remove_outliers(method='iqr'))
    
    report = processor.get_processing_report()
    
    logger.info(f"Data preprocessing completed. {report['rows_removed']} rows removed.")
    
    return processor.get_processed_data(), report
