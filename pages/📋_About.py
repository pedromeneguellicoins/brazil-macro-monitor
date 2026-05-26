"""
About — Metodologia, fontes, limitações.
"""
import streamlit as st
from utils.styling import get_custom_css, render_header, render_footer

st.set_page_config(page_title="About | BRL Monitor", page_icon="📋", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown(
    render_header(
        title=" About",
        subtitle="Metodologia, fontes de dados e limitações",
        sources=["Documentação técnica"]
    ),
    unsafe_allow_html=True
)

st.markdown("""
## O que é este monitor

**BRL Macro Monitor** é uma ferramenta de monitoramento contextual de drivers macroeconômicos do real brasileiro (BRL). Foi construída com fontes públicas e gratuitas, com foco em apoiar análise pré-cotação e construção de narrativa de mercado.

Não é um sistema de decisão automatizada nem substitui análise fundamental. É **infraestrutura de apoio à conversa de mercado**.

## Fontes de dados

| Fonte | O que fornece | Latência | Custo |
|---|---|---|---|
| **BCB SGS** | PTAX (USD/BRL), Selic, CDI, séries macro Brasil | D-0 (final do dia) | Gratuito |
| **Yahoo Finance** | DXY, CNH, VIX, commodities (iron ore, soja, Brent) | 15 min delay | Gratuito |
| **FRED** | DTWEXBGS, Fed Funds, UST yields, séries macro EUA | D-1 (semanal em alguns casos) | Gratuito (com API key) |
| **Exchanges públicas** | Preços USDT/BRL (Binance, Mercado Bitcoin, Foxbit) | Tempo real | Gratuito |

## Metodologia

### Correlação rolling
Calculada sobre **retornos percentuais** (não preços), em janelas configuráveis (padrão 30 dias). Retornos resolvem o problema de não-estacionariedade de séries de preço.

### Identificação de regimes
- Diferencial de correlação `corr(PTAX, DTWEXBGS) − corr(PTAX, DXY)` indica se o BRL está sendo movido por fatores G10 vs EM/China.
- Z-score (em versões futuras) normaliza desvios da média histórica.

### Forward-fill
Séries com calendários diferentes (PTAX diário, DTWEXBGS semanal) são alinhadas por forward-fill nos índices não-PTAX.

## Limitações

- **Não inclui CDS puro** (Bloomberg only). Usado proxy via spread NTN-B/UST quando disponível.
- **Sem vol implícita de opções FX** (CME/B3 only via fontes pagas).
- **Latência de fechamento**, não tempo real intradiário.
- **Dependência de APIs externas** — se BCB, Yahoo ou FRED estiverem fora, a página afetada não carrega.

## Contato

Construído por **Pedro Meneguelli** · FX/Crypto OTC Trader · pedromeneguelli@hotmail.com
""")

st.markdown(render_footer(), unsafe_allow_html=True)
