# � LinkedIn Market Intelligence & Analyzer

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

> **Unlock the Jobs no one is looking for.** An advanced market intelligence dashboard designed to help job seekers find "Hidden Gems"—high-paying roles with low competition.

---

## 🔗 [Explore the Live Dashboard](https://linkedin-analyzer-5t8haku5nvnoymdkpdzzww.streamlit.app/)

---

## ✨ Key Features

### � Advanced Dashboard
- **Market Opportunity Matrix**: A 4-quadrant scatter plot identifying roles with high salary and low competition.
- **Hidden Gems List**: Automatically ranks the top high-opportunity jobs currently available.
- **Market Sentiment Index**: A real-time gauge indicating whether the current market favors candidates or employers.

### 🌍 Market Intelligence Map
- **Geographic Analysis**: Discover which locations offer the highest average salaries for your target roles.
- **Role Demand Heatmap**: Visualizes the most competitive roles based on median LinkedIn views.
- **Market Hierarchy Treemap**: See the distribution of jobs across major companies and titles in a single, interactive view.

### ⚔️ Role Face-Off (Market Battle)
- **Head-to-Head Comparison**: Compare any two job titles across three critical dimensions: Salary, Competition (Views), and Volume.
- **Interactive Visual Comparison**: High-impact metric cards that highlight which role wins in each category.

### 📈 Precision Analytics
- **Salary Benchmarker**: See exactly how a specific role's pay compares to the broader market average.
- **Salary Distribution**: Deep-dive histograms showing the realistic income brackets for any job title.

### 🌐 Smart Filtering & Remote Detection
- **Remote-First Intelligence**: Automated detection of "Remote", "WFH", and "Anywhere" tags within job descriptions.
- **Dynamic Filtering**: Filter by location, salary range, and specific keywords with live-updating charts.

---

## 🛠️ Technical Architecture

- **Core Framework**: [Streamlit](https://streamlit.io/) for a reactive, data-driven UI.
- **Analytics Engine**: [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/) for high-performance data processing.
- **Visuals**: [Plotly](https://plotly.com/) for a premium, interactive charting experience.
- **Data Optimization**: [Parquet](https://parquet.apache.org/) format integration for sub-second data loading.
- **Design System**: Custom CSS injected via Streamlit's markdown system to provide a premium, cohesive look.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation & Run
1. **Clone the repository:**
   ```bash
   git clone https://github.com/DiyaMittal02/LinkedIn-Analyzer.git
   cd LinkedIn-Analyzer
   ```

2. **Setup virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Intelligence App:**
   ```bash
   python -m streamlit run app.py
   ```

---

## 📂 Project Structure
```text
├── .streamlit/             # Streamlit configuration
├── data/                    # Raw and intermediate datasets
├── dashboard/               # Additional dashboard assets
├── app.py                   # Main application logic & UI
├── market_data.parquet      # Optimized dataset for speed
├── README.md                # You are here!
└── requirements.txt         # Project dependencies
```

---

## 📬 Contact & Contribution
Created by **Diya Mittal**. 

Contributions are welcome! If you find a bug or have a feature request, please open an issue. If you find this project useful, consider giving it a ⭐ on GitHub!

---
*Disclaimer: Data analyzed by this tool is subject to the snapshot of LinkedIn listings collected at the time of data cleaning.*
