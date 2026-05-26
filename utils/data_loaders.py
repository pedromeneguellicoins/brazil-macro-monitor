"""
Carregamento centralizado de dados.
Todas as páginas importam funções daqui — evita duplicação de código.
"""
import pandas as pd
import requests
import yfinance as yf
import streamlit as st
from datetime import datetime, timedelta
from fredapi import Fred


# ============================================================
# FRED
# ============================================================
def get_fred_client():
    """Retorna cliente FRED inicializado com a key dos secrets."""
    if "FRED_API_KEY" not in st.secrets:
        st.error("⚠️ FRED_API_KEY não configurada nos Secrets do Streamlit.")
        st.stop()
    return Fred(api_key=st.secrets["FRED_API_KEY"])


# ============================================================
# BCB SGS — séries do Banco Central
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
        1178 = DI 1 ano (pode variar)
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
    """Atalho pra PTAX (série 1)."""
    return load_bcb_sgs(1, start_date, end_date, col_name='PTAX')


# ============================================================
# YAHOO FINANCE
# ============================================================
@st.cache_data(ttl=3600)
def load_yahoo(ticker, start_date, end_date, col_name=None):
    """
    Carrega série do Yahoo Finance.
    Tickers úteis:
        DX-Y.NYB = DXY
        CNY=X    = Yuan onshore
        CNH=X    = Yuan offshore
        TIO=F    = Iron ore futures
        ZS=F     = Soybean futures
        BZ=F     = Brent crude
        ^VIX     = VIX
    """
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
    """
    Carrega série do FRED.
    Séries úteis:
        DTWEXBGS = Trade-weighted broad dollar
        DFF      = Fed Funds effective rate
        DGS10    = US Treasury 10Y
        DGS2     = US Treasury 2Y
    """
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
    """
    Faz join de várias séries com forward-fill em colunas específicas.
    Útil pra combinar séries de calendários diferentes (PTAX diário,
    DTWEXBGS semanal, etc).
    """
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
