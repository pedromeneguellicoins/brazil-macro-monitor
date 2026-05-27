"""
Commodities & Termos de Troca — Pilar 3 + 4.
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
from utils.data_loaders import (
    load_ptax, load_yahoo, load_commodity,
    COMMODITY_TICKERS, normalize_to_base100, join_and_align
)
from utils.glossary import render_inline_description, render_detail_expander

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="Commodities | BRL Monitor",
    page_icon="🌾",
    layout="wide"
)
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown(
    render_header(
        title="Commodities & Termos de Troca",
        subtitle="Cestas de exportação e importação do Brasil + impacto no BRL",
        sources=["Yahoo Finance", "BCB SGS"]
    ),
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### ⚙️ Parâmetros")
    anos = st.slider("Anos de histórico", 1, 5, 2)
    janela_corr = st.slider("Janela de correlação (dias)", 10, 90, 30)

# ============================================================
# CARREGAMENTO
# ============================================================
end_date = datetime.today()
start_date = end_date - timedelta(days=anos * 365)

EXPORT_COMMODITIES = ['Brent', 'Soja', 'Minério de Ferro', 'Café Arábica']
IMPORT_COMMODITIES = ['Gasolina', 'Diesel', 'Gás Natural']

with st.spinner("Carregando commodities..."):
    # PTAX
    ptax = load_ptax(start_date, end_date)

    # CNH
    try:
        cnh = load_yahoo('CNH=X', start_date, end_date, col_name='CNH')
        if cnh.empty:
            cnh = load_yahoo('CNY=X', start_date, end_date, col_name='CNH')
    except Exception:
        cnh = pd.DataFrame()

    # Exportações
    exports = {}
    for name in EXPORT_COMMODITIES:
        df_c = load_commodity(name, start_date, end_date)
        if not df_c.empty:
            exports[name] = df_c

    # Importações
    imports = {}
    for name in IMPORT_COMMODITIES:
        df_c = load_commodity(name, start_date, end_date)
        if not df_c.empty:
            imports[name] = df_c

# ============================================================
# CONSTRUÇÃO DO DATAFRAME MESTRE
# ============================================================
# Junta tudo num único DataFrame, alinhado por data
all_series = [ptax]
if not cnh.empty:
    all_series.append(cnh)
for name, df_c in exports.items():
    all_series.append(df_c)
for name, df_c in imports.items():
    all_series.append(df_c)

# Merge
df = all_series[0].copy()
for s in all_series[1:]:
    df = df.join(s, how='outer')

df = df.sort_index().ffill().dropna(subset=['PTAX'])

# ============================================================
# NORMALIZAÇÃO E CESTAS
# ============================================================
# Base = primeiro dia com dados completos
base_date = df.dropna().index.min()

# Normaliza cada commodity (base 100 na primeira data válida)
norm_cols_export = []
for name in exports.keys():
    if name in df.columns:
        col_name = f'{name}_norm'
        df[col_name] = normalize_to_base100(df[name].dropna(), base_date=base_date)
        df[col_name] = df[col_name].reindex(df.index).ffill()
        norm_cols_export.append(col_name)

norm_cols_import = []
for name in imports.keys():
    if name in df.columns:
        col_name = f'{name}_norm'
        df[col_name] = normalize_to_base100(df[name].dropna(), base_date=base_date)
        df[col_name] = df[col_name].reindex(df.index).ffill()
        norm_cols_import.append(col_name)

# Cesta de exportação = média dos normalizados
if norm_cols_export:
    df['Cesta_Export'] = df[norm_cols_export].mean(axis=1)
if norm_cols_import:
    df['Cesta_Import'] = df[norm_cols_import].mean(axis=1)

# Termos de Troca
if 'Cesta_Export' in df.columns and 'Cesta_Import' in df.columns:
    df['Terms_of_Trade'] = (df['Cesta_Export'] / df['Cesta_Import']) * 100

# PTAX normalizada (pra comparar com TT no mesmo eixo)
df['PTAX_norm'] = normalize_to_base100(df['PTAX'].dropna(), base_date=base_date)
df['PTAX_norm'] = df['PTAX_norm'].reindex(df.index).ffill()

df = df.dropna(subset=['PTAX'])

# Correlações PTAX vs commodities
df['ret_ptax'] = df['PTAX'].pct_change()
for name in list(exports.keys()) + list(imports.keys()):
    if name in df.columns:
        df[f'ret_{name}'] = df[name].pct_change()
        df[f'corr_{name}'] = df['ret_ptax'].rolling(janela_corr).corr(df[f'ret_{name}'])

# Correlação PTAX vs Termos de Troca
if 'Terms_of_Trade' in df.columns:
    df['ret_TT'] = df['Terms_of_Trade'].pct_change()
    df['corr_TT_PTAX'] = df['ret_ptax'].rolling(janela_corr).corr(df['ret_TT'])

# ============================================================
# KPIs TOPO
# ============================================================
kpi_cols = st.columns(4)

# PTAX
ptax_now = df['PTAX'].iloc[-1]
ptax_chg = (df['PTAX'].iloc[-1] / df['PTAX'].iloc[-2] - 1) * 100 if len(df) > 1 else 0
kpi_cols[0].markdown(
    render_kpi("PTAX", f"R$ {ptax_now:.4f}", ptax_chg, border_color=COLORS['ptax']),
    unsafe_allow_html=True
)

# Termos de Troca
if 'Terms_of_Trade' in df.columns:
    tt_now = df['Terms_of_Trade'].iloc[-1]
    tt_30d = df['Terms_of_Trade'].iloc[-30] if len(df) > 30 else tt_now
    tt_chg = (tt_now / tt_30d - 1) * 100
    tt_color = COLORS['positive'] if tt_now > 100 else COLORS['negative']
    kpi_cols[1].markdown(
        render_kpi("Termos de Troca", f"{tt_now:.1f}", tt_chg, border_color=tt_color),
        unsafe_allow_html=True
    )
else:
    kpi_cols[1].markdown(render_kpi("Termos de Troca", "—", None, border_color=COLORS['neutral']), unsafe_allow_html=True)

# Cesta Export
if 'Cesta_Export' in df.columns:
    ce_now = df['Cesta_Export'].iloc[-1]
    ce_30d = df['Cesta_Export'].iloc[-30] if len(df) > 30 else ce_now
    ce_chg = (ce_now / ce_30d - 1) * 100
    kpi_cols[2].markdown(
        render_kpi("Cesta Exportação", f"{ce_now:.1f}", ce_chg, border_color=COLORS['commodities']),
        unsafe_allow_html=True
    )

# Cesta Import
if 'Cesta_Import' in df.columns:
    ci_now = df['Cesta_Import'].iloc[-1]
    ci_30d = df['Cesta_Import'].iloc[-30] if len(df) > 30 else ci_now
    ci_chg = (ci_now / ci_30d - 1) * 100
    kpi_cols[3].markdown(
        render_kpi("Cesta Importação", f"{ci_now:.1f}", ci_chg, border_color=COLORS['amber']),
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📤 Exportações", "📥 Importações", "🇨🇳 CNH",
    "⚖️ Termos de Troca", "📖 Metodologia"
])

# Cores
COLOR_MAP = {
    'Brent': '#000000',  # vai mudar (preto não dá no tema dark)
    'Soja': '#90BE6D',
    'Minério de Ferro': '#A0522D',
    'Café Arábica': '#6F4E37',
    'Gasolina': '#FFA500',
    'Diesel': '#FF4500',
    'Gás Natural': '#00BFFF',
}
# Ajuste Brent pra tema dark
COLOR_MAP['Brent'] = '#FFD700'  # dourado

# --- TAB 1: EXPORTAÇÕES ---
with tab1:
    col_chart, col_info = st.columns([3, 1])

    with col_chart:
        n_cmd = len(exports)
        if n_cmd > 0:
            fig = make_subplots(
                rows=n_cmd, cols=1, shared_xaxes=True,
                subplot_titles=list(exports.keys()),
                vertical_spacing=0.06
            )
            for i, name in enumerate(exports.keys()):
                if name in df.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=df.index, y=df[name],
                            name=name,
                            line=dict(color=COLOR_MAP.get(name, '#FFA500'), width=2),
                        ),
                        row=i+1, col=1
                    )
                    unit = COMMODITY_TICKERS[name]['unit']
                    fig.update_yaxes(title_text=unit, row=i+1, col=1)

            fig.update_layout(**PLOTLY_LAYOUT, height=200*n_cmd, showlegend=False)
            fig.update_xaxes(**PLOTLY_AXIS)
            fig.update_yaxes(**PLOTLY_AXIS)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Nenhuma commodity de exportação carregou.")

    with col_info:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(render_inline_description("COMMODITIES_EXPORT"), unsafe_allow_html=True)

    # Correlações
    st.markdown("##### 🔗 Correlação rolling com PTAX")
    fig_corr = go.Figure()
    for name in exports.keys():
        corr_col = f'corr_{name}'
        if corr_col in df.columns:
            fig_corr.add_trace(go.Scatter(
                x=df.index, y=df[corr_col],
                name=name,
                line=dict(color=COLOR_MAP.get(name, '#888'), width=2)
            ))
    fig_corr.add_hline(y=0, line_dash="dash", line_color=COLORS['neutral'], opacity=0.5)
    fig_corr.update_layout(**PLOTLY_LAYOUT, height=350,
                            title=f"Correlação {janela_corr}d (retornos)")
    fig_corr.update_xaxes(**PLOTLY_AXIS)
    fig_corr.update_yaxes(**PLOTLY_AXIS, range=[-1, 1])
    st.plotly_chart(fig_corr, use_container_width=True)
    st.caption("Correlações **negativas** são esperadas: quando a commodity sobe (preço em USD), o BRL aprecia (PTAX cai).")

# --- TAB 2: IMPORTAÇÕES ---
with tab2:
    col_chart, col_info = st.columns([3, 1])

    with col_chart:
        n_cmd = len(imports)
        if n_cmd > 0:
            fig = make_subplots(
                rows=n_cmd, cols=1, shared_xaxes=True,
                subplot_titles=list(imports.keys()),
                vertical_spacing=0.06
            )
            for i, name in enumerate(imports.keys()):
                if name in df.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=df.index, y=df[name],
                            name=name,
                            line=dict(color=COLOR_MAP.get(name, '#FFA500'), width=2),
                        ),
                        row=i+1, col=1
                    )
                    unit = COMMODITY_TICKERS[name]['unit']
                    fig.update_yaxes(title_text=unit, row=i+1, col=1)

            fig.update_layout(**PLOTLY_LAYOUT, height=200*n_cmd, showlegend=False)
            fig.update_xaxes(**PLOTLY_AXIS)
            fig.update_yaxes(**PLOTLY_AXIS)
            st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(render_inline_description("COMMODITIES_IMPORT"), unsafe_allow_html=True)

    # Correlações
    st.markdown("##### 🔗 Correlação rolling com PTAX")
    fig_corr = go.Figure()
    for name in imports.keys():
        corr_col = f'corr_{name}'
        if corr_col in df.columns:
            fig_corr.add_trace(go.Scatter(
                x=df.index, y=df[corr_col],
                name=name,
                line=dict(color=COLOR_MAP.get(name, '#888'), width=2)
            ))
    fig_corr.add_hline(y=0, line_dash="dash", line_color=COLORS['neutral'], opacity=0.5)
    fig_corr.update_layout(**PLOTLY_LAYOUT, height=350,
                            title=f"Correlação {janela_corr}d (retornos)")
    fig_corr.update_xaxes(**PLOTLY_AXIS)
    fig_corr.update_yaxes(**PLOTLY_AXIS, range=[-1, 1])
    st.plotly_chart(fig_corr, use_container_width=True)
    st.caption("Correlações **positivas** são esperadas: quando custo de importação sobe, BRL deprecia (PTAX sobe).")

# --- TAB 3: CNH ---
with tab3:
    if 'CNH' in df.columns and not df['CNH'].dropna().empty:
        col_chart, col_info = st.columns([3, 1])

        with col_chart:
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                subplot_titles=["CNH/USD (Yuan offshore)", "Cesta de Exportação Brasileira"],
                                vertical_spacing=0.1)
            fig.add_trace(
                go.Scatter(x=df.index, y=df['CNH'], name='CNH',
                           line=dict(color=COLORS['cnh'], width=2)),
                row=1, col=1
            )
            if 'Cesta_Export' in df.columns:
                fig.add_trace(
                    go.Scatter(x=df.index, y=df['Cesta_Export'], name='Cesta Export',
                               line=dict(color=COLORS['commodities'], width=2)),
                    row=2, col=1
                )
            fig.update_layout(**PLOTLY_LAYOUT, height=500, showlegend=False)
            fig.update_xaxes(**PLOTLY_AXIS)
            fig.update_yaxes(**PLOTLY_AXIS)
            st.plotly_chart(fig, use_container_width=True)

            # Correlação CNH vs Cesta Export
            if 'Cesta_Export' in df.columns:
                df['ret_cnh'] = df['CNH'].pct_change()
                df['ret_cesta'] = df['Cesta_Export'].pct_change()
                df['corr_cnh_cesta'] = df['ret_cnh'].rolling(janela_corr).corr(df['ret_cesta'])

                fig_c = go.Figure(go.Scatter(
                    x=df.index, y=df['corr_cnh_cesta'],
                    name='Corr CNH × Cesta Export',
                    line=dict(color=COLORS['cnh'], width=2)
                ))
                fig_c.add_hline(y=0, line_dash="dash", line_color=COLORS['neutral'])
                fig_c.update_layout(**PLOTLY_LAYOUT, height=300,
                                    title=f"Correlação CNH × Cesta de Exportação ({janela_corr}d)")
                fig_c.update_xaxes(**PLOTLY_AXIS)
                fig_c.update_yaxes(**PLOTLY_AXIS, range=[-1, 1])
                st.plotly_chart(fig_c, use_container_width=True)

        with col_info:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(render_inline_description("CNH"), unsafe_allow_html=True)
    else:
        st.warning("Dados de CNH não disponíveis no momento.")

# --- TAB 4: TERMOS DE TROCA (estrela) ---
with tab4:
    if 'Terms_of_Trade' not in df.columns:
        st.warning("Dados insuficientes para calcular Termos de Troca.")
    else:
        col_chart, col_info = st.columns([3, 1])

        with col_chart:
            # Gráfico 1: Cesta Exp vs Cesta Imp
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=df.index, y=df['Cesta_Export'], name='Cesta Exportação',
                line=dict(color=COLORS['commodities'], width=2)
            ))
            fig1.add_trace(go.Scatter(
                x=df.index, y=df['Cesta_Import'], name='Cesta Importação',
                line=dict(color=COLORS['amber'], width=2)
            ))
            fig1.add_hline(y=100, line_dash="dash", line_color=COLORS['neutral'],
                            annotation_text="Base 100")
            fig1.update_layout(**PLOTLY_LAYOUT, height=350,
                                title="Cestas Normalizadas (base 100 no início do período)")
            fig1.update_xaxes(**PLOTLY_AXIS)
            fig1.update_yaxes(**PLOTLY_AXIS)
            st.plotly_chart(fig1, use_container_width=True)

            # Gráfico 2: Termos de Troca vs PTAX (eixos separados)
            fig2 = make_subplots(specs=[[{"secondary_y": True}]])
            fig2.add_trace(
                go.Scatter(x=df.index, y=df['Terms_of_Trade'],
                           name='Termos de Troca', line=dict(color=COLORS['ptax'], width=2.5)),
                secondary_y=False
            )
            fig2.add_trace(
                go.Scatter(x=df.index, y=df['PTAX'],
                           name='PTAX', line=dict(color=COLORS['dxy'], width=2)),
                secondary_y=True
            )
            fig2.add_hline(y=100, line_dash="dash", line_color=COLORS['neutral'])
            fig2.update_layout(**PLOTLY_LAYOUT, height=450,
                                title="Termos de Troca vs PTAX (eixo secundário)")
            fig2.update_xaxes(**PLOTLY_AXIS)
            fig2.update_yaxes(title_text="Termos de Troca", secondary_y=False, gridcolor=COLORS['border'])
            fig2.update_yaxes(title_text="PTAX", secondary_y=True, gridcolor=COLORS['border'])
            st.plotly_chart(fig2, use_container_width=True)

            # Gráfico 3: Correlação rolling TT vs PTAX
            if 'corr_TT_PTAX' in df.columns:
                fig3 = go.Figure(go.Scatter(
                    x=df.index, y=df['corr_TT_PTAX'],
                    name='Corr TT × PTAX',
                    fill='tozeroy',
                    line=dict(color='#A78BFA', width=2),
                    fillcolor='rgba(167, 139, 250, 0.15)',
                ))
                fig3.add_hline(y=0, line_dash="dash", line_color=COLORS['neutral'])
                fig3.update_layout(**PLOTLY_LAYOUT, height=300,
                                    title=f"Correlação rolling {janela_corr}d: Termos de Troca × PTAX")
                fig3.update_xaxes(**PLOTLY_AXIS)
                fig3.update_yaxes(**PLOTLY_AXIS, range=[-1, 1])
                st.plotly_chart(fig3, use_container_width=True)
                st.caption("⚠️ Correlação **negativa** é o esperado: TT sobe → BRL aprecia (PTAX cai).")

        with col_info:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(render_inline_description("TERMS_OF_TRADE"), unsafe_allow_html=True)

        # Estatísticas
        st.markdown("##### 📊 Estatísticas do Período")
        tt_serie = df['Terms_of_Trade'].dropna()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("TT Atual", f"{tt_serie.iloc[-1]:.1f}")
        c2.metric("TT Média", f"{tt_serie.mean():.1f}")
        c3.metric("TT Máx", f"{tt_serie.max():.1f}")
        c4.metric("TT Mín", f"{tt_serie.min():.1f}")

        if 'corr_TT_PTAX' in df.columns:
            corr_now = df['corr_TT_PTAX'].iloc[-1]
            corr_mean = df['corr_TT_PTAX'].dropna().mean()
            c5, c6 = st.columns(2)
            c5.metric(f"Corr TT×PTAX Atual ({janela_corr}d)", f"{corr_now:+.3f}")
            c6.metric("Corr TT×PTAX Média Período", f"{corr_mean:+.3f}")

# --- TAB 5: METODOLOGIA ---
with tab5:
    render_detail_expander("COMMODITIES_EXPORT", st)
    render_detail_expander("COMMODITIES_IMPORT", st)
    render_detail_expander("TERMS_OF_TRADE", st)

# ============================================================
# FOOTER
# ============================================================
st.markdown(render_footer(), unsafe_allow_html=True)
