"""
USDT/BRL Premium Monitor — Pilar 1.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

from utils.styling import (
    COLORS, PLOTLY_LAYOUT, PLOTLY_AXIS,
    get_custom_css, render_header, render_footer, render_kpi
)
from utils.data_loaders import load_ptax, load_all_usdt_brl_with_p2p
from utils.glossary import render_inline_description, render_detail_expander

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(page_title="USDT Premium | BRL Monitor", page_icon="🪙", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown(
    render_header(
        title="USDT/BRL Premium Monitor",
        subtitle="Premium do USDT em BRL — exchanges spot vs PTAX",
        sources=["Mercado Bitcoin", "Foxbit", "Bitso", "NovaDAX", "OKX", "BCB"]
    ),
    unsafe_allow_html=True
)

col_refresh, _ = st.columns([1, 5])
if col_refresh.button("🔄 Atualizar agora"):
    st.cache_data.clear()
    st.rerun()

# ============================================================
# CARREGAMENTO
# ============================================================
@st.cache_data(ttl=3600)
def get_ptax_latest():
    end = datetime.today()
    start = end - timedelta(days=10)
    ptax = load_ptax(start, end)
    if ptax.empty:
        return None, None
    return ptax['PTAX'].iloc[-1], ptax.index[-1]


with st.spinner("Carregando preços ao vivo..."):
    ptax_value, ptax_date = get_ptax_latest()
    exchanges_data = load_all_usdt_brl_with_p2p()

if ptax_value is None:
    st.error("❌ Não foi possível carregar PTAX.")
    st.stop()

valid = [e for e in exchanges_data if 'error' not in e]
failed = [e for e in exchanges_data if 'error' in e]

if not valid:
    st.error("❌ Nenhuma fonte respondeu.")
    st.stop()

for ex in valid:
    if ex.get('bid', 0) > 0 and ex.get('ask', 0) > 0:
        ex['premium_bid_pct'] = (ex['bid'] / ptax_value - 1) * 100
        ex['premium_ask_pct'] = (ex['ask'] / ptax_value - 1) * 100
        ex['premium_mid_pct'] = ((ex['bid'] + ex['ask']) / 2 / ptax_value - 1) * 100
        ex['spread_pct'] = (ex['ask'] / ex['bid'] - 1) * 100
    else:
        ex['premium_bid_pct'] = ex['premium_ask_pct'] = ex['premium_mid_pct'] = ex['spread_pct'] = None

spot_exchanges = [e for e in valid if 'P2P' not in e['exchange']]
p2p_exchanges = [e for e in valid if 'P2P' in e['exchange']]

spot_with_premium = [e for e in spot_exchanges if e['premium_mid_pct'] is not None]
avg_premium_spot = (sum(e['premium_mid_pct'] for e in spot_with_premium) / len(spot_with_premium)) if spot_with_premium else None

avg_premium_p2p = p2p_exchanges[0]['premium_mid_pct'] if p2p_exchanges and p2p_exchanges[0].get('premium_mid_pct') is not None else None
diff_p2p_spot = (avg_premium_p2p - avg_premium_spot) if (avg_premium_p2p is not None and avg_premium_spot is not None) else None

valid_with_premium = [e for e in valid if e.get('bid', 0) > 0]
best_bid_ex = max(valid_with_premium, key=lambda e: e['bid']) if valid_with_premium else None
best_ask_ex = min(valid_with_premium, key=lambda e: e['ask']) if valid_with_premium else None

# ============================================================
# KPIs
# ============================================================
def color_by_premium(p):
    if p is None: return COLORS['neutral']
    if p > 2: return COLORS['negative']
    if p > 1: return COLORS['amber']
    if p > 0: return COLORS['neutral']
    return COLORS['positive']

kpi_cols = st.columns(4)
kpi_cols[0].markdown(render_kpi(f"PTAX ({ptax_date.strftime('%d/%m')})", f"R$ {ptax_value:.4f}", None, border_color=COLORS['ptax']), unsafe_allow_html=True)
kpi_cols[1].markdown(render_kpi("Premium Spot Médio", f"{avg_premium_spot:+.2f}%" if avg_premium_spot is not None else "—", None, border_color=color_by_premium(avg_premium_spot)), unsafe_allow_html=True)
kpi_cols[2].markdown(render_kpi("Premium P2P", f"{avg_premium_p2p:+.2f}%" if avg_premium_p2p is not None else "—", None, border_color=color_by_premium(avg_premium_p2p)), unsafe_allow_html=True)
kpi_cols[3].markdown(render_kpi("Diferencial P2P-Spot", f"{diff_p2p_spot:+.2f}pp" if diff_p2p_spot is not None else "—", None, border_color=COLORS['cyan']), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# MELHORES OFERTAS + PRÊMIO BID-ASK
# ============================================================
if best_bid_ex and best_ask_ex:
    # Layout: bid | chip arbitragem | ask
    col_a, col_mid, col_b = st.columns([1, 0.7, 1])

    col_a.markdown(render_kpi("🟢 Melhor BID (vender USDT)", f"R$ {best_bid_ex['bid']:.4f}", None, border_color=COLORS['positive']), unsafe_allow_html=True)
    col_a.caption(f"→ **{best_bid_ex['exchange']}** · premium {best_bid_ex['premium_bid_pct']:+.2f}%")

    # Prêmio entre melhor bid e melhor ask, em bps
    # bid - ask: se positivo, há arbitragem cross-exchange (compra no ask, vende no bid)
    with col_mid:
        spread_bps = (best_bid_ex['bid'] / best_ask_ex['ask'] - 1) * 10000
        if spread_bps > 0:
            chip_color = COLORS['positive']
            chip_label = "ARBITRAGEM"
            chip_hint = "bid > ask cross-exchange"
            arrow = "▲"
        else:
            chip_color = COLORS['negative']
            chip_label = "SPREAD"
            chip_hint = "mercado normal"
            arrow = "▼"
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="
            background-color: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-top: 2px solid {chip_color};
            padding: 0.6rem 0.8rem; text-align: center;
            font-family: 'JetBrains Mono', monospace;
        ">
            <span style="color: {COLORS['text_dim']}; font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.1em;">{chip_label} BID−ASK</span><br>
            <span style="color: {chip_color}; font-size: 1.2rem; font-weight: 700;">{arrow} {spread_bps:+.1f} bps</span><br>
            <span style="color: {COLORS['text_dim']}; font-size: 0.58rem;">{chip_hint}</span>
        </div>
        """, unsafe_allow_html=True)

    col_b.markdown(render_kpi("🔵 Melhor ASK (comprar USDT)", f"R$ {best_ask_ex['ask']:.4f}", None, border_color=COLORS['cyan']), unsafe_allow_html=True)
    col_b.caption(f"→ **{best_ask_ex['exchange']}** · premium {best_ask_ex['premium_ask_pct']:+.2f}%")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# ALERTAS
