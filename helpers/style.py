import streamlit as st


def load_css():
    """Inject the dashboard's custom CSS (cards, tabs, insight callouts)."""

    st.markdown(
        """

    <style>

    .main{
        padding-top:1rem;
    }

    div[data-testid="metric-container"]{
        background:white;
        border-radius:15px;
        padding:20px;
        box-shadow:0px 3px 12px rgba(0,0,0,.08);
        border:1px solid #EEEEEE;
    }

    h1{
        color:#2563EB;
    }

    h2, h3{
        color:#1F2937;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"]{
        gap: 6px;
    }

    .stTabs [data-baseweb="tab"]{
        background-color:#F5F7FA;
        border-radius:10px 10px 0px 0px;
        padding:8px 16px;
        font-weight:600;
    }

    .stTabs [aria-selected="true"]{
        background-color:#2563EB !important;
        color:white !important;
    }

    /* Insight callout box */
    .insight-box{
        background:#EFF6FF;
        border-left:5px solid #2563EB;
        padding:14px 18px;
        border-radius:10px;
        margin:10px 0px;
        font-size:0.95rem;
        color:#1F2937;
    }

    .insight-box b{
        color:#2563EB;
    }

    /* Section subtitle */
    .section-caption{
        color:#6B7280;
        font-size:0.9rem;
        margin-top:-8px;
        margin-bottom:10px;
    }

    </style>

    """,
        unsafe_allow_html=True,
    )


def insight_box(text: str):
    """Render a highlighted insight/finding callout under a chart."""

    st.markdown(f'<div class="insight-box">💡 {text}</div>', unsafe_allow_html=True)
