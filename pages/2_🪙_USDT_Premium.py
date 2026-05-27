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
st.set_page_config(
    page_title="USDT Premium | BRL Monitor",
    page_icon="🪙",
    layout="wide"
)
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown(
    render_header(
        title="USDT/BRL Premium Monitor",
        subtitle="Premium do USDT em BRL — 4 exchanges spot + P2P Binance vs PTAX",
        sources=["Binance", "Mercado Bitcoin", "Foxbit", "Bitso", "BCB"]
    ),
    unsafe_allow_html=True
)

# ============================================================
# BOTÃO DE REFRESH
# ============================================================
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

# Separa válidas e falhas
valid = [e for e in exchanges_data if 'error' not in e]
failed = [e for e in exchanges_data if 'error' in e]

if not valid:
    st.error("❌ Nenhuma fonte respondeu.")
    st.info("Possível causa: APIs bloqueando IPs de data centers (Streamlit Cloud).")
    st.stop()

# Calcula premium
for ex in valid:
    if ex.get('bid', 0) > 0 and ex.get('ask', 0) > 0:
        ex['premium_bid_pct'] = (ex['bid'] / ptax_value - 1) * 100
        ex['premium_ask_pct'] = (ex['ask'] / ptax_value - 1) * 100
        ex['premium_mid_pct'] = ((ex['bid'] + ex['ask']) / 2 / ptax_value - 1) * 100
        ex['spread_pct'] = (ex['ask'] / ex['bid'] - 1) * 100
    else:
        ex['premium_bid_pct'] = None
        ex['premium_ask_pct'] = None
        ex['premium_mid_pct'] = None
        ex['spread_pct'] = None

# Separa spot e P2P
spot_exchanges = [e for e in valid if 'P2P' not in e['exchange']]
p2p_exchanges = [e for e in valid if 'P2P' in e['exchange']]

# Médias
spot_with_premium = [e for e in spot_exchanges if e['premium_mid_pct'] is not None]
avg_premium_spot = (sum(e['premium_mid_pct'] for e in spot_with_premium) / len(spot_with_premium)) if spot_with_premium else None

avg_premium_p2p = p2p_exchanges[0]['premium_mid_pct'] if p2p_exchanges and p2p_exchanges[0]['premium_mid_pct'] is not None else None

diff_p2p_spot = (avg_premium_p2p - avg_premium_spot) if (avg_premium_p2p is not None and avg_premium_spot is not None) else None

# Melhor bid/ask
valid_with_premium = [e for e in valid if e.get('bid', 0) > 0]
best_bid_ex = max(valid_with_premium, key=lambda e: e['bid']) if valid_with_premium else None
best_ask_ex = min(valid_with_premium, key=lambda e: e['ask']) if valid_with_premium else None

# ============================================================
# KPIs TOPO
# ============================================================
def color_by_premium(p):
    if p is None:
        return COLORS['neutral']
    if p > 2:
        return COLORS['negative']
    if p > 1:
        return COLORS['amber']
    if p > 0:
        return COLORS['neutral']
    return COLORS['positive']


kpi_cols = st.columns(4)

kpi_cols[0].markdown(
    render_kpi(
        f"PTAX ({ptax_date.strftime('%d/%m')})",
        f"R$ {ptax_value:.4f}",
        None,
        border_color=COLORS['ptax']
    ),
    unsafe_allow_html=True
)

kpi_cols[1].markdown(
    render_kpi(
        "Premium Spot Médio",
        f"{avg_premium_spot:+.2f}%" if avg_premium_spot is not None else "—",
        None,
        border_color=color_by_premium(avg_premium_spot)
    ),
    unsafe_allow_html=True
)

kpi_cols[2].markdown(
    render_kpi(
        "Premium P2P Binance",
        f"{avg_premium_p2p:+.2f}%" if avg_premium_p2p is not None else "—",
        None,
        border_color=color_by_premium(avg_premium_p2p)
    ),
    unsafe_allow_html=True
)

