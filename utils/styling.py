"""
Estilo Bloomberg Terminal-inspired.
Fundo preto puro, dados em âmbar, sinais verde/vermelho fosforescente.
"""

# ============================================================
# PALETA BLOOMBERG TERMINAL
# ============================================================
COLORS = {
    # Background
    'bg_main': '#000000',
    'bg_card': '#0A0A0A',
    'bg_header': '#000000',
    'bg_hover': '#1A1A1A',
    'border': '#2D2D2D',
    'border_light': '#404040',

    # Text
    'text_main': '#FFFFFF',
    'text_dim': '#808080',
    'text_secondary': '#B0B0B0',

    # Bloomberg colors
    'amber': '#FFA500',          # cor primária Bloomberg
    'amber_bright': '#FFB733',
    'cyan': '#00BFFF',           # links, info
    'yellow': '#FFFF00',         # warnings, destaques

    # Sinais
    'positive': '#00FF41',       # verde fosforescente
    'negative': '#FF3939',       # vermelho saturado
    'neutral': '#808080',

    # Cores por categoria (mantidas pra gráficos)
    'ptax': '#FFA500',           # âmbar (BRL é o destaque principal)
    'dxy': '#00BFFF',            # cyan
    'dtwexbgs': '#FFFF00',       # amarelo
    'cnh': '#FF6B35',            # laranja escuro
    'usdt_premium': '#B266FF',   # roxo
    'vix': '#FF3939',            # vermelho (risco)
    'commodities': '#00FF41',    # verde
    'rates': '#FF8C00',          # laranja
}

# ============================================================
# LAYOUT PLOTLY
# ============================================================
PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor=COLORS['bg_main'],
    plot_bgcolor=COLORS['bg_main'],
    font=dict(family="'Courier New', monospace", size=11, color=COLORS['text_main']),
    hovermode='x unified',
    margin=dict(l=40, r=20, t=40, b=40),
)

PLOTLY_AXIS = dict(
    gridcolor=COLORS['border'],
    zerolinecolor=COLORS['border_light'],
    tickfont=dict(family="'Courier New', monospace", color=COLORS['text_secondary']),
)


# ============================================================
# LOGO SVG — terminal style
# ============================================================
LOGO_SVG = """
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" fill="#000000" stroke="#FFA500" stroke-width="1.5"/>
  <text x="6" y="20" font-family="Courier New, monospace" font-weight="bold"
        font-size="12" fill="#FFA500">BRL</text>
  <text x="6" y="34" font-family="Courier New, monospace"
        font-size="9" fill="#FFFFFF">MACRO</text>
  <rect x="32" y="8" width="3" height="14" fill="#00FF41"/>
  <rect x="36" y="14" width="3" height="8" fill="#00FF41"/>
  <rect x="40" y="11" width="3" height="11" fill="#FF3939"/>
  <rect x="32" y="28" width="11" height="1" fill="#FFA500"/>
  <text x="32" y="40" font-family="Courier New, monospace"
        font-size="7" fill="#808080">v1.0</text>
</svg>
"""


