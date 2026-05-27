"""
Rates — Brasil vs EUA.
Selic, CDI, Fed Funds, UST curve e carry real.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

from utils.styling import (
    COLORS, PLOTLY_LAYOUT, PLOTLY_AXIS,
    get_custom_css, render_header, render_footer, render_kpi
)
from utils.data_loaders import load_ptax, load_bcb_sgs, load_fred
from utils.glossary import render_inline_description, render_detail_expander

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="Rates | BRL Monitor",
    page_icon="📈",
    layout="wide"
)
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown(
    render_header(
        title="Rates — Brasil vs EUA",
        subtitle="Selic, Fed Funds, UST curve e carry real — pilares do BRL",
        sources=["BCB SGS", "FRED"]
    ),
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### ⚙️ Parâmetros")
    anos = st.slider("Anos de histórico", 1, 10, 5)
    janela_corr = st.slider("Janela de correlação (dias)", 10, 90, 30)

# ============================================================
# CARREGAMENTO
# ============================================================
end_date = datetime.today()
start_date = end_date - timedelta(days=anos * 365)

with st.spinner("Carregando taxas..."):
    # Brasil
    try:
        selic = load_bcb_sgs(432, start_date, end_date, col_name='Selic')
    except Exception:
        selic = pd.DataFrame()

    try:
        cdi = load_bcb_sgs(12, start_date, end_date, col_name='CDI')
        # CDI vem diário, anualiza
        if not cdi.empty:
            cdi['CDI'] = ((1 + cdi['CDI'] / 100) ** 252 - 1) * 100
    except Exception:
        cdi = pd.DataFrame()

    try:
        di1y = load_bcb_sgs(1178, start_date, end_date, col_name='DI_1Y')
    except Exception:
        di1y = pd.DataFrame()

    try:
        # IPCA 12 meses acumulado
        ipca = load_bcb_sgs(433, start_date, end_date, col_name='IPCA_12m')
    except Exception:
        ipca = pd.DataFrame()

    # EUA
    try:
        fed = load_fred('DFF', start_date, end_date, col_name='Fed_Funds')
    except Exception:
        fed = pd.DataFrame()

    try:
        ust2y = load_fred('DGS2', start_date, end_date, col_name='UST_2Y')
    except Exception:
        ust2y = pd.DataFrame()

    try:
        ust10y = load_fred('DGS10', start_date, end_date, col_name='UST_10Y')
    except Exception:
        ust10y = pd.DataFrame()

    try:
        # CPI mensal — calcular 12m
        cpi_raw = load_fred('CPIAUCSL', start_date - timedelta(days=400), end_date, col_name='CPI_idx')
        if not cpi_raw.empty:
            cpi = pd.DataFrame()
            cpi['CPI_12m'] = (cpi_raw['CPI_idx'].pct_change(12) * 100).dropna()
            cpi.index = cpi_raw.index[12:]
        else:
            cpi = pd.DataFrame()
    except Exception:
        cpi = pd.DataFrame()

    # PTAX (pra tab 3)
    try:
        ptax = load_ptax(start_date, end_date)
    except Exception:
        ptax = pd.DataFrame()

# ============================================================
# MERGE
# ============================================================
df = pd.DataFrame()
for serie in [selic, cdi, di1y, ipca, fed, ust2y, ust10y, cpi, ptax]:
    if not serie.empty:
        if df.empty:
            df = serie.copy()
        else:
            df = df.join(serie, how='outer')

df = df.sort_index().ffill()

# Calcula spread e carry
if 'Selic' in df.columns and 'Fed_Funds' in df.columns:
    df['Spread_BR_US'] = df['Selic'] - df['Fed_Funds']

if all(c in df.columns for c in ['Selic', 'IPCA_12m', 'Fed_Funds', 'CPI_12m']):
    df['Real_BR'] = df['Selic'] - df['IPCA_12m']
    df['Real_US'] = df['Fed_Funds'] - df['CPI_12m']
    df['Carry_Real'] = df['Real_BR'] - df['Real_US']

if 'UST_10Y' in df.columns and 'UST_2Y' in df.columns:
    df['UST_Spread_10Y_2Y'] = df['UST_10Y'] - df['UST_2Y']

df = df.dropna(subset=['Selic']) if 'Selic' in df.columns else df

# ============================================================
# KPIs
# ============================================================
def get_latest(col):
    """Pega último valor não-nulo da coluna."""
    if col not in df.columns:
        return None
    serie = df[col].dropna()
    return serie.iloc[-1] if not serie.empty else None


kpi_cols = st.columns(4)

selic_now = get_latest('Selic')
fed_now = get_latest('Fed_Funds')
spread_now = get_latest('Spread_BR_US')
carry_now = get_latest('Carry_Real')

kpi_cols[0].markdown(
    render_kpi("Selic Meta", f"{selic_now:.2f}%" if selic_now else "—",
               None, border_color=COLORS['ptax']),
    unsafe_allow_html=True
)
kpi_cols[1].markdown(
    render_kpi("Fed Funds", f"{fed_now:.2f}%" if fed_now else "—",
               None, border_color=COLORS['dxy']),
    unsafe_allow_html=True
)

spread_color = COLORS['positive'] if spread_now and spread_now > 3 else COLORS['amber']
kpi_cols[2].markdown(
    render_kpi("Spread Nominal BR-US",
               f"{spread_now:+.2f} pp" if spread_now else "—",
               None, border_color=spread_color),
    unsafe_allow_html=True
)

carry_color = COLORS['positive'] if carry_now and carry_now > 2 else (COLORS['amber'] if carry_now and carry_now > 0 else COLORS['negative'])
kpi_cols[3].markdown(
    render_kpi("Carry Real",
               f"{carry_now:+.2f} pp" if carry_now else "—",
               None, border_color=carry_color),
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Taxas Básicas",
    "🇺🇸 Curva Americana",
    "💱 Spread vs PTAX",
    "💰 Carry Real",
    "📖 Metodologia"
])

# --- TAB 1: Taxas básicas ---
with tab1:
    col_chart, col_info = st.columns([3, 1])

    with col_chart:
        # Gráfico Selic vs Fed Funds
        fig = go.Figure()
        if 'Selic' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df['Selic'], name='Selic Meta',
                line=dict(color=COLORS['ptax'], width=2.5)
            ))
        if 'Fed_Funds' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df['Fed_Funds'], name='Fed Funds',
                line=dict(color=COLORS['dxy'], width=2.5)
            ))
        fig.update_layout(**PLOTLY_LAYOUT, height=400,
                          title="Selic Meta vs Fed Funds")
        fig.update_xaxes(**PLOTLY_AXIS)
        fig.update_yaxes(**PLOTLY_AXIS, title_text="%")
        st.plotly_chart(fig, use_container_width=True)

        # Gráfico do spread
        if 'Spread_BR_US' in df.columns:
            fig2 = go.Figure(go.Scatter(
                x=df.index, y=df['Spread_BR_US'],
                fill='tozeroy',
                line=dict(color=COLORS['amber'], width=2),
                fillcolor='rgba(255, 165, 0, 0.15)',
                name='Spread BR-US'
            ))
            fig2.add_hline(y=0, line_dash="dash", line_color=COLORS['neutral'])
            fig2.update_layout(**PLOTLY_LAYOUT, height=300,
                               title="Spread Nominal: Selic − Fed Funds (pontos percentuais)")
            fig2.update_xaxes(**PLOTLY_AXIS)
            fig2.update_yaxes(**PLOTLY_AXIS, title_text="pp")
            st.plotly_chart(fig2, use_container_width=True)

    with col_info:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(render_inline_description("SELIC"), unsafe_allow_html=True)
        st.markdown(render_inline_description("FED_FUNDS"), unsafe_allow_html=True)
        st.markdown(render_inline_description("RATE_SPREAD"), unsafe_allow_html=True)

# --- TAB 2: Curva americana ---
with tab2:
    col_chart, col_info = st.columns([3, 1])

    with col_chart:
        fig = go.Figure()
        if 'UST_2Y' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df['UST_2Y'], name='UST 2Y',
                line=dict(color=COLORS['cyan'], width=2)
            ))
        if 'UST_10Y' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df['UST_10Y'], name='UST 10Y',
                line=dict(color=COLORS['amber'], width=2)
            ))
        fig.update_layout(**PLOTLY_LAYOUT, height=400,
                          title="Treasuries Americanos: 2Y vs 10Y")
        fig.update_xaxes(**PLOTLY_AXIS)
        fig.update_yaxes(**PLOTLY_AXIS, title_text="%")
        st.plotly_chart(fig, use_container_width=True)

        # Spread 10Y-2Y
        if 'UST_Spread_10Y_2Y' in df.columns:
            fig2 = go.Figure(go.Scatter(
                x=df.index, y=df['UST_Spread_10Y_2Y'],
                fill='tozeroy',
                line=dict(color='#A78BFA', width=2),
                fillcolor='rgba(167, 139, 250, 0.15)',
                name='Spread 10Y-2Y'
            ))
            fig2.add_hline(y=0, line_dash="dash", line_color=COLORS['negative'],
                           annotation_text="Inversão = sinal de recessão")
            fig2.update_layout(**PLOTLY_LAYOUT, height=350,
                               title="Spread 10Y - 2Y (sinal clássico de recessão quando negativo)")
            fig2.update_xaxes(**PLOTLY_AXIS)
            fig2.update_yaxes(**PLOTLY_AXIS, title_text="pp")
            st.plotly_chart(fig2, use_container_width=True)

    with col_info:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(render_inline_description("UST_CURVE"), unsafe_allow_html=True)

# --- TAB 3: Spread vs PTAX ---
with tab3:
    if 'Spread_BR_US' in df.columns and 'PTAX' in df.columns:
        col_chart, col_info = st.columns([3, 1])

        with col_chart:
            # Eixo duplo: spread + PTAX
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Scatter(x=df.index, y=df['Spread_BR_US'],
                           name='Spread BR-US',
                           line=dict(color=COLORS['amber'], width=2.5)),
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=df.index, y=df['PTAX'],
                           name='PTAX (eixo direito)',
                           line=dict(color=COLORS['ptax'], width=2)),
                secondary_y=True
            )
            fig.update_layout(**PLOTLY_LAYOUT, height=500,
                              title="Spread Selic−Fed vs PTAX (eixos separados)")
            fig.update_xaxes(**PLOTLY_AXIS)
            fig.update_yaxes(title_text="Spread (pp)", secondary_y=False, gridcolor=COLORS['border'])
            fig.update_yaxes(title_text="PTAX (R$)", secondary_y=True, gridcolor=COLORS['border'])
            st.plotly_chart(fig, use_container_width=True)

            # Correlação rolling
            df_corr = df[['Spread_BR_US', 'PTAX']].dropna().copy()
            df_corr['ret_spread'] = df_corr['Spread_BR_US'].diff()
            df_corr['ret_ptax'] = df_corr['PTAX'].pct_change()
            df_corr['corr'] = df_corr['ret_spread'].rolling(janela_corr).corr(df_corr['ret_ptax'])

            fig_c = go.Figure(go.Scatter(
                x=df_corr.index, y=df_corr['corr'],
                line=dict(color='#A78BFA', width=2),
                name='Corr'
            ))
            fig_c.add_hline(y=0, line_dash="dash", line_color=COLORS['neutral'])
            fig_c.update_layout(**PLOTLY_LAYOUT, height=300,
                                title=f"Correlação rolling {janela_corr}d: Δ Spread × Retorno PTAX")
            fig_c.update_xaxes(**PLOTLY_AXIS)
            fig_c.update_yaxes(**PLOTLY_AXIS, range=[-1, 1])
            st.plotly_chart(fig_c, use_container_width=True)
            st.caption("Correlação **negativa** é o esperado: spread sobe → BRL aprecia (PTAX cai).")

        with col_info:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(render_inline_description("RATE_SPREAD"), unsafe_allow_html=True)
    else:
        st.warning("Dados insuficientes — precisa de Selic, Fed Funds e PTAX.")

# --- TAB 4: Carry Real ---
with tab4:
    if 'Carry_Real' in df.columns:
        col_chart, col_info = st.columns([3, 1])

        with col_chart:
            # Comparação Real BR vs Real US
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df.index, y=df['Real_BR'],
                name='Juro Real BR (Selic - IPCA)',
                line=dict(color=COLORS['ptax'], width=2)
            ))
            fig.add_trace(go.Scatter(
                x=df.index, y=df['Real_US'],
                name='Juro Real US (Fed - CPI)',
                line=dict(color=COLORS['dxy'], width=2)
            ))
            fig.add_hline(y=0, line_dash="dash", line_color=COLORS['neutral'])
            fig.update_layout(**PLOTLY_LAYOUT, height=400,
                              title="Juros Reais: Brasil vs EUA")
            fig.update_xaxes(**PLOTLY_AXIS)
            fig.update_yaxes(**PLOTLY_AXIS, title_text="%")
            st.plotly_chart(fig, use_container_width=True)

            # Carry real (diferença)
            fig2 = go.Figure(go.Scatter(
                x=df.index, y=df['Carry_Real'],
                fill='tozeroy',
                line=dict(color=COLORS['commodities'], width=2),
                fillcolor='rgba(144, 190, 109, 0.15)',
                name='Carry Real'
            ))
            fig2.add_hline(y=0, line_dash="dash", line_color=COLORS['neutral'])
            fig2.update_layout(**PLOTLY_LAYOUT, height=400,
                               title="Carry Real (Spread Real BR - US)")
            fig2.update_xaxes(**PLOTLY_AXIS)
            fig2.update_yaxes(**PLOTLY_AXIS, title_text="pp")
            st.plotly_chart(fig2, use_container_width=True)

            # Stats
            st.markdown("##### 📊 Estatísticas do Período")
            carry_serie = df['Carry_Real'].dropna()
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Atual", f"{carry_serie.iloc[-1]:+.2f} pp")
            c2.metric("Média", f"{carry_serie.mean():+.2f} pp")
            c3.metric("Máx", f"{carry_serie.max():+.2f} pp")
            c4.metric("Mín", f"{carry_serie.min():+.2f} pp")

        with col_info:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(render_inline_description("CARRY_REAL"), unsafe_allow_html=True)
    else:
        st.warning("Dados insuficientes para calcular carry real.")

# --- TAB 5: Metodologia ---
with tab5:
    render_detail_expander("SELIC", st)
    render_detail_expander("FED_FUNDS", st)
    render_detail_expander("RATE_SPREAD", st)
    render_detail_expander("CARRY_REAL", st)
    render_detail_expander("UST_CURVE", st)

# ============================================================
# FOOTER
# ============================================================
st.markdown(render_footer(), unsafe_allow_html=True)
