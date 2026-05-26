"""
Glossário centralizado — definições e contexto de cada indicador.
Quando adicionar nova métrica ao app, registra aqui.

Estrutura de cada entrada:
- short: 1-2 linhas pra caixa lateral ao gráfico
- detail: explicação completa pro expander "Saiba mais"
- why: por que esse indicador importa pra o BRL
- source: fonte e periodicidade
"""

GLOSSARY = {
    # ============================================================
    # FX & MOEDAS
    # ============================================================
    "PTAX": {
        "title": "PTAX (BRL/USD)",
        "short": "Taxa oficial de câmbio USD/BRL divulgada pelo Banco Central. É a referência para liquidação de contratos cambiais e indexação de derivativos no Brasil.",
        "detail": """
A **PTAX** é a média ponderada das cotações de compra e venda do dólar praticadas no mercado interbancário brasileiro, calculada e divulgada pelo Banco Central do Brasil em 4 boletins ao longo do dia (10h, 11h, 12h, 13h) mais o fechamento.

A PTAX usada como referência neste monitor é a **PTAX venda** (série 1 do BCB SGS), que é o valor padrão para liquidação de NDFs (Non-Deliverable Forwards), contratos cambiais e operações estruturadas no Brasil.

**Características técnicas:**
- Calculada apenas em dias úteis (calendário B3)
- Não inclui movimentos intradiários após o último boletim
- Pode divergir do "dólar comercial" cotado pelas mesas no fim do dia
        """,
        "why": "É o preço de referência para qualquer hedge cambial estruturado no Brasil. Toda análise de regime do real começa aqui.",
        "source": "BCB SGS · Série 1 · Diária (D+0)",
    },

    "DXY": {
        "title": "DXY — US Dollar Index",
        "short": "Índice que mede o dólar contra 6 moedas de economias desenvolvidas (EUR, JPY, GBP, CAD, SEK, CHF). É 57% EUR/USD invertido.",
        "detail": """
O **DXY** (ICE U.S. Dollar Index) é o índice mais antigo e popular de força do dólar americano. Foi criado em 1973 pelo Fed após o fim do Bretton Woods.

**Composição (pesos fixos):**
- EUR: 57,6%
- JPY: 13,6%
- GBP: 11,9%
- CAD: 9,1%
- SEK: 4,2%
- CHF: 3,6%

**Limitação para análise de emergentes:** O DXY foi desenhado em 1973 e não inclui nenhuma moeda asiática emergente (sem CNY, sem INR, sem MXN, sem BRL). Para BRL, é apenas um indicador parcial — útil pra capturar movimento "macro global do dólar", mas insuficiente sozinho.

**Quando subir:** geralmente reflete Fed mais hawkish, fuga pra dólar (safe haven), ou crise no G10 (Europa/Japão).
        """,
        "why": "Termômetro de força do dólar globalmente. Quando DXY sobe, emergentes em geral apanham — mas o BRL pode se descolar se houver fator local dominante.",
        "source": "Yahoo Finance · DX-Y.NYB · Diária",
    },

    "DTWEXBGS": {
        "title": "DTWEXBGS — Trade-Weighted Broad Dollar Index",
        "short": "Índice do Fed que mede o dólar contra 26 moedas, ponderado por volume de comércio dos EUA. Inclui CNY e outras moedas emergentes — mais relevante para o BRL que o DXY.",
        "detail": """
O **DTWEXBGS** (Trade-Weighted Broad Dollar Index – Goods and Services) é mantido pelo Federal Reserve e oferece uma medida muito mais completa da força do dólar que o DXY tradicional.

**Diferenças cruciais para o DXY:**
- Inclui 26 moedas (vs 6 do DXY)
- Inclui **CNY (yuan chinês)**, ausente no DXY
- Inclui MXN, KRW, INR, BRL, e outras emergentes
- Pesos ajustados anualmente conforme fluxo comercial real dos EUA

**Por que é mais relevante para o BRL:**
A China é o maior parceiro comercial do Brasil. Quando o yuan se enfraquece, ativos brasileiros tendem a sofrer junto — esse canal não é capturado pelo DXY mas está no DTWEXBGS.

**Limitação:** atualização semanal (sextas-feiras), não diária. Por isso fazemos forward-fill nos dias úteis intermediários.
        """,
        "why": "Para análise de moedas emergentes, especialmente BRL, é um indicador estruturalmente mais informativo que o DXY clássico — captura a perna asiática/emergente do dólar.",
        "source": "FRED · Série DTWEXBGS · Semanal (sextas)",
    },

    "CNH": {
        "title": "CNH — Yuan Offshore (Hong Kong)",
        "short": "Yuan negociado fora da China continental (em Hong Kong). Mais sensível a fluxos de mercado que o yuan onshore (CNY), e o principal driver China-side do BRL.",
        "detail": """
O **CNH** é o yuan chinês negociado em mercados offshore (principalmente Hong Kong). É diferente do **CNY**, que é negociado dentro da China continental e tem banda de flutuação controlada pelo PBoC (banco central chinês).

**Por que CNH e não CNY:**
- CNH flutua livremente (CNY tem banda diária de ±2%)
- CNH reflete o que estrangeiros estão dispostos a pagar pelo yuan
- Quando o spread CNH-CNY se abre, é sinal de pressão de mercado contra a política do PBoC

**Por que importa pro BRL:**
China é o maior comprador de commodities brasileiras (minério, soja, carne). Quando o yuan enfraquece:
1. Commodities cotadas em USD ficam mais caras pra China
2. China reduz importações ou pressiona por preços menores
3. Termos de troca do Brasil pioram → BRL deprecia

O canal CNH→BRL pode ser observado historicamente com defasagem de poucos dias durante stress.
        """,
        "why": "Quando o yuan offshore enfraquece, BRL geralmente segue dentro de dias — é um indicador antecedente útil para movimentos de moedas emergentes commodity-exporters.",
        "source": "Yahoo Finance · CNH=X · Diária",
    },

    "VIX": {
        "title": "VIX — Índice de Volatilidade Implícita do S&P 500",
        "short": "Mede a volatilidade implícita das opções do S&P 500 nos próximos 30 dias. É o termômetro global de apetite por risco — sobe em momentos de stress e cai em períodos calmos.",
        "detail": """
O **VIX** (CBOE Volatility Index) é calculado a partir dos prêmios das opções de S&P 500 e representa a volatilidade implícita esperada nos próximos 30 dias.

**Faixas de referência (regimes históricos):**
- **VIX < 15:** mercado calmo, "risk-on" — bom para carry trade em moedas emergentes
- **VIX 15–20:** normal
- **VIX 20–30:** stress moderado — emergentes começam a apanhar
- **VIX > 30:** crise — fuga pra dólar e ativos seguros, EMs em queda forte
- **VIX > 50:** pânico — eventos como COVID (mar/2020), Lehman (2008)

**Limitação:** mede apenas vol implícita americana. Choques idiossincráticos brasileiros (fiscal, político) não aparecem no VIX, mas movem o BRL.
        """,
        "why": "Quando o VIX sobe, capital flui pra dólar e Treasuries — moedas emergentes incluindo BRL apanham mesmo sem evento local. É contexto essencial para distinguir movimento global vs idiossincrático.",
        "source": "Yahoo Finance · ^VIX · Tempo real (15min delay)",
    },

    # ============================================================
    # ANÁLISES DERIVADAS
    # ============================================================
    "CORR_ROLLING": {
        "title": "Correlação Rolling",
        "short": "Correlação entre retornos do BRL e do índice em janela móvel (padrão: 30 dias). Quando próxima de zero ou negativa, sinaliza que o BRL está se descolando do driver normal.",
        "detail": """
A **correlação rolling** é calculada sobre **retornos percentuais** (não preços) em janela móvel de N dias (configurável na sidebar).

**Por que retornos e não preços:**
Séries de preço são não-estacionárias (têm tendência). Correlação em nível dá resultados espúrios. Retornos percentuais resolvem esse problema — é a abordagem padrão em análise quantitativa de FX.

**Interpretação:**
- **Correlação positiva forte (>0,5):** BRL se move como esperado pelo driver
- **Correlação fraca (-0,2 a 0,2):** outros fatores dominam — sinal de regime atípico
- **Correlação negativa:** algo idiossincrático está movendo o BRL contra o fluxo global

**Janela:**
- 10 dias: muito ruidosa, capta movimento muito recente
- 30 dias: padrão de mesa, equilíbrio entre ruído e tendência
- 90 dias: estrutural, suaviza eventos pontuais
        """,
        "why": "Identifica quando o BRL está em regime atípico — momentos em que fatores locais (fiscal, político, regulatório) dominam sobre o driver global. É o sinal mais limpo de stress idiossincrático Brasil.",
        "source": "Cálculo interno · janela ajustável",
    },

    "CORR_DIFFERENTIAL": {
        "title": "Diferencial de Correlação (DTWEXBGS – DXY)",
        "short": "Indica se o BRL está mais correlacionado com dólar contra emergentes (DTWEXBGS) ou contra G10 (DXY). Identifica em qual 'regime' o real está operando.",
        "detail": """
O **diferencial de correlação** é calculado como: Diff = corr(PTAX, DTWEXBGS) − corr(PTAX, DXY)

**Interpretação:**
- **Diferencial positivo (>0):** BRL se comporta mais como moeda emergente típica — está se movendo junto com peso mexicano, rand sul-africano, yuan. Regime "EM-driven", normal pra economia emergente exportadora de commodities.

- **Diferencial negativo (<0):** BRL se comporta mais como moeda G10 — provavelmente carry-trade driven ou com risco idiossincrático dominante. Regime atípico, exige atenção.

- **Mudanças bruscas:** indicam transição de regime — momentos cruciais para reavaliar posições e narrativa de mercado.

**Aplicação prática:**
Saber em qual regime o BRL está operando ajuda a escolher o hedge correto:
- Regime EM → hedge via cesta de emergentes ou DTWEXBGS
- Regime G10 → hedge via DXY ou par específico
- Transição → prêmio adicional necessário em derivativos
        """,
        "why": "Trader que entende regime cobra spread diferente que trader que opera correlação estática. Esse indicador é o sinal mais limpo de mudança de regime no BRL.",
        "source": "Cálculo interno · derivado de correlações",
    },
}


