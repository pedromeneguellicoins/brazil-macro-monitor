"""
Carregamento centralizado de dados.
"""
import pandas as pd
import requests
import yfinance as yf
import streamlit as st
import statistics
from datetime import datetime, timedelta
from fredapi import Fred


# ============================================================
# FRED
# ============================================================
def get_fred_client():
    if "FRED_API_KEY" not in st.secrets:
        st.error("⚠️ FRED_API_KEY não configurada nos Secrets do Streamlit.")
        st.stop()
    return Fred(api_key=st.secrets["FRED_API_KEY"])


# ============================================================
# BCB SGS
# ============================================================
@st.cache_data(ttl=3600)
def load_bcb_sgs(serie_code, start_date, end_date, col_name=None):
    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie_code}/dados"
        f"?formato=json"
        f"&dataInicial={start_date.strftime('%d/%m/%Y')}"
        f"&dataFinal={end_date.strftime('%d/%m/%Y')}"
    )
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    df = pd.DataFrame(r.json())
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df['valor'] = df['valor'].astype(float)
    df = df.set_index('data')
    if col_name:
        df = df.rename(columns={'valor': col_name})
    return df


@st.cache_data(ttl=3600)
def load_ptax(start_date, end_date):
    return load_bcb_sgs(1, start_date, end_date, col_name='PTAX')


# ============================================================
# YAHOO FINANCE
# ============================================================
@st.cache_data(ttl=3600)
def load_yahoo(ticker, start_date, end_date, col_name=None):
    df = yf.download(ticker, start=start_date, end=end_date,
                     progress=False, auto_adjust=False)
    if df.empty:
        return pd.DataFrame()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df[['Close']].copy()
    df.columns = [col_name or ticker]
    return df


# ============================================================
# FRED
# ============================================================
@st.cache_data(ttl=3600)
def load_fred(serie, start_date, end_date, col_name=None):
    fred = get_fred_client()
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    try:
        s = fred.get_series(serie, observation_start=start_str,
                            observation_end=end_str)
        df = pd.DataFrame(s, columns=[col_name or serie])
        df.index = pd.to_datetime(df.index)
        return df.dropna()
    except Exception as e:
        st.error(f"Erro ao carregar {serie} do FRED: {e}")
        return pd.DataFrame()


# ============================================================
# JOIN HELPER
# ============================================================
def join_and_align(df_base, *others, ffill_cols=None):
    df = df_base.copy()
    for other in others:
        if not other.empty:
            df = df.join(other, how='left')

    df = df.sort_index()

    if ffill_cols:
        for col in ffill_cols:
            if col in df.columns:
                df[col] = df[col].ffill()

    return df.dropna()


# ============================================================
# EXCHANGES BRASILEIRAS — USDT/BRL SPOT
# ============================================================
@st.cache_data(ttl=60)
def load_mercadobitcoin_usdt_brl():
    """USDT/BRL no Mercado Bitcoin."""
    try:
        url = "https://api.mercadobitcoin.net/api/v4/tickers"
        params = {"symbols": "USDT-BRL"}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()[0]

        return {
            'exchange': 'Mercado Bitcoin',
            'bid': float(data['buy']),
            'ask': float(data['sell']),
            'last': float(data['last']),
            'volume_24h': float(data['vol']),
            'change_24h': None,
        }
    except Exception as e:
        return {'exchange': 'Mercado Bitcoin', 'error': str(e)}