kpi_cols[3].markdown(
    render_kpi(
        "Diferencial P2P - Spot",
        f"{diff_p2p_spot:+.2f}pp" if diff_p2p_spot is not None else "—",
        None,
        border_color=COLORS['cyan']
    ),
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# MELHORES OFERTAS
# ============================================================
if best_bid_ex and best_ask_ex:
    col_a, col_b = st.columns(2)
    col_a.markdown(
        render_kpi(
            "🟢 Melhor BID (vender USDT)",
            f"R$ {best_bid_ex['bid']:.4f}",
            None,
            border_color=COLORS['positive']
        ),
        unsafe_allow_html=True
    )
    col_a.caption(f"→ **{best_bid_ex['exchange']}** · premium {best_bid_ex['premium_bid_pct']:+.2f}%")

    col_b.markdown(
        render_kpi(
            "🔵 Melhor ASK (comprar USDT)",
            f"R$ {best_ask_ex['ask']:.4f}",
            None,
            border_color=COLORS['cyan']
        ),
        unsafe_allow_html=True
    )
    col_b.caption(f"→ **{best_ask_ex['exchange']}** · premium {best_ask_ex['premium_ask_pct']:+.2f}%")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# ALERTAS
# ============================================================
if avg_premium_spot is not None:
    if avg_premium_spot > 3:
        st.error(f"🚨 **REGIME DE STRESS:** Premium spot médio em {avg_premium_spot:+.2f}% — sinaliza demanda forte por dólar via cripto. Oportunidade clara de arbitragem.")
    elif avg_premium_spot > 1.5:
        st.warning(f"⚠️ **ATENÇÃO:** Premium spot em {avg_premium_spot:+.2f}% — acima da faixa normal (0,5-1,5%). Monitorar.")
    elif avg_premium_spot < -0.5:
        st.info(f"ℹ️ **OFERTA EXCESSIVA:** Premium em {avg_premium_spot:+.2f}% (negativo). USDT abaixo do PTAX.")

if diff_p2p_spot is not None and diff_p2p_spot > 1.5:
    st.warning(f"⚠️ **STRESS NO P2P:** Diferencial P2P-Spot em {diff_p2p_spot:+.2f}pp — demanda de varejo significativamente acima da institucional. Sinal antecedente.")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3 = st.tabs(["📊 Comparativo", "🤝 P2P Detalhado", "📖 Metodologia"])

# --- TAB 1 ---
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
                    'Vol 24h (USDT)': ex.get('volume_24h', 0),
                })

        if rows_spot:
            df_spot = pd.DataFrame(rows_spot).sort_values('Bid (R$)', ascending=False)
            st.dataframe(
                df_spot.style.format({
                    'Bid (R$)': '{:.4f}',
                    'Ask (R$)': '{:.4f}',
                    'Spread %': '{:+.3f}',
                    'Prem Bid %': '{:+.2f}',
                    'Prem Ask %': '{:+.2f}',
                    'Prem Mid %': '{:+.2f}',
                    'Vol 24h (USDT)': '{:,.0f}',
                }),
                use_container_width=True,
                hide_index=True
            )

        # Gráfico de barras
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
                x=df_chart['premium'],
                y=df_chart['source'],
                orientation='h',
                marker_color=colors_list,
                text=[f"{p:+.2f}%" for p in df_chart['premium']],
                textposition='outside',
            ))
            fig.add_vline(x=0, line_dash="dash", line_color=COLORS['neutral'])
            fig.update_layout(
                **PLOTLY_LAYOUT,
                height=300,
                showlegend=False,
                xaxis_title="Premium vs PTAX (%)",
            )
            fig.update_xaxes(**PLOTLY_AXIS)
            fig.update_yaxes(**PLOTLY_AXIS)
            st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(render_inline_description("USDT_PREMIUM"), unsafe_allow_html=True)

# --- TAB 2 ---
with tab2:
    if p2p_exchanges:
        p2p = p2p_exchanges[0]

        st.markdown("##### Top 5 Ofertas P2P Binance")
        st.caption("Mediana das top 5 ofertas — mais robusta que melhor preço (ignora outliers)")

        col_sell, col_buy = st.columns(2)

        with col_sell:
            st.markdown(f"**🔵 Quem está VENDENDO USDT** _(você compra)_")
            if 'p2p_sell_prices' in p2p:
                df_sell = pd.DataFrame({
                    'Rank': range(1, len(p2p['p2p_sell_prices']) + 1),
                    'Merchant': p2p.get('p2p_sell_merchants', ['—'] * len(p2p['p2p_sell_prices'])),
                    'Preço (R$)': p2p['p2p_sell_prices'],
                    'Premium %': [(p / ptax_value - 1) * 100 for p in p2p['p2p_sell_prices']],
                })
                st.dataframe(
                    df_sell.style.format({
                        'Preço (R$)': '{:.4f}',
                        'Premium %': '{:+.2f}',
                    }),
                    use_container_width=True,
                    hide_index=True
                )

        with col_buy:
            st.markdown(f"**🟢 Quem está COMPRANDO USDT** _(você vende)_")
            if 'p2p_buy_prices' in p2p:
                df_buy = pd.DataFrame({
                    'Rank': range(1, len(p2p['p2p_buy_prices']) + 1),
                    'Merchant': p2p.get('p2p_buy_merchants', ['—'] * len(p2p['p2p_buy_prices'])),
                    'Preço (R$)': p2p['p2p_buy_prices'],
                    'Premium %': [(p / ptax_value - 1) * 100 for p in p2p['p2p_buy_prices']],
                })
                st.dataframe(
                    df_buy.style.format({
                        'Preço (R$)': '{:.4f}',
                        'Premium %': '{:+.2f}',
                    }),
                    use_container_width=True,
                    hide_index=True
                )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(render_inline_description("P2P_VS_SPOT"), unsafe_allow_html=True)
    else:
        st.warning("⚠️ P2P Binance não disponível no momento. Pode ser bloqueio temporário de IP do servidor (data center → Binance).")

# --- TAB 3 ---
with tab3:
    render_detail_expander("USDT_PREMIUM", st)
    render_detail_expander("P2P_VS_SPOT", st)

# ============================================================
# FALHAS
# ============================================================
if failed:
    with st.expander(f"⚠️ {len(failed)} fonte(s) com erro"):
        for f in failed:
            st.text(f"{f.get('exchange', f.get('trade_type', '?'))}: {f['error']}")

# ============================================================
# FOOTER
# ============================================================
st.markdown(render_footer(), unsafe_allow_html=True)
