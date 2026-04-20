# Quick Start Guide
## Manufacturing Process Health Dashboard - Setup & Execution

---

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **Disk Space**: 500MB for installation + data
- **Internet**: For pip package installation (first time only)

---

## 🚀 Installation Steps

### Step 1: Navigate to Project Directory

```bash
cd "Manufacturing Process Health and Operational Efficiency Analysis in 6G-Enabled Smart Factories"
```

### Step 2: Create Virtual Environment

**Windows (PowerShell/CMD)**:
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Upgrade pip

```bash
python -m pip install --upgrade pip setuptools wheel
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**Installation Time**: ~2-5 minutes (first time)

### Step 5: Verify Installation

```bash
python -c "import streamlit; import pandas; print('✅ Installation successful!')"
```

---

## ▶️ Running the Dashboard

### Launch the Application

```bash
streamlit run app.py
```

**Expected Output**:
```
You can now view your Streamlit app in your browser.

  URL: http://localhost:8501
```

### Access the Dashboard

Open your web browser and navigate to: **http://localhost:8501**

---

## 📊 Using the Dashboard

### Navigation Structure

1. **Factory Health Overview** 📊
   - Overall efficiency metrics
   - Sensor average values
   - Mode-based efficiency comparison

2. **Machine Health Dashboard** 🤖
   - Per-machine health scores
   - Sensor trend analysis
   - Individual machine detail view

3. **Production & Quality Panel** 📈
   - Production vs defect correlation
   - Error rate analysis
   - Quality metrics by machine

4. **Efficiency Diagnostics** ⚡
   - Efficiency distribution breakdown
   - Critical machine identification
   - Root cause indicators

5. **Data Explorer** 📋
   - Raw data browser with pagination
   - Customizable column selection
   - CSV download functionality

### Using Filters

**Sidebar Controls**:
- **Machine Selector**: Choose specific machines to analyze
- **Operation Mode Filter**: Include/exclude specific modes
- **Efficiency Status Filter**: Focus on High/Medium/Low operations

---

## 📓 Running the Analysis Notebook

### Open Jupyter Environment

```bash
# Option 1: Using JupyterLab
jupyter lab notebooks/EDA_Research.ipynb

# Option 2: Using Jupyter Notebook
jupyter notebook notebooks/EDA_Research.ipynb
```

### Execute Notebook Sections

1. **Import Libraries** - Install and verify dependencies
2. **Load Data** - Read and validate dataset
3. **Data Cleaning** - Standardize and prepare data
4. **Analysis** - Explore patterns and relationships
5. **KPI Calculations** - Compute performance metrics
6. **Export Results** - Save processed data for dashboard

**Execution Time**: ~5-10 minutes for complete notebook

---

## 🔧 Using Analysis Modules Directly

### Python Script Example

```python
from src.data_loader import load_and_validate_data
from src.data_processor import preprocess_data
from src.analyzer import perform_analysis
from src.kpi_calculator import calculate_kpis

# Step 1: Load data
data, is_valid, report = load_and_validate_data()
print(f"Data loaded: {is_valid}")

# Step 2: Process data
processed_data, proc_report = preprocess_data(data)
print(f"Rows processed: {len(processed_data)}")

# Step 3: Analyze
analysis_results = perform_analysis(processed_data)
print(f"Key insights: {analysis_results['insights']}")

# Step 4: Calculate KPIs
kpis = calculate_kpis(processed_data)
print(f"Machine health scores: {kpis['machine_health_index']}")
```

---

## 📂 Project File Structure

```
Project Root/
├── app.py                           # Main Streamlit application
├── requirements.txt                 # Package dependencies
├── README.md                        # Full documentation
├── QUICK_START.md                   # This file
│
├── config/
│   ├── __init__.py
│   └── config.py                    # Configuration constants
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py               # Data loading module
│   ├── data_processor.py            # Data preprocessing module
│   ├── analyzer.py                  # EDA and analysis module
│   ├── kpi_calculator.py            # KPI computation module
│   └── dashboard_components.py      # Streamlit components
│
├── notebooks/
│   └── EDA_Research.ipynb           # Jupyter analysis notebook
│
├── docs/
│   ├── RESEARCH_PAPER.md            # Detailed research findings
│   └── EXECUTIVE_SUMMARY.md         # C-level summary
│
├── data/
│   ├── processed_data.csv           # Processed dataset (auto-generated)
│   ├── machine_health_index.csv     # Health scores (auto-generated)
│   ├── kpi_summary.json             # KPI metrics (auto-generated)
│   ├── correlation_matrix.csv       # Correlations (auto-generated)
│   └── machine_performance.csv      # Performance data (auto-generated)
│
├── Thales_Group_Manufacturing (1).csv  # Raw dataset
└── .gitignore                           # Git configuration
```

---

## ⚙️ Configuration

### Modify Settings

Edit `config/config.py` to customize:

```python
# Sensor thresholds
SENSOR_THRESHOLDS = {
    'Temperature_C': {
        'normal_min': 20.0,
        'normal_max': 80.0,
        'warning_max': 95.0,
        'critical_max': 105.0,
    },
    # ... more thresholds
}

# KPI weights
KPI_WEIGHTS = {
    'temperature_stability': 0.25,
    'vibration_control': 0.25,
    'power_efficiency': 0.20,
    'network_reliability': 0.15,
    'predictive_maintenance': 0.15,
}

