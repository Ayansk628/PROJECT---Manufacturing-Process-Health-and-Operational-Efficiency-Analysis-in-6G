# Streamlit Cloud Deployment Guide

## 📦 Prerequisites

1. **GitHub Account** - Push code to GitHub
2. **Streamlit Account** - Sign up at https://streamlit.io
3. **Git** - Version control

---

## 🚀 Deployment Steps

### Step 1: Prepare Repository

```bash
# Make sure all files are committed to GitHub
git add .
git commit -m "Ready for Streamlit deployment"
git push origin main
```

### Step 2: Add Data File to Repository

The Thales Group manufacturing data file **must be committed** to GitHub:

```bash
# Remove from .gitignore if blocked
git add -f "Thales_Group_Manufacturing (1).csv"
git commit -m "Add manufacturing dataset"
git push origin main
```

### Step 3: Connect to Streamlit Cloud

1. Go to **https://share.streamlit.io**
2. Click **"New app"**
3. Connect your **GitHub account**
4. Select the repository containing this project
5. Set **Main file path** to: `app.py`
6. Click **Deploy**

### Step 4: Verify Deployment

- App should load within 1-2 minutes
- Check logs for any errors
- Test all dashboard tabs

---

## 🔧 Troubleshooting Deployment

### ❌ Error: "Data file not found"

**Solution**: The data file must be in the repository:

```bash
# Force add the data file
git add -f "Thales_Group_Manufacturing (1).csv"
git commit -m "Add dataset"
git push origin main

# Then redeploy in Streamlit
```

### ❌ Error: "Module not found"

**Solution**: Update `requirements.txt` and redeploy:

```bash
# In Streamlit Cloud: Settings > Reboot app
```

### ❌ Error: "PermissionError or FileNotFoundError"

**Solution**: The app now searches multiple paths automatically. If still failing:

1. Go to app settings
2. Click "Reboot app"
3. Check deployment logs

---

## 📁 Repository Structure for Deployment

```
repository/
├── app.py                              # Main app
├── requirements.txt                    # Dependencies
├── Thales_Group_Manufacturing (1).csv  # ✅ MUST BE COMMITTED
├── config/
│   ├── __init__.py
│   └── config.py
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_processor.py
│   ├── analyzer.py
│   ├── kpi_calculator.py
│   └── dashboard_components.py
├── notebooks/
│   └── EDA_Research.ipynb
├── docs/
│   ├── RESEARCH_PAPER.md
│   └── EXECUTIVE_SUMMARY.md
├── .streamlit/
│   └── config.toml                     # ✅ Streamlit config
└── .gitignore
```

---

## ⚙️ Required Files for Deployment

These files **must exist** in your repository:

- ✅ `app.py` - Main application
- ✅ `requirements.txt` - Python dependencies
- ✅ `Thales_Group_Manufacturing (1).csv` - Dataset
- ✅ `config/config.py` - Configuration
- ✅ `src/*.py` - All source modules
- ✅ `.streamlit/config.toml` - Streamlit configuration

---

## 🔒 Important: Data File in Git

### Why Include the Data File?

The CSV file contains the manufacturing dataset needed for the dashboard to function. Without it, the app will crash.

### How to Include It

```bash
# Update .gitignore
# Change: *.csv
# To: !Thales_Group_Manufacturing (1).csv

# Then add it
git add "Thales_Group_Manufacturing (1).csv"
git commit -m "Add required dataset"
git push origin main
```

### File Size

If the file is **> 50 MB**, consider:
- Using Git LFS (Large File Storage)
- Splitting into smaller chunks
- Using a cloud storage service (AWS S3, etc.)

---

## 📊 Monitoring Deployment

### View App Logs

1. Go to your app on **share.streamlit.io**
2. Click **"Manage app"**
3. Select **"Logs"** tab
4. See real-time logs

### Common Issues

| Issue | Log Message | Solution |
|-------|------------|----------|
| File not found | `FileNotFoundError: Data file not found` | Commit CSV file to repo |
| Missing module | `ModuleNotFoundError: No module named 'src'` | Check imports and structure |
| Port conflict | `Error: Port 8501 already in use` | Not applicable to Streamlit Cloud |
| Memory limit | `Out of memory` | Consider reducing dataset size |

---

## 🔄 Redeploying Updates

### After Making Changes

```bash
# Local development
git add .
git commit -m "Update feature X"
git push origin main

# Streamlit automatically detects and redeploys
# (usually within 1-2 minutes)
```

### Manual Reboot

1. Go to **share.streamlit.io**
2. Click your app
3. Settings → **"Reboot app"**

---

## 🌐 Custom Domain (Optional)

1. Go to app settings
2. Click **"Custom domain"**
3. Add your domain
4. Update DNS records

---

## 📞 Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Deployment Guide**: https://docs.streamlit.io/deploy/streamlit-cloud
- **Community**: https://discuss.streamlit.io

---

## ✅ Final Checklist

Before deploying:

- [ ] Data file committed to repo
- [ ] `requirements.txt` updated
- [ ] `config.toml` in `.streamlit/` folder
- [ ] All source files committed
- [ ] No hardcoded absolute paths
- [ ] `.gitignore` configured correctly
- [ ] Tested locally: `streamlit run app.py`
- [ ] GitHub repo is public or Streamlit has access

---

**Status**: Ready for Streamlit Cloud Deployment ✅
