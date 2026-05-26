"""
BRL Macro Monitor — Home page.
Overview com os principais indicadores em uma tela.
"""
import streamlit as st
import pandas as pd
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
        sources=["BCB SGS", "Yahoo Finance", "FRED", "Exchanges públicas"]
    ),
    unsafe_allow_html=True
)

# ============================================================
# OVERVIEW — INDICADORES PRINCIPAIS
# ============================================================
st.markdown("### 🎯 Snapshot de Mercado")

end_date = datetime.today()
start_date = end_date - timedelta(days=60)  # 60d só pra ter histórico recente

# Carrega dados rapidamente
try:
    with st.spinner("Carregando indicadores..."):
        ptax = load_ptax(start_date, end_date)
        dxy = load_yahoo('DX-Y.NYB', start_date, end_date, col_name='DXY')
        vix = load_yahoo('^VIX', start_date, end_date, col_name='VIX')
        cnh = load_yahoo('CNH=X', start_date, end_date, col_name='CNH')

    # KPIs
    col1, col2, col3, col4 = st.columns(4)

    if not ptax.empty:
        ptax_now = ptax['PTAX'].iloc[-1]
        ptax_chg = (ptax['PTAX'].iloc[-1] / ptax['PTAX'].iloc[-2] - 1) * 100
        col1.markdown(
            render_kpi("PTAX (BRL/USD)", f"R$ {ptax_now:.4f}", ptax_chg,
                       border_color=COLORS['ptax']),
            unsafe_allow_html=True
        )

    if not dxy.empty:
        dxy_now = dxy['DXY'].iloc[-1]
        dxy_chg = (dxy['DXY'].iloc[-1] / dxy['DXY'].iloc[-2] - 1) * 100
        col2.markdown(
            render_kpi("DXY", f"{dxy_now:.2f}", dxy_chg,
                       border_color=COLORS['dxy']),
            unsafe_allow_html=True
        )

    if not cnh.empty:
        cnh_now = cnh['CNH'].iloc[-1]
        cnh_chg = (cnh['CNH'].iloc[-1] / cnh['CNH'].iloc[-2] - 1) * 100
        col3.markdown(
            render_kpi("CNH (Yuan offshore)", f"{cnh_now:.4f}", cnh_chg,
                       border_color=COLORS['cnh']),
            unsafe_allow_html=True
        )

    if not vix.empty:
        vix_now = vix['VIX'].iloc[-1]
        vix_chg = (vix['VIX'].iloc[-1] / vix['VIX'].iloc[-2] - 1) * 100
        col4.markdown(
            render_kpi("VIX", f"{vix_now:.2f}", vix_chg,
                       border_color=COLORS['vix']),
            unsafe_allow_html=True
        )

except Exception as e:
    st.warning(f"Algumas séries não carregaram: {e}")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# GUIA DE NAVEGAÇÃO
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
# CONTEXTO DO PROJETO
# ============================================================
with st.expander("ℹ️ Sobre este monitor"):
    st.markdown("""
    **O que é:** Monitor contextual de drivers macroeconômicos do BRL, construído com fontes públicas e gratuitas.

    **Para quê serve:**
    - Acompanhar regimes de correlação do BRL com indicadores globais e locais
    - Identificar quando o real se descola dos drivers tradicionais (sinal de fator idiossincrático)
    - Apoiar narrativa de mercado em conversas com clientes e em análise pré-cotação

    **Limitações:**
    - Latência: dados de fechamento (não tempo real)
    - Não é sistema de decisão automatizada — é monitor contextual
    - Cobertura limitada ao que está em fontes gratuitas (sem CDS puro, sem vol implícita de opções FX)

    **Atualização:** dados são atualizados automaticamente com cache de 1 hora.
    """)

# ============================================================
# FOOTER
# ============================================================
st.markdown(render_footer(), unsafe_allow_html=True)