# ============================================================
if avg_premium_spot is not None:
    if avg_premium_spot > 3:
        st.error(f"🚨 **REGIME DE STRESS:** Premium spot médio em {avg_premium_spot:+.2f}% — demanda forte por dólar via cripto. Oportunidade de arbitragem.")
    elif avg_premium_spot > 1.5:
        st.warning(f"⚠️ **ATENÇÃO:** Premium spot em {avg_premium_spot:+.2f}% — acima da faixa normal (0,5-1,5%).")
    elif avg_premium_spot < -0.5:
        st.info(f"ℹ️ **OFERTA EXCESSIVA:** Premium em {avg_premium_spot:+.2f}% (negativo). USDT abaixo do PTAX.")

# Alerta de arbitragem cross-exchange
if best_bid_ex and best_ask_ex:
    arb_bps = (best_bid_ex['bid'] / best_ask_ex['ask'] - 1) * 10000
    if arb_bps > 0:
        st.error(f"🎯 **ARBITRAGEM CROSS-EXCHANGE:** Melhor bid ({best_bid_ex['exchange']} R$ {best_bid_ex['bid']:.4f}) está ACIMA do melhor ask ({best_ask_ex['exchange']} R$ {best_ask_ex['ask']:.4f}) — spread de {arb_bps:.1f} bps. Comprar no ask e vender no bid = lucro bruto (antes de custos/taxas/transferência).")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3 = st.tabs(["📊 Comparativo", "🤝 P2P Detalhado", "📖 Metodologia"])

