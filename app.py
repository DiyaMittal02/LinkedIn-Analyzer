
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# -------------------------------
# 1. PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="LinkedIn Market Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------
# 2. CUSTOM CSS (LinkedIn Theme)
# -------------------------------
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    .stApp {
        background-color: #f3f2ef;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Ensure text visibility */
    h1, h2, h3, h4, h5, h6, .stMarkdown, p, li, label {
        color: #000000 !important;
    }
    
    .stDataFrame {
         border: 1px solid #e0e0e0;
         border-radius: 8px;
    }

    /* Header/Title */
    .header-container {
        padding: 1.5rem;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 1.5rem;
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .header-title {
        color: #0a66c2 !important;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    .header-subtitle {
        color: #666666 !important;
        font-size: 0.9rem;
        margin-top: 5px;
    }

    /* Cards */
    .metric-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .metric-label {
        font-size: 0.85rem;
        color: #666666 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0a66c2 !important;
    }

    /* Job Card for Listing */
    .job-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .job-title { font-weight: 600; color: #0a66c2 !important; font-size: 1.1rem; }
    .job-company { color: #191919 !important; font-weight: 500; }
    .job-location { color: #666666 !important; font-size: 0.9rem; }
    .job-meta { color: #666666 !important; font-size: 0.85rem; margin-top: 5px; }
    .badge-opportunity {
        background-color: #d1e7dd;
        color: #0f5132 !important;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    /* Sidebar Fixes */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: #0a66c2 !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 3. HELPER FUNCTIONS (Charts & Data)
# -------------------------------
@st.cache_data
def load_data():
    try:
        # Load optimized parquet file first
        if pd.io.common.file_exists("market_data.parquet"):
            df = pd.read_parquet("market_data.parquet")
        else:
            # Fallback to CSV if parquet is missing
            df = pd.read_csv("final_cleaned_jobs.csv")

        # Ensure numeric types
        if 'normalized_salary' in df.columns:
            df['normalized_salary'] = pd.to_numeric(df['normalized_salary'], errors='coerce')
        if 'views' in df.columns:
            df['views'] = pd.to_numeric(df['views'], errors='coerce').fillna(0)
            
        # Feature Engineering: Opportunity Score (Only if not already in parquet)
        if 'opportunity_score' not in df.columns and 'normalized_salary' in df.columns and 'views' in df.columns:
            max_sal = df['normalized_salary'].max()
            max_views = df['views'].max()
            if max_sal > 0 and max_views > 0:
                norm_sal = df['normalized_salary'] / max_sal
                inv_norm_views = 1 - (df['views'] / max_views) 
                df['opportunity_score'] = (norm_sal * 0.7) + (inv_norm_views * 0.3)
                df['opportunity_score'] = df['opportunity_score'].round(2) * 100
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def create_market_scatter(dataframe):
    if 'normalized_salary' in dataframe.columns and 'views' in dataframe.columns:
        plot_df = dataframe.dropna(subset=['normalized_salary', 'views'])
        if not plot_df.empty:
            fig = px.scatter(
                plot_df, 
                x="views", 
                y="normalized_salary", 
                color="opportunity_score",
                size="normalized_salary",
                hover_data=["title", "company_name", "location"],
                color_continuous_scale="Blues",
                title="Market Opportunity Matrix: Salary vs. Competition"
            )
            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                font={'family': 'Roboto', 'color': '#333'},
                xaxis=dict(showgrid=True, gridcolor='#f3f2ef', title="Competition (Views)"),
                yaxis=dict(showgrid=True, gridcolor='#f3f2ef', title="Salary ($)"),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            return fig
    return None

def create_salary_dist(dataframe):
    if 'normalized_salary' in dataframe.columns and not dataframe.empty:
        # Safe drop
        plot_df = dataframe.dropna(subset=['normalized_salary'])
        if not plot_df.empty:
            fig = px.histogram(
                plot_df, 
                x="normalized_salary", 
                nbins=30, 
                title="Overall Salary Distribution",
                color_discrete_sequence=['#0a66c2']
            )
            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                font={'family': 'Roboto', 'color': '#333'},
                xaxis_title="Salary ($)",
                yaxis_title="Job Count"
            )
            return fig
    return None

def generate_html_report(dataframe, avg_s, med_v, t_loc):
    # Create charts for the report
    scatter_fig = create_market_scatter(dataframe)
    dist_fig = create_salary_dist(dataframe)
    
    # Convert charts to HTML (div string)
    scatter_html = scatter_fig.to_html(full_html=False, include_plotlyjs='cdn') if scatter_fig else "<p>No Scatter Data</p>"
    dist_html = dist_fig.to_html(full_html=False, include_plotlyjs='cdn') if dist_fig else "<p>No Dist Data</p>"

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; margin: 40px; }}
            h1 {{ color: #0a66c2; border-bottom: 2px solid #0a66c2; padding-bottom: 10px; }}
            h2 {{ color: #333; margin-top: 30px; }}
            .kpi-container {{ display: flex; gap: 20px; margin-bottom: 30px; }}
            .kpi-box {{ 
                flex: 1; 
                background: #f3f2ef; 
                padding: 20px; 
                border-radius: 8px; 
                text-align: center;
            }}
            .kpi-value {{ font-size: 24px; font-weight: bold; color: #0a66c2; }}
            .kpi-label {{ font-size: 14px; color: #666; text-transform: uppercase; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; font-size: 0.9em; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #0a66c2; color: white; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .chart-box {{ border: 1px solid #eee; padding: 15px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        </style>
    </head>
    <body>
        <h1>LinkedIn Market Analysis Report</h1>
        <p><strong>Generated on:</strong> {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}</p>
        
        <h2>📊 Market Snapshot</h2>
        <div class='kpi-container'>
            <div class='kpi-box'>
                <div class='kpi-value'>{len(dataframe):,}</div>
                <div class='kpi-label'>Total Jobs Analyzed</div>
            </div>
            <div class='kpi-box'>
                <div class='kpi-value'>${avg_s:,.0f}</div>
                <div class='kpi-label'>Average Salary</div>
            </div>
            <div class='kpi-box'>
                <div class='kpi-value'>{int(med_v)}</div>
                <div class='kpi-label'>Median Views</div>
            </div>
            <div class='kpi-box'>
                <div class='kpi-value'>{t_loc}</div>
                <div class='kpi-label'>Top Location</div>
            </div>
        </div>

        <h2>📈 Market Analysis Charts</h2>
        <div class="chart-box">
            {scatter_html}
        </div>
        <div class="chart-box">
            {dist_html}
        </div>

        <h2>💎 Top 10 High-Opportunity Jobs</h2>
        <p>These jobs have the best ratio of high salary vs. low competition in the filtered dataset.</p>
    """
    
    if 'opportunity_score' in dataframe.columns:
        safe_top = dataframe.dropna(subset=['opportunity_score', 'normalized_salary', 'views'])
        if not safe_top.empty:
            top_10 = safe_top.sort_values(by='opportunity_score', ascending=False).head(10)
            cols = ['title', 'company_name', 'location', 'normalized_salary', 'views', 'opportunity_score']
            display_df = top_10[cols].copy()
            # Format
            display_df['normalized_salary'] = display_df['normalized_salary'].apply(lambda x: f"${x:,.0f}")
            html += display_df.to_html(index=False, classes='table', border=0)
        else:
            html += "<p>No opportunity data available (missing salary/views).</p>"
    
    html += """
        <p style="margin-top: 50px; color: #999; font-size: 0.8em; text-align: center;">Generated by LinkedIn Market Intelligence App</p>
    </body>
    </html>
    """
    return html

# -------------------------------
# 4. LOAD & FILTER DATA
# -------------------------------
df = load_data()

st.sidebar.markdown("### **Market Intelligence**")
with st.sidebar.expander("🔍 **Filters**", expanded=True):
    # Location Filter
    if 'location' in df.columns:
        all_locs = sorted(df['location'].dropna().unique().tolist())
        sel_loc = st.multiselect("Location", all_locs)
        if sel_loc:
            df = df[df['location'].isin(sel_loc)]

    # Job Title Search
    search_query = st.text_input("Job Title / Keyword", placeholder="e.g. Data Scientist")
    if search_query:
        df = df[df['title'].str.contains(search_query, case=False, na=False) | df['company_name'].str.contains(search_query, case=False, na=False)]

    # Salary Slider
    if 'normalized_salary' in df.columns and not df.empty and df['normalized_salary'].notna().any():
        min_val = df['normalized_salary'].min()
        max_val = df['normalized_salary'].max()
        if pd.notna(min_val) and pd.notna(max_val):
            min_s, max_s = int(min_val), int(max_val)
            if min_s < max_s:
                sal_range = st.slider("Salary Range ($)", min_s, max_s, (min_s, max_s))
                df = df[(df['normalized_salary'] >= sal_range[0]) & (df['normalized_salary'] <= sal_range[1])]
            else:
                st.info(f"Fixed Salary: ${min_s}")
    else:
        st.info("Jobs found: " + str(len(df)))

st.sidebar.markdown("---")

# -------------------------------
# 5. MAIN CONTENT
# -------------------------------
st.markdown("""
<div class="header-container">
    <div class="header-title">Job Market Insights</div>
    <div class="header-subtitle">Real-time data analysis of salary trends, competition, and top opportunities.</div>
</div>
""", unsafe_allow_html=True)

# Calculation of KPIs
total_jobs = len(df)
avg_sal = df['normalized_salary'].mean() if not df.empty and 'normalized_salary' in df.columns else 0
avg_sal = 0 if pd.isna(avg_sal) else avg_sal

med_views = df['views'].median() if not df.empty and 'views' in df.columns else 0
med_views = 0 if pd.isna(med_views) else med_views

top_loc = "N/A"
if not df.empty and 'location' in df.columns:
    v_locs = df['location'].dropna()
    if not v_locs.empty:
        top_loc = v_locs.mode()[0]

# Display KPIs
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='metric-card'><div class='metric-label'>Active Jobs</div><div class='metric-value'>{total_jobs:,}</div></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric-card'><div class='metric-label'>Avg. Salary</div><div class='metric-value'>${avg_sal:,.0f}</div></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric-card'><div class='metric-label'>Median Views</div><div class='metric-value'>{int(med_views)}</div></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='metric-card'><div class='metric-label'>Top Location</div><div class='metric-value'>{top_loc}</div></div>", unsafe_allow_html=True)

st.markdown("###")

# Sidebar Export logic
st.sidebar.markdown("### 📥 Export Report")
if not df.empty:
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("Download Filtered Data (CSV)", csv, "market_data.csv", "text/csv")
    
    # Generate HTML report
    report_html = generate_html_report(df, avg_sal, med_views, top_loc)
    st.sidebar.download_button("Download Full Report (HTML)", report_html, "market_report.html", "text/html")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚀 Dashboard", "⚔️ Market Battle", "🏆 Top Companies", "📈 Analytics", "📋 Raw Data"])

# TAB 1: DASHBOARD
with tab1:
    fig_matrix = create_market_scatter(df)
    
    col_matrix, col_list = st.columns([1.8, 1.2])
    
    with col_matrix:
        st.markdown("### 📊 Market Opportunity Matrix")
        st.caption("Identify 'Hidden Gems': Jobs with **High Salary** but **Low Competition**.")
        if fig_matrix:
            st.plotly_chart(fig_matrix, use_container_width=True)
        else:
            st.info("No data available for Matrix.")

    with col_list:
        st.markdown("### 💎 Top 'Hidden Gems'")
        st.caption("Highest Opportunity Score")
        
        if 'opportunity_score' in df.columns:
            safe_opps = df.dropna(subset=['opportunity_score', 'normalized_salary', 'views'])
            if not safe_opps.empty:
                top_opps = safe_opps.sort_values(by="opportunity_score", ascending=False).head(4)
                for _, row in top_opps.iterrows():
                    st.markdown(f"""
                    <div class="job-card">
                        <div style="flex:1;">
                            <div class="job-title" style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{row['title']}</div>
                            <div class="job-company">{row['company_name']}</div>
                            <div class="job-meta">💰 ${row['normalized_salary']:,.0f} | 👁 {int(row['views'])}</div>
                        </div>
                        <div class="badge-opportunity" style="margin-left:10px;">{int(row['opportunity_score'])}/100</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No opportunity data.")
        else:
            st.info("Opportunity data missing.")

# TAB 2: MARKET BATTLE
with tab2:
    st.markdown("### ⚔️ Role Face-Off")
    st.caption("Compare two different job roles head-to-head.")
    
    if 'title' in df.columns:
        top_roles = df['title'].value_counts().head(50).index.tolist()
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            role_a = st.selectbox("Role A", top_roles, index=0, key="role_a")
        with col_b2:
            role_b = st.selectbox("Role B", top_roles, index=1, key="role_b")
            
        if role_a and role_b:
            df_a = df[df['title'] == role_a]
            df_b = df[df['title'] == role_b]
            
            # Metrics
            sal_a = df_a['normalized_salary'].mean() if not df_a.empty else 0
            sal_b = df_b['normalized_salary'].mean() if not df_b.empty else 0
            
            views_a = df_a['views'].median() if not df_a.empty else 0
            views_b = df_b['views'].median() if not df_b.empty else 0
            
            count_a = len(df_a)
            count_b = len(df_b)
            
            # Visualization
            c_comp1, c_comp2 = st.columns(2)
            
            with c_comp1:
                st.markdown(f"""
                <div class="metric-card" style="border-top: 4px solid #0a66c2;">
                    <h3 style="margin:0; color:#0a66c2 !important;">{role_a}</h3>
                    <div style="margin-top:10px;">
                        <div class="metric-label">Avg Salary</div>
                        <div class="metric-value" style="font-size:1.5rem;">${sal_a:,.0f}</div>
                    </div>
                    <div style="margin-top:10px;">
                        <div class="metric-label">Median Views</div>
                        <div class="metric-value" style="font-size:1.5rem;">{int(views_a)}</div>
                    </div>
                     <div style="margin-top:10px;">
                        <div class="metric-label">Job Count</div>
                        <div class="metric-value" style="font-size:1.5rem;">{count_a}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with c_comp2:
                st.markdown(f"""
                <div class="metric-card" style="border-top: 4px solid #cf3c4f;">
                    <h3 style="margin:0; color:#cf3c4f !important;">{role_b}</h3>
                    <div style="margin-top:10px;">
                        <div class="metric-label">Avg Salary</div>
                        <div class="metric-value" style="font-size:1.5rem; color:#cf3c4f !important;">${sal_b:,.0f}</div>
                    </div>
                    <div style="margin-top:10px;">
                        <div class="metric-label">Median Views</div>
                        <div class="metric-value" style="font-size:1.5rem; color:#cf3c4f !important;">{int(views_b)}</div>
                    </div>
                    <div style="margin-top:10px;">
                        <div class="metric-label">Job Count</div>
                        <div class="metric-value" style="font-size:1.5rem; color:#cf3c4f !important;">{count_b}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# TAB 3: TOP COMPANIES
with tab3:
    st.markdown("### 🏆 Top Companies by Opportunity")
    st.caption("Companies offering the best balance of **High Salary** and **Low Competition**. (Min. 3 listings)")
    
    if 'company_name' in df.columns and 'opportunity_score' in df.columns:
        # Group by company
        co_stats = df.groupby('company_name').agg({
            'opportunity_score': 'mean',
            'normalized_salary': 'mean',
            'views': 'median',
            'title': 'count'
        }).reset_index()
        
        # Filter for min 3 listings like "real" analysis
        qualified_co = co_stats[co_stats['title'] >= 2] # Lowered to 2 for smaller datasets
        
        if not qualified_co.empty:
            ranked_co = qualified_co.sort_values(by='opportunity_score', ascending=False).head(10)
            
            # Styles table
            st.dataframe(
                ranked_co,
                use_container_width=True,
                column_config={
                    "company_name": st.column_config.TextColumn("Company"),
                    "opportunity_score": st.column_config.ProgressColumn(
                        "Opp. Score",
                        format="%.1f",
                        min_value=0,
                        max_value=100,
                    ),
                    "normalized_salary": st.column_config.NumberColumn(
                        "Avg Salary",
                        format="$%d"
                    ),
                    "views": st.column_config.NumberColumn(
                        "Med. Views",
                        format="%d"
                    ),
                    "title": st.column_config.NumberColumn(
                        "Job Count",
                        format="%d"
                    )
                },
                hide_index=True
            )
        else:
            st.info("Not enough data to rank companies (need companies with >1 job listing).")

# TAB 4: ANALYTICS
with tab4:
    st.markdown("### ⚖️ Salary Benchmarker")
    if 'title' in df.columns:
        top_titles = df['title'].value_counts().head(50).index.tolist()
        selected_role = st.selectbox("Select a Role", top_titles)
        
        if selected_role:
            role_df = df[df['title'] == selected_role]
            role_avg = role_df['normalized_salary'].mean() if not role_df.empty else 0
            
            c_bench1, c_bench2 = st.columns([1, 2])
            
            with c_bench1:
                diff = ((role_avg - avg_sal) / avg_sal) * 100 if avg_sal > 0 else 0
                color = "green" if diff > 0 else "red"
                arrow = "⬆" if diff > 0 else "⬇"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{selected_role} Avg</div>
                    <div class="metric-value">${role_avg:,.0f}</div>
                    <div style="color:{color}; font-weight:bold; margin-top:5px;">
                        {arrow} {abs(diff):.1f}% vs Market Avg
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with c_bench2:
                if not role_df.empty:
                    fig_hist = px.histogram(role_df, x="normalized_salary", nbins=20, title=f"Salary Distribution: {selected_role}", color_discrete_sequence=['#0a66c2'])
                    fig_hist.add_vline(x=avg_sal, line_dash="dash", line_color="red", annotation_text="Market Avg")
                    fig_hist.update_layout(plot_bgcolor="white", xaxis_title="Salary ($)", yaxis_title="Count")
                    st.plotly_chart(fig_hist, use_container_width=True)
                else:
                    st.info("No data for histogram.")

# TAB 5: RAW DATA
with tab5:
    st.dataframe(df.sort_values(by='normalized_salary', ascending=False), use_container_width=True)
