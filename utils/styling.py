"""
Estilo centralizado: paleta de cores, layout Plotly, CSS comum.
"""

# ============================================================
# PALETA
# ============================================================
COLORS = {
    'ptax': '#00D4AA',
    'dxy': '#4A9EFF',
    'dtwexbgs': '#FF9F40',
    'cnh': '#E63946',
    'usdt_premium': '#A78BFA',
    'vix': '#F77F00',
    'commodities': '#90BE6D',
    'rates': '#F4A261',

    'positive': '#00D4AA',
    'negative': '#FF4B6E',
    'neutral': '#8B92A8',

    'bg_main': '#0E1117',
    'bg_card': '#1A1F2E',
    'bg_header': '#0A0E17',
    'border': '#2A3142',
    'text_dim': '#8B92A8',
    'text_main': '#FAFAFA',
}

# ============================================================
# LAYOUT PLOTLY
# ============================================================
PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor=COLORS['bg_main'],
    plot_bgcolor=COLORS['bg_main'],
    font=dict(family="monospace", size=11, color=COLORS['text_main']),
    hovermode='x unified',
    margin=dict(l=40, r=20, t=40, b=40),
)

PLOTLY_AXIS = dict(
    gridcolor=COLORS['border'],
    zerolinecolor=COLORS['border'],
)


# ============================================================
# LOGO SVG (inline, sem dependência externa)
# ============================================================
LOGO_SVG = """
<svg width="44" height="44" viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg">
  <!-- Background circle -->
  <circle cx="22" cy="22" r="21" fill="#0E1117" stroke="#00D4AA" stroke-width="1.5"/>
  <!-- Bar chart bars -->
  <rect x="9" y="24" width="4" height="10" fill="#4A9EFF" rx="1"/>
  <rect x="15" y="19" width="4" height="15" fill="#FF9F40" rx="1"/>
  <rect x="21" y="14" width="4" height="20" fill="#00D4AA" rx="1"/>
  <rect x="27" y="21" width="4" height="13" fill="#A78BFA" rx="1"/>
  <!-- Trend line -->
  <polyline points="11,22 17,17 23,12 29,19 33,15"
            fill="none" stroke="#FAFAFA" stroke-width="1.5"
            stroke-linejoin="round" opacity="0.4"/>
  <!-- BRL marker dot -->
  <circle cx="33" cy="15" r="2" fill="#00D4AA" stroke="#FAFAFA" stroke-width="1"/>
</svg>
"""