with tab1:
    col_table, col_info = st.columns([3, 1])
    with col_table:
        st.markdown("##### Spot — Exchange Order Books")
        rows_spot = []
        for ex in spot_exchanges:
            if ex.get('premium_mid_pct') is not None:
                rows_spot.append({
                    'Exchange': ex['exchange'],
                    'Bid (R$)': ex['bid'],
                    'Ask (R$)': ex['ask'],
                    'Spread %': ex['spread_pct'],
                    'Prem Bid %': ex['premium_bid_pct'],
                    'Prem Ask %': ex['premium_ask_pct'],
                    'Prem Mid %': ex['premium_mid_pct'],
                    'Vol 24h (USDT)': ex.get('volume_24h', 0) if ex.get('volume_24h', 0) > 0 else None,
                })
        if rows_spot:
            df_spot = pd.DataFrame(rows_spot).sort_values('Bid (R$)', ascending=False)
            st.dataframe(
                df_spot.style.format({
                    'Bid (R$)': '{:.4f}', 'Ask (R$)': '{:.4f}', 'Spread %': '{:+.3f}',
                    'Prem Bid %': '{:+.2f}', 'Prem Ask %': '{:+.2f}', 'Prem Mid %': '{:+.2f}',
                    'Vol 24h (USDT)': lambda x: '{:,.0f}'.format(x) if pd.notna(x) and x > 0 else '—',
                }),
                use_container_width=True, hide_index=True
            )

        st.markdown("##### Premium Mid por Fonte")
        all_premiums = []
        for ex in spot_exchanges:
            if ex.get('premium_mid_pct') is not None:
                all_premiums.append({'source': ex['exchange'], 'premium': ex['premium_mid_pct'], 'type': 'Spot'})
        for ex in p2p_exchanges:
            if ex.get('premium_mid_pct') is not None:
                all_premiums.append({'source': ex['exchange'], 'premium': ex['premium_mid_pct'], 'type': 'P2P'})
        if all_premiums:
            df_chart = pd.DataFrame(all_premiums).sort_values('premium')
            colors_list = [COLORS['amber'] if t == 'P2P' else COLORS['cyan'] for t in df_chart['type']]
            fig = go.Figure(go.Bar(
                x=df_chart['premium'], y=df_chart['source'], orientation='h',
                marker_color=colors_list,
                text=[f"{p:+.2f}%" for p in df_chart['premium']], textposition='outside',
            ))
            fig.add_vline(x=0, line_dash="dash", line_color=COLORS['neutral'])
            fig.update_layout(**PLOTLY_LAYOUT, height=300, showlegend=False, xaxis_title="Premium vs PTAX (%)")
            fig.update_xaxes(**PLOTLY_AXIS)
            fig.update_yaxes(**PLOTLY_AXIS)
            st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(render_inline_description("USDT_PREMIUM"), unsafe_allow_html=True)

with tab2:
    st.info("""
    **P2P Binance temporariamente indisponível neste ambiente.**

    A Binance bloqueia requisições de data centers internacionais (erro HTTP 451 — geo-restrição), incluindo o IP do Streamlit Cloud.

    **Alternativas:** acessar diretamente o [P2P Binance](https://p2p.binance.com/pt-BR/trade/all-payments/USDT?fiat=BRL) ou rodar localmente.
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(render_inline_description("P2P_VS_SPOT"), unsafe_allow_html=True)

with tab3:
    render_detail_expander("USDT_PREMIUM", st)
    render_detail_expander("P2P_VS_SPOT", st)

# ============================================================
# DEBUG
# ============================================================
with st.expander("🔧 Status das fontes de dados"):
    st.caption("Status de conexão com cada exchange")
    for ex in exchanges_data:
        ex_name = ex.get('exchange', ex.get('trade_type', '?'))
        if 'error' in ex:
            st.text(f"❌ {ex_name}: {ex['error']}")
        else:
            debug = ex.get('debug_source', 'endpoint padrão')
            partial = ' [DADOS PARCIAIS]' if ex.get('partial_data') else ''
            st.text(f"✅ {ex_name}: {debug}{partial}")

st.markdown(render_footer(), unsafe_allow_html=True)
