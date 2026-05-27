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
    """
    Carrega série do BCB SGS.
    Códigos úteis:
        1    = PTAX USD/BRL venda
        12   = CDI diário
        432  = Selic meta
        4189 = Selic anualizada
        1178 = DI 1 ano
    """
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
# EXCHANGES CRYPTO — USDT/BRL SPOT
# ============================================================
@st.cache_data(ttl=60)
def load_binance_usdt_brl():
    """USDT/BRL spot na Binance."""
    try:
        url = "https://api.binance.com/api/v3/ticker/bookTicker"
        params = {"symbol": "USDTBRL"}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        book = r.json()

        url24 = "https://api.binance.com/api/v3/ticker/24hr"
        r24 = requests.get(url24, params=params, timeout=10)
        r24.raise_for_status()
        ticker = r24.json()

        return {
            'exchange': 'Binance',
            'bid': float(book['bidPrice']),
            'ask': float(book['askPrice']),
            'last': float(ticker['lastPrice']),
            'volume_24h': float(ticker['volume']),
            'change_24h': float(ticker['priceChangePercent']),
        }
    except Exception as e:
        return {'exchange': 'Binance', 'error': str(e)}


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
    """USDT/BRL na Foxbit."""
    try:
        url = "https://api.foxbit.com.br/rest/v3/markets/usdtbrl/ticker/24hr"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        return {
            'exchange': 'Foxbit',
            'bid': float(data.get('best_bid', 0)),
            'ask': float(data.get('best_ask', 0)),
            'last': float(data.get('last', 0)),
            'volume_24h': float(data.get('volume', 0)),
            'change_24h': None,
        }
    except Exception as e:
        return {'exchange': 'Foxbit', 'error': str(e)}


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


def load_all_usdt_brl():
    """4 exchanges spot."""
    return [
        load_binance_usdt_brl(),
        load_mercadobitcoin_usdt_brl(),
        load_foxbit_usdt_brl(),
        load_bitso_usdt_brl(),
    ]


# ============================================================
# BINANCE P2P
# ============================================================
@st.cache_data(ttl=120)
def load_binance_p2p(trade_type="SELL", rows=5):
    """
    P2P USDT/BRL Binance.
    trade_type='SELL' = anunciantes vendendo USDT (você compra)
    trade_type='BUY'  = anunciantes comprando USDT (você vende)
    """
    try:
        url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
        payload = {
            "fiat": "BRL",
            "page": 1,
            "rows": rows,
            "tradeType": trade_type,
            "asset": "USDT",
            "countries": [],
            "proMerchantAds": False,
            "shieldMerchantAds": False,
            "publisherType": None,
            "payTypes": [],
            "classifies": ["mass", "profession"]
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        }
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()

        if not data.get('success') or not data.get('data'):
            return {'trade_type': trade_type, 'error': 'sem dados retornados'}

        prices = [float(ad['adv']['price']) for ad in data['data']]
        if not prices:
            return {'trade_type': trade_type, 'error': 'lista vazia'}

        volumes = [float(ad['adv']['surplusAmount']) for ad in data['data']]
        merchants = [ad['advertiser']['nickName'] for ad in data['data']]

        return {
            'trade_type': trade_type,
            'prices': prices,
            'median': statistics.median(prices),
            'mean': statistics.mean(prices),
            'min': min(prices),
            'max': max(prices),
            'volumes': volumes,
            'total_volume': sum(volumes),
            'merchants': merchants,
            'count': len(prices),
        }
    except Exception as e:
        return {'trade_type': trade_type, 'error': str(e)}


def load_binance_p2p_both_sides():
    """Retorna P2P em formato compatível com tabela de exchanges."""
    sell_side = load_binance_p2p(trade_type="SELL")
    buy_side = load_binance_p2p(trade_type="BUY")

    if 'error' in sell_side or 'error' in buy_side:
        errors = []
        if 'error' in sell_side:
            errors.append(f"SELL: {sell_side['error']}")
        if 'error' in buy_side:
            errors.append(f"BUY: {buy_side['error']}")
        return {'exchange': 'Binance P2P', 'error': ' | '.join(errors)}

    return {
        'exchange': 'Binance P2P',
        'bid': buy_side['median'],
        'ask': sell_side['median'],
        'last': (buy_side['median'] + sell_side['median']) / 2,
        'volume_24h': buy_side['total_volume'] + sell_side['total_volume'],
        'change_24h': None,
        'p2p_buy_prices': buy_side['prices'],
        'p2p_sell_prices': sell_side['prices'],
        'p2p_buy_merchants': buy_side['merchants'],
        'p2p_sell_merchants': sell_side['merchants'],
    }


def load_all_usdt_brl_with_p2p():
    """4 exchanges spot + P2P Binance."""
    return [
        load_binance_usdt_brl(),
        load_mercadobitcoin_usdt_brl(),
        load_foxbit_usdt_brl(),
        load_bitso_usdt_brl(),
        load_binance_p2p_both_sides(),
    ]
