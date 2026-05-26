"""
Página FX e Dollar — PTAX × DXY × DTWEXBGS.
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
from utils.data_loaders import load_ptax, load_yahoo, load_fred, join_and_align
from utils.glossary import render_inline_description, render_detail_expander

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="FX e Dollar | BRL Monitor",
    page_icon="💱",
    layout="wide"
)
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### ⚙️ Parâmetros")
    anos = st.slider("Anos de histórico", 1, 10, 5)
    janela_corr = st.slider("Janela de correlação (dias)", 10, 90, 30)

    indices_selecionados = st.multiselect(
        "Índices de dólar",
        options=["DXY", "DTWEXBGS"],
        default=["DXY", "DTWEXBGS"]
    )

# ============================================================
# HEADER
# ============================================================
st.markdown(
    render_header(
        title="FX & Dollar Indices",
        subtitle="PTAX × DXY × DTWEXBGS — análise de correlação e regimes",
        sources=["BCB SGS", "Yahoo Finance", "FRED"]
    ),
    unsafe_allow_html=True
)

# ============================================================
# CARREGAMENTO
# ============================================================
end_date = datetime.today()
start_date = end_date - timedelta(days=anos * 365)

with st.spinner("Carregando dados..."):
    ptax = load_ptax(start_date, end_date)
    series_to_join = []
    cols_idx = []

    if "DXY" in indices_selecionados:
        dxy = load_yahoo('DX-Y.NYB', start_date, end_date, col_name='DXY')
        if not dxy.empty:
            series_to_join.append(dxy)
            cols_idx.append('DXY')

    if "DTWEXBGS" in indices_selecionados:
        twd = load_fred('DTWEXBGS', start_date, end_date)
        if not twd.empty:
            series_to_join.append(twd)
            cols_idx.append('DTWEXBGS')

    df = join_and_align(ptax, *series_to_join, ffill_cols=cols_idx)

if len(df) < janela_corr + 5:
    st.error(f"❌ Dados insuficientes ({len(df)} linhas).")
    st.stop()

df['ret_ptax'] = df['PTAX'].pct_change()
for idx in cols_idx:
    df[f'ret_{idx}'] = df[idx].pct_change()
    df[f'corr_{idx}'] = df['ret_ptax'].rolling(janela_corr).corr(df[f'ret_{idx}'])

# ============================================================
# KPIs
# ============================================================
kpi_cols = st.columns(1 + len(cols_idx) + 1)

ptax_now = df['PTAX'].iloc[-1]
ptax_chg = (df['PTAX'].iloc[-1] / df['PTAX'].iloc[-2] - 1) * 100
kpi_cols[0].markdown(
    render_kpi("PTAX", f"R$ {ptax_now:.4f}", ptax_chg, border_color=COLORS['ptax']),
    unsafe_allow_html=True
)

cores_idx_map = {'DXY': COLORS['dxy'], 'DTWEXBGS': COLORS['dtwexbgs']}
for i, idx in enumerate(cols_idx):
    val = df[idx].iloc[-1]
    chg = (df[idx].iloc[-1] / df[idx].iloc[-2] - 1) * 100
    kpi_cols[i+1].markdown(
        render_kpi(idx, f"{val:.2f}", chg, border_color=cores_idx_map.get(idx)),
        unsafe_allow_html=True
    )

if cols_idx:
    corr_now = df[f'corr_{cols_idx[0]}'].iloc[-1]
    kpi_cols[-1].markdown(
        render_kpi(f"Corr {janela_corr}d", f"{corr_now:.3f}",
                   border_color=COLORS['neutral']),
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔗 Correlações",
                                    "🔍 Diferencial", "📋 Dados"])

# --- TAB 1: Overview ---
with tab1:
    # Layout: gráfico (col esquerda larga) + descrições (col direita estreita)
    col_chart, col_info = st.columns([3, 1])

    with col_chart:
        fig = make_subplots(
            rows=1 + len(cols_idx), cols=1, shared_xaxes=True,
            subplot_titles=["PTAX (BRL/USD)"] + cols_idx,
            vertical_spacing=0.08
        )

        fig.add_trace(
            go.Scatter(x=df.index, y=df['PTAX'], name='PTAX',
                       line=dict(color=COLORS['ptax'], width=2)),
            row=1, col=1
        )

        for i, idx in enumerate(cols_idx):
            fig.add_trace(
                go.Scatter(x=df.index, y=df[idx], name=idx,
                           line=dict(color=cores_idx_map.get(idx, '#888'), width=2)),
                row=i+2, col=1
            )

        fig.update_layout(**PLOTLY_LAYOUT, height=250*(1+len(cols_idx)),
                           showlegend=False)
        fig.update_xaxes(**PLOTLY_AXIS)
        fig.update_yaxes(**PLOTLY_AXIS)
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(render_inline_description("PTAX"), unsafe_allow_html=True)
        for idx in cols_idx:
            st.markdown(render_inline_description(idx), unsafe_allow_html=True)

    # Expanders detalhados abaixo
    st.markdown("---")
    st.markdown("##### 📖 Documentação técnica")
    render_detail_expander("PTAX", st)
    for idx in cols_idx:
        render_detail_expander(idx, st)

# --- TAB 2: Correlações ---
with tab2:
    col_chart, col_info = st.columns([3, 1])

    with col_chart:
        fig_corr = go.Figure()
        for idx in cols_idx:
            fig_corr.add_trace(go.Scatter(
                x=df.index, y=df[f'corr_{idx}'],
                name=f'PTAX × {idx}',
                line=dict(color=cores_idx_map.get(idx, '#888'), width=2)
            ))
        fig_corr.add_hline(y=0, line_dash="dash", line_color=COLORS['neutral'],
                            opacity=0.5)
        fig_corr.update_layout(**PLOTLY_LAYOUT, height=450,
                                title=f"Correlação Rolling {janela_corr} dias")
        fig_corr.update_xaxes(**PLOTLY_AXIS)
        fig_corr.update_yaxes(**PLOTLY_AXIS, range=[-1, 1])
        st.plotly_chart(fig_corr, use_container_width=True)

    with col_info:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(render_inline_description("CORR_ROLLING"), unsafe_allow_html=True)

    st.markdown("##### 📈 Estatísticas comparativas")
    stats = []
    for idx in cols_idx:
        corr_serie = df[f'corr_{idx}'].dropna()
        stats.append({
            'Índice': idx,
            'Média': corr_serie.mean(),
            'Mediana': corr_serie.median(),
            'Mín': corr_serie.min(),
            'Máx': corr_serie.max(),
            '% > 0': (corr_serie > 0).mean() * 100,
            'Atual': corr_serie.iloc[-1]
        })
    st.dataframe(pd.DataFrame(stats).round(3),
                  use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("##### 📖 Documentação técnica")
    render_detail_expander("CORR_ROLLING", st)

# --- TAB 3: Diferencial ---
with tab3:
    if "DXY" in cols_idx and "DTWEXBGS" in cols_idx:
        col_chart, col_info = st.columns([3, 1])

        df['diff_corr'] = df['corr_DTWEXBGS'] - df['corr_DXY']

        with col_chart:
            fig_diff = go.Figure()
            fig_diff.add_trace(go.Scatter(
                x=df.index, y=df['diff_corr'],
                fill='tozeroy',
                line=dict(color='#A78BFA', width=2),
                fillcolor='rgba(167, 139, 250, 0.2)',
                name='Diff'
            ))
            fig_diff.add_hline(y=0, line_dash="dash", line_color=COLORS['neutral'])
            fig_diff.update_layout(**PLOTLY_LAYOUT, height=500,
                                    title="Diferencial de Correlação (regime indicator)")
            fig_diff.update_xaxes(**PLOTLY_AXIS)
            fig_diff.update_yaxes(**PLOTLY_AXIS)
            st.plotly_chart(fig_diff, use_container_width=True)

        with col_info:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(render_inline_description("CORR_DIFFERENTIAL"),
                       unsafe_allow_html=True)

        col_a, col_b, col_c, col_d = st.columns(4)
        diff_serie = df['diff_corr'].dropna()
        col_a.metric("Atual", f"{diff_serie.iloc[-1]:+.3f}")
        col_b.metric(f"Média {anos}y", f"{diff_serie.mean():+.3f}")
        col_c.metric("% tempo EM-driven", f"{(diff_serie > 0).mean()*100:.1f}%")
        col_d.metric("Mediana", f"{diff_serie.median():+.3f}")

        st.markdown("---")
        st.markdown("##### 📖 Documentação técnica")
        render_detail_expander("CORR_DIFFERENTIAL", st)
    else:
        st.info("Selecione DXY e DTWEXBGS na sidebar para ver o diferencial.")

# --- TAB 4: Dados ---
with tab4:
    st.dataframe(
        df[['PTAX'] + cols_idx + [f'corr_{i}' for i in cols_idx]].round(4),
        use_container_width=True, height=500
    )
    csv = df.to_csv().encode('utf-8')
    st.download_button(
        "⬇️ Download CSV",
        data=csv,
        file_name=f"brl_fx_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv'
    )

# ============================================================
# FOOTER
# ============================================================
st.markdown(render_footer(), unsafe_allow_html=True)