# ============================================================
# CSS — override agressivo
# ============================================================
def get_custom_css():
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        /* ============ BASE ============ */
        html, body, [class*="css"], .stApp {{
            background-color: {COLORS['bg_main']} !important;
            color: {COLORS['text_main']} !important;
            font-family: 'JetBrains Mono', 'Courier New', monospace !important;
        }}

        .stApp {{
            background-color: {COLORS['bg_main']} !important;
        }}

        .main .block-container {{
            background-color: {COLORS['bg_main']} !important;
            padding-top: 1rem;
        }}

        /* ============ HEADER ============ */
        .main-header {{
            background-color: {COLORS['bg_card']};
            padding: 1.2rem 1.5rem;
            border: 1px solid {COLORS['border']};
            border-left: 3px solid {COLORS['amber']};
            margin-bottom: 1.5rem;
        }}
        .header-flex {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1.5rem;
        }}
        .header-left {{
            display: flex;
            align-items: center;
            gap: 1.2rem;
        }}
        .header-logo {{
            flex-shrink: 0;
        }}
        .header-text {{
            display: flex;
            flex-direction: column;
        }}
        .header-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {COLORS['amber']} !important;
            margin: 0;
            font-family: 'JetBrains Mono', monospace !important;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            line-height: 1.2;
        }}
        .header-title-accent {{
            color: {COLORS['amber']} !important;
        }}
        .header-subtitle {{
            font-size: 0.8rem;
            color: {COLORS['text_secondary']};
            margin-top: 0.3rem;
            font-family: 'JetBrains Mono', monospace;
        }}
        .header-meta {{
            font-size: 0.72rem;
            color: {COLORS['text_secondary']};
            font-family: 'JetBrains Mono', monospace;
            text-align: right;
            line-height: 1.7;
        }}
        .header-meta-label {{
            color: {COLORS['amber']};
            font-weight: 600;
            text-transform: uppercase;
        }}

        /* ============ HEADINGS (override AGRESSIVO) ============ */
        h1, h2, h3, h4, h5, h6,
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
        .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
            color: {COLORS['amber']} !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .stMarkdown h3 {{
            font-size: 1rem !important;
            border-left: 3px solid {COLORS['amber']};
            padding-left: 0.8rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            background-color: {COLORS['bg_card']};
            padding: 0.6rem 0.8rem;
            border-top: 1px solid {COLORS['border']};
            border-bottom: 1px solid {COLORS['border']};
            border-right: 1px solid {COLORS['border']};
        }}

        /* ============ TEXTO GERAL ============ */
        .stMarkdown p, .stMarkdown li, .stMarkdown span,
        p, div, span, label {{
            color: {COLORS['text_main']};
            font-family: 'JetBrains Mono', monospace;
        }}

        .stCaption, [data-testid="stCaptionContainer"] {{
            color: {COLORS['text_dim']} !important;
            font-family: 'JetBrains Mono', monospace !important;
        }}

        /* ============ KPI CARDS ============ */
        .kpi-card {{
            background-color: {COLORS['bg_card']};
            padding: 1rem 1.2rem;
            border: 1px solid {COLORS['border']};
            border-left: 3px solid {COLORS['amber']};
            margin-bottom: 0.5rem;
        }}
        .kpi-label {{
            font-size: 0.7rem;
            color: {COLORS['text_dim']};
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
        }}
        .kpi-value {{
            font-size: 1.6rem;
            font-weight: 700;
            color: {COLORS['amber']};
            margin: 0.4rem 0 0.2rem 0;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.02em;
        }}
        .kpi-delta-pos {{
            color: {COLORS['positive']};
            font-size: 0.8rem;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
        }}
        .kpi-delta-neg {{
            color: {COLORS['negative']};
            font-size: 0.8rem;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
        }}
        .kpi-delta-neutral {{
            color: {COLORS['text_dim']};
            font-size: 0.8rem;
            font-family: 'JetBrains Mono', monospace;
        }}

        /* ============ TABS ============ */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 2px;
            background-color: {COLORS['bg_main']};
            border-bottom: 1px solid {COLORS['border']};
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: {COLORS['bg_card']} !important;
            border-radius: 0 !important;
            padding: 0.6rem 1.4rem !important;
            color: {COLORS['text_secondary']} !important;
            font-weight: 500 !important;
            font-family: 'JetBrains Mono', monospace !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.8rem !important;
            border: 1px solid {COLORS['border']} !important;
            border-bottom: none !important;
        }}
        .stTabs [data-baseweb="tab"] p {{
            color: {COLORS['text_secondary']} !important;
            font-family: 'JetBrains Mono', monospace !important;
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            background-color: {COLORS['bg_hover']} !important;
            color: {COLORS['amber']} !important;
        }}
        .stTabs [data-baseweb="tab"]:hover p {{
            color: {COLORS['amber']} !important;
        }}
        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            background-color: {COLORS['amber']} !important;
            color: {COLORS['bg_main']} !important;
            font-weight: 700 !important;
        }}
        .stTabs [data-baseweb="tab"][aria-selected="true"] p {{
            color: {COLORS['bg_main']} !important;
            font-weight: 700 !important;
        }}
        .stTabs [data-baseweb="tab-highlight"] {{
            display: none !important;
        }}
        .stTabs [data-baseweb="tab-border"] {{
            background-color: {COLORS['amber']} !important;
        }}

        /* ============ SIDEBAR ============ */
        [data-testid="stSidebar"] {{
            background-color: {COLORS['bg_card']} !important;
            border-right: 1px solid {COLORS['border']};
        }}
        [data-testid="stSidebar"] * {{
            color: {COLORS['text_main']} !important;
            font-family: 'JetBrains Mono', monospace !important;
        }}
        [data-testid="stSidebar"] .stMarkdown h3 {{
            color: {COLORS['amber']} !important;
            border-left: 2px solid {COLORS['amber']};
            background-color: transparent;
            border-top: none;
            border-bottom: none;
            border-right: none;
            padding: 0.3rem 0.6rem;
            font-size: 0.85rem !important;
        }}
        [data-testid="stSidebarNav"] {{
            background-color: {COLORS['bg_card']};
        }}
        [data-testid="stSidebarNav"] a {{
            color: {COLORS['text_main']} !important;
            font-family: 'JetBrains Mono', monospace !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.8rem;
        }}
        [data-testid="stSidebarNav"] a:hover {{
            background-color: {COLORS['bg_hover']} !important;
            color: {COLORS['amber']} !important;
        }}

        /* ============ INPUTS / SLIDERS ============ */
        .stSlider [data-baseweb="slider"] {{
            color: {COLORS['amber']};
        }}
        .stSlider [role="slider"] {{
            background-color: {COLORS['amber']} !important;
            border-color: {COLORS['amber']} !important;
        }}
        .stSelectbox label, .stMultiSelect label,
        .stSlider label, .stCheckbox label {{
            color: {COLORS['text_main']} !important;
            font-family: 'JetBrains Mono', monospace !important;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }}
        .stMultiSelect [data-baseweb="tag"] {{
            background-color: {COLORS['amber']} !important;
            color: {COLORS['bg_main']} !important;
        }}
        .stMultiSelect [data-baseweb="select"] > div,
        .stSelectbox [data-baseweb="select"] > div {{
            background-color: {COLORS['bg_card']} !important;
            border-color: {COLORS['border']} !important;
        }}

        /* ============ DATAFRAMES / TABELAS ============ */
        [data-testid="stDataFrame"] {{
            background-color: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
        }}
        [data-testid="stTable"] {{
            font-family: 'JetBrains Mono', monospace !important;
        }}

        /* ============ METRIC NATIVA DO STREAMLIT ============ */
        [data-testid="stMetricLabel"] {{
            color: {COLORS['text_dim']} !important;
            font-family: 'JetBrains Mono', monospace !important;
            text-transform: uppercase;
            font-size: 0.7rem !important;
            letter-spacing: 0.1em;
        }}
        [data-testid="stMetricValue"] {{
            color: {COLORS['amber']} !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-weight: 700 !important;
        }}
        [data-testid="stMetricDelta"] {{
            font-family: 'JetBrains Mono', monospace !important;
        }}

        /* ============ EXPANDER ============ */
        .streamlit-expanderHeader,
        [data-testid="stExpander"] summary {{
            background-color: {COLORS['bg_card']} !important;
            border: 1px solid {COLORS['border']} !important;
            color: {COLORS['amber']} !important;
            font-family: 'JetBrains Mono', monospace !important;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.05em;
        }}
        [data-testid="stExpander"] {{
            background-color: {COLORS['bg_card']} !important;
            border: 1px solid {COLORS['border']} !important;
        }}

        /* ============ BUTTONS ============ */
        .stButton button, .stDownloadButton button {{
            background-color: {COLORS['bg_card']} !important;
            color: {COLORS['amber']} !important;
            border: 1px solid {COLORS['amber']} !important;
            border-radius: 0 !important;
            font-family: 'JetBrains Mono', monospace !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600 !important;
        }}
        .stButton button:hover, .stDownloadButton button:hover {{
            background-color: {COLORS['amber']} !important;
            color: {COLORS['bg_main']} !important;
        }}

        /* ============ TABELAS MARKDOWN ============ */
        .stMarkdown table {{
            border: 1px solid {COLORS['border']} !important;
            font-family: 'JetBrains Mono', monospace !important;
        }}
        .stMarkdown table th {{
            background-color: {COLORS['bg_card']} !important;
            color: {COLORS['amber']} !important;
            border-bottom: 2px solid {COLORS['amber']} !important;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }}
        .stMarkdown table td {{
            background-color: {COLORS['bg_main']} !important;
            color: {COLORS['text_main']} !important;
            border: 1px solid {COLORS['border']} !important;
        }}
        .stMarkdown table tr:hover td {{
            background-color: {COLORS['bg_card']} !important;
        }}

        /* ============ FOOTER ============ */
        footer {{visibility: hidden;}}
        .footer-custom {{
            margin-top: 3rem;
            padding: 1rem;
            border-top: 1px solid {COLORS['border']};
            text-align: center;
            color: {COLORS['text_dim']};
            font-size: 0.75rem;
            font-family: 'JetBrains Mono', monospace;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}

        /* ============ CODE / PRE ============ */
        code {{
            background-color: {COLORS['bg_card']} !important;
            color: {COLORS['amber']} !important;
            border: 1px solid {COLORS['border']};
            padding: 0.1em 0.4em;
            border-radius: 0;
            font-family: 'JetBrains Mono', monospace !important;
        }}

        /* ============ HEADER ICONS (Share, Star, etc) ============ */
        [data-testid="stToolbar"] {{
            background-color: {COLORS['bg_main']} !important;
        }}

        /* ============ SCROLLBAR ============ */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        ::-webkit-scrollbar-track {{
            background: {COLORS['bg_main']};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {COLORS['border']};
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS['amber']};
        }}
    </style>
    """


# ============================================================
# RENDER HELPERS
# ============================================================
def render_kpi(label, value, delta_value=None, delta_format="pct", border_color=None):
    border = border_color or COLORS['amber']
    delta_html = ""
    if delta_value is not None:
        if delta_format == "pct":
            delta_str = f"{delta_value:+.2f}%"
        elif delta_format == "bps":
            delta_str = f"{delta_value:+.0f} bps"
        else:
            delta_str = f"{delta_value:+.3f}"

        if delta_value > 0:
            css_class = "kpi-delta-pos"
            arrow = "▲"
        elif delta_value < 0:
            css_class = "kpi-delta-neg"
            arrow = "▼"
        else:
            css_class = "kpi-delta-neutral"
            arrow = "■"
        delta_html = f'<div class="{css_class}">{arrow} {delta_str}</div>'

    return f"""
    <div class="kpi-card" style="border-left-color: {border};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color: {border};">{value}</div>
        {delta_html}
    </div>
    """


def render_header(title, subtitle, sources=None):
    from datetime import datetime
    sources_str = " · ".join(sources) if sources else ""

    return f"""
    <div class="main-header">
        <div class="header-flex">
            <div class="header-left">
                <div class="header-logo">{LOGO_SVG}</div>
                <div class="header-text">
                    <p class="header-title">{title}</p>
                    <p class="header-subtitle">{subtitle}</p>
                </div>
            </div>
            <div class="header-meta">
                <div><span class="header-meta-label">Updated:</span> {datetime.now().strftime('%Y-%m-%d %H:%M UTC-3')}</div>
                <div><span class="header-meta-label">Sources:</span> {sources_str}</div>
            </div>
        </div>
    </div>
    """


def render_footer():
    return """
    <div class="footer-custom">
        BRL Macro Monitor · Terminal v1.0 · Pedro Mendes
    </div>
    """
