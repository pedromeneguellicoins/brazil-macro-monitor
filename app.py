"""
BRL Macro Monitor — Home page.
Overview com os principais indicadores em uma tela.
"""
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

from utils.styling import (
    COLORS, get_custom_css, render_header, render_footer, render_kpi
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
# HELPER: KPI seguro (lida com séries vazias, NaN, etc.)
# ============================================================
def safe_kpi(col, label, df, col_name, fmt="num", border_color=None):
    """Renderiza KPI com tratamento defensivo."""
    if df is None or df.empty or col_name not in df.columns:
        col.markdown(
            render_kpi(label, "—", None, border_color=border_color or COLORS['neutral']),
            unsafe_allow_html=True
        )
        return

    serie = df[col_name].dropna()
    if len(serie) < 2:
        col.markdown(
            render_kpi(label, "—", None, border_color=border_color or COLORS['neutral']),
            unsafe_allow_html=True
        )
        return

    now = serie.iloc[-1]
    prev = serie.iloc[-2]

    if pd.isna(now) or pd.isna(prev) or prev == 0:
        col.markdown(
            render_kpi(label, "—", None, border_color=border_color or COLORS['neutral']),
            unsafe_allow_html=True
        )
        return

    chg = (now / prev - 1) * 100

    if fmt == "price":
        val_str = f"R$ {now:.4f}"
    elif fmt == "crypto":
        if now >= 1000:
            val_str = f"${now:,.0f}"
        elif now >= 1:
            val_str = f"${now:.4f}"
        else:
            val_str = f"${now:.6f}"
    else:
        val_str = f"{now:.2f}"

    col.markdown(
        render_kpi(label, val_str, chg, border_color=border_color or COLORS['neutral']),
        unsafe_allow_html=True
    )


# ============================================================
# HELPER: Preços crypto via CoinGecko
# ============================================================
@st.cache_data(ttl=300)
def get_crypto_prices():
    """Retorna dict com preço e variação 24h de USDT, USDC, BTC vs USD."""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "tether,usd-coin,bitcoin",
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        return {
            'USDT/USD': {
                'price': data['tether']['usd'],
                'change_24h': data['tether'].get('usd_24h_change', 0)
            },
            'USDC/USD': {
                'price': data['usd-coin']['usd'],
                'change_24h': data['usd-coin'].get('usd_24h_change', 0)
            },
            'BTC/USD': {
                'price': data['bitcoin']['usd'],
                'change_24h': data['bitcoin'].get('usd_24h_change', 0)
            }
        }
    except Exception as e:
        st.warning(f"CoinGecko indisponível: {e}")
        return None


def safe_crypto_kpi(col, label, crypto_data, key, border_color):
    """Renderiza KPI de crypto com tratamento defensivo."""
    if crypto_data is None or key not in crypto_data:
        col.markdown(
            render_kpi(label, "—", None, border_color=border_color),
            unsafe_allow_html=True
        )
        return

    price = crypto_data[key]['price']
    chg = crypto_data[key]['change_24h']

    if price >= 1000:
        val_str = f"${price:,.0f}"
    elif price >= 1:
        val_str = f"${price:.4f}"
    else:
        val_str = f"${price:.6f}"

    col.markdown(
        render_kpi(label, val_str, chg, border_color=border_color),
        unsafe_allow_html=True
    )


# ============================================================
# SEÇÃO 1: MACRO TRADICIONAL
# ============================================================
st.markdown("### 🎯 Snapshot Macro")

end_date = datetime.today()
start_date = end_date - timedelta(days=60)

with st.spinner("Carregando indicadores macro..."):
    ptax = pd.DataFrame()
    dxy = pd.DataFrame()
    cnh = pd.DataFrame()
    vix = pd.DataFrame()

    try:
        ptax = load_ptax(start_date, end_date)
    except Exception as e:
        st.caption(f"⚠️ PTAX: {e}")

    try:
        dxy = load_yahoo('DX-Y.NYB', start_date, end_date, col_name='DXY')
    except Exception as e:
        st.caption(f"⚠️ DXY: {e}")

    try:
        cnh = load_yahoo('CNH=X', start_date, end_date, col_name='CNH')
        if cnh.empty:
            cnh = load_yahoo('CNY=X', start_date, end_date, col_name='CNH')
    except Exception as e:
        st.caption(f"⚠️ CNH: {e}")

    try:
        vix = load_yahoo('^VIX', start_date, end_date, col_name='VIX')
    except Exception as e:
        st.caption(f"⚠️ VIX: {e}")

col1, col2, col3, col4 = st.columns(4)
safe_kpi(col1, "PTAX (BRL/USD)", ptax, 'PTAX', fmt='price', border_color=COLORS['ptax'])
safe_kpi(col2, "DXY", dxy, 'DXY', fmt='num', border_color=COLORS['dxy'])
safe_kpi(col3, "CNH (Yuan)", cnh, 'CNH', fmt='num', border_color=COLORS['cnh'])
safe_kpi(col4, "VIX", vix, 'VIX', fmt='num', border_color=COLORS['vix'])

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# SEÇÃO 2: CRYPTO
# ============================================================
st.markdown("### 🪙 Snapshot Crypto")
st.caption("Atualizado a cada 5 minutos · Fonte: CoinGecko")

with st.spinner("Carregando preços crypto..."):
    crypto = get_crypto_prices()

col5, col6, col7 = st.columns(3)
safe_crypto_kpi(col5, "BTC/USD", crypto, 'BTC/USD', border_color='#F7931A')
safe_crypto_kpi(col6, "USDT/USD", crypto, 'USDT/USD', border_color='#26A17B')
safe_crypto_kpi(col7, "USDC/USD", crypto, 'USDC/USD', border_color='#2775CA')

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# NAVEGAÇÃO
# ============================================================
st.markdown("### 🧭 Navegação")
st.markdown("""
Use o menu lateral pra acessar as análises detalhadas:

| Página | Conteúdo | Status |
|---|---|---|
| **💱 FX e Dollar** | PTAX × DXY × DTWEXBGS, correlações, regimes | ✅ Disponível |
| **🪙 USDT Premium** | Premium USDT/BRL vs PTAX em múltiplas exchanges | 🚧 Em construção |
| **📈 Rates** | Curva DI Brasil + diferencial Fed Funds | 🚧 Em construção |
| **🌾 Commodities** | Iron ore, soja, Brent + CNH/Yuan | 🚧 Em construção |
| **⚠️ Risk Sentiment** | VIX + spread NTN-B/UST (proxy CDS Brasil) | 🚧 Em construção |
| **📋 About** | Metodologia, fontes, limitações | ✅ Disponível |
""")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# CONTEXTO
# ============================================================
with st.expander("ℹ️ Sobre este monitor"):
    st.markdown("""
    **O que é:** Monitor contextual de drivers macroeconômicos do BRL, construído com fontes públicas e gratuitas.

    **Para quê serve:**
    - Acompanhar regimes de correlação do BRL com indicadores globais e locais
    - Identificar quando o real se descola dos drivers tradicionais
    - Apoiar narrativa de mercado em conversas com clientes e em análise pré-cotação

    **Limitações:**
    - Latência: dados de fechamento (não tempo real, exceto crypto)
    - Não é sistema de decisão automatizada — é monitor contextual
    - Cobertura limitada ao que está em fontes gratuitas

    **Atualização:** macro com cache de 1 hora · crypto com cache de 5 minutos.
    """)

# ============================================================
# FOOTER
# ============================================================
st.markdown(render_footer(), unsafe_allow_html=True)
