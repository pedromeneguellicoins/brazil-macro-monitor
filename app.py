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
        title="📈 BRL Macro Monitor",
        subtitle="Monitor de drivers macroeconômicos do real brasileiro",
        sources=["BCB SGS", "Yahoo Finance", "FRED", "Binance", "CoinGecko"]
    ),
    unsafe_allow_html=True
)

# ============================================================
# HELPER: KPI seguro (lida com séries vazias, NaN, etc.)
# ============================================================
def safe_kpi(col, label, df, col_name, fmt="num", border_color=None):
    """
    Renderiza KPI com tratamento defensivo.
    fmt: 'num' (2 casas), 'price' (4 casas BRL), 'crypto' (variável)
    """
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

    # Formatação do valor
    if fmt == "price":
        val_str = f"R$ {now:.4f}"
    elif fmt == "crypto":
        if now >= 1000:
            val_str = f"${now:,.0f}"
        elif now >= 1:
            val_str = f"${now:.4f}"
        else:
            val_str = f"${now:.6f}"
    else:  # num
        val_str = f"{now:.2f}"

    col.markdown(
        render_kpi(label, val_str, chg, border_color=border_color or COLORS['neutral']),
        unsafe_allow_html=True
    )


# ============================================================
# HELPER: Preços crypto via CoinGecko (gratuito, sem auth)
# ============================================================
@st.cache_data(ttl=300)  # cache de 5 min
def get_crypto_prices():
    """
    Retorna dict com preço atual e variação 24h de USDT, USDC, BTC vs USD.
    Fonte: CoinGecko (gratuito, sem API key).
    """
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
