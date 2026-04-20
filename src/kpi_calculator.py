"""
KPI Calculation Module
Computes Key Performance Indicators for manufacturing analysis
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, Optional, List, Tuple
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import (
    SENSOR_THRESHOLDS,
    BENCHMARK_VALUES,
    KPI_WEIGHTS,
    LOG_LEVEL
)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class KPICalculator:
    """
    Calculates Key Performance Indicators from manufacturing data
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialize KPICalculator
        
        Args:
            data: Processed DataFrame with manufacturing data
        """
        self.data = data
        self.kpis = {}
        self.machine_kpis = {}

    def calculate_machine_health_index(self) -> pd.DataFrame:
        """
        Calculate composite Machine Health Index
        
        Returns:
            DataFrame with health index by machine
        """
        try:
            machine_groups = self.data.groupby('Machine_ID').agg({
                'Temperature_C': ['mean', 'std'],
                'Vibration_Hz': ['mean', 'std'],
                'Power_Consumption_kW': ['mean', 'std'],
                'Network_Latency_ms': ['mean', 'std'],
                'Packet_Loss_%': 'mean',
                'Predictive_Maintenance_Score': 'mean',
            }).round(3)
            
            health_index = pd.DataFrame(index=self.data['Machine_ID'].unique())
            
            # Temperature component (lower is better, but not too low)
            temp_optimal = BENCHMARK_VALUES['temperature_optimal']
            temp_penalty = (machine_groups['Temperature_C']['mean'] - temp_optimal).abs() / temp_optimal
            temp_score = (1 - np.clip(temp_penalty, 0, 1)) * 0.25
            
            # Vibration component (lower is better)
            vib_optimal = BENCHMARK_VALUES['vibration_acceptable']
            vib_penalty = machine_groups['Vibration_Hz']['mean'] / vib_optimal
            vib_score = (1 - np.clip(vib_penalty, 0, 1)) * 0.25
            
            # Power efficiency component
            power_mean = self.data['Power_Consumption_kW'].mean()
            power_penalty = machine_groups['Power_Consumption_kW']['mean'] / power_mean
            power_score = (1 - np.clip(power_penalty - 0.5, 0, 0.5) * 2) * 0.20
            
            # Network reliability component
            network_penalty = machine_groups['Network_Latency_ms']['mean'] / 50
            network_score = (1 - np.clip(network_penalty, 0, 1)) * 0.15
            
            # Predictive maintenance score (higher is better)
            maintenance_score = machine_groups['Predictive_Maintenance_Score']['mean'] * 0.15
            
            # Combine scores
            health_index['Health_Score'] = (
                temp_score + vib_score + power_score + network_score + maintenance_score
            ).iloc[:, 0]
            
            health_index['Health_Status'] = pd.cut(
                health_index['Health_Score'],
                bins=[0, 0.33, 0.66, 1.0],
                labels=['Poor', 'Fair', 'Good']
            )
            
            self.kpis['machine_health_index'] = health_index
            logger.info("Machine Health Index calculated successfully")
            
            return health_index
        
        except Exception as e:
            logger.error(f"Error calculating Machine Health Index: {str(e)}")
            return pd.DataFrame()

    def calculate_average_production_speed(self) -> Dict:
        """
        Calculate average production speed metrics
        
        Returns:
            Dictionary with production speed metrics
        """
        try:
            metrics = {
                'overall_avg': self.data['Production_Speed_units_per_hr'].mean(),
                'overall_std': self.data['Production_Speed_units_per_hr'].std(),
                'overall_min': self.data['Production_Speed_units_per_hr'].min(),
                'overall_max': self.data['Production_Speed_units_per_hr'].max(),
                'by_machine': self.data.groupby('Machine_ID')['Production_Speed_units_per_hr'].agg(['mean', 'std', 'min', 'max']).round(2),
                'by_mode': self.data.groupby('Operation_Mode')['Production_Speed_units_per_hr'].agg(['mean', 'std', 'count']).round(2),
            }
            
            self.kpis['production_speed'] = metrics
            logger.info("Production Speed metrics calculated")
            
            return metrics
        
        except Exception as e:
            logger.error(f"Error calculating Production Speed: {str(e)}")
            return {}

    def calculate_defect_density_score(self) -> pd.DataFrame:
        """
        Calculate defect rate relative to production volume
        
        Returns:
            DataFrame with defect density metrics
        """
        try:
            # Create bins for production speed ranges
            self.data['Speed_Category'] = pd.qcut(
                self.data['Production_Speed_units_per_hr'],
                q=4,
                labels=['Low', 'Medium', 'High', 'Very High'],
                duplicates='drop'
            )
            
            density_metrics = self.data.groupby('Speed_Category').agg({
                'Quality_Control_Defect_Rate_%': ['mean', 'std', 'min', 'max'],
                'Production_Speed_units_per_hr': 'count',
            }).round(3)
            
            density_metrics.columns = ['Avg_Defect_Rate', 'Std_Defect_Rate', 'Min_Defect_Rate', 'Max_Defect_Rate', 'Count']
            
            # Calculate defect density score
            density_metrics['Density_Score'] = (
                (density_metrics['Avg_Defect_Rate'] / BENCHMARK_VALUES['defect_rate_target']) * 100
            ).round(2)
            
            self.kpis['defect_density'] = density_metrics
            logger.info("Defect Density Score calculated")
            
            return density_metrics
        
        except Exception as e:
            logger.error(f"Error calculating Defect Density: {str(e)}")
            return pd.DataFrame()

    def calculate_error_frequency_index(self) -> Dict:
        """
        Calculate error frequency metrics
        
        Returns:
            Dictionary with error frequency metrics
        """
        try:
            metrics = {
                'overall_avg': self.data['Error_Rate_%'].mean(),
                'overall_std': self.data['Error_Rate_%'].std(),
                'total_error_instances': (self.data['Error_Rate_%'] > 0).sum(),
                'error_percentage': ((self.data['Error_Rate_%'] > 0).sum() / len(self.data) * 100).round(2),
                'by_machine': self.data.groupby('Machine_ID')['Error_Rate_%'].agg(['mean', 'max', 'count']).round(2),
                'by_mode': self.data.groupby('Operation_Mode')['Error_Rate_%'].agg(['mean', 'std', 'max']).round(2),
                'high_error_machines': self.data[self.data['Error_Rate_%'] > 10]['Machine_ID'].unique().tolist(),
            }
            
            self.kpis['error_frequency'] = metrics
            logger.info("Error Frequency Index calculated")
            
            return metrics
        
        except Exception as e:
            logger.error(f"Error calculating Error Frequency: {str(e)}")
            return {}

    def calculate_efficiency_distribution(self) -> Dict:
        """
        Calculate efficiency status distribution
        
        Returns:
            Dictionary with efficiency distribution metrics
        """
        try:
            # Overall distribution
            efficiency_dist = self.data['Efficiency_Status'].value_counts(normalize=True) * 100
            efficiency_counts = self.data['Efficiency_Status'].value_counts()
            
            # By machine
            machine_efficiency = self.data.groupby('Machine_ID')['Efficiency_Status'].value_counts(normalize=True).unstack(fill_value=0) * 100
            
            # By operation mode
            mode_efficiency = self.data.groupby('Operation_Mode')['Efficiency_Status'].value_counts(normalize=True).unstack(fill_value=0) * 100
            
            # By hour of day
            if 'Hour' in self.data.columns:
                hour_efficiency = self.data.groupby('Hour')['Efficiency_Status'].value_counts(normalize=True).unstack(fill_value=0) * 100
            else:
                hour_efficiency = None
            
            metrics = {
                'overall_distribution': efficiency_dist.round(2).to_dict(),
                'overall_counts': efficiency_counts.to_dict(),
                'by_machine': machine_efficiency.round(2),
                'by_mode': mode_efficiency.round(2),
                'by_hour': hour_efficiency,
            }
            
            self.kpis['efficiency_distribution'] = metrics
            logger.info("Efficiency Distribution calculated")
            
            return metrics
        
        except Exception as e:
            logger.error(f"Error calculating Efficiency Distribution: {str(e)}")
            return {}

    def calculate_sensor_correlations(self) -> pd.DataFrame:
        """
        Calculate correlations between sensor metrics and efficiency
        
        Returns:
            DataFrame with correlation coefficients
        """
        try:
            sensor_cols = [
                'Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW',
                'Network_Latency_ms', 'Packet_Loss_%', 'Quality_Control_Defect_Rate_%',
                'Error_Rate_%', 'Production_Speed_units_per_hr'
            ]
            
            # Create numeric efficiency (High=3, Medium=2, Low=1)
            efficiency_numeric = self.data['Efficiency_Status'].map({'High': 3, 'Medium': 2, 'Low': 1})
            
            correlations = {}
            for col in sensor_cols:
                if col in self.data.columns:
                    corr = self.data[col].corr(efficiency_numeric)
                    correlations[col] = corr
            
            corr_df = pd.DataFrame(list(correlations.items()), columns=['Metric', 'Correlation_with_Efficiency'])
            corr_df = corr_df.sort_values('Correlation_with_Efficiency', ascending=False).round(3)
            
            self.kpis['sensor_correlations'] = corr_df
            logger.info("Sensor Correlations calculated")
            
            return corr_df
        
        except Exception as e:
            logger.error(f"Error calculating Sensor Correlations: {str(e)}")
            return pd.DataFrame()

    def calculate_temperature_defect_relationship(self) -> pd.DataFrame:
        """
        Analyze relationship between temperature and defect rate
        
        Returns:
            DataFrame with temperature-defect analysis
        """
        try:
            # Create temperature bins
            self.data['Temp_Bin'] = pd.cut(
                self.data['Temperature_C'],
                bins=10,
                labels=[f'Bin{i}' for i in range(10)]
            )
            
            analysis = self.data.groupby('Temp_Bin', observed=True).agg({
                'Quality_Control_Defect_Rate_%': ['mean', 'std', 'min', 'max'],
                'Machine_ID': 'count',
                'Temperature_C': 'mean',
            }).round(3)
            
            analysis.columns = ['Avg_Defect_Rate', 'Std_Defect_Rate', 'Min_Defect_Rate', 
                               'Max_Defect_Rate', 'Count', 'Avg_Temperature']
            
            self.kpis['temperature_defect'] = analysis
            logger.info("Temperature-Defect relationship calculated")
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error calculating Temperature-Defect relationship: {str(e)}")
            return pd.DataFrame()

    def calculate_vibration_error_relationship(self) -> pd.DataFrame:
        """
        Analyze relationship between vibration and error rate
        
        Returns:
            DataFrame with vibration-error analysis
        """
        try:
            # Create vibration bins
            self.data['Vib_Bin'] = pd.cut(
                self.data['Vibration_Hz'],
                bins=10,
                labels=[f'Bin{i}' for i in range(10)]
            )
            
            analysis = self.data.groupby('Vib_Bin', observed=True).agg({
                'Error_Rate_%': ['mean', 'std', 'min', 'max'],
                'Machine_ID': 'count',
                'Vibration_Hz': 'mean',
            }).round(3)
            
            analysis.columns = ['Avg_Error_Rate', 'Std_Error_Rate', 'Min_Error_Rate', 
                               'Max_Error_Rate', 'Count', 'Avg_Vibration']
            
            self.kpis['vibration_error'] = analysis
            logger.info("Vibration-Error relationship calculated")
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error calculating Vibration-Error relationship: {str(e)}")
            return pd.DataFrame()

    def calculate_all_kpis(self) -> Dict:
        """
        Calculate all KPIs in one call
        
        Returns:
            Dictionary with all KPI results
        """
        logger.info("Starting KPI calculation...")
        
        self.calculate_machine_health_index()
        self.calculate_average_production_speed()
        self.calculate_defect_density_score()
        self.calculate_error_frequency_index()
        self.calculate_efficiency_distribution()
        self.calculate_sensor_correlations()
        self.calculate_temperature_defect_relationship()
        self.calculate_vibration_error_relationship()
        
        logger.info("All KPIs calculated successfully")
        return self.kpis

    def get_kpis(self) -> Dict:
        """
        Get calculated KPIs
        
        Returns:
            Dictionary with all KPIs
        """
        if not self.kpis:
            return self.calculate_all_kpis()
        return self.kpis


def calculate_kpis(data: pd.DataFrame) -> Dict:
    """
    Convenience function to calculate all KPIs
    
    Args:
        data: Processed DataFrame
        
    Returns:
        Dictionary with all KPIs
    """
    calculator = KPICalculator(data)
    return calculator.calculate_all_kpis()
