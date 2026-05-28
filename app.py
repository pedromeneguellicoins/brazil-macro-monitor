"""
BRL Macro Monitor — Home page.
"""
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

from utils.styling import (
    COLORS, get_custom_css, render_header, render_footer, render_kpi, now_brasilia
)
from utils.data_loaders import load_ptax, load_yahoo, load_fred

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="BRL Macro Monitor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Renomeia "app" → "Monitor Macro" na sidebar
st.markdown("""
<style>
    [data-testid="stSidebarNav"] ul li:first-child a span {
        visibility: hidden; position: relative;
    }
    [data-testid="stSidebarNav"] ul li:first-child a span::after {
        content: "MONITOR MACRO";
        visibility: visible; position: absolute; left: 0; top: 0; white-space: nowrap;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown(
    render_header(
        title="BRL Macro Monitor",
        subtitle="Monitor de drivers macroeconômicos do real brasileiro",
        sources=["BCB SGS", "Yahoo Finance", "FRED", "CoinGecko"]
    ),
    unsafe_allow_html=True
)

# ============================================================
# HELPERS
# ============================================================
def safe_kpi(col, label, df, col_name, fmt="num", border_color=None):
    if df is None or df.empty or col_name not in df.columns:
        col.markdown(render_kpi(label, "—", None, border_color=border_color or COLORS['neutral']), unsafe_allow_html=True)
        return
    serie = df[col_name].dropna()
    if len(serie) < 2:
        col.markdown(render_kpi(label, "—", None, border_color=border_color or COLORS['neutral']), unsafe_allow_html=True)
        return
    now = serie.iloc[-1]; prev = serie.iloc[-2]
    if pd.isna(now) or pd.isna(prev) or prev == 0:
        col.markdown(render_kpi(label, "—", None, border_color=border_color or COLORS['neutral']), unsafe_allow_html=True)
        return
    chg = (now / prev - 1) * 100
    if fmt == "price":
        val_str = f"R$ {now:.4f}"
    elif fmt == "em":
        val_str = f"{now:.4f}"
    else:
        val_str = f"{now:.2f}"
    col.markdown(render_kpi(label, val_str, chg, border_color=border_color or COLORS['neutral']), unsafe_allow_html=True)


@st.cache_data(ttl=300)
def get_crypto_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": "tether,usd-coin,bitcoin", "vs_currencies": "usd", "include_24hr_change": "true"}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        return {
            'USDT/USD': {'price': data['tether']['usd'], 'change_24h': data['tether'].get('usd_24h_change', 0)},
            'USDC/USD': {'price': data['usd-coin']['usd'], 'change_24h': data['usd-coin'].get('usd_24h_change', 0)},
            'BTC/USD': {'price': data['bitcoin']['usd'], 'change_24h': data['bitcoin'].get('usd_24h_change', 0)}
        }
    except Exception as e:
        st.warning(f"CoinGecko indisponível: {e}")
        return None


def safe_crypto_kpi(col, label, crypto_data, key, border_color):
    if crypto_data is None or key not in crypto_data:
        col.markdown(render_kpi(label, "—", None, border_color=border_color), unsafe_allow_html=True)
        return
    price = crypto_data[key]['price']; chg = crypto_data[key]['change_24h']
    if price >= 1000:
        val_str = f"${price:,.0f}"
    elif price >= 1:
        val_str = f"${price:.4f}"
    else:
        val_str = f"${price:.6f}"
    col.markdown(render_kpi(label, val_str, chg, border_color=border_color), unsafe_allow_html=True)


def render_premium_chip(label, value_bps, hint=""):
    """Chip pequeno mostrando prêmio em bps."""
    if value_bps is None:
        return
    color = COLORS['positive'] if value_bps > 0 else (COLORS['negative'] if value_bps < 0 else COLORS['neutral'])
    arrow = "▲" if value_bps > 0 else ("▼" if value_bps < 0 else "■")
    st.markdown(f"""
    <div style="
        background-color: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-top: 2px solid {color};
        padding: 0.5rem 0.8rem; text-align: center;
        font-family: 'JetBrains Mono', monospace; margin: 0.3rem 0;
    ">
        <span style="color: {COLORS['text_dim']}; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em;">{label}</span><br>
        <span style="color: {color}; font-size: 1.1rem; font-weight: 700;">{arrow} {value_bps:+.1f} bps</span>
        <span style="color: {COLORS['text_dim']}; font-size: 0.6rem;"> {hint}</span>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# CARREGAMENTO
# ============================================================
end_date = datetime.today()
start_date = end_date - timedelta(days=60)

with st.spinner("Carregando indicadores..."):
    ptax = pd.DataFrame(); dxy = pd.DataFrame(); cnh = pd.DataFrame(); vix = pd.DataFrame()
    mxn = pd.DataFrame(); zar = pd.DataFrame(); try_ = pd.DataFrame()

    try: ptax = load_ptax(start_date, end_date)
    except Exception as e: st.caption(f"⚠️ PTAX: {e}")
    try: dxy = load_yahoo('DX-Y.NYB', start_date, end_date, col_name='DXY')
    except Exception as e: st.caption(f"⚠️ DXY: {e}")
    try:
        cnh = load_yahoo('CNH=X', start_date, end_date, col_name='CNH')
        if cnh.empty:
            cnh = load_yahoo('CNY=X', start_date, end_date, col_name='CNH')
    except Exception as e: st.caption(f"⚠️ CNH: {e}")
    try: vix = load_yahoo('^VIX', start_date, end_date, col_name='VIX')
    except Exception as e: st.caption(f"⚠️ VIX: {e}")
    try: mxn = load_yahoo('MXN=X', start_date, end_date, col_name='MXN')
    except Exception as e: st.caption(f"⚠️ MXN: {e}")
    try: zar = load_yahoo('ZAR=X', start_date, end_date, col_name='ZAR')
    except Exception as e: st.caption(f"⚠️ ZAR: {e}")
    try: try_ = load_yahoo('TRY=X', start_date, end_date, col_name='TRY')
    except Exception as e: st.caption(f"⚠️ TRY: {e}")

# ============================================================
# SEÇÃO 1: MACRO BRL
# ============================================================
st.markdown("### 🎯 Snapshot Macro BRL")
col1, col2, col3, col4 = st.columns(4)
safe_kpi(col1, "PTAX (BRL/USD)", ptax, 'PTAX', fmt='price', border_color=COLORS['ptax'])
safe_kpi(col2, "DXY", dxy, 'DXY', fmt='num', border_color=COLORS['dxy'])
safe_kpi(col3, "CNH/USD (Yuan)", cnh, 'CNH', fmt='em', border_color=COLORS['cnh'])
safe_kpi(col4, "VIX", vix, 'VIX', fmt='num', border_color=COLORS['vix'])

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# SEÇÃO 2: PEERS EMERGENTES
# ============================================================
st.markdown("### 🌎 Peers Emergentes")
st.caption("Comparação com moedas de outras economias emergentes — contexto para entender se o movimento do BRL é idiossincrático ou parte de um movimento EM geral")
col5, col6, col7 = st.columns(3)
safe_kpi(col5, "MXN/USD (México)", mxn, 'MXN', fmt='em', border_color='#006847')
safe_kpi(col6, "ZAR/USD (África do Sul)", zar, 'ZAR', fmt='em', border_color='#FFB81C')
safe_kpi(col7, "TRY/USD (Turquia)", try_, 'TRY', fmt='num', border_color='#E30A17')

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# SEÇÃO 3: CRYPTO
# ============================================================
st.markdown("### 🪙 Snapshot Crypto")
st.caption("Atualizado a cada 5 minutos · Fonte: CoinGecko")

with st.spinner("Carregando preços crypto..."):
    crypto = get_crypto_prices()

# Layout: BTC | USDT | [prêmio USDT-USDC] | USDC
cc1, cc2, cc3, cc4 = st.columns([1, 1, 0.8, 1])
safe_crypto_kpi(cc1, "BTC/USD", crypto, 'BTC/USD', border_color='#F7931A')
safe_crypto_kpi(cc2, "USDT/USD", crypto, 'USDT/USD', border_color='#26A17B')

# Prêmio USDT vs USDC em bps
with cc3:
    if crypto and 'USDT/USD' in crypto and 'USDC/USD' in crypto:
        usdt_p = crypto['USDT/USD']['price']
        usdc_p = crypto['USDC/USD']['price']
        # prêmio USDT sobre USDC, em bps
        premium_bps = (usdt_p / usdc_p - 1) * 10000
        st.markdown("<br>", unsafe_allow_html=True)
        render_premium_chip("USDT − USDC", premium_bps, "")

safe_crypto_kpi(cc4, "USDC/USD", crypto, 'USDC/USD', border_color='#2775CA')

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# NAVEGAÇÃO
# ============================================================
st.markdown("### 🧭 Navegação")
st.markdown("""
| Página | Conteúdo | Status |
|---|---|---|
| **💱 FX e Dollar** | PTAX × DXY × DTWEXBGS, correlações, regimes | ✅ Disponível |
| **🪙 USDT Premium** | Premium USDT/BRL vs PTAX em múltiplas exchanges | ✅ Disponível |
| **📈 Rates** | Curva DI Brasil + diferencial Fed Funds | ✅ Disponível |
| **🌾 Commodities** | Iron ore, soja, Brent + Termos de Troca | ✅ Disponível |
| **⚠️ Risk Sentiment** | VIX + spread NTN-B/UST (proxy CDS Brasil) | 🚧 Em construção |
| **📋 About** | Metodologia, fontes, limitações | ✅ Disponível |
""")

st.markdown("<br>", unsafe_allow_html=True)

with st.expander("ℹ️ Sobre este monitor"):
    st.markdown("""
    **O que é:** Monitor contextual de drivers macroeconômicos do BRL, construído com fontes públicas e gratuitas.

    **Para quê serve:**
    - Acompanhar regimes de correlação do BRL com indicadores globais e locais
    - Identificar quando o real se descola dos drivers tradicionais
    - Comparar BRL com peers emergentes pra contextualizar movimentos
    - Apoiar narrativa de mercado em conversas com clientes e análise pré-cotação

    **Atualização:** macro com cache de 1 hora · crypto com cache de 5 minutos.
    """)

st.markdown(render_footer(), unsafe_allow_html=True)