# Benchmark values
BENCHMARK_VALUES = {
    'temperature_optimal': 50.0,
    'vibration_acceptable': 2.5,
    'defect_rate_target': 2.0,
    'error_rate_target': 3.0,
}
```

---

## 🐛 Troubleshooting

### Issue: "Module not found" errors

**Solution**:
```bash
# Reinstall all packages
pip install -r requirements.txt --force-reinstall

# Or install specific package
pip install streamlit --upgrade
```

### Issue: Port 8501 already in use

**Solution**:
```bash
# Run on different port
streamlit run app.py --server.port 8502
```

### Issue: Data file not found

**Solution**:
```bash
# Verify file location
ls "Thales_Group_Manufacturing (1).csv"

# Update path in config.py if needed
DATA_FILE = Path(__file__).parent / "path/to/file.csv"
```

### Issue: Slow performance

**Solution**:
- Reduce number of selected machines in filters
- Use Data Explorer pagination
- Close other applications to free RAM
- Consider running on higher-spec machine

### Issue: Dashboard not loading

**Solution**:
```bash
# Clear Streamlit cache
streamlit cache clear

# Run with debug output
streamlit run app.py --logger.level=debug
```

---

## 📊 Sample Analysis Output

### Dashboard Metrics (Example Values)

```
Total Records: 48,000
Unique Machines: 50
High Efficiency: 30%
Average Production Speed: 282.5 units/hr
Average Defect Rate: 4.8%
Average Error Rate: 7.3%
Network Latency: 25.3 ms
```

### Machine Health Index Distribution

```
Excellent (0.75-1.0): 3 machines
Good (0.6-0.75): 9 machines
Fair (0.4-0.6): 20 machines
Poor (0.2-0.4): 15 machines
Critical (<0.2): 3 machines
```

---

## 📈 Next Steps After Installation

1. **Run Dashboard** → Explore real-time metrics
2. **Review Notebook** → Understand data analysis methodology
3. **Check Reports** → Read research paper and executive summary
4. **Configure** → Customize thresholds for your environment
5. **Deploy** → Set up production monitoring system

---

## 📞 Support & Help

### Getting Help

- **Data Issues**: Check `README.md` Data Format section
- **Dashboard Usage**: Explore tab descriptions and filter options
- **Analysis Questions**: Review `docs/RESEARCH_PAPER.md`
- **Configuration**: Consult `config/config.py` documentation

### Common Questions

**Q: How often is data updated?**  
A: Dashboard updates in real-time as new data is available (per-minute granularity).

**Q: Can I add more machines?**  
A: Yes, simply add more CSV rows with new Machine_IDs. Dashboard scales automatically.

**Q: How do I export results?**  
A: Use "Data Explorer" tab → "Download as CSV" button for current filtered view.

**Q: Can I modify KPI calculations?**  
A: Yes, edit `src/kpi_calculator.py` and run the notebook to regenerate metrics.

---

## 🎓 Educational Resources

### Learning Modules

1. **Data Processing**: `src/data_processor.py` - Learn data cleaning techniques
2. **Analysis Methods**: `src/analyzer.py` - Understand EDA approaches
3. **KPI Framework**: `src/kpi_calculator.py` - Study composite scoring
4. **Dashboard Design**: `src/dashboard_components.py` - Explore Streamlit patterns

### Python Concepts Demonstrated

- Object-oriented programming (DataLoader, DataProcessor classes)
- Functional programming (Analysis functions)
- Error handling and logging
- Data validation and quality checks
- Statistical analysis and correlation
- Data visualization and reporting

---

## ✅ Verification Checklist

After installation, verify:

- [ ] Python version >= 3.8
- [ ] Virtual environment activated
- [ ] All packages installed (`pip list | grep pandas`)
- [ ] Data file present in project root
- [ ] Dashboard launches without errors
- [ ] Can navigate all 5 dashboard tabs
- [ ] Can apply filters and see data updates
- [ ] Can download data from explorer
- [ ] Notebook executes all cells successfully
- [ ] Documentation files readable

---

## 🚀 Performance Tips

### For Large Datasets

```python
# Load specific date range only
data = load_data(nrows=10000)  # Load first 10,000 rows

# Filter early to reduce processing
filtered = data[data['Machine_ID'].isin([1, 2, 3])]
```

### For Better Performance

- Use SSD storage for data files
- Close unnecessary browser tabs
- Run dashboard on machine with 8+ GB RAM
- Use latest Python version (3.11 or 3.12)

---

## 📅 Maintenance Schedule

### Daily
- Monitor dashboard for alerts
- Review efficiency trends

### Weekly
- Check KPI trending
- Verify data quality

### Monthly
- Generate trend reports
- Review machine health index
- Plan maintenance actions

### Quarterly
- Update analysis models
- Optimize KPI weights
- Strategic planning review

---

## 🔐 Security Best Practices

- Store credentials separately (use environment variables)
- Limit dashboard access to authorized users
- Enable HTTPS for production deployment
- Regular backup of data and configurations
- Audit log retention (30+ days)

---

## 📞 Contact & Support

For questions or issues:
1. Check documentation first (README.md, this file)
2. Review research paper for methodology
3. Contact analytics team for troubleshooting
4. Submit bug reports with error logs

---

**Version**: 1.0  
**Last Updated**: April 2026  
**Python Compatibility**: 3.8+  
**Status**: Production Ready  

---

**Happy analyzing! 🎉**