@st.cache_data(ttl=60)
def load_foxbit_usdt_brl():
    """
    USDT/BRL na Foxbit.
    Tenta múltiplos endpoints em cascata, já que a API da Foxbit
    mudou várias vezes.
    """
    endpoints_to_try = [
        # Endpoint 1: v3 markets ticker
        {
            'url': "https://api.foxbit.com.br/rest/v3/markets/usdtbrl/ticker/24hr",
            'parser': lambda d: {
                'bid': float(d.get('best_bid', 0)),
                'ask': float(d.get('best_ask', 0)),
                'last': float(d.get('last', 0)),
                'volume': float(d.get('volume', 0)),
            }
        },
        # Endpoint 2: v3 markets quotes
        {
            'url': "https://api.foxbit.com.br/rest/v3/markets/usdtbrl/quotes",
            'parser': lambda d: {
                'bid': float(d.get('bid', 0)),
                'ask': float(d.get('ask', 0)),
                'last': float(d.get('last', 0)),
                'volume': 0,
            }
        },
        # Endpoint 3: ticker book (orderbook top)
        {
            'url': "https://api.foxbit.com.br/rest/v3/markets/usdtbrl/orderbook?depth=1",
            'parser': lambda d: {
                'bid': float(d['bids'][0][0]) if d.get('bids') else 0,
                'ask': float(d['asks'][0][0]) if d.get('asks') else 0,
                'last': (float(d['bids'][0][0]) + float(d['asks'][0][0])) / 2 if d.get('bids') and d.get('asks') else 0,
                'volume': 0,
            }
        },
    ]

    last_error = None
    for endpoint in endpoints_to_try:
        try:
            r = requests.get(endpoint['url'], timeout=10)
            r.raise_for_status()
            data = r.json()

            parsed = endpoint['parser'](data)
            if parsed['bid'] > 0 and parsed['ask'] > 0:
                return {
                    'exchange': 'Foxbit',
                    'bid': parsed['bid'],
                    'ask': parsed['ask'],
                    'last': parsed['last'],
                    'volume_24h': parsed['volume'],
                    'change_24h': None,
                }
        except Exception as e:
            last_error = str(e)
            continue

    return {'exchange': 'Foxbit', 'error': last_error or 'todos endpoints falharam'}


@st.cache_data(ttl=60)
def load_bitso_usdt_brl():
    """USDT/BRL na Bitso."""
    try:
        url = "https://api.bitso.com/v3/ticker/"
        params = {"book": "usdt_brl"}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()['payload']

        return {
            'exchange': 'Bitso',
            'bid': float(data['bid']),
            'ask': float(data['ask']),
            'last': float(data['last']),
            'volume_24h': float(data.get('volume', 0)),
            'change_24h': None,
        }
    except Exception as e:
        return {'exchange': 'Bitso', 'error': str(e)}


@st.cache_data(ttl=60)
def load_novadax_usdt_brl():
    """USDT/BRL na NovaDAX."""
    try:
        url = "https://api.novadax.com/v1/market/ticker"
        params = {"symbol": "USDT_BRL"}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()['data']

        return {
            'exchange': 'NovaDAX',
            'bid': float(data['bid']),
            'ask': float(data['ask']),
            'last': float(data['lastPrice']),
            'volume_24h': float(data.get('baseVolume24h', 0)),
            'change_24h': None,
        }
    except Exception as e:
        return {'exchange': 'NovaDAX', 'error': str(e)}


@st.cache_data(ttl=60)
def load_okx_usdt_brl():
    """
    USDT/BRL na OKX (global, suporta BRL via P2P fiat).
    A OKX tem endpoint público para market data.
    """
    try:
        # OKX usa formato com hífen: USDT-BRL
        url = "https://www.okx.com/api/v5/market/ticker"
        params = {"instId": "USDT-BRL"}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        if data.get('code') != '0' or not data.get('data'):
            return {'exchange': 'OKX', 'error': f"resposta inválida: {data.get('msg', 'desconhecido')}"}

        ticker = data['data'][0]
        bid = float(ticker.get('bidPx', 0))
        ask = float(ticker.get('askPx', 0))

        if bid == 0 or ask == 0:
            return {'exchange': 'OKX', 'error': 'par USDT-BRL sem liquidez ou indisponível'}

        return {
            'exchange': 'OKX',
            'bid': bid,
            'ask': ask,
            'last': float(ticker.get('last', 0)),
            'volume_24h': float(ticker.get('vol24h', 0)),
            'change_24h': None,
        }
    except Exception as e:
        return {'exchange': 'OKX', 'error': str(e)}


def load_all_usdt_brl():
    """Exchanges brasileiras + OKX."""
    return [
        load_mercadobitcoin_usdt_brl(),
        load_foxbit_usdt_brl(),
        load_bitso_usdt_brl(),
        load_novadax_usdt_brl(),
        load_okx_usdt_brl(),
    ]


# Alias mantido pra compatibilidade
def load_all_usdt_brl_with_p2p():
    return load_all_usdt_brl()