# ============================================================
# CSS CUSTOMIZADO
# ============================================================
def get_custom_css():
    return f"""
    <style>
        /* ============ HEADER DARK ============ */
        .main-header {{
            background: linear-gradient(135deg, {COLORS['bg_header']} 0%, {COLORS['bg_card']} 100%);
            padding: 1.5rem 1.8rem;
            border-radius: 12px;
            border: 1px solid {COLORS['border']};
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
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
            gap: 1rem;
        }}
        .header-logo {{
            flex-shrink: 0;
        }}
        .header-text {{
            display: flex;
            flex-direction: column;
        }}
        .header-title {{
            font-size: 1.75rem;
            font-weight: 700;
            color: {COLORS['text_main']};
            margin: 0;
            font-family: monospace;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        .header-title-accent {{
            color: {COLORS['ptax']};
        }}
        .header-subtitle {{
            font-size: 0.85rem;
            color: {COLORS['text_dim']};
            margin-top: 0.2rem;
        }}
        .header-meta {{
            font-size: 0.75rem;
            color: {COLORS['text_dim']};
            font-family: monospace;
            text-align: right;
            line-height: 1.6;
        }}
        .header-meta-label {{
            color: {COLORS['neutral']};
            font-size: 0.7rem;
        }}

        /* ============ KPI CARDS ============ */
        .kpi-card {{
            background-color: {COLORS['bg_card']};
            padding: 1.2rem;
            border-radius: 8px;
            border-left: 3px solid {COLORS['ptax']};
            margin-bottom: 0.5rem;
        }}
        .kpi-label {{
            font-size: 0.75rem;
            color: {COLORS['text_dim']};
            text-transform: uppercase;
            letter-spacing: 0.05rem;
            font-weight: 600;
        }}
        .kpi-value {{
            font-size: 1.6rem;
            font-weight: 700;
            color: {COLORS['text_main']};
            margin: 0.3rem 0;
            font-family: monospace;
        }}
        .kpi-delta-pos {{ color: {COLORS['positive']}; font-size: 0.85rem; font-family: monospace; }}
        .kpi-delta-neg {{ color: {COLORS['negative']}; font-size: 0.85rem; font-family: monospace; }}
        .kpi-delta-neutral {{ color: {COLORS['neutral']}; font-size: 0.85rem; font-family: monospace; }}

        /* ============ TABS (com contraste correto) ============ */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 6px;
            background-color: transparent;
            border-bottom: 1px solid {COLORS['border']};
            padding-bottom: 0;
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: {COLORS['bg_card']};
            border-radius: 8px 8px 0 0;
            padding: 0.7rem 1.4rem;
            color: {COLORS['text_dim']} !important;
            font-weight: 500;
            border: 1px solid {COLORS['border']};
            border-bottom: none;
            transition: all 0.15s ease;
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            background-color: {COLORS['border']};
            color: {COLORS['text_main']} !important;
        }}
        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            background-color: {COLORS['ptax']} !important;
            color: {COLORS['bg_main']} !important;
            font-weight: 700;
            border-color: {COLORS['ptax']};
        }}
        .stTabs [data-baseweb="tab"][aria-selected="true"] p {{
            color: {COLORS['bg_main']} !important;
            font-weight: 700 !important;
        }}
        .stTabs [data-baseweb="tab-panel"] {{
            padding-top: 1rem;
        }}

        /* ============ FOOTER ============ */
        footer {{visibility: hidden;}}
        .footer-custom {{
            margin-top: 3rem;
            padding: 1.2rem;
            border-top: 1px solid {COLORS['border']};
            text-align: center;
            color: {COLORS['text_dim']};
            font-size: 0.8rem;
            font-family: monospace;
        }}

        /* ============ HEADINGS h3 (Snapshot Macro, etc) ============ */
        .stMarkdown h3 {{
            color: {COLORS['text_main']};
            font-weight: 600;
            border-left: 3px solid {COLORS['ptax']};
            padding-left: 0.8rem;
            margin-top: 1.2rem;
            margin-bottom: 1rem;
        }}

        /* ============ EXPANDER ============ */
        .streamlit-expanderHeader {{
            background-color: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
        }}

        /* ============ SIDEBAR ============ */
        [data-testid="stSidebar"] {{
            background-color: {COLORS['bg_header']};
            border-right: 1px solid {COLORS['border']};
        }}
    </style>
    """


# ============================================================
# RENDER HELPERS
# ============================================================
def render_kpi(label, value, delta_value=None, delta_format="pct", border_color=None):
    border = border_color or COLORS['ptax']
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
            arrow = "●"
        delta_html = f'<div class="{css_class}">{arrow} {delta_str}</div>'

    return f"""
    <div class="kpi-card" style="border-left-color: {border};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """


def render_header(title, subtitle, sources=None):
    """Header dark com logo SVG inline."""
    from datetime import datetime
    sources_str = " · ".join(sources) if sources else ""

    # Permite destacar parte do título com a cor accent
    # (ex: "BRL Macro Monitor" → "BRL" fica verde)
    title_words = title.split(" ", 1)
    if len(title_words) > 1 and not title.startswith(("📈", "💱", "🪙", "📈", "🌾", "⚠️", "📋")):
        title_html = f'<span class="header-title-accent">{title_words[0]}</span> {title_words[1]}'
    else:
        title_html = title

    return f"""
    <div class="main-header">
        <div class="header-flex">
            <div class="header-left">
                <div class="header-logo">{LOGO_SVG}</div>
                <div class="header-text">
                    <p class="header-title">{title_html}</p>
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
        BRL Macro Monitor v1.0 · Built with Streamlit · Pedro Mendes
    </div>
    """
