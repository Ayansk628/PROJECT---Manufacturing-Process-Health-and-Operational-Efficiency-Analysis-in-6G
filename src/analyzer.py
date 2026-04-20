"""
Analysis Module
Comprehensive exploratory data analysis functions
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, Optional, Tuple, List
from pathlib import Path
import sys
from scipy import stats

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import SENSOR_THRESHOLDS, BENCHMARK_VALUES, LOG_LEVEL

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataAnalyzer:
    """
    Performs comprehensive exploratory data analysis
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialize DataAnalyzer
        
        Args:
            data: Processed DataFrame
        """
        self.data = data
        self.analysis_results = {}

    def get_descriptive_statistics(self) -> Dict:
        """
        Calculate descriptive statistics
        
        Returns:
            Dictionary with statistical summary
        """
        try:
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            
            stats_dict = {}
            for col in numeric_cols:
                stats_dict[col] = {
                    'count': self.data[col].count(),
                    'mean': self.data[col].mean(),
                    'std': self.data[col].std(),
                    'min': self.data[col].min(),
                    '25%': self.data[col].quantile(0.25),
                    '50%': self.data[col].quantile(0.50),
                    '75%': self.data[col].quantile(0.75),
                    'max': self.data[col].max(),
                    'skewness': self.data[col].skew(),
                    'kurtosis': self.data[col].kurtosis(),
                }
            
            self.analysis_results['descriptive_stats'] = stats_dict
            logger.info("Descriptive statistics calculated")
            
            return stats_dict
        
        except Exception as e:
            logger.error(f"Error calculating descriptive statistics: {str(e)}")
            return {}

    def analyze_sensor_distributions(self) -> Dict:
        """
        Analyze distributions of sensor data
        
        Returns:
            Dictionary with distribution analysis
        """
        try:
            sensor_cols = [
                'Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW',
                'Network_Latency_ms', 'Packet_Loss_%'
            ]
            
            distributions = {}
            for col in sensor_cols:
                if col in self.data.columns:
                    col_data = self.data[col].dropna()
                    
                    # Normality test (Shapiro-Wilk for samples < 5000)
                    if len(col_data) > 5000:
                        col_sample = col_data.sample(5000)
                    else:
                        col_sample = col_data
                    
                    try:
                        _, p_value = stats.shapiro(col_sample)
                        is_normal = p_value > 0.05
                    except:
                        is_normal = None
                    
                    distributions[col] = {
                        'is_normal': is_normal,
                        'skewness_interpretation': self._interpret_skewness(col_data.skew()),
                        'distribution_type': self._detect_distribution(col_data),
                        'outlier_count': self._count_outliers(col_data),
                        'outlier_percentage': (self._count_outliers(col_data) / len(col_data) * 100),
                    }
            
            self.analysis_results['sensor_distributions'] = distributions
            logger.info("Sensor distributions analyzed")
            
            return distributions
        
        except Exception as e:
            logger.error(f"Error analyzing sensor distributions: {str(e)}")
            return {}

    def analyze_machine_performance(self) -> Dict:
        """
        Analyze performance metrics by machine
        
        Returns:
            Dictionary with machine performance analysis
        """
        try:
            machine_performance = {}
            
            for machine_id in self.data['Machine_ID'].unique():
                machine_data = self.data[self.data['Machine_ID'] == machine_id]
                
                machine_performance[machine_id] = {
                    'record_count': len(machine_data),
                    'efficiency_high_pct': (machine_data['Efficiency_Status'] == 'High').sum() / len(machine_data) * 100,
                    'efficiency_medium_pct': (machine_data['Efficiency_Status'] == 'Medium').sum() / len(machine_data) * 100,
                    'efficiency_low_pct': (machine_data['Efficiency_Status'] == 'Low').sum() / len(machine_data) * 100,
                    'avg_temperature': machine_data['Temperature_C'].mean(),
                    'avg_vibration': machine_data['Vibration_Hz'].mean(),
                    'avg_error_rate': machine_data['Error_Rate_%'].mean(),
                    'avg_defect_rate': machine_data['Quality_Control_Defect_Rate_%'].mean(),
                    'avg_production_speed': machine_data['Production_Speed_units_per_hr'].mean(),
                    'maintenance_score': machine_data['Predictive_Maintenance_Score'].mean(),
                }
            
            # Sort by efficiency
            machine_performance = dict(sorted(
                machine_performance.items(),
                key=lambda x: x[1]['efficiency_high_pct'],
                reverse=True
            ))
            
            self.analysis_results['machine_performance'] = machine_performance
            logger.info(f"Performance analyzed for {len(machine_performance)} machines")
            
            return machine_performance
        
        except Exception as e:
            logger.error(f"Error analyzing machine performance: {str(e)}")
            return {}

    def analyze_operation_modes(self) -> Dict:
        """
        Analyze different operation modes
        
        Returns:
            Dictionary with operation mode analysis
        """
        try:
            mode_analysis = {}
            
            for mode in self.data['Operation_Mode'].unique():
                mode_data = self.data[self.data['Operation_Mode'] == mode]
                
                mode_analysis[mode] = {
                    'record_count': len(mode_data),
                    'avg_temperature': mode_data['Temperature_C'].mean(),
                    'avg_vibration': mode_data['Vibration_Hz'].mean(),
                    'avg_power': mode_data['Power_Consumption_kW'].mean(),
                    'avg_production_speed': mode_data['Production_Speed_units_per_hr'].mean(),
                    'avg_defect_rate': mode_data['Quality_Control_Defect_Rate_%'].mean(),
                    'avg_error_rate': mode_data['Error_Rate_%'].mean(),
                    'avg_network_latency': mode_data['Network_Latency_ms'].mean(),
                    'packet_loss_avg': mode_data['Packet_Loss_%'].mean(),
                }
            
            self.analysis_results['operation_modes'] = mode_analysis
            logger.info(f"Operation modes analyzed: {list(mode_analysis.keys())}")
            
            return mode_analysis
        
        except Exception as e:
            logger.error(f"Error analyzing operation modes: {str(e)}")
            return {}

    def identify_critical_machines(self, threshold: float = 0.4) -> Dict:
        """
        Identify machines that need attention
        
        Args:
            threshold: Low efficiency percentage threshold
            
        Returns:
            Dictionary with critical machine information
        """
        try:
            critical_machines = {}
            
            for machine_id in self.data['Machine_ID'].unique():
                machine_data = self.data[self.data['Machine_ID'] == machine_id]
                low_eff_pct = (machine_data['Efficiency_Status'] == 'Low').sum() / len(machine_data) * 100
                
                if low_eff_pct >= threshold:
                    high_error = machine_data['Error_Rate_%'].mean() > BENCHMARK_VALUES['error_rate_target']
                    high_defect = machine_data['Quality_Control_Defect_Rate_%'].mean() > BENCHMARK_VALUES['defect_rate_target']
                    high_temp = machine_data['Temperature_C'].mean() > SENSOR_THRESHOLDS['Temperature_C']['warning_max']
                    
                    critical_machines[machine_id] = {
                        'low_efficiency_pct': low_eff_pct,
                        'issues': [],
                    }
                    
                    if high_error:
                        critical_machines[machine_id]['issues'].append('High Error Rate')
                    if high_defect:
                        critical_machines[machine_id]['issues'].append('High Defect Rate')
                    if high_temp:
                        critical_machines[machine_id]['issues'].append('High Temperature')
            
            self.analysis_results['critical_machines'] = critical_machines
            logger.info(f"Identified {len(critical_machines)} critical machines")
            
            return critical_machines
        
        except Exception as e:
            logger.error(f"Error identifying critical machines: {str(e)}")
            return {}

    def analyze_temporal_patterns(self) -> Dict:
        """
        Analyze temporal patterns in the data
        
        Returns:
            Dictionary with temporal analysis
        """
        try:
            temporal_analysis = {}
            
            # Hour of day analysis
            if 'Hour' in self.data.columns:
                hourly = self.data.groupby('Hour').agg({
                    'Production_Speed_units_per_hr': 'mean',
                    'Error_Rate_%': 'mean',
                    'Quality_Control_Defect_Rate_%': 'mean',
                    'Temperature_C': 'mean',
                    'Machine_ID': 'count',
                }).round(3)
                
                temporal_analysis['by_hour'] = hourly.to_dict()
            
            # Shift analysis
            if 'Shift' in self.data.columns:
                shift_data = self.data.groupby('Shift').agg({
                    'Production_Speed_units_per_hr': 'mean',
                    'Error_Rate_%': 'mean',
                    'Quality_Control_Defect_Rate_%': 'mean',
                    'Efficiency_Status': lambda x: (x == 'High').sum() / len(x) * 100,
                }).round(2)
                
                temporal_analysis['by_shift'] = shift_data.to_dict()
            
            self.analysis_results['temporal_patterns'] = temporal_analysis
            logger.info("Temporal patterns analyzed")
            
            return temporal_analysis
        
        except Exception as e:
            logger.error(f"Error analyzing temporal patterns: {str(e)}")
            return {}

    def generate_insights(self) -> List[str]:
        """
        Generate key insights from analysis
        
        Returns:
            List of insight strings
        """
        try:
            insights = []
            
            # Overall efficiency insight
            high_eff_pct = (self.data['Efficiency_Status'] == 'High').sum() / len(self.data) * 100
            insights.append(
                f"Only {high_eff_pct:.1f}% of operations achieved 'High' efficiency status."
            )
            
            # Machine diversity
            num_machines = self.data['Machine_ID'].nunique()
            insights.append(
                f"Data includes {num_machines} unique machines with varying performance profiles."
            )
            
            # Critical sensor insight
            avg_temp = self.data['Temperature_C'].mean()
            if avg_temp > SENSOR_THRESHOLDS['Temperature_C']['normal_max']:
                insights.append(
                    f"Average temperature ({avg_temp:.1f}°C) exceeds normal operating range."
                )
            
            # Error insight
            machines_with_errors = (self.data['Error_Rate_%'] > 0).sum()
            error_pct = machines_with_errors / len(self.data) * 100
            insights.append(
                f"{error_pct:.1f}% of records show operational errors requiring attention."
            )
            
            # Production consistency
            prod_std = self.data['Production_Speed_units_per_hr'].std()
            prod_mean = self.data['Production_Speed_units_per_hr'].mean()
            cv = (prod_std / prod_mean) * 100
            if cv > 50:
                insights.append(
                    f"High variability in production speed (CV: {cv:.1f}%) suggests inconsistent operations."
                )
            
            self.analysis_results['insights'] = insights
            logger.info(f"Generated {len(insights)} key insights")
            
            return insights
        
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return []

    def _interpret_skewness(self, skewness: float) -> str:
        """Helper to interpret skewness"""
        if abs(skewness) < 0.5:
            return "Fairly Symmetric"
        elif skewness > 0:
            return "Right Skewed"
        else:
            return "Left Skewed"

    def _detect_distribution(self, data: pd.Series) -> str:
        """Helper to detect distribution type"""
        if abs(data.skew()) < 0.5 and abs(data.kurtosis()) < 1:
            return "Normal-like"
        elif data.skew() > 1:
            return "Right Skewed"
        elif data.skew() < -1:
            return "Left Skewed"
        else:
            return "Other"

    def _count_outliers(self, data: pd.Series, method: str = 'iqr') -> int:
        """Helper to count outliers"""
        if method == 'iqr':
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return ((data < lower_bound) | (data > upper_bound)).sum()
        return 0

    def get_full_analysis(self) -> Dict:
        """
        Run complete analysis
        
        Returns:
            Dictionary with all analysis results
        """
        logger.info("Starting comprehensive analysis...")
        
        self.get_descriptive_statistics()
        self.analyze_sensor_distributions()
        self.analyze_machine_performance()
        self.analyze_operation_modes()
        self.identify_critical_machines()
        self.analyze_temporal_patterns()
        self.generate_insights()
        
        logger.info("Analysis completed successfully")
        return self.analysis_results


def perform_analysis(data: pd.DataFrame) -> Dict:
    """
    Convenience function to perform complete analysis
    
    Args:
        data: Processed DataFrame
        
    Returns:
        Dictionary with all analysis results
    """
    analyzer = DataAnalyzer(data)
    return analyzer.get_full_analysis()
