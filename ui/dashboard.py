import streamlit as st
import plotly.graph_objects as bar_plot
import re

def render_scorecard(raw_report):
    st.markdown("## 📊 Executive Evaluation Dashboard")
    
    # Extracting scores using Regex
    tech = re.search(r"Technical Score:\s*(\d+)", raw_report)
    comm = re.search(r"Communication Score:\s*(\d+)", raw_report)
    conf = re.search(r"Confidence Score:\s*(\d+)", raw_report)
    
    t_score = int(tech.group(1)) if tech else 70
    m_score = int(comm.group(1)) if comm else 70
    c_score = int(conf.group(1)) if conf else 70

    # Beautiful Plotly Radar/Polar Graph
    categories = ['Technical Depth', 'Communication', 'Confidence']
    scores = [t_score, m_score, c_score]

    fig = bar_plot.Figure(data=bar_plot.Scatterpolar(
        r=scores, theta=categories, fill='toself',
        marker=dict(color='#ff4b4b')
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Print Verdict & Rest Details
    st.markdown("### 📝 Full Qualitative Breakdown")
    st.write(raw_report.split("---")[-1])