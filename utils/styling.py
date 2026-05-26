"""
Estilo centralizado: paleta de cores, layout Plotly, CSS comum.
Todas as páginas importam daqui pra garantir visual consistente.
"""

# ============================================================
# PALETA DE CORES (tema dark)
# ============================================================
COLORS = {
    # Cores principais
    'ptax': '#00D4AA',       # verde-água (BRL, destaque principal)
    'dxy': '#4A9EFF',        # azul (G10)
    'dtwexbgs': '#FF9F40',   # laranja (Broad dollar)
    'cnh': '#E63946',        # vermelho (China)
    'usdt_premium': '#A78BFA', # roxo (cripto)
    'vix': '#F77F00',        # laranja queimado (risco)
    'commodities': '#90BE6D', # verde oliva
    'rates': '#F4A261',      # ocre (juros)

    # Sinais
    'positive': '#00D4AA',
    'negative': '#FF4B6E',
    'neutral': '#8B92A8',

    # Background
    'bg_main': '#0E1117',
    'bg_card': '#1A1F2E',
    'border': '#2A3142',
    'text_dim': '#8B92A8',
    'text_main': '#FAFAFA',
}

# ============================================================
# LAYOUT PLOTLY COMUM
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
# CSS CUSTOMIZADO
# ============================================================
def get_custom_css():
    """Retorna o bloco de CSS pra injetar em cada página."""
    return f"""
    <style>
        /* Header customizado */
        .main-header {{
            padding: 1rem 0;
            border-bottom: 1px solid {COLORS['border']};
            margin-bottom: 1.5rem;
        }}
        .header-title {{
            font-size: 2rem;
            font-weight: 700;
            color: {COLORS['text_main']};
            margin: 0;
        }}
        .header-subtitle {{
            font-size: 0.9rem;
            color: {COLORS['text_dim']};
            margin-top: 0.3rem;
        }}
        .header-meta {{
            font-size: 0.8rem;
            color: {COLORS['text_dim']};
            font-family: monospace;
        }}

        /* KPI cards */
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

        /* Esconde footer "Made with Streamlit" */
        footer {{visibility: hidden;}}

        /* Footer custom */
        .footer-custom {{
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid {COLORS['border']};
            text-align: center;
            color: {COLORS['text_dim']};
            font-size: 0.8rem;
            font-family: monospace;
        }}

        /* Tabs customizadas */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: {COLORS['bg_card']};
            border-radius: 6px 6px 0 0;
            padding: 0.5rem 1.2rem;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {COLORS['ptax']} !important;
            color: {COLORS['bg_main']} !important;
        }}
    </style>
    """


# ============================================================
# HELPERS DE RENDERIZAÇÃO
# ============================================================
def render_kpi(label, value, delta_value=None, delta_format="pct", border_color=None):
    """Renderiza KPI card customizado. Retorna HTML string."""
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
    """Header padronizado pro topo de cada página."""
    from datetime import datetime
    sources_str = " · ".join(sources) if sources else ""
    return f"""
    <div class="main-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-end;">
            <div>
                <p class="header-title">{title}</p>
                <p class="header-subtitle">{subtitle}</p>
            </div>
            <div class="header-meta">
                <div>Updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC-3')}</div>
                <div>Sources: {sources_str}</div>
            </div>
        </div>
    </div>
    """


def render_footer():
    """Footer minimalista."""
    return """
    <div class="footer-custom">
        BRL Macro Monitor v1.0 · Built with Streamlit
    </div>
    """