def get_term(key):
    """Retorna entrada do glossário, ou None se não existir."""
    return GLOSSARY.get(key)


def render_inline_description(key, layout="side"):
    """
    Renderiza descrição curta de um termo.

    layout:
        'side': caixa lateral (pra colocar ao lado de gráfico)
        'inline': caixa inline (acima do gráfico)
    """
    term = get_term(key)
    if not term:
        return ""

    return f"""
    <div style="
        background-color: #0A0A0A;
        border: 1px solid #2D2D2D;
        border-left: 3px solid #FFA500;
        padding: 0.8rem 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #B0B0B0;
        line-height: 1.6;
        margin: 0.5rem 0;
    ">
        <div style="color: #FFA500; font-weight: 600; margin-bottom: 0.4rem; text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.05em;">
            ℹ {term['title']}
        </div>
        <div>{term['short']}</div>
    </div>
    """


def render_detail_expander(key, st):
    """
    Renderiza expander completo de um termo (use st passado pela página).
    Coloca DENTRO do código da página, não no styling.
    """
    term = get_term(key)
    if not term:
        return

    with st.expander(f"📖 Saiba mais sobre {term['title']}"):
        st.markdown(term['detail'])
        st.markdown(f"**Por que importa para o BRL:** {term['why']}")
        st.caption(f"📊 {term['source']}")
